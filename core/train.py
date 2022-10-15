# import required libraries
import sqlite3
import os
import numpy as np
import pandas as pd
import re
import pickle
import string
from string import digits

# import nltk
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


# function to load the training dataset
def load_dataset(filename):
    df = pd.read_excel(filename, sheet_name='final', names=["Questions", "Intent", "Answer"])
    # print(df.head())
    intent = df["Intent"]
    unique_intent = list(set(intent))
    Questions = df["Questions"]
    # Questions = list(df["Questions"])
    return (intent, unique_intent, Questions)


# function to preprocess the data
def preprocess_dataset(sentence):
    # Remove punctuations
    c = sentence.str.translate(str.maketrans(' ', ' ', string.punctuation))
    # Remove Digits
    c = c.str.translate(str.maketrans(' ', ' ', '\n'))
    c = c.str.translate(str.maketrans(' ', ' ', digits))
    # Split combined words
    c = c.apply(lambda tweet: re.sub(r'([a-z])([A-Z])', r'\1 \2', tweet))
    # Convert to lowercase
    c = c.str.lower()
    # Split/ tokenize - Split each sentence using delimiter
    c = c.str.split()
    # Lemmatize - Convert Word to Base Form
    from tqdm import tqdm
    lemmatizer = WordNetLemmatizer()
    com = []
    for y in tqdm(c):
        new = []
        for x in y:
            z = lemmatizer.lemmatize(x)
            z = lemmatizer.lemmatize(z, 'v')
            new.append(z)
        y = new
        com.append(y)
        # print('Lemmatize', com[:5])
    cleaned_words = list(com)
    return (cleaned_words)


# Function to train the chatbot
def trainbot():
    conn = sqlite3.connect('db.sqlite3')
    conn.commit()
    # Loading data from Django Models
    from core.models import Intents, Questions
    df1 = pd.DataFrame(list(Intents.objects.all().values()))
    df2 = pd.DataFrame(list(Questions.objects.all().values()))
    intents = []
    for i in range(len(df2)):
        for j in range(len(df1)):
            if (df2.loc[i, "intents_id"] == df1.loc[j, "id"]):
                intents.append(df1.loc[j, "intent"])
    df2['intents'] = pd.DataFrame(intents)

    Questions = df2['question']
    intent = df2['intents']

    # preprocess the data
    clean_words = preprocess_dataset(Questions)

    # Data obtained after Lemmatization is in array form, and is converted to Dataframe in the next step.
    clean_data = pd.DataFrame(np.array(clean_words), index=Questions.index, columns={'text'})
    clean_data['text'] = clean_data['text'].str.join(" ")

    # clean data for training
    data = clean_data['text']

    # Initialize a CountVectorizer object: count_vectorizer
    count_vec = TfidfVectorizer(analyzer='word', ngram_range=(1, 1), max_df=1.0, min_df=1, max_features=None)

    # Transforms the data into a bag of words
    count_train = count_vec.fit(data)
    bag_of_words = count_vec.transform(data)

    count_vec.vocabulary_;

    # Train the model
    model = MultinomialNB(alpha=0.001)
    model.fit(bag_of_words.todense(), intent.values.ravel());

    # Saving the model and intent data to pickle file
    pickl = {
        'count_vec': count_vec,
        'model': model
    }

    modelfile = "models.p"
    if os.path.isfile(modelfile):
        os.remove(modelfile)

    pickle.dump(pickl, open('models' + ".p", "wb"))
    # intent_answers.to_pickle("./intent_answers.pkl")
