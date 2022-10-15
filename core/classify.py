# import required libraries
import pandas as pd
from spellchecker import SpellChecker
from google_trans_new import google_translator
import pickle
import re
import string
from string import digits
from nltk.stem import WordNetLemmatizer
from charbot_api.settings import BASE_DIR_REF


# function to check and fix the spelling
def fix_spellings(sentence):
    spell = SpellChecker()
    sentence_split = sentence.split()
    for x in sentence_split:
        spell_check = spell.unknown([x])
        spell_fix = spell.correction(x)
        if spell_check == set():
            pass
        else:
            sentence = sentence.replace(x, spell_fix)
    return (sentence)


# function to preprocess the question
def preprocess(text):
    # Remove punctuations
    c = text.translate(str.maketrans(' ', ' ', string.punctuation))
    # Remove Digits
    c = c.translate(str.maketrans(' ', ' ', '\n'))
    c = c.translate(str.maketrans(' ', ' ', digits))
    # Split combined words
    c = re.sub(r'([a-z])([A-Z])', r'\1 \2', c)
    # Convert to lowercase
    c = c.lower()
    # Split/ tokenize - Split each sentence using delimiter
    c = c.split()

    # Lemmatize - Convert Word to Base Form
    lemmatizer = WordNetLemmatizer()
    com = []
    for y in c:
        z = lemmatizer.lemmatize(y)
        z = lemmatizer.lemmatize(z, 'v')
        com.append(z)
    cleaned_words = list(com)
    cleaned_words = " ".join(cleaned_words)
    return (cleaned_words)


# function to translate and classify the questions
def classify_question(question, language):
    # new_question = "hoe to sign up for sevrice?"
    question = fix_spellings(question)

    # If the language is French, translate to English
    if language == 'FR':
        translator = google_translator()
        translate_text = translator.translate(question, lang_tgt='en')
    else:
        translate_text = question

    # loading the model from disk
    with open(BASE_DIR_REF + '/models.p', 'rb') as pickled:
        model = pickle.load(pickled)
    count_vec = model['count_vec']
    model = model['model']

    # loading intent file with answers
    # intent_answers = pd.read_pickle("./core/intent_answers.pkl")
    from core.models import Intents, Intent_Answers
    df1 = pd.DataFrame(list(Intents.objects.all().values().order_by('id')))
    df3 = pd.DataFrame(list(Intent_Answers.objects.all().values().order_by('intent_id')))
    intent_answers = pd.concat([df1['intent'], df3['EN_Answer'], df3['FR_Answer']], axis=1)

    clean_Q = preprocess(translate_text)
    # predict the question
    test_tfidf = count_vec.transform([clean_Q])
    test = test_tfidf.todense()
    result = model.predict(test)
    print(result)

    for i in range(len(intent_answers)):
        if result == intent_answers.loc[i, "intent"]:
            if language == 'EN':
                Answer = intent_answers.loc[i, "EN_Answer"]
            else:
                Answer = intent_answers.loc[i, "FR_Answer"]
            # print(Answer)

    class_probabilities = model.predict_proba(test)
    for item in range(0, len(class_probabilities[0])):
        if result == model.classes_[item]:
            intent_probability = "{0:.2f}".format(round(class_probabilities[0][item], 3) * 100)
            # print(intent_probability)

    return (Answer, intent_probability)

# classify_question("Y a-t-il un prix à payer pour CANATRACE?", "FR")
# classify_question("What is the monthly fee for CANATRACE?", "EN")
