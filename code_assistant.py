from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import os
import json
from service_init import model_init
model_init()

with open('config.json') as f:
    config = json.load(f)


# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'lumen-b-ctl-047-e2aeb24b0ea0.json'
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"

template = """You are a chatbot having a conversation with a human developer.

{chat_history}
Developer: {human_input}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")


llm = VertexAI(max_output_tokens=2048, project = config['PROJECT_ID'], location = config['location'])
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    memory=memory,
)

async def companion(websocket: WebSocket):
    memory.clear()
    while True:
        usr_ip = await websocket.receive_text()
        if usr_ip == "quit":
            break
        # print(f"You: {usr_ip}")
        response = llm_chain.run(usr_ip)
        await websocket.send_text(response)
        
