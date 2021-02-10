from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_login import LoginManager


app = Flask(__name__)
#import secrets
#secrets.token_hex(16)
app.config["SECRET_KEY"] = '0e1892da231b615d2c3144c49ed3fe69'

consumer_key = '7fpeLe1tRyCRZVQJXWbAg2Gtw'
consumer_secret = 'RgV6j3Lw4Q1rMnjRiI7o4eFUVyFpb018PvgcGodjyoFHJzsQ5g'
access_key = '2370053247-7ekzTGu6iihSjE4wtB6TEUeGvTzwm1utj5Swmdd'
access_secret = 'AoIFIBPYi2IcEAgrJne2Eem2MeXpKym3FGmK2TxfY3Vzi'

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
