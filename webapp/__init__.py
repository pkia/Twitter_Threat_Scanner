from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_login import LoginManager

app = Flask(__name__)
#import secrets
#secrets.token_hex(16)
app.config["SECRET_KEY"] = '0e1892da231b615d2c3144c49ed3fe69'

'''
#deploy keys
consumer_key = 'ltNaOnGftDF5dFfCLhwSRAcbT'
consumer_secret = 'KFNkCJUhhwd887Feunm89UHV3ePqRKmnQSuz8anzzMfBLGDveD'
access_key = '1354421821744029700-XpVPmzhduRZoadRl6I0sSLcief0XEg'
access_secret = 'YEPi451YAO9IYqw9mY5vnOrb3Myvkk8E1f2a38yIfnakl'
'''

#localhost keys
consumer_key = 'Q2NUpbG72s2gh5zcVkIrEhrWK'
consumer_secret = 'ccMterplEvPFV94FCH0HyL7IvfkovYb1AYS7JOkeOyztKvN0yR'
access_key = '2370053247-UyXnLLZzMlF34zXUuN53BKjHSebOA0XN6eJiTCG'
access_secret = 'DRPc1pY88rvkIyEa0yxIyKrraVNiVp5l4MxSVAWSV2CyH'


import tweepy
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
#auth.set_access_token(access_key, access_secret)
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
