import json
import os 
from google.cloud import bigquery
from google.cloud import aiplatform
import vertexai

with open('config.json', 'r') as file:
    config = json.load(file)


def model_init():
    #os.environ["GOOGLE_CLOUD_CREDENTIALS"] = config['GOOGLE_APPLICATION_CREDENTIALS_VERTEX']
    vertexai.init(project = config['PROJECT_ID'], location = config['location'])
    aiplatform.init(project = config['PROJECT_ID'], location = config['location'])


def bq_init():
    os.environ["GOOGLE_CLOUD_CREDENTIALS"] = config['GOOGLE_CLOUD_CREDENTIALS']
    bq_client = bigquery.Client()
    return bq_client
