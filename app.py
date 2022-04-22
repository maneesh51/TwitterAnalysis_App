# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 13:30:54 2022

@author: yadav
"""

from textblob import TextBlob

## to handle twotter api
import tweepy
import matplotlib.pyplot as plt
import numpy as np

import streamlit as st
from annotated_text import annotated_text
from datetime import datetime
from datetime import timedelta
import plotly.graph_objects as go


consumer_api_key = "private"
consumer_api_key_secret = "private"

bearer_token = "private"

client_id = "private"
client_id_secret = "private"

access_token = "private"
access_token_secret = "private"

auth = tweepy.OAuthHandler(consumer_api_key, consumer_api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)
type(api)


#### Convert all tweets in percentage"""

def Search_and_Sentiments(search_term, no_of_tweets, date_since, date_until):
   
  tweets = tweepy.Cursor(api.search, q = search_term, since=date_since, until=date_until).items(no_of_tweets)
  
  positive = 0
  negative = 0
  neutral = 0
  polarity = 0

  for tweet in tweets:
    analysis = TextBlob(tweet.text)
    polarity += analysis.sentiment.polarity

    if(analysis.sentiment.polarity == 0):
      neutral+=1
    if(analysis.sentiment.polarity < 0):
      negative+=1
    if(analysis.sentiment.polarity > 0):
      positive+=1

    positive_pcent = format(100*positive/no_of_tweets, '.2f')
    negative_pcent = format(100*negative/no_of_tweets, '.2f')
    neutral_pcent = format(100*neutral/no_of_tweets, '.2f')
    polarity_pcent = format(100*polarity/no_of_tweets, '.2f')

  return np.array([positive_pcent, negative_pcent, neutral_pcent, polarity_pcent])



st.write("""      
# Twitter Sentiment Analysis
#### This app will show you the sentiments based on tweets.
       
 """     )


### input text
text_input = st.text_area("Type your keyword:")
today = datetime.now().date()
st.markdown("---")
cols = st.columns(2)

back_days = cols[0].slider("Select number of past days from today:", 1, 100, 1)
NumTweets = cols[1].slider("Number of tweets:", 1, 100, 10)

prev_date = today - timedelta(back_days) 
st.write('Analyzing {:} tweets between {:}'.format(NumTweets, prev_date), 'and {:}'.format(today))
st.markdown("---")
show_results = st.button(label="Show Results")

###############################################################################
st.sidebar.header('User Input Features')
# selected_model = st.sidebar.selectbox("Select a pre-trained model", options=["Random forest", "Support Vector Machine (SVM)"])

# if selected_model=='Random forest':
#     predictions = prediction_rf
#     prediction_prob = prediction_prob_rf 

# if selected_model=='Support Vector Machine (SVM)':
#     predictions = prediction_svm
#     prediction_prob = prediction_prob_svm

if text_input and back_days and NumTweets:
    
    SentimentsPcent = Search_and_Sentiments(search_term=text_input, no_of_tweets=NumTweets, date_since=prev_date, date_until=today)
        
    if show_results:
        st.markdown("---")
        st.write('Showing results for {:}:'.format(text_input))
        
        ### sentiments
        Sentiments = ['Positive', 'Negative', 'Neutral']
        layout = go.Layout(height = 600, width = 600,  autosize = False, title = 'Main title')
        fig = go.Figure(go.Pie(hole = 0.4, labels=Sentiments, values=SentimentsPcent[:3], hoverinfo = "label+percent", textfont_size=40), layout = layout)
        st.plotly_chart(fig)
        st.markdown("---")
    
    
    
    
    
    
    
    
