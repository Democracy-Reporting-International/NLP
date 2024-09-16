# This script shows how to perform sentiment analysis on text data. We are currently looking for better packages that do this, but for now we use Vader

!pip install nltk
!pip install flair

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import word_tokenize
import pandas as pd
import spacy
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()

# DEFINE SENTIMENT FUNCTION

def sentiment_scores_categorical(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        sentiment="Positive"
    elif sentiment_dict['compound'] <= - 0.05 :
        sentiment="Negative"
    else :
        sentiment="Neutral"
    return sentiment

# LOAD DATA

# Optional organisation, adjust depending on social media type 

PATH= "/content/drive/MyDrive/Twitter Analysis/"
DATE_COLUMN = "created_at"
TEXT_COLUMN = "text_english"
GERMAN_TEXT_COLUMN = "text"
AUTHOR_COLUMN = "author_name"
LIKES_COLUMN = "likes_count"
REPLY_COLUMN = "reply_count"
RETWEET_COLUMN = "retweet_count"
QUOTE_COLUMN = "quote_count"
LANGUAGE = "english"

df = pd.read_csv(PATH+"data.csv")

# RUN FUNCTION

df[TEXT_COLUMN] = df[TEXT_COLUMN].astype(str)
df[TEXT_COLUMN] = df[TEXT_COLUMN].replace('nan', '')
df["Sentiment"] = [sentiment_scores_categorical(text) for text in df[TEXT_COLUMN]]

df.to_csv(PATH+"sent.csv", sep=',', encoding='utf-8')#choose file name and save
