import os
from langchain_google_vertexai import VertexAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
import tempfile
import re
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain import PromptTemplate
from google.cloud import storage
import datetime
import logging
import io
from PyPDF2 import PdfReader

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0 4.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"
llm = VertexAI(model="claude-3-opus@20240229", temperature=0, max_output_tokens=2000)

def get_latest_blob(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs())
    blobs.sort(key=lambda x: x.updated, reverse=True)
    return blobs[0]


def load_and_split_pdf(blob, chunk_size=1000, chunk_overlap=200):
    def get_pdf_splits(pdf_file):
        pdfreader = PdfReader(pdf_file)
        raw_text = ""
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                raw_text += content
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=2000,
            chunk_overlap=100,
            length_function=len,
        )
        texts = text_splitter.split_text(raw_text) 
        return texts
    try:
        pdf_bytes = blob.download_as_string()
        pdf=io.BytesIO(pdf_bytes)
        pdf_splitter = get_pdf_splits(pdf)
        # print(pdf_splitter)
        
        return pdf_splitter
    
    except Exception as e:
        logging.error(f"Error loading and splitting PDF: {e}")
        return []

def summarize_text(texts, llm):
    summarize_prompt = PromptTemplate(
        input_variables=["text"],
        template="Summarize the following text in a way that highlights the key steps, processes, and flow of activities described. Focus on extracting the sequential flow and logical progression of actions, as this summary will be used to generate a flow chart. Do it in a concise manner:\n\n{text}"
    )
    
    summaries = []
    for text in texts:
        prompt = summarize_prompt.format(text=texts)
        summary_chunk = llm(prompt)
        summaries.append(summary_chunk)
    
    summary = " ".join(summaries)
    print(f"summary: {summary}")
    return summary

def generate_mermaid_code(summary, llm):
    mermaid_prompt = PromptTemplate(
        input_variables=["summary"],
        template="Based on the following summary descriptions, generate a Mermaid diagram code:\n\n{summary}"
    )
    
    prompt = mermaid_prompt.format(summary=summary)
    mermaid_code = llm(prompt)
    mermaid_code = mermaid_code.replace("```mermaid", "").replace("```", "")
    return mermaid_code

def solution_architecture():
    # bucket_name = 'temp-bucket-chat'
    bucket_name = "Co-pilot-bot-bucket"
    latest_blob = get_latest_blob(bucket_name)
    texts = load_and_split_pdf(latest_blob)
    summary = summarize_text(texts, llm)
    mermaid_code = generate_mermaid_code(summary, llm)
    return mermaid_code

# print(f"Mermaid Diagram Code:\n\n{mermaid_code}")