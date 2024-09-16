# This script uses BERTopic to retrieve the major topics in a column of a dataframe which contains textual data. 
# BERTopic is an advanced topic modeling technique that uses transformers (like BERT) and clustering to identify topics within textual data.

!pip install bertopic

from bertopic import BERTopic
import pandas as pd

# DEFINE THE FUNCTIONS

def clean_text(text):
    # Remove any word that begins with '@'
    text = re.sub(r'@\w+', '', text)
    # Remove any word that starts with 'http'
    text = re.sub(r'http\S+', '', text)
    return text

# Apply the clean_text function to the text column
def clean_text_column(df, text_column):
    df[text_column] = df[text_column].astype(str).apply(clean_text)
    return df

def topic_modelling(text, min_topic_size, language="english"):
    model = BERTopic(n_gram_range=(1, 2), verbose=True, language=language, low_memory=True, min_topic_size=min_topic_size)
    topics, probs = model.fit_transform(text)
    topic_info = model.get_topic_info()

    return topics, topic_info, model

# LOAD DATASET

# This line reads an excel file but can just as easily be changed to read a csv 
df = pd.read_excel(PATH+"data.xlsx")# add here the correct data file 

# Optional: rename the column of interest as TEXT_COLUMN for easier replicability with future datasets
TEXT_COLUMN = df['Column']
df[TEXT_COLUMN] = df[TEXT_COLUMN].astype(str)

# CLEAN DATA

# Replace 'nan' strings with empty strings
df[TEXT_COLUMN] = df[TEXT_COLUMN].replace('nan', '')
df[TEXT_COLUMN].clean_text_column(df, TEXT_COLUMN)

# RUN THE FUNCTION
# Feel free to adjust the minimum topic size depending on how big your dataset is 

topics, topic_info, model = topic_modelling(df_ukraine[TEXT_COLUMN].tolist(), min_topic_size=5)

#Display the result
topic_info
