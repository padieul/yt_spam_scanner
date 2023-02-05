import os
import glob
import joblib
import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


class GenericClassifier:

    def __init__(self):
        self.model, self.model_name = self._load_model()
        self.corpus = self._load_corpus()
        self.vectorizer = CountVectorizer(binary=True, max_df=0.95) # TODO tfidf? TODO arguments?
        #self.tfidf_vectorizer = TfidfVectorizer(max_df=0.95, use_idf=True, stop_words='english')
        self._download_nltk_packages()
        #self.nlp = spacy.load("en_core_web_sm", disable=["ner"]) # TODO spacy instaed of nltk?
        self._preprocess_corpus()

    def _load_model(self, model_path = "saved_models/svc_35-37.joblib"):
        """
        Load stored classifier
        """
        #model_path = "saved_models/svc_35-37.joblib" # TODO decide on trained classifier
        return joblib.load(model_path), (model_path[model_path.index("/")+1:][:model_path[model_path.index("/")+1:].index("_")])

    def _load_corpus(self, data_path = "data/YouTube-Spam-Collection/"):
        """
        Load YouTube spam collection (kaggle dataset) from given path
        """
        #data_path = r"data/YouTube-Spam-Collection/"
        files = glob.glob(os.path.join(data_path, "*.csv"))
        return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)

    def _download_nltk_packages(self):
        """
        Download required nltk packages
        """
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download('omw-1.4')
        nltk.download("wordnet")


    def _preprocess_corpus(self):
        """
        Preprocessing pipeline for YouTube spam collection
        """
        # drop irrelevant features
        # rename columns

        # remove blank rows
        self.corpus.dropna()

        # add column for representation
        self.corpus['REPR'] = self.corpus.loc[:, 'CONTENT']

        # lowercase
        self.corpus['REPR'] = self.corpus['REPR'].str.lower()

        lemmatizer = WordNetLemmatizer()
        stop_words = stopwords.words("english")

        for comment in self.corpus["REPR"]:
            comment = nltk.word_tokenize(comment) # tokenizing
            comment = [lemmatizer.lemmatize(word) for word in comment] # lemmatizing
            comment = [word for word in comment if word not in stop_words] # removing stopwords # TODO decide whether to remove them?
            # TODO more steps?
            comment = " ".join(comment)

        """for comment in self.corpus["REPR"]:
            doc = self.nlp(comment)
            comment = " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
            
        self.tfidf_vectorizer.fit_transform(self.corpus["REPR"])""" # TODO spacy, tfid?

        self.vectorizer.fit_transform(self.corpus["REPR"])


    def _preprocess_single_comment(self, comment):
        """
        Preprocessing pipeline for given comment
        """
        lemmatizer = WordNetLemmatizer()
        stop_words = stopwords.words("english")

        comment = nltk.word_tokenize(comment) # tokenizing
        comment = [lemmatizer.lemmatize(word) for word in comment] # lemmatizing
        comment = [word for word in comment if word not in stop_words] # removing stopwords # TODO decide whether to remove them?
        # TODO more steps?

        """return " ".join([token.lemma_ for token in self.nlp(comment) if not token.is_stop and not token.is_punct])""" #TODO spacy?

        return " ".join(comment)

    
    def _get_single_comment_embedding(self, comment):
        #return self.tfidf_vectorizer.transform([[self._preprocess_single_comment(comment)]])
        return self.vectorizer.transform([self._preprocess_single_comment(comment)])


    def predict_single_comment(self, comment):
        """
        Classify the comment using the loaded classifier/model
        """
        prediction_label = self.model.predict(self._get_single_comment_embedding(comment))
        return { f"{self.model_name}_prediction": prediction_label }
