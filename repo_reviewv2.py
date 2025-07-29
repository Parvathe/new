from fastapi import WebSocket
import git
from git import Repo
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.chains.llm import LLMChain
from langchain_google_vertexai import VertexAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains import StuffDocumentsChain, LLMChain
from langchain.memory import ConversationBufferMemory, ConversationTokenBufferMemory, ConversationBufferMemory
from docx import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
import os
import logging

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"

prompt_template = """You are an programmer assistant. Evaluate the code and give suggestions for improvement of the code. Be concise and on point. Answer in points.
    Code: {text}
    Assistant:
    """
prompt = PromptTemplate.from_template(prompt_template)
llm = VertexAI(model="gemini-1.5-pro", temperature=0.5, max_output_tokens=1024)
llm_chain = LLMChain(llm=llm, prompt=prompt)
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

def summarize_pdf(pdf_file_path):
    try:
        loader = PyPDFLoader(pdf_file_path)
        docs = loader.load()
    except:
        loader = Docx2txtLoader(pdf_file_path)
        docs = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_docs = text_splitter.split_documents(docs)
    # summary = stuff_chain.invoke(docs)
    return split_docs

def git_extract(username, access_token, repo_name,organization_name):
    repo_url = f"https://{username}:{access_token}@github.com/{organization_name}/{repo_name}"
    try:
        repo = git.Repo.clone_from(repo_url, repo_name)
        print("Repository cloned successfully:", repo)
    except git.exc.GitCommandError as e:
        print("Cloning failed. Removing directory and trying again...")
        try:
            os.system(f'rm -rf {repo_name}')
            repo = git.Repo.clone_from(repo_url, repo_name)
            print("Repository cloned successfully:", repo)
        except git.exc.GitCommandError as e:
            print("Failed to clone repository after removing directory.")

def convert_to_docx(code_path, docx_path):
    try:
        with open(code_path, 'r') as code_file:
            code_content = code_file.read()
        doc = Document()
        doc.add_paragraph(code_content)
        doc.save(docx_path)
        return code_content
    except Exception as e:
        print(f"Error converting file: {e}")
        return "File format is not supported"

def get_directory_structure(repo_path):
    directory_structure = []

    def traverse_directory(path, parent=None):
        for root, dirs, files in os.walk(path):
            if '.git' in dirs:
                dirs.remove('.git')

            folder_data = {
                "name": os.path.basename(root),
                "type": "folder",
                "folder": []
            }

            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                folder_data["folder"].append(traverse_directory(dir_path, folder_data))

            for file_name in files:
                # file_path = os.path.join(root, file_name)
                file_data = {
                    "name": file_name,
                    "type": "file"
                }
                folder_data["folder"].append(file_data)

            if parent:
                return folder_data
            else:
                directory_structure.append(folder_data)

    traverse_directory(repo_path)
    return directory_structure

async def git_push(file_path, code_content, local_repo_path, remote_repo_url):
    if not os.path.isdir(local_repo_path):
        Repo.clone_from(remote_repo_url, local_repo_path)
    repo = Repo(local_repo_path)
    print(f"test print {repo}")
    
    if repo.is_dirty():
        return "The repo has uncommitted changes."

    if repo.active_branch.name != "main":
        return "You are not on the main branch."


    # Write code_content to a file
    # file_full_path = os.path.join(local_repo_path, file_path)
    file_full_path = os.path.join(os.getcwd(), file_path)
    print(f"test print2 {file_full_path}")
    with open(file_full_path, "w") as file:
        file.write(code_content)

    # Add, commit, and push changes
    try:
        repo.git.add(file_full_path)
        repo.index.commit("Add or update file")
        origin = repo.remote(name="origin")
        origin.push()

        print("File has been pushed to the repository.")
        return "File has been pushed to the repository."
    except Exception as e:
        return "File has not been pushed. Check the credentials or reconnect."
    
qa_template = """
        - You are a chatbot named Cody having a conversation with a human developer.
        - You NEVER answer that your are an AI language model.
        - If you don't have the context from the documents, answer from your knowledge with the context of the stuffed document.

        Given the following extracted parts of a long document and a question, create a final answer.

        {context}
        {chat_history}
        Human: {question}
        Chatbot:"""
qa_prompt = PromptTemplate(
    input_variables=["chat_history","question", "context"], 
    template=qa_template
)

memory = ConversationBufferMemory(memory_key='chat_history', input_key='question')
chain = load_qa_chain(llm=llm, chain_type="stuff", prompt=qa_prompt, memory=memory)

async def chat_with_git(websocket: WebSocket, username, access_token, repo_name,organization_name):
    # await websocket.accept()
    git_extract(username, access_token, repo_name,organization_name)
    repo_path = os.path.join(repo_name)
    
    # await websocket.send_text("Available files in the repository:")
    # await websocket.send_text("Please select a file to chat with:")
    
    file_paths = []
    files_list = []
    for root, dirs, files in os.walk(repo_path):
        if '.git' in dirs:
            dirs.remove('.git')
        for file_name in files:
            full_path = os.path.join(root, file_name)
            # await websocket.send_text(f"- {file_name}")
            # files_list.append(file_name)
            files_list.append(os.path.relpath(full_path, start=repo_path))
            file_paths.append(full_path)
    
    # await websocket.send_json({"type": "files", "content" : files_list})
    directory_structure = get_directory_structure(repo_path)
    # await websocket.send_json({"type": "files", "content": [directory_structure[0]]})
    await websocket.send_json([directory_structure[0]])
    async def file_select(file_choice = None):
        if file_choice == None:        
            file_choice = await websocket.receive_json()
        
        selected_file = next((file_path for file_path in file_paths if os.path.basename(file_path) == file_choice['data']), None)
        
        if not selected_file:
            await websocket.send_json({"type": "error", "content": f"Invalid file choice- {file_choice['data']}. Please try again."})
        else:
            file_base_name = os.path.splitext(os.path.basename(selected_file))[0]
            docx_path = f"docstore/doc_{file_base_name}.docx"
            content = convert_to_docx(selected_file, docx_path)
            docs = summarize_pdf(docx_path)
            await websocket.send_json({"type": "code", "data": content})
            # await websocket.send_json({"type": "message", "data": "Do you want me to analyze and provide suggestions for improvements in your code? (Y/N)"})
            # summary_nod = await websocket.receive_json()
            # if summary_nod['data'].lower() == 'y':
            #     await websocket.send_json({"type": "message", "data": str(summary)})
            # else:
            #     pass
            # await websocket.send_json({"type": "message", "data": str(summary)})

        while True:
            question = await websocket.receive_json()
            if question["type"] == "message":
                answer = chain.run(input_documents=docs, question=question["data"])
                await websocket.send_json({"type": "message", "data": str(answer)})
            elif question['type'] == "git":
                memory.clear()
                logging.info('chat_with_git')
                await chat_with_git(websocket, question["data"]["username"], question["data"]["access_token"], question["data"]["repo_name"],question["data"]["organization_name"])
            elif question['type'] == "git-push":
                code_content = question['data']
                file_path = selected_file
                local_repo_path = os.path.join(os.getcwd(), repo_name)
                # local_repo_path = repo_name
                remote_repo_url = f"https://{username}:{access_token}@github.com/{organization_name}/{repo_name}.git"
                print(remote_repo_url)
                result =await git_push(file_path, code_content, local_repo_path, remote_repo_url)
                await websocket.send_json({"type": "message", "data": result})
            elif question['type'] == "file":
                memory.clear()
                await file_select(question)
            else:
                break
    
    await file_select()
