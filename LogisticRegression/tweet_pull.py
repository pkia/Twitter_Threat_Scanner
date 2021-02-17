__author__ = "Evan Dunbar"
__version__ = "1.0.1"
__maintainer__ = "Evan Dunbar"
__status__ = "Production"

'''
Function utilising pandas.dict to format tweets into a dict list format for further data manipulation
'''


from auth import api
import pandas as pd


def tweetpull(screen_name):

    alltweets = []  # List to buffer incoming tweets before being formatted for pd.dict
    new_tweets = api.user_timeline(screen_name=screen_name, count=200, tweet_mode='extend')  # Limitation to amount of tweets able to pull by twitter api
    alltweets.extend(new_tweets)  # Saving most recent tweets to alltweets
    oldest = alltweets[-1].id - 1  # Acts as counter for the each iteration starting at the oldest possible tweet -1
    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest, tweet_mode='extend')
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1  # Asks almost like a pointer that allows the func to see which tweet it needs to pull next

    outtweets = [{'created_at': tweet.created_at,  # Makes new formatted list of tweets using a pandas dict format to allow further data manipulation in future functions
                  'tweet_id': tweet.id,
                  'tweet_text': tweet.text} for tweet in alltweets]
    return pd.DataFrame.from_dict(outtweets)
