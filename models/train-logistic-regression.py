import pandas as pd
import numpy as np
import joblib
import datetime

from sklearn.model_selection import train_test_split # split to training and testing datasets
from sklearn.model_selection import GridSearchCV # cross validation
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import spacy



def preprocess_data(corpus):
    """Preprocessing pipeline"""
    nlp = spacy.load("en_core_web_sm")

    # remove blank rows if any
    corpus.dropna(inplace=True)

    # add column for representation
    corpus['REPR'] = corpus.loc[:, 'CONTENT']

    # lower case
    corpus['REPR'] = corpus['REPR'].str.lower()

    # lemmatize, remove stopwords
    for comment in corpus["REPR"]:
        doc = nlp(comment)
        comment = " ".join([token.lemma_ for token in doc if not token.is_stop])


def split_data(features, labels):
    """Split the data into training and test datasets"""
    return train_test_split(features,labels, test_size=0.3,random_state=42,shuffle=True)


def save_model(model, tfidf):
    """Save a trained model to disk"""
    now = datetime.datetime.now()
    model_output_path = "saved_models/"+model.__class__.__name__.lower()+"_"+str(now.minute)+"-"+str(now.second)+".joblib"
    joblib.dump(model, open(model_output_path, 'wb+'))
    tfidf_output_path = "saved_models/tfidf_"+str(now.minute)+"-"+str(now.second)+".joblib"
    joblib.dump(tfidf, open(tfidf_output_path, 'wb+'))


def train_lg_classifier(features, labels, vect):
    """Train logistic regression classifier and find optimal parameters via crossvalidation"""
    X_train, X_test, y_train, y_test = split_data(features, labels) # split data
    param = {'C': [1e-5, 1e-3, 1e-1, 1e0, 1e1, 1e2]}

    clf = GridSearchCV(LogisticRegression(), param, cv=5, n_jobs=2, verbose=0)

    clf.fit(X_train, y_train)
    lg_clf = clf.best_estimator_

    save_model(lg_clf, vect) # save model to disk



if __name__ == "__main__":
    corpus = pd.read_csv("../data/dataset.csv")
    preprocess_data(corpus)

    # binary feature representation
    #vectorizer = CountVectorizer(binary=True, max_df=0.95) #max_features=10000, tokenizer=lambda doc: doc)
    #BOW = vectorizer.fit_transform(corpus["REPR"])

    # count based feature representation
    #vectorizer_2 = CountVectorizer(binary=False, max_df=0.95) #max_features=10000)
    #BOW_2 = vectorizer_2.fit_transform(corpus["REPR"])

    # bag of 2-Grams
    #bigram_vectorizer = CountVectorizer(tokenizer=lambda doc: doc, ngram_range=(2,2))
    #BOW_3 = bigram_vectorizer.fit_transform(corpus["REPR"])

    # TF-IDF
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, use_idf=True, stop_words='english') #min_df= 3, stop_words="english", sublinear_tf=True, norm='l2', ngram_range=(1, 2))
    tfidf_voc = tfidf_vectorizer.fit_transform(corpus["REPR"])

    #train_lg_classifier(BOW, np.asarray(corpus["CLASS"]))
    #train_lg_classifier(BOW_2, np.asarray(corpus["CLASS"]))
    #train_lg_classifier(BOW_3, np.asarray(corpus["CLASS"]))
    train_lg_classifier(tfidf_voc, np.asarray(corpus["CLASS"]), tfidf_vectorizer)
