from webapp.models import Report
from webapp import app
from webapp import db
from webapp import api
from datetime import datetime
from webapp import tweepy
import pandas as pd
from joblib import load
import preprocessor as p
        
def scan(username):
    pipeline = load("LogisticRegression/BERT.joblib")
    tweets = tweetpull(username) # get the target's tweets
    total_tweets = len(tweets)
    buffer = []
    c = -1
    for tweet in tweets['tweet_text']:
        c += 1
        tweets['prediction'] = pipeline.classify_text(tweet)
        if 'LABEL_1' in str(tweets['prediction']):
            id = tweets['tweet_id'][c]
            buffer.append((id,tweet))
    bad_tweets = pd.DataFrame.from_dict([{'Flagged_tweets': tweet} for tweet in buffer])
    intial_results = bad_tweets["Flagged_tweets"] 
        # gets the bad tweet ids, the tweet text and the overall account summary
    tweet_ids = []
    tweet_text = []
    for item in intial_results.iteritems():
        tweet_ids.append(item[0])
        tweet_text.append(item[1])
    tweets = list(zip(tweet_ids, tweet_text))
    total_scanned_tweets = len(bad_tweets)
    account_summary = get_account_summary(username, total_scanned_tweets, total_tweets)
    profile = get_twitter_info(username)
    return tweets, account_summary, profile # returns results (bad tweet ids, the tweet text and the overall account summary) and account summary and profile
    
def scan_all_function(followers):
    bad = [] # list of usernames where something bad was found
    for follower in followers: # for follower id in follower id list
        if check_if_protected(follower): # if user is protected don't scan
            continue
        tweets, account_summary, profile = scan(follower) # get results of bad followers
        if len(tweets) > 0: # if there were flagged tweets
            scanned_user = [tweets, account_summary, profile]# save a list with the profile and the results of the follower
            bad.append(scanned_user) # add it to a list of bad results/profiles
    return bad

def get_twitter_info(screen_name):
    screen_name = screen_name.lower() # make sure it is lowercase
    user_info = api.get_user(screen_name) # use tweepy to get user object or return error if doesn't exist
    profile = [user_info.screen_name.lower(), user_info.name, user_info.profile_image_url, user_info.protected]# [0]screen_name [1]name [2]profile picture [3] boolean if they're protected or not
    return profile

def get_followers(screenname, limit=10):
    follower_list = []
    if limit < 0:
        raise Exception("Enter a number above 0!")  
    elif limit > 100:  # Basic error control
        raise Exception("Max limit 100")
    for follower in tweepy.Cursor(api.followers, screenname).items(int(limit)):  # Uses tweepys cursor function to add most recent followers to a list
        follower_list.append(follower.screen_name)
    return follower_list # screen names of all followers of entered user

def tweetpull(screen_name):
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

def check_if_protected(screen_name):
    protected = False
    profile = get_twitter_info(screen_name)
    if profile[3] == True:
        protected = True
    return protected


def get_account_summary(screen_name, total_scanned_tweets, total_tweets):
    total_reports = len(Report.query.filter_by(account_id=screen_name).all())
    danger_level = get_danger_level(screen_name, total_tweets, total_scanned_tweets)
    account_summary = [total_reports, total_tweets, total_scanned_tweets, danger_level]
    return account_summary


def get_danger_level(screen_name, total_tweets, total_scanned_tweets):
    if total_tweets > 100:
        total_tweets = 100
    percent = total_scanned_tweets / total_tweets
    danger_level = percent * 10
    danger_level = round(danger_level)
    return danger_level

def mute_user(screen_name):
    api.create_mute(screen_name)
    
def unfollow_user(screen_name):
    api.destroy_friendship(screen_name)
    
def block_user(screen_name):
    api.create_block(screen_name)
