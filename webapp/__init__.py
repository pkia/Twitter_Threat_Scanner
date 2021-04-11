from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_login import LoginManager

app = Flask(__name__)
#import secrets
#secrets.token_hex(16)
app.config["SECRET_KEY"] = ''
#  for securely signing session cookies and extension requirements

'''

import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_key, access_secret)
# access keys are now taken from user's account to enable mute/block/unfollow functions
api = tweepy.API(auth) 

# flask dance uses blueprint to create routes that allow user to login with twitter
twitter_blueprint = make_twitter_blueprint(api_key=consumer_key, api_secret=consumer_secret)
app.register_blueprint(twitter_blueprint, url_prefix='/login')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login' # login route in views.py
login_manager.login_message = '' # removes unwanted login message

from webapp import scanning
from webapp import views
