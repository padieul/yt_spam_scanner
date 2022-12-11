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
        self.corpus = self._load_data()
        self.vectorizer = CountVectorizer(binary=True, max_df=0.95) #TODO decide on arguments
        self._nltk_download()
        self._preprocess_data()

    def _load_data(self):
        """
        Load spam collection from given path
        """
        data_path = r"data/YouTube-Spam-Collection/"
        files = glob.glob(os.path.join(data_path, "*.csv"))
        return pd.concat((pd.read_csv(file) for file in files), ignore_index=True)

    def _load_model(self):
        """
        Load stored classifier
        """
        model_path = "saved_models/svc_35-37.joblib"
        return joblib.load(model_path)

    def _nltk_download(self):
        """
        Download required nltk packages
        """
        nltk.download("punkt")
        nltk.download("stopwords")
        nltk.download('omw-1.4')
        nltk.download("wordnet")


    def _preprocess_data(self,
                    irrelevant_features=["COMMENT_ID", "AUTHOR", "DATE"],
                    #rename_columns={"CONTENT":"COMMENT"}
                   ):
        """
        Preprocessing pipeline for YT spam collection
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
            comment = [word for word in comment if word not in stop_words] # removing stopwords #TODO decide whether to remove them
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
        comment = [word for word in comment if word not in stop_words] # removing stopwords #TODO decide whether to remove them
        return list(" ".join(comment))

        
    def _get_comment_embedding(self, comment):
        return self.vectorizer.transform(self._preprocess_single_comment(comment)).toarray()


    def make_prediction(self, comment):
        """
        Classify the comment using the SVM classifier
        """
        try:
            prediction_label = self.model.predict(self._get_comment_embedding(comment))
            print("working: ", prediction_label)
        except:
            print("TERRIBLE !!!!: ", comment)
            prediction_label = 3

        return { "svc_prediction": prediction_label }
