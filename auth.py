__author__ = "Evan Dunbar"
__version__ = "1.0.1"
__maintainer__ = "Evan Dunbar"
__status__ = "Production"

'''
Basic twitter api auth file, used for fast OAuth between functions.
'''

import tweepy
consumer_key = '7fpeLe1tRyCRZVQJXWbAg2Gtw'
consumer_secret = 'RgV6j3Lw4Q1rMnjRiI7o4eFUVyFpb018PvgcGodjyoFHJzsQ5g'
access_key = '2370053247-7ekzTGu6iihSjE4wtB6TEUeGvTzwm1utj5Swmdd'
access_secret = 'AoIFIBPYi2IcEAgrJne2Eem2MeXpKym3FGmK2TxfY3Vzi'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)