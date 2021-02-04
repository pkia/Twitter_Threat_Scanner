__author__ = "Evan Dunbar"
__version__ = "1.0.1"
__maintainer__ = "Evan Dunbar"
__status__ = "Production"

'''
Function to pull most recent following
'''

from auth import api
import tweepy


def get_following(screenname, limit):
    following_list = []
    if limit < 0:
        raise Exception("Enter a number above 0!")
    elif limit > 100:  # Basic error control
        raise Exception("Max limit 200")
    else:
        limit = 200  # limit auto set to max
    for following in tweepy.Cursor(api.following, screenname).items(int(limit)):  # Uses tweepys cursor function to add most recent following to a list
        following_list.append(following)
