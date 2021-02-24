from joblib import load
from tweet_pull import tweet_pull
import pandas as pd

# load the pipeline object
pipeline = load("BERT.joblib")


def requestResults(name):
    """Returns flagged tweets for a particular user query"""
    tweets = tweet_pull(name)
    buffer = []
    c = 0
    for tweet in tweets['tweet_text']:
        c += 1
        tweets['prediction'] = pipeline.classify_text(tweet)
        if 'LABEL_1' in str(tweets['prediction']):
            id = tweets['tweet_id'][c]
            buffer.append((id,tweet))
    flagged_tweets = pd.DataFrame.from_dict([{'Flagged_tweets': tweet} for tweet in buffer])
    return flagged_tweets

'''
app = Flask(__name__)


# render default webpage
@app.route('/')
def home():
    return render_template('home.html')


# when the post method detect, then redirect to success function
@app.route('/', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        user = request.form['search']
        return redirect(url_for('success', name=user))


# get the data for the requested query
@app.route('/success/<name>')
def success(name):
    return "<xmp>" + str(requestResults(name)) + " </xmp> "


if __name__ == '__main__':
    app.run(debug=True)
'''