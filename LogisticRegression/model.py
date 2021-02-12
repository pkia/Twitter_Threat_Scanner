__author__ = "Evan Dunbar"
__version__ = "1.0.1"
__maintainer__ = "Evan Dunbar"
__status__ = "Production"

'''
Model using Logistic regression of TfidVecs

'''


import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from joblib import dump

data = pd.read_csv('dataset/hate.csv')
data.head()
'''
TTS - Splits data into two subsets of arrays for training data and test data
Stratift makes a split of the sample produced

'''


train, test = train_test_split(data, test_size=0.9, stratify=data['label'])

'''
Returns td-idf score by find words that are distinct and frequent in the training set
STOPWORDS - Basic linking words you dont want to be taught to the model (I , I AM, THE, ETC)
'''

tfidf_vectorizer = TfidfVectorizer(lowercase= True, max_features=1000, stop_words=ENGLISH_STOP_WORDS)



tfidf_vectorizer.fit(train.tweet)

train_idf = tfidf_vectorizer.transform(train.tweet)
test_idf = tfidf_vectorizer.transform(test.tweet)

model_LR = LogisticRegression()


model_LR.fit(train_idf, train.label)


pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer(lowercase=True,
                                                      max_features=1000,
                                                      stop_words=ENGLISH_STOP_WORDS)),
                            ('model', LogisticRegression())])

pipeline.fit(train.tweet, train.label)


dump(pipeline, filename="text_class.joblib")
