from webapp.models import Account, Report, ScanResult
from webapp import app
from webapp import db
from webapp import api
from datetime import datetime
from webapp import tweepy
import pandas as pd
from joblib import load

def scan(username):
    ScanResult.query.filter_by(account_id=username).delete() # delete any previous results from the db
    db.session.commit()
    tweets = tweetpull(username) # get the target's tweets
    pipeline = load("LogisticRegression/text_class.joblib") # loads the logistic regression model
    tweets['prediction'] = pipeline.predict(tweets['tweet_text']) # adds a prediction column to the data which is 1 for hatespeech, 0 for all good
    data = tweets.prediction.value_counts() # this data is for the summary, contains total tweets and total flagged tweets
    bad_tweets = tweets.loc[tweets['prediction'] == 1] # these are pandas dataframes, these are all the tweets flagged as hatespeech
    results = [bad_tweets["tweet_id"], bad_tweets["tweet_text"], data] # gets the bad tweet ids, the tweet text and the overall account summary
    return results # returns results (bad tweet ids, the tweet text and the overall account summary)

def scan_user_function(username): 
    results = scan(username) # scan the target and save results
    scan_results = []
    if len(results[0]) > 0: # if there are 1 or more results
        if Account.query.get(username) == None: # if there is no account stored in db for this screen_name
            account = Account(id=username) # make an account for the target
            db.session.add(account)
            db.session.commit()
        for item in results[0].iteritems(): # for every tweet id in the bad scanned tweets list
            scan_result = ScanResult(id=item[1], threat_detected="hatespeech", account_id=username) # make a ScanResult object with that id
            db.session.add(scan_result) # add it to db
            scan_results.append(scan_result)
        db.session.commit()
    return scan_results # return list of scan results
    
def scan_all_function(username, followers):
    bad = [] # list of usernames where something bad was found
    for follower in followers: # for follower id in follower id list
        if check_if_protected(username): # if user is protected don't scan
            continue
        profile = get_twitter_info(username)
        scan_results = scan_user_function(follower) # get scan_results of every follower
        if len(scan_results) > 0: # if there were flagged tweets
            results = [profile, scan_results] # save a list with the profile and the results of the follower
            bad.append(results) # add it to a list of bad results/profiles
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
    alltweets = []  # List to buffer incoming tweets before being formatted for pd.dict
    if check_if_protected(screen_name) is False: # if not protected acc
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)  # Limitation to amount of tweets able to pull by twitter api
        alltweets.extend(new_tweets)  # Saving most recent tweets to alltweets
        if len(alltweets) > 0:
            oldest = alltweets[-1].id - 1  # Acts as counter for the each iteration starting at the oldest possible tweet -1
        while len(new_tweets) > 0:
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1  # Asks almost like a pointer that allows the func to see which tweet it needs to pull next

    outtweets = [{'created_at': tweet.created_at,  # Makes new formatted list of tweets using a pandas dict format to allow further data manipulation in future functions
                  'tweet_id': tweet.id,
                  'tweet_text': tweet.text} for tweet in alltweets]
    return pd.DataFrame.from_dict(outtweets)

def check_if_protected(screen_name):
    protected = False
    profile = get_twitter_info(screen_name)
    if profile[3] == True:
        protected = True
    return protected
    
    
def get_account_summary(screen_name):
    pass
