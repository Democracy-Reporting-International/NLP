# In our 2024 investigation into disinformation on YouTube, we experimented with using ChatGPT 4o mini to summarise the transcripts we pulled from the YouTube API
# This methodology is quite new to the team and therefore subject to adjustment. Due to rate limits, we had to manually create subsets of the data 100 entries large and 
# run the function for each subset. There is probably a more efficient way to do this.

!pip install openai
import openai
import time
from osgeo import ogr
import pandas as pd

api_key = 'API KEY' #replace with the actual API key from OpenAI

# Initialize the API client with the API key
openai.api_key = api_key

# DEFINE FUNCTIONS

def summarize_document(text):
  try:
    response = openai.chat.completions.create(
    model= "gpt-4o-mini", # can also try "gpt-3.5-turbo" if 4o mini is not responding
    messages=[
          {"role": "user", "content": f"Please summarize the following video transcript, presenting the main topics: {text}"}  # feel free to experiement with this prompt depending on the research task
      ],
      max_tokens=150,  # Adjust as needed based on the expected length of the summary
      temperature=0.7  # You can adjust the temperature for creativity vs. consistency
  )
    summary = response.choices[0].message.content
    return summary
  except Exception as e:
        print(f"Error summarizing document: {e}")
        return None

def summarize_documents(texts):
    summaries = []
    for text in texts:
        summary = summarize_document(text)
        if summary:  # Only append if summarization was successful
            summaries.append(summary)
            print("about to sleep")
            time.sleep(21)
            print("slept")
    return summaries

# LOAD DATA

df = pd.read_excel(PATH+'data.xlsx')
transcripts_list = df['Transcript'].tolist()

# Create a subset of the list with entries 1 to 100 to avoid exceeding the rate limit
subset_transcripts = transcripts_list[0:99]  # Python lists are 0-indexed, so 100-200 is [100:201]

# RUN THE FUNCTION

texts = subset_transcripts

summaries = summarize_documents(texts)
for i, summary in enumerate(summaries):
    print(f"{summary}")


# EXPORT THE SUMMARIES

df = pd.DataFrame(summaries, columns=['Summary'])
df.to_excel(PATH+'summaries.xlsx', index=False)

