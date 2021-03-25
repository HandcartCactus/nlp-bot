def api_cert_validate(api):
    return not api.VerifyCredentials() is None

def whole_number(i):
    assert i==int(i) and i>0

def format_mention(tweet):
    text = tweet.full_text
    at = tweet.created_at
    user_sn = tweet.user.screen_name
    user_n = tweet.user.name
    user_followers = tweet.user.followers_count
    s = f"Tweet: \"{text}\" from {user_n} (@{user_sn}, {user_followers} followers) at {at}."
    return s


