# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 14:29:49 2020

@author: MERT
"""

# Importing the libraries
import tweepy
from tweepy import OAuthHandler
 
# Please change with your own consumer key, consumer secret, access token and access secret
# Initializing the keys
consumer_key ="ve8i7grdg5K37DmIJB7YKL8bO"
consumer_secret ="NlkzanYQiuumfFmWGoiQJ3o6vGiJ2bojVCHHYGPyv0PSLiKZdX"
access_token ="1063098639688572930-VZMudEY99trns6SQAQlTiUcFEoEG8O"
access_secret ="tKspiM0TbbaaTyoXLRui8TcT1mBs3Cw7FglGAY2cc4XL4"
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth,timeout=10)
        
#initialize a list to hold all the tweepy Tweets
alltweets = []    
        
#make initial request for most recent tweets (200 is the maximum allowed count)
new_tweets = api.user_timeline(screen_name = "",count=200)
        
#save most recent tweets
alltweets.extend(new_tweets)
 
tweettexts = [tweet.text.encode("utf-8") for tweet in alltweets]
 
print(tweettexts)