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
from keras.models import model_from_json
from keras.preprocessing import text, sequence

import nltk
import string

nltk.download("wordnet")

from nltk.corpus import stopwords

import emoji

stop = stopwords.words('english')
ps = nltk.PorterStemmer()
lm = nltk.WordNetLemmatizer()

script_dir = os.path.dirname(__file__)

def getPickleResult(text):
    rel_path = "tokenizer_final5.pickle"
    abs_path = os.path.join(script_dir, rel_path)

    # print(abs_path)

    with open(abs_path, 'rb') as handle:
        tokenizer = pickle.load(handle)

        xx = tokenizer.texts_to_sequences([text])
        xx = pad_sequences(xx, maxlen=224)

        return xx

def getSentimentResult(xx_text):
    rel_path = "sentiment_analysis-final.h5"
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

def punctuation(val): 
  
    punctuations = '''()-[]{};:'"\,<>./@#$%^&_~'''
    for x in val.lower(): 
        if x in punctuations: 
            val = val.replace(x, " ") 
    return val

def clean_text(val):
    # val = p.clean(val)
    val = ' '.join(punctuation(emoji.demojize(val)).split())
    return val

def get_pickle_result(val):
    rel_path = 'token.pickle'
    abs_path = os.path.join(script_dir, rel_path)
    with open(abs_path, 'rb') as handle:
        token = pickle.load(handle)
        #tokenize
        text = clean_text(val)
        twt = token.texts_to_sequences([text])
        twt = sequence.pad_sequences(twt, maxlen=160, dtype='int32')

        return twt



def get_sentiment(twt):
    rel_path = 'model.h5'
    abs_path = os.path.join(script_dir, rel_path)
    model = load_model(abs_path)

    sent_to_id  = {"empty":0, "sadness":1,"enthusiasm":2,"neutral":3,"worry":4,
                        "surprise":5,"love":6,"fun":7,"hate":8,"happiness":9,"boredom":10,"relief":11,"anger":12}

    sentiment = model.predict(twt,batch_size=1,verbose = 2)
    sent = np.round(np.dot(sentiment,100).tolist(),0)[0]
    result = pd.DataFrame([sent_to_id.keys(),sent]).T
    result.columns = ["sentiment","percentage"]
    # result=result[result.percentage ==NaN]

    return result

# The sentiment is provided as soon as possible.