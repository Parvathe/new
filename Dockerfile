# FROM ubuntu:latest
# FROM python:3.11-slim
# RUN apt-get -y update
# RUN apt-get -y install git
FROM nexusprod.corp.intranet:4567/null/qf-chatbot:copilot_bot-11
 
# Set the working directory to /app
 
# Copy the current directory contents into the container at /app
COPY . . /
# Install any needed packages specified in requirements.txt
# RUN chmod a+r /diag-as-a-service-prod.json
RUN pip3 install -r requirements.txt
# Make port 8765 available to the world outside this container
EXPOSE 8085
# Run app.py when the container
CMD python3 codey_api_test.py


# aiohttp==3.9.3
# aiosignal==1.3.1
# annotated-types==0.6.0
# anyio==4.3.0
# async-timeout==4.0.3
# attrs==23.2.0
# cachetools==5.3.3
# certifi==2024.2.2
# charset-normalizer==3.3.2
# click==8.1.7
# contourpy==1.2.0
# cycler==0.12.1
# dataclasses-json==0.6.4
# docx==0.2.4
# docx2txt==0.8
# et-xmlfile==1.1.0
# exceptiongroup==1.2.0
# fastapi==0.110.0
# fonttools==4.50.0
# frozenlist==1.4.1
# git-python==1.0.3
# gitdb==4.0.11
# google-api-core==2.18.0
# google-auth==2.29.0
# google-cloud-aiplatform==1.44.0
# google-cloud-bigquery==3.19.0
# google-cloud-core==2.4.1
# google-cloud-resource-manager==1.12.3
# google-cloud-storage==2.16.0
# google-crc32c==1.5.0
# google-resumable-media==2.7.0
# googleapis-common-protos==1.63.0
# greenlet==3.0.3
# grpc-google-iam-v1==0.13.0
# grpcio==1.62.1
# grpcio-status==1.62.1
# h11==0.14.0
# haversine==2.8.1
# idna==3.6
# importlib_resources==6.4.0
# jsonpatch==1.33
# jsonpointer==2.4
# kiwisolver==1.4.5
# langchain==0.1.13
# langchain-community==0.0.29
# langchain-core==0.1.33
# langchain-google-vertexai==0.1.1
# langchain-text-splitters==0.0.1
# langsmith==0.1.31
# lxml==5.2.1
# marshmallow==3.21.1
# matplotlib==3.8.3
# multidict==6.0.5
# mypy-extensions==1.0.0
# numpy==1.26.4
# openpyxl==3.1.2
# orjson==3.9.15
# packaging==23.2
# pandas==2.2.1
# pillow==10.2.0
# proto-plus==1.23.0
# protobuf==4.25.3
# pyasn1==0.5.1
# pyasn1-modules==0.3.0
# pydantic==2.6.4
# pydantic_core==2.16.3
# pyparsing==3.1.2
# PyPDF2==3.0.1
# python-dateutil==2.9.0.post0
# python-docx==1.1.0
# python-multipart==0.0.9
# pytz==2024.1
# PyYAML==6.0.1
# requests==2.31.0
# rsa==4.9
# seaborn==0.13.2
# shapely==2.0.3
# six==1.16.0
# smmap==5.0.1
# sniffio==1.3.1
# SQLAlchemy==2.0.29
# starlette==0.36.3
# tenacity==8.2.3
# types-protobuf==4.24.0.20240311
# types-requests==2.31.0.20240311
# typing-inspect==0.9.0
# typing_extensions==4.10.0
# tzdata==2024.1
# urllib3==2.2.1
# uvicorn==0.29.0
# websockets==12.0
# yarl==1.9.4
# zipp==3.18.1
