import os
import glob
import joblib
import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split

import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

from fastapi import FastAPI
import requests

from app.data_retriever import YtDataRetriever, ESConnect
#from classifier import GenericClassifier


app = FastAPI()


@app.get("/")
def read_root():
    """
    For testing purpose
    """
    for elem in range(4):
        print(elem)
    return {"Hello": "World"}


@app.get("/es-status/")
def get_es_status():
    """
    Make a request for ElasticSearch and return the status code
    """
    es_status = requests.get(
        "http://es01:9200/", auth=("elastic", os.environ["ELASTIC_PASSWORD"]), timeout=10
        )
    return es_status.json()


@app.post("/retrieve_comments/{video_id}")
def retrieve_comments(video_id: str = ""):
    """
    Retrieve the comments from a given YouTube video using the ID
    """
    if video_id == "":
        print("******************************************")
        print("No video ID received!")
    else:
        print("******************************************")
        print(f"The ID {video_id} is received")
        yt = YtDataRetriever()
        data = yt.get_video_data(video_id)
        es = ESConnect()
        status = es.store_video_data(data, video_id)

    return { "answer": status } # TODO handle status


@app.get("/predict/{video_id}")#{model_id}")
def predict_comments(video_id):#model_id: int = 0):
    """
    Output predictions made using certain model
    """
    """if model_id == 0:
        # apply svm
        svm_clf = joblib.load("saved_models/svc_35-37.joblib")
        prediction = make_prediction(svm_clf).tolist()
    if model_id == 1:
        # apply naive bayes
        nb_clf = joblib.load("saved_models/multinomialnb_32-21.joblib")
        prediction = make_prediction(nb_clf).tolist()
        return {"nb_prediction": prediction}
    if model_id == 2:
        # apply logistic regression
        lr_clf = joblib.load("saved_models/logisticregression_34-12.joblib")
        prediction = make_prediction(lr_clf).tolist()
        return {"lr_prediction": prediction}
    if model_id == 3:
        ... # apply ensemble model # TODO to be implemented
    return {"lr_prediction": [] } # TODO default"""


@app.get("/spam/{video_id}")
def return_spam_comments(video_id):
    """"
    Output spam comments from given video
    """
    es = ESConnect()
    return { "spam comments": es.get_spam_comments(video_id) }


"""
@app.get("/predict/")
def predict():
    
    #Make predictions for the comments using default model (here: SVM) and return the spam comments

    # TODO make predictions for the given yt video
    comments = ["nice song!", "Go to my page"]
    predictions = make_prediction(comments)
    return { "spam comments": [comment for comment, prediction in zip(comments, predictions) if prediction==[1]] }

def make_prediction(comments):
    
    #Make predictions for given yt comments using the generic classifier class
    
    clf = GenericClassifier()
    predictions = [clf.predict_comment(comment) for comment in comments]

    return predictions
"""


if __name__ == "__main__":
    print("main.py")
