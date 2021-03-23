"""
Code for interacting with users once the message was recieved
"""
import os

from flatten_json import flatten
import pandas as pd

class CommandManager(object):
    def __init__(self, api, commands, help_command):
        """Parses Mentions Tweet content and returns relevant commands, already constructed

        Args:
            api (twitter.API): the twitter api
            commands (dict(str: Command class)): dict of string names and their related command object
            help_command (Command class): if the command cannot be parsed, returns this command instead
        """
        self.api = api
        self.commands = commands
        self.help_command = help_command

    def _full_text_2_cmd(self, full_text, make_lowercase=True):
        try:
            key = full_text.split(' ')[1]
            if make_lowercase:
                key = key.lower()
            return self.commands[key]
        except:
            return None

    def _full_text_2_options(self, full_text):
        try:
            options = " ".join(full_text.split(' ')[2:])
            return options
        except:
            return None

    def parse(self, tweet, make_lowercase=True):
        #expects "@bot name <command> [options string]"

        text = tweet.full_text
        user_id = tweet.user.id
        tweet_id = tweet.id

        cmd_class = self._full_text_2_cmd(text)
        
        if cmd_class is None:
            return self.help_command(self.api, tweet_id, user_id)
        else:
            options = self._full_text_2_options(text)
            return cmd_class(api=self.api, tweet_id=tweet_id, user_id=user_id, options_string=options)


class MentionsLogger(object):
    def __init__(self, fpath):
        self.fpath = fpath
        self.built = os.path.isfile(self.fpath)
    
    def _tweet_2_flat_dict(self, tweet):
        return flatten(tweet.AsDict())

    def _first_write(self, flat_tweet):
        df = pd.DataFrame(columns=flat_tweet.keys(), data=[flat_tweet.values()])
        df.to_csv(self.fpath)
        self.built = True

    def _append(self, flat_tweet):
        df = pd.read_csv(self.fpath, index_col=0)
        print(df)
        df = df.append(flat_tweet, ignore_index=True)
        df.to_csv(self.fpath)

    def log(self, tweet):
        flat_tweet = self._tweet_2_flat_dict(tweet)
        if self.built:
            self._append(flat_tweet)
        else:
            self._first_write(flat_tweet)

