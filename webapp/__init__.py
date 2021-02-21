from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_login import LoginManager

app = Flask(__name__)
#import secrets
#secrets.token_hex(16)
app.config["SECRET_KEY"] = '0e1892da231b615d2c3144c49ed3fe69'

#marks keys
consumer_key = 'yY98pqqvjxSQtua2IjCx0GOhP'
consumer_secret = 'z2Umqy3CnS484yOjDZ9hw0pT0JEG36p9AfiBhd57xwhGNnT3zF'
access_key = '1354421821744029700-G4y8X7P2pwLbKIo3KVXHF3iQs1MSb3'
access_secret = '9MWD5hMyf4UEThXdMFL4wuiwyiX77oxZyGQIakM8nXAtb'

'''
#evans keys
consumer_key = 'T9Zf9RjXPzUR74MElwXSc322V'
consumer_secret = 'EcFc0W8ZMVHVr9zPViClxeinjkNDSaMRH33vC9SRkv4J5CgB58'
access_key = '2370053247-nuZnBzC316VEGYtCHPDWP47VFh7wAis3blVtoLZ'
access_secret = 'Ra6uNqSNztob2UmLQG6nVTuFNF608CI3190CkxndNSeik'
'''

import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth) 

twitter_blueprint = make_twitter_blueprint(api_key=consumer_key, api_secret=consumer_secret)
app.register_blueprint(twitter_blueprint, url_prefix='/login')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = ''

from webapp import scanning
from webapp import views
