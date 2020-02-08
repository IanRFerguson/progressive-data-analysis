#NOTE: You'll need your own Twitter developer profile to run this script

import tweepy
import pandas as pd

# Set your Twitter developer credentials
authSet = tweepy.OAuthHandler(consumer_key = # INPUT,
                              consumer_secret = # INPUT)

authSet.set_access_token(key = # INPUT,
                         secret = # INPUT)

api = tweepy.API(authSet, wait_on_rate_limit = True)

# Verify that these credentials are valid - if not script will exit
try:
    api.verify_credentials()
    print("\nConfirmed: Valid Credentials\n")
except:
    print("\nError: Invalid Credentials\n")

# Build scraper function
def scraper(target, count):

    """

    Target <- Keyword or #Hashtag you want to search for ... e.g., "#GreenNewDeal"
    Count <- Number of tweets you want to pull ... Twitter's rate limit is sensitive so be careful!

    """

    # Empty lists to push scraped Twitter data into
    created, name, location, text, likes, rts = [], [], [], [], [], []

    # You can mess with this - add "-filter:mentions" for example
    queryTarget = target + " -filter:retweets -filter:links"

    # Actual meat of the function!
    # Searches for target while appending Tweet data into the lists above
    for tweet in tweepy.Cursor(api.search, q = queryTarget,
                               lang = 'en',
                               tweet_mode = 'extended',
                               result_type = 'recent').items(count):

        created.append(tweet.created_at)
        name.append(tweet.user.name)
        location.append(tweet.user.location)
        text.append(tweet.full_text)
        likes.append(tweet.favorite_count)
        rts.append(tweet.retweet_count)

    # Organize tweet data into a Pandas DataFrame
    tweetData = pd.DataFrame({'DateTime': created,
                         'User Name': name,
                         'Location': location,
                         'Tweet': text,
                         'Likes': likes,
                         'Retweets': rts})

    return tweetData

# WORKING EXAMPLE!
import os
cwd = os.getcwd()

# Store scraped tweets into a variable
data = scraper('#GreenNewDeal', 1000)

# Save tweets to a local CSV file
data.to_csv(os.path.join(cwd + "/Twitter_Data.csv"))
