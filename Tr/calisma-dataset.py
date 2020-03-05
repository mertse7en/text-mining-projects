# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 17:11:46 2020

@author: MERT
"""
from sklearn.datasets import load_files
import os 
import nltk
import pandas as pd
import xlrd
import re
from nltk.corpus import stopwords
import sklearn
import pickle


konumum = os.getcwd()
print("konumun :",konumum)



# Openning the excel files normmalde i do it this with pd.read_csv("....")

WBook = xlrd.open_workbook("ReviewsAndRatings_all_19_06.xls")
WSheets = WBook.sheets()
ReviewWS,RatingsWS = WSheets
Ratings = RatingsWS.col_values(0)
Reviews = ReviewWS.col_values(0)
Ratings_Normal = RatingsWS.col_values(1)




#pos_sentences = []
#neg_sentences = []
mertoRating = []
for i in Ratings_Normal:
    if i >2.5:
        mertoRating.append(1)
        
    else :
        mertoRating.append(0)

X,y =Reviews,mertoRating

corpus = []
for i in range (0,len(X)):
    review = re.sub(r"\W"," ",str(X[i]))
    review = review.lower()
    review = re.sub(r"\s+[a-z]\s+"," ",review)
    review = re.sub(r"^[a-z]\s+"," ",review)
    review = re.sub(r"\s+"," ",review)
    corpus.append(review)
    
    

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=5000,min_df=3 , max_df=0.6, stop_words=stopwords.words("turkish"))
X= cv.fit_transform(corpus).toarray()


from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()
X = transformer.fit_transform(X).toarray()
print(X.shape)

from sklearn.feature_extraction.text import TfidfVectorizer
cv=TfidfVectorizer(max_features=2000,min_df=3 , max_df=0.6, stop_words=stopwords.words("turkish"))
X= cv.fit_transform(corpus).toarray()


from sklearn.model_selection import train_test_split
X_train,X_test ,y_train , y_test = train_test_split(X,y,test_size =0.2,random_state = 1)


from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train,y_train)


y_pred = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_pred ,y_test)
print("with logistic regression your confusion matrix is ")
print(cm)

from sklearn.metrics import accuracy_score
acc_scpre = accuracy_score(y_pred,y_test,normalize = True)
print(acc_scpre)

#Classifierimi ve vectorizer i pickle ediyorum
with open("classifierim.pickle","wb") as f:
    pickle.dump(classifier,f)
    
with open("model.pickle","wb") as f:
    pickle.dump(cv,f)
    


#Unpickle yapıp test ediicem burda claısıyorusa twitterde türkce data çekmeye başlıyıcam 
with open("classifierim.pickle","rb") as f:
    clf = pickle.load(f)
    
    
with open("model.pickle","rb") as f:
    vectorizerim = pickle.load(f)
    
    

#------>> OKEY ÇALIŞTI BU PROJE BENIM CLASSİFİERİM 
    
    
    
    








       

        