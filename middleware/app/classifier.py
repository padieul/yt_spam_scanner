import os
import glob
import joblib
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

MODEL_PATH = "saved_models/logisticregression_34-23.joblib"
VECTORIZER_PATH = "saved_models/logisticregression_34-23.joblib"


class GenericClassifier:

    def __init__(self, model_path=MODEL_PATH):
        self.model, self.model_name = self._load_model(model_path)
        self.corpus = self._load_corpus()
        self.tfidf_vectorizer = self._load_vectorizer(VECTORIZER_PATH)
        #self.tfidf_vectorizer = TfidfVectorizer(max_df=0.95, use_idf=True, stop_words='english')
        self.nlp = spacy.load("en_core_web_sm", disable=["ner"])
        self._preprocess_corpus()


    def _load_model(self, path):
        """Load stored classifier"""
        #path = "saved_models/multinomialnb_33-38.joblib" # TODO decide on trained classifier
        return joblib.load(path), (path[path.index("/")+1:][:path[path.index("/")+1:].index("_")])

    def _load_vectorizer(self, path):
        """Load stored vectorizer"""
        return joblib.load(path)


    def _load_corpus(self, data_path = "data/"):
        """Load own YouTube comments collection from the given path"""
        #data_path = r"data/YouTube-Spam-Collection/" # dataset from kaggle (1,956 comments from 5 videos among the 10 most viewed on the collection period)
        files = glob.glob(os.path.join(data_path, "*.csv"))
        return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)


    def _preprocess_corpus(self):
        """Preprocessing pipeline for the YouTube comments collection: provides lowercasing, spacy tokenization and lemmatization, and removes stopwords"""
        # remove blank rows
        self.corpus.dropna(inplace=True)

        # add column for representation
        self.corpus['REPR'] = self.corpus.loc[:, 'CONTENT']

        # lowercase
        self.corpus['REPR'] = self.corpus['REPR'].str.lower()

        # lemmatize, remove stopwords
        for comment in self.corpus["REPR"]:
            doc = self.nlp(comment)
            comment = " ".join([token.lemma_ for token in doc if not token.is_stop]) # TODO not token.is_punct?

        self.tfidf_vectorizer.fit_transform(self.corpus["REPR"])


    def _preprocess_single_comment(self, comment):
        """Preprocessing pipeline for given comment: provides lowercasing, spacy tokenization and lemmatization, and removes stopwords"""
        return " ".join([token.lemma_ for token in self.nlp(comment) if not token.is_stop]) # TODO not token.is_punct?


    def _get_single_comment_embedding(self, comment):
        """Return embedding for a given comment"""
        return self.tfidf_vectorizer.transform([self._preprocess_single_comment(comment)])


    def predict_single_comment(self, comment):
        """Classify the given comment using the loaded classifier/model"""
        emb = self._get_single_comment_embedding(comment)
        prediction_label = self.model.predict(emb)
        return { f"{self.model_name}_prediction": prediction_label }
