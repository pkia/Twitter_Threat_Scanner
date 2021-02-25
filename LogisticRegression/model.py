""" Generates .joblib """
from happytransformer import HappyTextClassification
from joblib import dump

happy_tc = HappyTextClassification('BERT', 'Hate-speech-CNERG/dehatebert-mono-english', 2)
model = happy_tc
dump(model, filename="BERT.joblib")
