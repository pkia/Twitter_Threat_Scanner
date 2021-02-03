__author__ = "Evan Dunbar"
__version__ = "1.0.1"
__maintainer__ = "Evan Dunbar"
__status__ = "Production"

'''
Function to pull twitter users data (screen_name, followers count, following count, profile image url)
'''

from auth import api


def get_twitter_info(screen_name):
    user_info = api.get_user(screen_name)  # Finds user with api
    screen_name = user_info.name  # Gets user screen name
    alias = "@" + user_info.screen_name  # Gets users twitter @
    followers_count = user_info.followers_count  # Gets users follower count
    following_count = user_info.friends_count  # Gets users following count
    profile_image = user_info.profile_image_url  # Get profile image url
    return screen_name, alias, followers_count, following_count, profile_image
