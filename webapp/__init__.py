from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_login import LoginManager


app = Flask(__name__)
#import secrets
#secrets.token_hex(16)
app.config["SECRET_KEY"] = '0e1892da231b615d2c3144c49ed3fe69'

consumer_key = 'GjjvbJew47BO9z7NaML7QfvkR'
consumer_secret = '6Llv4LplqMvm3vBXycPI64pgEyTzAXPkPNJe0bQHtWqZFpKULr'
access_key = '1354421821744029700-k2IIBGBQs5T0pJJDUkMoI5qfpBqdSS'
access_secret = 'Ed7V4uOq7PwBGcoEKccz6lSSu6TnFWm9M0drE7NzL2ueS'

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

from webapp import views
