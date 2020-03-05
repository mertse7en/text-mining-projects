# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 18:54:22 2020

@author: MERT
"""

import tweepy
import pickle
import re 
import nltk


from tweepy import OAuthHandler


#Keyleri initialize etmeliyim 1 ******
consumer_key ="ve8i7grdg5K37DmIJB7YKL8bO"
consumer_secret ="NlkzanYQiuumfFmWGoiQJ3o6vGiJ2bojVCHHYGPyv0PSLiKZdX"
access_token ="1063098639688572930-VZMudEY99trns6SQAQlTiUcFEoEG8O"
access_secret ="tKspiM0TbbaaTyoXLRui8TcT1mBs3Cw7FglGAY2cc4XL4"


auth =OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
args = ["sehidimizvar"]
api = tweepy.API(auth,timeout = 10)


list_tweets = []

query =args[0]
if len(args) == 1:
    for status in tweepy.Cursor(api.search, q=query+"-filter:retweets", lang = "tr",result_type ="recent").items(100):
        #queryden retweet leri almaadım cunku bir cok kez tekrar etmiş olabilir
        #lang tr , recent_type ise 10 yıl oncenın tweetlerini istemiyorum recent twitleri istiyorum
        list_tweets.append(status.text)
        
        
        
with open ("model.pickle" , "rb") as f:
    vectorizer = pickle.load(f)   
     
with open ("classifierim.pickle" , "rb") as f:
    clf = pickle.load(f)
    
    
    
sample1 = ["bu proje cok kotu olmus hiç beğenmedim"]
sample2 = ["seneryo cok kisitli daha iyi olabilirdi ama guzel"]
sample3 =["tam anlamıyla harika beğenmeyenin kafasında sikinti var"]
sample4=["yine döktürmüş kenan hoca"]
sample5=["güzel fena değil"]
sample6=["bosa gecti bir saatim berbat"]

analiz = clf.predict(vectorizer.transform(sample1).toarray())
print(sample1 ," == " ,analiz)

analiz = clf.predict(vectorizer.transform(sample2).toarray())
print(sample2 ," == " ,analiz)

analiz = clf.predict(vectorizer.transform(sample3).toarray())
print(sample3 ," == " ,analiz)

analiz = clf.predict(vectorizer.transform(sample4).toarray())
print(sample4 ," == " ,analiz)

analiz = clf.predict(vectorizer.transform(sample5).toarray())
print(sample5 ," == " ,analiz)

analiz = clf.predict(vectorizer.transform(sample6).toarray())
print(sample6 ," == " ,analiz)


print("CLASİFY TEST VE ORNEKLER UZERINDEN BİTİİ")
print("----------------------------------------")




    
    
    
total_pos = 0
total_neg = 0

#from nltk.corpus import stopwords
#nltk.download("stopwords")
#turkishstopwords = stopwords.words("turkish")
#en = stopwords.words("english")


clearList_tweets = []
for tweet in list_tweets:
    tweet = re.sub(r"^https://t.co/[a-zA-Z0-9]*\s" , " ",tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*\s", " " ,tweet)
    tweet = re.sub(r"\s+https://t.co/[a-zA-Z0-9]*$" , " " ,tweet)
    tweet = tweet.lower()
    
    tweet = re.sub(r"bok","kotu",tweet)
    
    
    
    
    
    tweet = re.sub(r"\W"," ",tweet)
    tweet = re.sub(r"\d"," ",tweet)
    tweet= re.sub(r"s+[a-z]\s+"," ",tweet)
    tweet =re.sub(r"\s+[a-z]$"," ",tweet)
    tweet=re.sub(r"^[a-z]\s+" , " ",tweet)
    tweet = re.sub(r"\s+"," ",tweet)
    clearList_tweets += tweet
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
    
    




