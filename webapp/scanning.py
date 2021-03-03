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
    pipeline = load("./BERT.joblib")
    tweets = tweetpull(username)  # get the target's tweets
    total_tweets = len(tweets)
    buffer = []
    counter = -1
    for tweet in tweets['tweet_text']:
        counter += 1
        tweets['prediction'] = pipeline.classify_text(tweet)
        if 'LABEL_1' in str(tweets['prediction']):
            id = tweets['tweet_id'][counter]
            buffer.append((tweet, id))
    bad_tweets = [{'tweet_text': tweet,
                   'tweet_id': id} for tweet, id in buffer]
    total_scanned_tweets = len(bad_tweets)
    user_info = api.get_user(username)
    profile_info = [{'username': str(user_info.screen_name.lower()),
                     'screenname': user_info.name,
                     'profile_img_url': user_info.profile_image_url,
                     'private': user_info.protected,
                     'total_reports': int(len(Report.query.filter_by(account_id=username).all())),
                     'total_tweets': int(total_tweets),
                     'total_scanned_tweets': int(total_scanned_tweets),
                     'danger_level': get_danger_level(username, total_tweets, total_scanned_tweets)
                     }]
    bad_tweets_df = pd.DataFrame.from_dict(bad_tweets)
    profile_info_df = pd.DataFrame.from_dict(profile_info)
    scan_results = profile_info_df.join(bad_tweets_df)
    return scan_results
    # returns results (bad tweet ids, the tweet text and the overall account summary) and account summary and profile


def get_twitter_info(screen_name):
    screen_name = screen_name.lower()  # make sure it is lowercase
    user_info = api.get_user(screen_name)  # use tweepy to get user object or return error if doesn't exist
    twitter_info = pd.DataFrame.from_dict[{'username': user_info.screen_name.lower(),
                                           'screenname': user_info.name,
                                           'profile_img_url': user_info.profile_image_url,
                                           'private': user_info.protected
                                           }]
    return twitter_info


def get_followers(screenname, limit=10):
    follower_list = []
    if limit < 0:
        raise Exception("Enter a number above 0!")
    elif limit > 100:  # Basic error control
        raise Exception("Max limit 100")
    for follower in tweepy.Cursor(api.followers, screenname).items(
            int(limit)):  # Uses tweepys cursor function to add most recent followers to a list
        follower_list.append(follower.screen_name)
    return follower_list  # screen names of all followers of entered user


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
                    'tweet_text': p.clean(tweet.text)
                    } for tweet in all_tweets]

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
    account_summary = [{'total_reports': total_reports,
                        'total_tweets': total_tweets,
                        'total_scanned_tweets': total_scanned_tweets,
                        'danger_level': danger_level
                        }]
    return pd.DataFrame.from_dict(account_summary)


def get_danger_level(screen_name, total_tweets, total_scanned_tweets):
    if total_tweets > 100:
        total_tweets = 100
    percent = total_scanned_tweets / total_tweets
    danger_level = percent * 10
    danger_level = round(danger_level)
    return danger_level


def scan_all_function(followers):
    scan_results = pd.DataFrame()
    for follower in followers:
        user_info = api.get_user(follower)
        if not user_info.protected:
            follower_report = scan(follower)
            print(follower_report)
            frames = [scan_results, follower_report]
            scan_results = pd.concat(frames)
    return scan_results


def mute_user(screen_name):
    api.create_mute(screen_name)


def unfollow_user(screen_name):
    api.destroy_friendship(screen_name)


def block_user(screen_name):
    api.create_block(screen_name)