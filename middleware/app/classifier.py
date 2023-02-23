import os
import glob
import joblib
import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class GenericClassifier:

    def __init__(self, model_path="saved_models/multinomialnb_33-38.joblib"):
        self.model, self.model_name = self._load_model(model_path)
        self.corpus = self._load_corpus()
        #self.vectorizer = CountVectorizer(binary=True, max_df=0.95) # TODO tfidf? TODO arguments?
        self.tfidf_vectorizer = TfidfVectorizer(max_df=0.95, use_idf=True, stop_words='english')
        #self._download_nltk_packages()
        self.nlp = spacy.load("en_core_web_sm", disable=["ner"]) # TODO spacy instaed of nltk?
        self._preprocess_corpus()

    def _load_model(self, path):
        """
        Load stored classifier
        """
        #path = "saved_models/multinomialnb_33-38.joblib" # TODO decide on trained classifier
        return joblib.load(path), (path[path.index("/")+1:][:path[path.index("/")+1:].index("_")])

    def _load_corpus(self, data_path = "data/YouTube-Spam-Collection/"):
        """
        Load YouTube spam collection (kaggle dataset) from given path
        """
        #data_path = r"data/YouTube-Spam-Collection/"
        files = glob.glob(os.path.join(data_path, "*.csv"))
        return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)

    """def _download_nltk_packages(self):
        #Download required nltk packages
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download('omw-1.4')
        nltk.download("wordnet")"""


    def _preprocess_corpus(self):
        """
        Preprocessing pipeline for YouTube spam collection
        """
        # remove blank rows
        self.corpus.dropna(inplace=True)

        # add column for representation
        self.corpus['REPR'] = self.corpus.loc[:, 'CONTENT']

        # lowercase
        self.corpus['REPR'] = self.corpus['REPR'].str.lower()

        for comment in self.corpus["REPR"]:
            doc = self.nlp(comment)
            # lemmatize, remove stopwords
            comment = " ".join([token.lemma_ for token in doc if not token.is_stop]) # TODO not token.is_punct?
       
        self.tfidf_vectorizer.fit_transform(self.corpus["REPR"]) # TODO tfid or countVectorizer?
        #self.vectorizer.fit_transform(self.corpus["REPR"])

    def _preprocess_single_comment(self, comment):
        """
        Preprocessing pipeline for given comment
        """
        return " ".join([token.lemma_ for token in self.nlp(comment) if not token.is_stop]) # TODO not token.is_punct?

    
    def _get_single_comment_embedding(self, comment):
        return self.tfidf_vectorizer.transform([self._preprocess_single_comment(comment)])
        #return self.vectorizer.transform([self._preprocess_single_comment(comment)])


    def predict_single_comment(self, comment):
        """
        Classify the comment using the loaded classifier/model
        """
        prediction_label = self.model.predict(self._get_single_comment_embedding(comment))
        return { f"{self.model_name}_prediction": prediction_label }
