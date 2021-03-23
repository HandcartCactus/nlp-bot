from sklearn.feature_extraction.text import CountVectorizer

def tweet2doc(tweet, patterns_del=[]):
    """Converts a tweet "Status" class into a stripped plaintext string

    Args:
        tweet (twitter.models.Status): A tweet
        patterns_del (list(str)): A list containing strings to remove

    Returns:
        str: tweet plaintext
    """
    t = tweet.full_text
    for u in tweet.user_mentions:
        sc = u.screen_name
        t = t.replace('@'+sc,'')
    for url in tweet.urls:
        t = t.replace(str(url.url),'')
    for w in patterns_del:
        t = t.replace(w,'')
    return t

def tweetlist2docs(tweets):
    """Turns a list of tweets into a list of strings

    Args:
        tweets (list(twitter.models.Status)): list of tweets

    Returns:
        list(str): a corpus of tweets
    """
    return [tweet2doc(s) for s in tweets]

def get_max_tweets(api, user_id):
    """Get as many tweets as possible for a user

    Args:
        api (twitter.API): twitter api
        user_id (int): twitter user id as an int (not screen name!)

    Returns:
        list(twitter.models.Status): list of tweets from that user
    """
    tweets = api.GetUserTimeline(
        user_id=user_id,
        screen_name=None,
        since_id=None,
        max_id=None,
        count=200,
        include_rts=True,
        trim_user=False,
        exclude_replies=False
    )

    return tweets

def tweet_corpus(api, user_id):
    """Get a tweet corpus from a user

    Args:
        api (twitter.API): twitter api
        user_id (int): twitter user id

    Returns:
        list(str): tweet corpus for user
    """
    tweetlist = get_max_tweets(api, user_id)
    docs = tweetlist2docs(tweetlist)
    return docs