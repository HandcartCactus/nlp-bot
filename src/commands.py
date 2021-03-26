from abc import ABC, abstractclassmethod
from twitter import TwitterError
from datetime import datetime

class Command(ABC):
    def __init__(self, api, tweet_id, config, user_id=None, options_string=None):
        self.api = api
        self.tweet_id = int(tweet_id)
        self.user_id = user_id
        self.options_string = options_string
        self.config = config
        self.repr = 'Generic Command Class'

    
    @abstractclassmethod
    def reply_tweet(self):
        #self.api.PostUpdate(status)
        pass

    def __repr__(self):
        return self.repr

class Help(Command):
    def reply_tweet(self):
        message = f"I don't recognize that command. See my pinned tweet for help. ({datetime.now()})"
        try:
            self.api.PostUpdate(status=message, in_reply_to_status_id=self.tweet_id, auto_populate_reply_metadata=True)
        except TwitterError as e:
            print(e)

    def __repr__(self):
        return "Help Command"
