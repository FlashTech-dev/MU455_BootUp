import string
import os
import re
import nltk
script_dir = os.path.dirname(__file__)


nltk.download("wordnet")

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

lm = WordNetLemmatizer()
stop = stopwords.words('english')

def clean_text1(text):
    text = "".join([word.lower() for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    text = [word for word in tokens if word.isalpha()]
    text = " ".join([lm.lemmatize(word) for word in text if word not in stop])
    return text