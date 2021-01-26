#! /usr/bin/env python3.6

# ---------- Imports
import tweepy
import pandas as pd
import json
from tqdm import tqdm
import sys
from time import sleep


# ----------Helper Functions

def setup(target_json):
    """
    Fill
    """
    with open(target_json, "r") as incoming:
        credentials = json.load(incoming)

    authSet = tweepy.OAuthHandler(consumer_key=credentials["consumer_key"],
                                  consumer_secret=credentials["consumer_secret"])

    authSet.set_access_token(key=credentials["access_key"],
                             secret=credentials["secret_key"])

    api = tweepy.API(authSet, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
        print("\nConfirmed: Valid Credentials\n")
    except:
        print("\nError: Invalid Credentials\n")
        sys.exit(0)


def scrapeTargetTimeline(USER, COUNT):
    """
    Fill
    """

    output = {"Created At": [], "Username": [], "Tweet": [],
              "Likes": [], "Retweets": []}

    for status in tqdm(tweepy.Cursor(api.user_timeline, id=USER, count=COUNT).items()):
        output["Created At"].append(status.created_at)
        output["Username"].append(status.user.name)
        output["Tweet"].append(status.full_text)
        output["Likes"].append(status.favorite_count)
        output["Retweets"].append(status.retweet_count)

    return pd.DataFrame(output)


def scrapeKeyword(TARGET, COUNT):
    """
    Fill
    """

    output = {"Created At": [], "Username": [], "Tweet": [],
              "Likes": [], "Retweets": []}

    queryTarget = TARGET + " -filter:retweets -filter:links"

    for status in tqdm(tweepy.Cursor(api.search, q=queryTarget, lang="en",
                                     tweet_mode="extended", result_type="recent").items(COUNT)):
        output["Created At"].append(status.created_at)
        output["Username"].append(status.user.name)
        output["Tweet"].append(status.full_text)
        output["Likes"].append(status.favorite_count)
        output["Retweets"].append(status.retweet_count)

    return pd.DataFrame(output)


def getTargetFollowers(TARGET, COUNT):
    """
    Fill
    """

    follower_IDs = []

    for page in tqdm(tweepy.Cursor(api.follower_ids, screen_name=TARGET).pages(COUNT)):
        follower_IDs.extend(page)
        sleep(30)

    return follower_IDs
