import os
import requests

from collections import Counter

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.data_retriever import YtDataRetriever, ESConnect
from app.classifier import GenericClassifier


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = ESConnect()

##################################### For testing purpose #####################################

@app.get("/predict/")
def test_predict_example_comments():
    """
    For testing purposes: predicts labels for a small list of example comments
    """
    clf = GenericClassifier() # default is logistic regression (with tfidf)
    comments = ["Nice song! I love it!", "Come on.. Visit my page"]
    predictions = [ clf.predict_single_comment(comment) for comment in comments ]
    return { "predictions": list(zip(comments, predictions)) }

##################################### For making predictions with multiple classifiers #####################################

@app.get("/predict/{video_id}")
def test_predict_real_comments(video_id):
    """
    For testing and comparison purpose: Output predictions made using NB and LG classiiers
    """
    predictions = []

    nb_clf = GenericClassifier("saved_models/multinomialnb_33-38.joblib")
    lr_clf = GenericClassifier("saved_models/logisticregression_34-23.joblib")

    yt = YtDataRetriever()
    data = yt.get_video_data(video_id)

    for item in data["items"]: # observe only comments and not replies
        comment = item['snippet']['topLevelComment']['snippet']['textOriginal'].strip().rstrip()

        predictions.extend([nb_clf.predict_single_comment(comment),
                            #svm_clf.predict_single_comment(comment),
                            lr_clf.predict_single_comment(comment)
                            ])

    return { f"{nb_clf.model_name} and {lr_clf.model_name} predictions": predictions }


##################################### Main FastAPI functions #####################################

@app.get("/es_status/")
def get_es_status():
    """
    Make a request for ElasticSearch and return the status code
    """
    es_status = requests.get("http://es01:9200/", auth=("elastic", os.environ["ELASTIC_PASSWORD"]), timeout=10)
    return es_status.json()


@app.post("/retrieve_comments/{video_id}")
def retrieve_comments(video_id):
    """
    Retrieve the comments from a given YouTube video using the ID
    and store them in Elastic Search
    """
    status = ""
    if video_id:
        yt = YtDataRetriever()
        data = yt.get_video_data(video_id)
        status = es.store_video_data(data, video_id)

    return { "answer": status } 


@app.get("/spam/{video_id}")
async def return_spam_comments(video_id):
    """"
    Output spam comments from the given video:
    Accesses Elastic Search instance where the labeled comments for 
    this video should already be stored.
    """
    return { "spam": es.get_spam_comments(video_id) }


##################################### Main function #####################################

if __name__ == "__main__":
    # testing
    print(f"main.py:\n{test_predict_example_comments()}")
