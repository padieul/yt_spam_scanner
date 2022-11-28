from typing import Union
import os

from fastapi import FastAPI
import requests

app = FastAPI()


@app.get("/")
def read_root():
    for elem in range(4):
        print(elem)
    return {"Hello": "World"}


@app.get("/es-status/")
def get_es_status():
    es_status = requests.get(
        "http://es01:9200/", auth=("elastic", os.environ["ELASTIC_PASSWORD"]))
    return es_status.json()