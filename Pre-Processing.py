# Here you will find the script we use in many of our DD projects for preprocessing and cleaning data retrieved from social media

!pip install flair
!pip install stop_words

import pandas as pd
import nltk
from datetime import datetime
import re
from stop_words import get_stop_words
from nltk import word_tokenize
from datetime import datetime
from stop_words import get_stop_words
nltk.download('stopwords')
nltk.download('punkt')
from nltk import word_tokenize, sent_tokenize

# DEFINE CLEANING FUNCTIONS

#Create a column for the dates  of each post
def create_date_columns(data, DATE_COLUMN):
    date_utc = pd.to_datetime(data[DATE_COLUMN], format='%Y-%m-%d',utc=True)
    data['Year'] = date_utc.dt.strftime('%Y')
    data['Month'] = date_utc.dt.strftime('%Y-%m')
    data['Week'] = date_utc.dt.to_period("W").dt.start_time
    data['Day'] = date_utc.dt.strftime('%Y-%m-%d')
    return data

#Removes any mentions of social media handles from the text column
def replace_mentions(text):
    if text:
        new_text=[]
        for token in text.split(" "):
            token = "" if token.startswith('@') and len(token)>1 else token
            new_text.append(token)
        return " ".join(new_text)
    else:
        return text

#removes stopwords like 'or' & 'and' from the text column
def remove_stopwords(text,LANGUAGE):
    stopwords = get_stop_words(LANGUAGE.lower())
    return " ".join([token for token in word_tokenize(text) if token.lower() not in stopwords])

#Removes any emails or phone number from the text column
def replace_email_phone_links(text):
    text = re.sub('([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})', "<email>", text)
    text = re.sub('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',"<tel>",text)
    text = re.sub('(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])', "<link>", text)
    return text

def basic_preprocessing(texts,LANGUAGE,keyword="",del_stopwords=True):
    texts = texts.apply(replace_email_phone_links)
    # remove tel and email
    texts = texts.str.replace("<link>","")
    texts = texts.str.replace("<email>","")
    texts = texts.str.replace("<tel>","")
    texts = texts.str.replace(keyword,"")
    if del_stopwords:
        texts = [remove_stopwords(text,LANGUAGE) for text in texts]
    # Remove new line characters
    texts = [re.sub('\s+', ' ', t) for t in texts]
    # Remove single quotes
    texts = [re.sub("\'", "", sent) for sent in texts]

    return texts

# DEFINE PATH AND DATA COLUMNS 

PATH= "/content/drive/MyDrive/" # add here the correct path on Google Drive if using Collab

#Optional organisation, adjust depending on social media site data retrieved from:

DATE_COLUMN = "Post Created Date"
TEXT_COLUMN = "Message" # adapt to the correct column name for Facebook and Instagram
AUTHOR_COLUMN = "Page Name"
LIKES_COLUMN = "Likes"
REACTIONS_COLUMN = "Total Interactions"
LANGUAGE = "english"
REGEX = u'[A-Za-zÀ-ú]+' # words only

# LOAD DATA

df = pd.read_csv(PATH+"FileName.csv") # add here the correct data file name/content/drive/MyDrive/FileName.csv

# CLEAN DATA

#drop empty cells
df = df.dropna(axis=1,how="all")
df = df.drop_duplicates()
df[TEXT_COLUMN] = df[TEXT_COLUMN].fillna("")
df["Number of Posts"] = 1

#Optional: Create separate columns for month, week, day

df = create_date_columns(df, DATE_COLUMN) # generates 3 columns: Month, Week, Day
df.columns

# RUN THE FUNCTIONS

df[TEXT_COLUMN] = basic_preprocessing(df[TEXT_COLUMN],LANGUAGE,keyword="",del_stopwords=True)

df[TEXT_COLUMN] = [replace_mentions(text) for text in df[TEXT_COLUMN]]

# EXPORT CLEANED DATASET

df.to_csv(PATH+"FileName.csv", sep=',', encoding='utf-8')#choose file name and save

