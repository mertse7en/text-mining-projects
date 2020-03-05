# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:06:20 2020

@author: MERT
"""
import tweepy
import pickle
import re 


from tweepy import OAuthHandler


#Keyleri initialize etmeliyim 1 ******
consumer_key ="ve8i7grdg5K37DmIJB7YKL8bO"
consumer_secret ="NlkzanYQiuumfFmWGoiQJ3o6vGiJ2bojVCHHYGPyv0PSLiKZdX"
access_token ="1063098639688572930-VZMudEY99trns6SQAQlTiUcFEoEG8O"
access_secret ="tKspiM0TbbaaTyoXLRui8TcT1mBs3Cw7FglGAY2cc4XL4"



auth =OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
args = ["corona"]
api = tweepy.API(auth,timeout = 10)


list_tweets = []

query =args[0]
if len(args) == 1:
    for status in tweepy.Cursor(api.search, q=query+"-filter:retweets", lang = "en",result_type ="recent").items(100):
        #queryden retweet leri almaadım cunku bir cok kez tekrar etmiş olabilir
        #lang en , recent_type ise 10 yıl oncenın tweetlerini istemiyorum recent twitleri istiyorum
        list_tweets.append(status.text)
        
with open ("tfidfmodel.pickle" , "rb") as f:
    vectorizer = pickle.load(f)   
     
with open ("classifier.pickle" , "rb") as f:
    clf = pickle.load(f)
# Testing için kanks
sample = [""]
print("Classifiying ..... ")

if(clf.predict(vectorizer.transform(sample)) > 0.5 ):
    print("cümleniz olumlu")
else :
    print("cümlen negatif bro")

total_pos = 0
total_neg = 0


# Preprocessing Tweets 
for tweet in list_tweets:
    tweet = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s" , " ",tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " " ,tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$" , " " ,tweet)
    tweet = tweet.lower()
    tweet =re.sub(r"that's","that is",tweet)
    tweet =re.sub(r"there's", "there is",tweet)
    tweet =re.sub(r"what's", "what is",tweet)
    tweet =re.sub(r"where's", "where is",tweet)
    tweet =re.sub(r"it's", "it is",tweet)
    tweet =re.sub(r"who's", "who is",tweet)
    tweet =re.sub(r"I'm", "I am",tweet)
    tweet =re.sub(r"she's", "she is",tweet)
    tweet =re.sub(r"he's", "he is",tweet)
    tweet =re.sub(r"they're", "they are",tweet)
    tweet =re.sub(r"who're", "who are",tweet)
    tweet =re.sub(r"ain't", "am not",tweet)
    tweet =re.sub(r"wouldn't", "would not",tweet)
    tweet =re.sub(r"shouldn't", "should not",tweet)
    tweet =re.sub(r"can't", "they are not",tweet)
    tweet =re.sub(r"couldn't", "could not",tweet)
    tweet =re.sub(r"won't", "will not",tweet)
    tweet = re.sub(r"\W"," ",tweet)
    tweet = re.sub(r"\d"," ",tweet)
    tweet= re.sub(r"s+[a-z]\s+"," ",tweet)
    tweet =re.sub(r"\s+[a-z]$"," ",tweet)
    tweet=re.sub(r"^[a-z]\s+" , " ",tweet)
    tweet = re.sub(r"\s+"," ",tweet)
    
    sent = clf.predict(vectorizer.transform([tweet]).toarray())
    print(tweet ,":" ,sent)

    if sent[0] == 1:
        total_pos +=1
    else:
        total_neg +=1
    


        
import matplotlib.pyplot as plt
import numpy as np

objects = ["Positive", "Negative"]
y_pos = np.arange(len(objects))

plt.bar(y_pos , [total_pos ,total_neg],alpha = 0.5)
plt.xticks(y_pos,objects)
plt.ylabel("Number")
plt.title("Number of Positive and Negative Tweets")
plt.show()


    
    
    