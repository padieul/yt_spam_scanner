import os
import httplib2
import spacy
import googleapiclient
import googleapiclient.discovery
from oauth2client import client, GOOGLE_TOKEN_URI

from elasticsearch import helpers
from elasticsearch import Elasticsearch

from app.classifier import GenericClassifier


CLIENT_ID = "737324637694-b6ngjvspqdgv9cbkto3li52ljcl09k4h.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "refresh_token"
DEVELOPER_KEY = "AIzaSyB3pX9aY3rmP8xZSngxxX14NseZ6KCxb0U"
nlp = spacy.load("en_core_web_sm", disable=["ner"]) #TODO decide on arguments


class YtDataRetriever:

    def __init__(self):
        self._data_response = {}

        credentials = client.OAuth2Credentials(
            access_token=None,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            refresh_token=REFRESH_TOKEN,
            token_expiry=None,
            token_uri=GOOGLE_TOKEN_URI,
            user_agent=None,
            revoke_uri=None)

        self.http = credentials.authorize(httplib2.Http())


    # TODO old method that will be deleted soon (ok BUT still used!?)
    def get_video_data(self, video_id: str):

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = 'client_secret_737324637694-2c43sarhojqelig5rhvmp4pgkh8oiv5c.apps.googleusercontent.com.json'

        api_service_name = "youtube"
        api_version = "v3"

        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=DEVELOPER_KEY)

        self._data_response = self.get_video_comments(youtube, video_id)
        return self._data_response

    def get_comment_replies(self, service, comment_id):
        request = service.comments().list(
            parentId=comment_id,
            part='id,snippet',
            maxResults=100
        )
        replies = []

        while request:
            response = request.execute()
            replies.extend(response['items'])
            request = service.comments().list_next(
                request, response)

        return replies

    def get_video_comments(self, service, video_id):
        request = service.commentThreads().list(
            videoId=video_id,
            part='id,snippet,replies',
            maxResults=100
        )

        data = {}
        comments = []

        while request:
            response = request.execute()

            data['kind'] = response['kind']
            data['etag'] = response['etag']
            data['pageInfo'] = response['pageInfo']

            for comment in response['items']:
                reply_count = comment['snippet']['totalReplyCount']
                replies = comment.get('replies')
                if replies is not None and \
                        reply_count != len(replies['comments']):
                    replies['comments'] = self.get_comment_replies(service, comment['id'])

                # 'comment' is a 'CommentThreads Resource' that has it's
                # 'replies.comments' an array of 'Comments Resource'

                # Do fill in the 'comments' data structure
                # to be provided by this function:
                comments.append(comment)

            data['items'] = comments

            request = service.commentThreads().list_next(request, response)

        return data

class YtComment:

    def __init__(self, data_item = None):
        if data_item is None: # reply
            self._id = None
            self._text_original = None
            self._author_name = None
            self._author_channel_url = None
            self._author_channel_id = None
            self._like_count = None
            self._publish_date = None

            self._is_reply = None
            self._parent_id = None

        else: # comment
            self._id = data_item["snippet"]["topLevelComment"]["id"]
            self._text_original = data_item['snippet']['topLevelComment']['snippet']['textOriginal'].replace("\n", "")
            self._author_name = data_item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            self._author_channel_url = data_item["snippet"]["topLevelComment"]["snippet"]["authorChannelUrl"]
            self._author_channel_id = data_item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
            self._like_count = data_item['snippet']['topLevelComment']['snippet']['likeCount']
            self._publish_date = data_item['snippet']['topLevelComment']['snippet']['publishedAt']

            self._is_reply = False
            self._parent_id = self._id

    def set_id(self, arg):
        self._id = arg

    def set_text_original(self, arg):
        self._text_original = arg

    def set_author_name(self, arg):
        self._author_name = arg

    def set_author_chan_url(self, arg):
        self._author_channel_url = arg

    def set_author_chan_id(self, arg):
        self._author_channel_id = arg

    def set_like_count(self, arg):
        self._like_count = arg

    def set_publish_date(self, arg):
        self._publish_date = arg

    def set_is_reply(self, arg):
        self._is_reply = arg

    def set_parent_id(self, arg):
        self._parent_id = arg

    def get_text_original(self):
        return self._text_original

    def get_author_name(self):
        return self._author_name

    def get_author_chan_url(self):
        return self._author_channel_url

    def get_author_chan_id(self):
        return self._author_channel_id

    def get_like_count(self):
        return self._like_count

    def get_publish_date(self):
        return self._publish_date

    def get_is_reply(self):
        return self._is_reply

    def get_parent_id(self):
        return self._parent_id

    def get_id(self):
        return self._id

class YtCommentReply:

    def __init__(self, data_item):
        self._id = data_item["id"]
        self._text_original = data_item['snippet']['textOriginal'].replace("\n", "")
        self._author_name = data_item["snippet"]["authorDisplayName"]
        self._author_channel_url = data_item["snippet"]["authorChannelUrl"]
        self._author_channel_id = data_item["snippet"]["authorChannelId"]["value"]
        self._like_count = data_item['snippet']['likeCount']
        self._publish_date = data_item['snippet']['publishedAt']

        self._is_reply = True
        self._parent_id = data_item["snippet"]["parentId"]

    def to_yt_comment(self):
        yt_comment = YtComment()
        yt_comment.set_id(self._id)
        yt_comment.set_text_original(self._text_original)
        yt_comment.set_author_name(self._author_name)
        yt_comment.set_author_chan_url(self._author_channel_url)
        yt_comment.set_author_chan_id(self._author_channel_id)
        yt_comment.set_like_count(self._like_count)
        yt_comment.set_publish_date(self._publish_date)

        yt_comment.set_is_reply(self._is_reply)
        yt_comment.set_parent_id(self._parent_id)

        return yt_comment

class ESConnect:

    def __init__(self):
        #self._es_client = Elasticsearch("http://es01:9200", auth=("elastic", "1234"))
        self._es_client = Elasticsearch("http://es01:9200")
        self._classifier = GenericClassifier()
        self._es_index = "yt_video"
        self._es_index_name = ""

    def _set_es_index_name(self, video_id):
        self._es_index_name = (str(self._es_index) + "_" + str(video_id)).lower()

    def store_video_data(self, video_comments_data, video_id):
        """
        Loading data into elasticsearch
        """
        comments = []
        for item in video_comments_data["items"]:
            try:
                comment = YtComment(item)
                comments.append(comment)
            except:
                continue #TODO
            # except Exception as e:
            #    print(e)
            if "replies" in item.keys():
                for reply in item["replies"]["comments"]:
                    try:
                        comment_reply = YtCommentReply(reply)
                        comments.append(comment_reply.to_yt_comment())
                    except:
                        continue #TODO
                # TODO replies of reply?

        actions = []
        self._set_es_index_name(video_id) # self._es_index_name = str(self._es_index) + "_" + str(video_id)

        for i, comment in enumerate(comments):
            source = { 'id': comment.get_id(),
                       'content': comment.get_text_original(),
                       'author_name': comment.get_author_name(),
                       'author_channel_url': comment.get_author_chan_url(),
                       'author_channel_id': comment.get_author_chan_id(),
                       'like_count': comment.get_like_count(),
                       'comment_length': len(nlp(comment.get_text_original())), # TODO by spacy sind PUNCT auch separate tokens -> len(comment.get_text_original().split(" ")) ?
                       'publish_date': comment.get_publish_date(),
                       'is_reply': comment.get_is_reply(),
                       'parent_id': comment.get_parent_id(),
                       "spam_label": self._classifier.predict_single_comment(comment.get_text_original()), # TODO list or single char? TODO ensemble model -> NB, LR ?
                       "classifier": "support_vector_machine" # TODO "naive_bayes", "logistic_regression" ?
                     }

            action = {
                "_index": self._es_index_name, #.lower(),
                '_op_type': 'index',
                "_type": '_doc',
                "_source": source
            }
            actions.append(action)

        res = helpers.bulk(self._es_client, actions)
        return res # TODO return statement? status of the action to be shown in frontend?


    def get_spam_comments(self, video_id): #TODO test
        """
        return the spam comments found/predicted in the given video
        """
        self._set_es_index_name(video_id)

        search_query = {"term": {
                                "spam_label.svm_prediction": {
                                    "value": 1
                                    }
                                }
                        }

        search_result = self._es_client.search(index=self._es_index_name, query=search_query)
        spam_comments = [ result["_source"]["content"] for result in search_result["hits"]["hits"] ]

        print(spam_comments)
        return spam_comments


if __name__ == "__main__":
    yt = YtDataRetriever()
    es = ESConnect()
    VIDEO_ID = "kdcvyfjuKCw"
    data = yt.get_video_data(VIDEO_ID)
    print(data)
    print(es.store_video_data(data, VIDEO_ID))
