# langchain_core.py
from langchain.retrievers import ParentDocumentRetriever
from langchain_core.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_vertexai import VertexAIEmbeddings, VertexAI
from langchain.storage import InMemoryStore
from langchain.memory import ConversationBufferMemory
import os

# Set Google application credentials
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"

def finance_assistant():

    child_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    parent_splitter = RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=100)
    embeddings = VertexAIEmbeddings(model_name="textembedding-gecko@002")
    
    try:
        vector_store = FAISS.load_local("fstore_embed", embeddings, allow_dangerous_deserialization = True)
    except:
        loader = PyPDFDirectoryLoader("finance_store")
        data = loader.load()
        content = "\n\n".join(str(page.page_content) for page in data)
        texts = child_splitter.split_text(content)
        vector_store = FAISS.from_texts(texts, embeddings)
        vector_store.save_local("fstore_embed")
        

    store = InMemoryStore()

    retriever = ParentDocumentRetriever(
        vectorstore=vector_store,
        docstore=store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter
    )

    prompt_template = """
     Welcome to your role as a financial advisor in the telecom industry.
     You are provided with a bunch of finance reports of telecom companies. You will answer questions effectively from the
     knowledge base specific to the telecom sector.
     Your task is to analyze financial reports of various telecom companies and provide insightful answers to questions related to telecom finance.
     Your responses should be grounded in the available knowledge base, avoiding any fabrication of numerical data.
     If the question lacks specificity, feel free to provide broader insights within the scope of your telecom industry knowledge base.
     Remember, your goal is to offer effective financial advice based on the information at hand.

     Instructions:
     - Break down the question for better understanding.
     - Analyze the context provided.
     - Provide insightful answers grounded in the telecom industry knowledge base.
     - Avoid fabrication of numerical data.
     - If the question lacks specificity, provide broader insights within the telecom industry scope.

     Context:\n {context}?\n\n
     Question: \n{question}\n\n
     Chat History: \n{chat_history}\n\n

     Answer:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question", "chat_history"])
    memory = ConversationBufferMemory(memory_key='chat_history', input_key='question')
    model = VertexAI(model="claude-3-opus@20240229", temperature=0.3, max_output_tokens=2048)

    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt, memory=memory)
    memory.clear()
    
    return retriever, chain