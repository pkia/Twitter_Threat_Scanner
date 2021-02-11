__author__ = "Evan Dunbar"
__version__ = "1.0.1"
__maintainer__ = "Evan Dunbar"
__status__ = "Production"

'''
flask dev enviroment using pipelining to display results of Logistic regression 
'''


from flask import Flask, render_template, request, redirect, url_for
from joblib import load
from tweet_pull import tweetpull

pipeline = load("text_class.joblib")


def requestResults(screen_name):
    tweets = tweetpull(screen_name)
    tweets['prediction'] = pipeline.predict(tweets['tweet_text'])
    return tweets.tweet_text[tweets.prediction == 1]

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        user = request.form['search']
        return redirect(url_for('success', name=user))


@app.route('/success/<name>')
def success(name):
    return "<xmp>" + str(requestResults(name)) + " </xmp> "


if __name__ == '__main__' :
    app.run(debug=True)

