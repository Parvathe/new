import os
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
# from langchain_community.vectorstores import Chroma
#import functions_framework
from langchain_google_vertexai import VertexAI,VertexAIEmbeddings
import langchain
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.chains import ConversationalRetrievalChain
# from datetime import datetime
from langchain_google_vertexai import VertexAI
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.agents.agent_types import AgentType
from langchain_community.vectorstores import FAISS
import json
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
# from langchain.memory import ConversationBufferMemory
# from langchain_community.embeddings import HuggingFaceEmbeddings
import re
from langchain_google_vertexai import VertexAI
# from vertexai.language_models import TextGenerationModel, CodeChatModel
import io


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "prj-adapt-app-dev-001--adapt-services.json"

embeddings = VertexAIEmbeddings(model_name='textembedding-gecko@003')
llm=VertexAI(model_name="gemini-1.5-pro")
with open ('examples.json','r') as f:
    examples=json.load(f)


def qc_chain(question):
    """This function classifies the question asked by user
Parameters:
question (str): question from user
Returns:
str: category of question
""" 
    example_prompt = PromptTemplate(
    input_variables=["question", "output"],
    template="question: {question}\noutput: {output}",)
    example_selector = SemanticSimilarityExampleSelector.from_examples(
    # The list of examples available to select from.
    examples,
    # The embedding class used to produce embeddings which are used to measure semantic similarity.
    embeddings,
    # The VectorStore class that is used to store the embeddings and do a similarity search over.
    FAISS,
    # The number of examples to produce.
    k=5,
    )
    similar_prompt = FewShotPromptTemplate(
    # We provide an ExampleSelector instead of examples.
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix="Given the examples below please classify the question and give the output \n examples: \n",
    suffix=" Classify the question below and give the output as result \n question: {question}\n output:",
    input_variables=["question"],
    )
    classification_chain = similar_prompt | llm #instantiating the chain
    question_category = classification_chain.invoke({"question":question}).strip()
    return question_category
