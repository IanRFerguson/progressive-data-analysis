import tweepy
import time
import pandas as pd
import datetime
from textblob import TextBlob

authSet = tweepy.OAuthHandler(consumer_key = ' # input ', 
                              consumer_secret = ' # input ')

authSet.set_access_token(key = ' # input ', 
                         secret = ' # input ')

api = tweepy.API(authSet, wait_on_rate_limit = True)

try:
    api.verify_credentials()
    print("\nConfirmed: Valid Credentials\n")
except:
    print("\nError: Invalid Credentials\n")
    
def sentimentAnalysis(text):
    analysis = TextBlob(text)
    
    if analysis.sentiment.polarity >=0:
        return 'Positive'
        
    else:
        return 'Negative'
    
    
created, name, location, text, likes, rts = [], [], [], [], [], []

for tweet in tweepy.Cursor(api.search, q = '#GreenNewDeal -filter:retweets -filter:links', 
                           lang = 'en', tweet_mode = 'extended').items(1000):
    
        created.append(tweet.created_at)
        name.append(tweet.user.name)
        location.append(tweet.user.location)            
        text.append(tweet.full_text) 
        likes.append(tweet.favorite_count)
        rts.append(tweet.retweet_count)
        

tweetData = pd.DataFrame({'DateTime': created,
                         'User Name': name,
                         'Location': location,
                         'Tweet': text,
                         'Likes': likes,
                         'Retweets': rts})

polarity = []

for index, tweet in enumerate(tweetData['Tweet']):
    
    analysis = TextBlob(tweet)
    
    if analysis.sentiment.polarity >=0:
        polarity.append('Positive')
        
    elif analysis.sentiment.polarity < 0:
        polarity.append('Negative')
        
tweetData['Polarity'] = polarity
    
