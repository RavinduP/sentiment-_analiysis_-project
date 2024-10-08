import numpy as np
import pandas as pd
import re
import string
import pickle

from nltk.stem import PorterStemmer
ps = PorterStemmer()

#loading the model
with open('static/model/model.pickle', 'rb') as f:
    model = pickle.load(f)

#loading the stopwords
with open('static/model/corpora/stopwords/english', 'r') as file:
    sw = file.read().splitlines()

#loading the tokens
vocab = pd.read_csv('static/model/vocabulary.txt', header=None)
tokens = vocab[0].tolist()


def remove_punctuation(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    return text

def preprocessing(text):
    data = pd.DataFrame([text], columns=['tweet'])
    data["tweet"] = data["tweet"].apply(lambda x: " ".join(x.lower() for x in x.split()))
    data["tweet"] = data["tweet"].apply(lambda x:" ".join(re.sub(r'http\S+|www\S+|https\S+', '', x, flags=re.MULTILINE) for x in x.split()))
    data["tweet"] = data["tweet"].apply(remove_punctuation)
    data["tweet"] = data["tweet"].str.replace(r'\d+', '', regex=True)
    data["tweet"] = data["tweet"].apply(lambda x:" ".join(x for x in x.split() if x not in sw))
    data["tweet"] = data["tweet"].apply(lambda x:" ".join(ps.stem(x) for x in x.split()))
    return data["tweet"]


def vectorizer(ds):
    vectorized_list = []

    for sentence in ds:
        sentence_list = np.zeros(len(tokens))

        for i in range(len(tokens)):
            if tokens[i] in sentence.split():
                sentence_list[i] = 1

        vectorized_list.append(sentence_list)

    vectorized_list_new = np.asarray(vectorized_list, dtype=np.float32)

    return vectorized_list_new


def get_prediction(vectorized_text):
    prediction = model.predict(vectorized_text)
    if prediction == 1:
        return 'negative'
    else:
        return 'positive'