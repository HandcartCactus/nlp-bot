"""
Run me!
(from root directory)
conda activate twitterbot
python src\client.py --config configs\config.ini
"""
import argparse
import configparser
from datetime import timedelta

from triggers import MentionsListener
from interactions import CommandManager, MentionsLogger
import commands
import utils
from topicmodel import TopicModelCorEx
from tweettimes import TweetTimes

import twitter

commands_dict = {
    'topics': TopicModelCorEx,
    'when': TweetTimes,
}

parser = argparse.ArgumentParser()
parser.add_argument('--config', help='configuration file')
parser.add_argument(
    '-e',
    help='minutes to expire in',
    type=int,
    default=None
)


if __name__ == '__main__':
    #load configs
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(args.config)

    keys = config['Twitter Keys']

    api = twitter.Api(
        consumer_key=keys['API_Key'],
        consumer_secret=keys['API_Secret_Key'],
        access_token_key=keys['Access_Token'],
        access_token_secret=keys['Access_Token_Secret'],
        tweet_mode="extended",
    )

    paths = config['Paths']
    command_configs = config['Commands']

    command_manager = CommandManager(api, commands_dict, commands.Help, command_configs)
    mentions_listener = MentionsListener(api, paths['Latest_Mentions_ID'])
    mentions_logger = MentionsLogger(paths['Mentions_Log'])

    assert utils.api_cert_validate(api)
    print("Credentials Valid! Starting up...")

    td_expire = timedelta(minutes=args.minsexpire)

    for mention in mentions_listener.listen(verbose=True, expire_in=td_expire):
        cmd = command_manager.parse(mention)
        print('\t',cmd)
        output = cmd.reply_tweet()
        mentions_logger.log(mention)


