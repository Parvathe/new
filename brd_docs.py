# from langchain.agents import create_sql_agent
# from langchain.agents.agent_toolkits import SQLDatabaseToolkit
# from langchain.sql_database import SQLDatabase
# from langchain.llms.openai import OpenAI
# from langchain.agents import AgentExecutor
# from langchain.agents.agent_types import AgentType
# from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import GPT4AllEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.document_loaders import PyPDFLoader
# from langchain.llms import Replicate
# from langchain.chains import ConversationalRetrievalChain
# import sqlite3
import os
# from datetime import datetime

from langchain_google_vertexai import VertexAI

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"
#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"
llm = VertexAI(model_name="gemini-1.5-pro")
# llm_1 = VertexAI(model_name="Gemini Pro Vision",temperature=0)


def brd_document(project_details):
    Brd_prompt = PromptTemplate(
        input_variables=['text_input'],
        template=""" You are a Business requirement document developer.
                    Develop a comprehensive business requirement document for a telecom based company based on the given project input.
                    Give the main heading as business Requirements Document in block:
                    Provide a blank space for a topic if the information is not present in the project input.
                    Provide a seprate Table of Contants.
                    Provide a detailed and Elaborate contant for each sections.
                    This document should include an introduction providing an overview of the project objectives and scope with atleast 2000 words.
                    Details of the project goals, including the desired features and functionalities in details.
                    
                    1 Document Details:
                                    Date: "Please provide the date for this document if provided."
                                    Intake: "What is the purpose or motivation behind creating this document?"
                                    Project Name: "What is the name of the project associated with this document?"
                                    Document Creator: "Who is the primary author or creator of this document?"
                                    Organization: "Which organization or company does this document belong to?"
                                    Additional Contributors:

                                    Name: "Please provide the name of additional contributors to this document."
                                    Title: "What is the title or role of the additional contributors?"
                                    Organization: "Which organization or company are the additional contributors associated with?"
                                    
                    2 Table of Contents:
                        3.1 Overview:
                                    High Level Summary: "Provide a brief summary of the project at a high level."
                                    Key Business Objectives: "What are the primary business goals or objectives of this project?"
                                    Related Projects or Dependencies: "Are there any other projects or dependencies related to this one?"
                        3.2 Scope:
                                    Project Scope Definition: "Define the boundaries and objectives of the project."
                                    Included in Scope: "List what is included in the project scope."
                                    Excluded from Scope: "Specify what is explicitly excluded from the project scope."
                                    Assumptions/Constraints/Factors/Risks: "Identify any assumptions, constraints, factors, or risks relevant to the project."
                                    Impacted Business Units: "Which business units or departments will be affected by this project?"
                        3.3 Definition: "Provide definitions for any key terms or concepts used throughout the document."
                        3.4 Common Requirements:
                                    Business Requirements: "Outline the business needs or objectives driving this project."
                                    Technical Requirements: "Specify any technical specifications or requirements for the project."
                                    Testing Requirements: "Describe the testing criteria and procedures for the project."
                                    Acceptance Criteria: "What criteria must be met for the project to be considered successful?"
                                    Data/Metrics/Reporting Requirements: "Identify any data, metrics, or reporting needs for the project."
                                    Training Requirements: "Outline any training needs for stakeholders involved in the project."
                        3.5 Business Unit Specific Requirements:
                                    Address & Facility: "Specify requirements related to addresses and facilities."
                                    Billing & Payment: "Describe requirements related to billing and payment processes."
                                    Buy Flow: "Outline requirements related to the purchasing or transaction process."
                                    Field Ops Dispatch: "Specify requirements for field operations dispatch."
                                    Field Ops Process & Mobility: "Describe requirements for field operations processes and mobility solutions."
                                    Service Assurance & Repair: "Outline requirements related to service assurance and repair processes."
                                    Service Delivery & Care: "Specify requirements for service delivery and customer care."
                        3.6 Benefits:
                                    Hard Benefits: "Identify measurable, tangible benefits of the project."
                                    Soft Benefits: "Describe intangible or qualitative benefits of the project."
                                    Unquantified Benefits: "Specify any benefits that cannot be easily quantified."
                        3.7 Project Governance:
                                    Project Sponsor: "Who is the sponsor or champion of this project?"
                                    Project Manager: "Who is responsible for managing and overseeing the project?"
                                    Stakeholders: "Identify key stakeholders involved in the project and their roles."
                                    Decision-Making Process: "Describe the process for making decisions related to the project."
                                    Communication Plan: "Outline how communication will be handled among team members and stakeholders."
                                    Change Management: "Describe how changes to requirements or scope will be managed and documented."
                                    Escalation Procedures: "Specify procedures for escalating issues or concerns that cannot be resolved at the project level."
                                    Meeting Schedule: "Provide details of regular meetings, including frequency, attendees, and agenda."
                                    Reporting Structure: "Outline how progress will be reported and to whom."
                                    Governance Structure: "Describe the overall governance structure for the project, including roles and responsibilities."
                        Detail the planning phase, including the process of defining project goals and objectives within the telecom domain.
                        Provide a detailed view of the requirements gathering process, identifying key stakeholders and methods for collecting functional and non-functional requirements.
                        Describe the architecture and design specifications, including components, interfaces, and data flow.
                        Discuss the coding and implementation process, specifying programming languages, frameworks, and tools to be used.
                        Explain the testing procedures to ensure the reliability and performance, including test case creation and execution.
                        Outline the deployment process, including pre-deployment checks, deployment steps, and post-deployment validation.
                        provide description and comments for all the section and topics possible: t\n\n {text_input}"""
    )


    Brd_chain = LLMChain(llm = llm, prompt=Brd_prompt)
    Brd = Brd_chain.run(project_details)
    return Brd
