import os
import pickle

import pandas as pd
import re
import numpy as np
from sklearn.model_selection import train_test_split

from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM, Embedding, Dropout
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

import nltk
import string

nltk.download("wordnet")


from nltk.corpus import stopwords

stop = stopwords.words('english')
ps = nltk.PorterStemmer()
lm = nltk.WordNetLemmatizer()

script_dir = os.path.dirname(__file__)

def getPickleResult(text):
    rel_path = "tokenizer_final1.pickle"
    abs_path = os.path.join(script_dir, rel_path)

    # print(abs_path)

    with open(abs_path, 'rb') as handle:
        tokenizer = pickle.load(handle)

        xx = tokenizer.texts_to_sequences([text])
        xx = pad_sequences(xx, maxlen=23)

        return xx

def getSentimentResult(xx_text):
    rel_path = "sentiment_analysis.h5"
    abs_path = os.path.join(script_dir, rel_path)

    new = load_model(abs_path)
    # new.summary()

    result_arr = new.predict(xx_text)

    print(result_arr)
    print(np.amax(result_arr))

    return result_arr

def getSentiment(result_arr):
    if np.argmax(result_arr)==0:
        result_sentiment = 'Negative'
    elif np.argmax(result_arr)==1:
        result_sentiment = 'Neutral'
    elif np.argmax(result_arr)==2:
        result_sentiment = 'Positive'

    print(result_sentiment)

    return result_sentiment