__author__ = "Evan Dunbar"
__version__ = "1.0.1"
__maintainer__ = "Evan Dunbar"
__status__ = "Production"

'''
Function to pull most recent followers
'''

from auth import api
import tweepy


def get_followers(screenname, limit):
    follower_list = []
    if limit < 0:
        raise Exception("Enter a number above 0!")
    elif limit > 200:  # Basic error control
        raise Exception("Max limit 200")
    else:
        limit = 200  # if limit not met auto set too max
    for follower in tweepy.Cursor(api.friends, screenname).items(int(limit)):  # Uses tweepys cursor function to add most recent followers to a list
        follower_list.append(follower.screen_name)