# Middleware

This folder contains:
- The Generic Classifier Class file [`classifier.py`](app/classifier.py), which allows loading the stored, already trained model and vectorizer, as well as preprocessing and prediction of single comments
- The Data Retrievers Module [`data_retriever.py`](app/data_retriever.py), which consists of 2 data classes (YtComment and YtCommentReply) for storing comment data and 2 interface classes for retrieving comments and storing them in Elastic Search
- The Main file [`main.py`](app/main.py) containing our FastAPI functions
- The Docker file [`Dockerfile`](Dockerfile) to create the FastAPI container
- The Shell file [`start.sh`](start.sh) to start the FastAPI inside the container
- The Requirements file [`requirements.txt`](requirements.txt) for the FastAPI container
