import os
import glob
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


class GenericClassifier:

    def __init__(self):
        self.model = self._load_model()
        self.corpus = self._load_corpus()
        self.vectorizer = CountVectorizer(binary=True, max_df=0.95) # TODO tfidf? TODO arguments?
        self._download_nltk_packages()
        self._preprocess_corpus()

    def _load_model(self, model_path = "saved_models/svc_35-37.joblib"):
        """
        Load stored classifier
        """
        #model_path = "saved_models/svc_35-37.joblib" # TODO decide on trained classifier
        return joblib.load(model_path)

    def _load_corpus(self):
        """
        Load YouTube spam collection (kaggle dataset) from given path
        """
        data_path = r"data/YouTube-Spam-Collection/"
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


    def _preprocess_corpus(self,
                    irrelevant_features=["COMMENT_ID", "AUTHOR", "DATE"],
                    #rename_columns={"CONTENT":"COMMENT"}
                   ):
        """
        Preprocessing pipeline for YouTube spam collection
        """
        # drop irrelevant features
        #self.corpus.drop(irrelevant_features, inplace=True, axis=1)

        # remove blank rows
        self.corpus.dropna()

        # add column for representation
        self.corpus['REPR'] = self.corpus.loc[:, 'CONTENT']

        # lower case
        self.corpus['REPR'] = self.corpus['REPR'].str.lower()

        # change column name
        #for old, new in rename_columns:
        #    self.corpus.rename({old : new}, axis=1, inplace=True)

        lemmatizer = WordNetLemmatizer()
        stop_words = stopwords.words("english")

        for comment in self.corpus["REPR"]:
            comment = nltk.word_tokenize(comment) # tokenizing
            comment = [lemmatizer.lemmatize(word) for word in comment] # lemmatizing
            comment = [word for word in comment if word not in stop_words] # removing stopwords # TODO decide whether to remove them?
            # TODO more steps?
            comment = " ".join(comment)

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
        return " ".join(comment)

        
    def _get_single_comment_embedding(self, comment):
        return self.vectorizer.transform([self._preprocess_single_comment(comment)])


    def predict_single_comment(self, comment):
        """
        Classify the comment using the loaded classifier/model
        """
        prediction_label = self.model.predict(self._get_single_comment_embedding(comment))
        return { "svm_prediction": prediction_label }
