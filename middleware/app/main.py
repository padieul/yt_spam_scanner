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


app = FastAPI()


@app.get("/")
def read_root():
    for elem in range(4):
        print(elem)
    return {"Hello": "World"}

@app.get("/predict/{model_id}")
def predict_params(model_id: int = 0):
    if model_id == 0:
        # apply svm 
        svm_clf = joblib.load("saved_models/svc_35-37.joblib")
        prediction = test_data(svm_clf).tolist()
        return {"svc_prediction": prediction}
    elif model_id == 1:
        # apply naive_bayes
        nb_clf = joblib.load("saved_models/multinomialnb_32-21.joblib")
        prediction = test_data(nb_clf).tolist()
        return {"nbc_prediction": prediction}
    elif model_id == 2:
        lr_clf = joblib.load("saved_models/logisticregression_34-12.joblib")
        prediction = test_data(lr_clf).tolist()
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

    return {"answer": "everything fine!"}


@app.get("/predict/")
def predict():
    clf = joblib.load("saved_models/svm_clf.joblib")
    print()
    prediction = test_data(clf).tolist()
    print("File location using os.getcwd():", os.getcwd())
    
    return {"prediction": prediction}


@app.get("/es-status/")
def get_es_status():
    es_status = requests.get(
        "http://es01:9200/", auth=("elastic", os.environ["ELASTIC_PASSWORD"]))
    return es_status.json()


def download():
    nltk.download("punkt")
    nltk.download("stopwords")
    nltk.download('omw-1.4')
    nltk.download("wordnet")

def load_data(data_path):
    files = glob.glob(os.path.join(data_path, "*.csv"))
    return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)

def preprocess_data(corpus,
                    columns=["CONTENT"],
                    irrelevant_features=["COMMENT_ID", "AUTHOR", "DATE"],
                    #rename_colunms={"CONTENT":"COMMENT"}
                   ):
    
    # drop irrelevant features
    corpus.drop(irrelevant_features, inplace=True, axis=1)

    # remove blank rows if any
    corpus.dropna()
    
    # add column for representation
    corpus['REPR'] = corpus.loc[:, 'CONTENT']
        
    # lower case
    corpus['REPR'] = corpus['REPR'].str.lower()

    # change column name
    #for old, new in rename_columns:
        #corpus.rename({old : new}, axis=1, inplace=True)

    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words("english")
    
    for comment in corpus["REPR"]:    
        comment = nltk.word_tokenize(comment) # tokenizing nltk.WordPunctTokenizer().tokenize(comment.lower())?
        comment = [lemmatizer.lemmatize(word) for word in comment] # lemmatizing
        comment = [word for word in comment if word not in stop_words] # removing stopwords
        comment = " ".join(comment)


def split_data(BOW, corpus):
    return train_test_split(BOW, np.asarray(corpus["CLASS"]), test_size=0.3, random_state=42, shuffle=True)

def test_data(clf):
    path = r"data/YouTube-Spam-Collection/"
    corpus = load_data(path)
    download()

    preprocess_data(corpus)

    vectorizer = CountVectorizer(binary=True, max_df=0.95) #max_features=10000, tokenizer=lambda doc: doc)
    BOW = vectorizer.fit_transform(corpus["REPR"])

    #vectorizer = CountVectorizer(max_features=10000)
    #BOW = vectorizer.fit_transform(cleaned_corpus)

    X_train, X_test, y_train, y_test = split_data(BOW, corpus)

    y_predict = clf.predict(X_test)
    
    return y_predict

if __name__ == "__main__":
    print("start")
    clf = joblib.load("../saved_models/svm_clf.joblib")
    prediction = test_data(clf).tolist()
    print(prediction)