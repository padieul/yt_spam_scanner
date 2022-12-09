from typing import Union
import os
import glob
import pandas as pd
import numpy as np

import joblib

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

from app.data_retriever import YtDataRetriever, ES_Connect


app = FastAPI()


@app.get("/")
def read_root():
    """
    For testing purpose
    """
    for elem in range(4):
        print(elem)
    return {"Hello": "World"}


@app.get("/predict/{model_id}")
def predict_params(model_id: int = 0):
    """"
    Output predictions made using certain model
    """
    if model_id == 0:
        # apply svm
        svm_clf = joblib.load("saved_models/svc_35-37.joblib")
        prediction = make_pred(svm_clf).tolist()
        return {"svc_prediction": prediction}
    if model_id == 1:
        # apply naive bayes
        nb_clf = joblib.load("saved_models/multinomialnb_32-21.joblib")
        prediction = make_pred(nb_clf).tolist()
        return {"nb_prediction": prediction}
    if model_id == 2:
        # apply logistic regression
        lr_clf = joblib.load("saved_models/logisticregression_34-12.joblib")
        prediction = make_pred(lr_clf).tolist()
        return {"lr_prediction": prediction}
        # apply logistic regression 
    elif model_id == 100:
        ... # apply ensemble model

@app.post("/retrieve_comments/{vid_id}")
def retrieve_comments(vid_id: str = ""):
    if vid_id == "":
        print("******************************************")
        print("No video ID received!")
    else:
        print("******************************************")
        print("The ID is {} !".format(vid_id))
        yt = YtDataRetriever()
        data = yt.get_video_data(vid_id)
        print(data)
        es = ES_Connect()
        es.store_video_data(data, vid_id)
        """
        yt_retriever = YtDataRetriever()
        yt_retriever.get_data()
        """

    return {"answer": "everything fine!"}


@app.get("/predict/")
def predict():
    """
    Make predictions using default model (here: SVM)
    """
    default_clf = joblib.load("saved_models/svm_clf.joblib")
    prediction = make_pred(default_clf).tolist()
    return {"prediction": prediction}


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
        print(f"The ID is {video_id}")

    return {"answer": "everything fine!"}


def nltk_download():
    """
    Download required nltk packages
    """
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download('omw-1.4')
    nltk.download("wordnet")


def load_data(data_path):
    """
    Load dataset from given path
    """
    files = glob.glob(os.path.join(data_path, "*.csv"))
    return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)


def preprocess_data(corpus,
                    irrelevant_features=["COMMENT_ID", "AUTHOR", "DATE"],
                    rename_columns={"CONTENT":"COMMENT"}
                   ):
    """
    Preprocessing pipeline
    """

    # drop irrelevant features
    corpus.drop(irrelevant_features, inplace=True, axis=1)

    # remove blank rows
    corpus.dropna()

    # add column for representation
    corpus['REPR'] = corpus.loc[:, 'CONTENT']

    # lower case
    corpus['REPR'] = corpus['REPR'].str.lower()

    # change column name
    for old, new in rename_columns:
        corpus.rename({old : new}, axis=1, inplace=True)

    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words("english")

    for comment in corpus["REPR"]:
        comment = nltk.word_tokenize(comment) # tokenizing
        comment = [lemmatizer.lemmatize(word) for word in comment] # lemmatizing
        comment = [word for word in comment if word not in stop_words] # removing stopwords
        comment = " ".join(comment)


def split_data(text_repr, corpus):
    """
    Split into training and testing dataset
    """
    return train_test_split(
        text_repr, np.asarray(corpus["CLASS"]), test_size=0.3, random_state=42, shuffle=True
        )


def make_pred(clf):
    """
    Make predictions using given classifier
    """
    path = r"data/YouTube-Spam-Collection/"
    corpus = load_data(path)
    nltk_download()

    preprocess_data(corpus)

    vectorizer = CountVectorizer(binary=True, max_df=0.95)
    #max_features=10000, tokenizer=lambda doc: doc)
    bow_repr = vectorizer.fit_transform(corpus["REPR"])

    X_train, X_test, y_train, y_test = split_data(bow_repr, corpus)
    y_pred = clf.predict(X_test)
    
    return y_pred


if __name__ == "__main__":
    print("Start...")
    classifier = joblib.load("../saved_models/svm_clf.joblib")
    predictions = make_pred(classifier).tolist()
    print(predictions)
