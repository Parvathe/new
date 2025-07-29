from codey_features import *
import uvicorn
from fastapi import FastAPI, WebSocket, File, UploadFile, WebSocketDisconnect
from codey_classifier import qc_chain
import logging
from vertexai.preview.generative_models import GenerativeModel
from brd_docs import brd_document
# import openai
from fastapi.responses import PlainTextResponse
from google.cloud import storage
from solution_architecturev2 import solution_architecture
# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
from fastapi.middleware.cors import CORSMiddleware
from repo_reviewv2 import chat_with_git
from finance_qa import finance_assistant
from code_assistant import companion
from pydantic import BaseModel
import json
import logging
from service_init import model_init
model_init()

#generation_config = { "temperature": 0, "top_p": 1, "top_k": 1, "max_output_tokens": 2048,}

class GitDetails(BaseModel):
    username:str
    access_token:str
    repo_name:str

retriever, chain = finance_assistant()

logging.basicConfig(filename='example.log', level=logging.DEBUG)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"
model = GenerativeModel("gemini-1.5-pro")
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "prj-adapt-app-dev-001--adapt-services.json"
# openai.api_key = "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"
# prompt = """
# You are chatbot agent which takes the input from the user and give the appropriate and accurate response
# """

#project_id
storage_client = storage.Client()
bucket_name = "Co-pilot-bot-bucket"
# bucket_name = "temp-bucket-chat"

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
      
#         classifier=qc_chain(data)
    
#         if classifier in globals():
#             response=globals()[classifier](data)
           
#             await websocket.send_text(str(response))
#         else:  
#             responses = model.generate_content(data, stream=True)
#             for response in responses:
#                 await websocket.send_text(response.text)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await companion(websocket)

@app.websocket("/requirement")
async def requirement_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        result = brd_document(data)
        await websocket.send_text(str(result))

# @app.websocket("/open_ai")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         response = openai.Completion.create(
#             engine="gpt-3.5-turbo-instruct",
#             prompt=prompt + "\n" + data,
#             max_tokens=3500,
#             temperature=0.4,  # Adjust temperature for creativity
#             top_p=1,  # Adjust top_p for diversity
#         )
#         await websocket.send_text(response.choices[0].text.strip())


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Save file to Google Cloud Storage
    if not file:
        return PlainTextResponse('No file part')

    with file.file as f:
        file_content = f.read()

    if not file_content:
        return PlainTextResponse('No selected file')

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file.filename)
    blob.upload_from_string(file_content, content_type=file.content_type)

    # Insert data into BigQuery

    return PlainTextResponse('File uploaded successfully')

@app.post("/architecture")
async def solution_arch():
    output = solution_architecture()
    return output

@app.websocket("/gitchat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        data = eval(data)
        if data["type"] == "git":
            logging.warning('entered git')
            await chat_with_git(websocket, data["data"]["username"], data["data"]["access_token"], data["data"]["repo_name"],data["data"]["organization_name"])
        elif data["type"] == "message":
            await websocket.send_json({"type": "message", "data": "Sample message"})
            
@app.websocket("/fchat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            if data == "quit":
                break
            docs = retriever.get_relevant_documents(data)
            response = chain({"input_documents": docs, "question": data}, return_only_outputs=True)
            await websocket.send_text(response['output_text'])
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()


if __name__ == "__main__":
    # uvicorn.run(app, host="249.146.0.51", port=9000)
    uvicorn.run(app, host="0.0.0.0", port=8085)
    # uvicorn.run(app)
