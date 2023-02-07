from collections import Counter
import os

from fastapi import FastAPI
import requests

from app.data_retriever import YtDataRetriever, ESConnect
from app.classifier import GenericClassifier


app = FastAPI()


@app.get("/")
def read_root():
    """
    For testing purpose
    """
    for elem in range(4):
        print(elem)
    return {"Hello": "World"}


@app.get("/predict/")
def test_predict():
    """
    For testing purpose
    """
    clf = GenericClassifier() # default SVM
    comments = ["Nice song! I love it!", "Come on.. Visit my page"]

    predictions = [ clf.predict_single_comment(comment) for comment in comments ]

    #return { "spam comments": [ comment for comment, prediction in zip(comments, predictions) if prediction == [1] ] }
    return { "predictions": list(zip(comments, predictions)) }


@app.get("/es-status/") # TODO stay consistent (- or _ -> e.g. retrieve_comments)
def get_es_status():
    """
    Make a request for ElasticSearch and return the status code
    """
    es_status = requests.get("http://es01:9200/", auth=("elastic", os.environ["ELASTIC_PASSWORD"]), timeout=10)

    return es_status.json()


@app.post("/retrieve_comments/{video_id}")
def retrieve_comments(video_id: str = ""):
    """
    Retrieve the comments from a given YouTube video using the ID
    """
    if not video_id: # empty string
        print("******************************************")
        print("No video ID received")
    else:
        print("******************************************")
        print(f"Video ID received: {video_id}")

        yt = YtDataRetriever()
        data = yt.get_video_data(video_id) # TODO which function is to be used? (get_video_comments)
        es = ESConnect()
        status = es.store_video_data(data, video_id)

    return { "answer": status } # TODO handle status


@app.get("/predict/{video_id}") #{model_id}") # TODO prediction is performed by storing the comments in ES
def predict_comments(video_id): #model_id: int = 0):
    """
    Output predictions made using certain model
    """
    # TODO train models again with the same preprocessing and vectorizer
    predictions = []
    ensemble_predictions = [] # TODO ensemble

    svm_clf = GenericClassifier("saved_models/svc_35-37.joblib")
    nb_clf = GenericClassifier("saved_models/multinomialnb_32-21.joblib")
    lr_clf = GenericClassifier("saved_models/logisticregression_34-12.joblib")

    yt = YtDataRetriever()
    data = yt.get_video_data(video_id)

    for item in data["items"]: # observe only comments and not replies
        comment = item['snippet']['topLevelComment']['snippet']['textOriginal'].replace("\n", "")
        predictions.extend([svm_clf.predict_single_comment(comment),
                            nb_clf.predict_single_comment(comment),
                            lr_clf.predict_single_comment(comment)
                            ])
        ensemble_predictions.append(Counter([svm_clf.predict_single_comment(comment),
                                            nb_clf.predict_single_comment(comment),
                                            lr_clf.predict_single_comment(comment)]
                                            ).most_common()[0])

    return { f"{svm_clf.model_name}, {nb_clf.model_name} and {lr_clf.model_name} predictions": predictions }
    # return { "ensemble predictions": ensemble_predictions }

# https://www.youtube.com/watch?v=OXEteCPQcGc

@app.post("/spam/{video_id}")
async def return_spam_comments(video_id):
    """"
    Output spam comments from given video
    """
    es = ESConnect()
    print("------------------------------------------------------")
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    return { "spam comments": es.get_spam_comments(video_id) }



if __name__ == "__main__":
    print("main.py")
    print(test_predict())
