from auth import api
import pandas as pd
import preprocessor as p


def tweet_pull(screen_name):
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1

    user_tweets = [{'created_at': tweet.created_at,
                   'tweet_id': tweet.id,
                   'tweet_text': p.clean(tweet.text)} for tweet in all_tweets]

    return pd.DataFrame.from_dict(user_tweets)
