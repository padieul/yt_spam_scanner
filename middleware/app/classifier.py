import os
import glob
import joblib
import spacy
import pandas as pd

MODEL_PATH = "saved_models/logisticregression_27-2-23_16-49-13.joblib" # LG model with tfidf
VECTORIZER_PATH = "saved_models/tfidf_logisticregression_27-2-23_16-49-13.joblib" # tfidf vectorizer


class GenericClassifier:

    def __init__(self, model_path=MODEL_PATH):
        self.model, self.model_name = self._load_model(model_path)
        self.corpus = self._load_corpus()
        self.tfidf_vectorizer = self._load_vectorizer(VECTORIZER_PATH)
        self.nlp = spacy.load("en_core_web_sm", disable=["ner"])


    def _load_model(self, path):
        """Load stored classifier"""
        return joblib.load(path), (path[path.index("/")+1:][:path[path.index("/")+1:].index("_")])


    def _load_vectorizer(self, path):
        """Load stored vectorizer"""
        return joblib.load(path)


    def _load_corpus(self, data_path = "data/"):
        """Load own YouTube comments collection from the given path"""
        files = glob.glob(os.path.join(data_path, "*.csv"))
        return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)


    def _preprocess_single_comment(self, comment):
        """
        Preprocessing pipeline for given comment:
        provides lowercasing, spacy tokenization and lemmatization, and removes stopwords
        """
        return " ".join([token.lemma_ for token in self.nlp(comment) if not token.is_stop])


    def _get_single_comment_embedding(self, comment):
        """Return embedding for a given comment"""
        return self.tfidf_vectorizer.transform([self._preprocess_single_comment(comment)])


    def predict_single_comment(self, comment):
        """Classify the given comment using the loaded classifier/model"""
        emb = self._get_single_comment_embedding(comment)
        prediction_label = self.model.predict(emb)
        return { f"{self.model_name}_prediction": prediction_label }
