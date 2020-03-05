# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 16:46:24 2020

@author: MERT
"""

import nltk
import pickle
import numpy as np
import re
from nltk.corpus import stopwords
from sklearn.datasets import load_files
nltk.download("stopwords")


#Dataseti import
reviews = load_files("txt_sentoken/")
X,y =reviews.data,reviews.target
fakeX,fakey = X,y



##şimdi load_files 2000 text için hızlı olabilir ancak bizim textimii 1million datasetimiz felan olduugnda
##sıkıntıya giricek bunun için işlemlerin hızlı olması içinb pickle file ları mesela sımdı X ve y yi pickle file olarak yazıcam
#daha sonra x ve y yi silip yazdıgım pickle file den read etcem7
#e bu gereksiz ama pickle kullanımını ogrenmelıyım




#STORİNG as Pickle Files
with open("X.pickles","wb") as f:    #x pickle, wb = write byte 
    pickle.dump(X,f)

with open("y.pickles","wb") as f:
    pickle.dump(y,f)
    
 ## okey bunları yazarak pickle file a store ettim 
 
 
 #şimdi pickle file den okuma zamanı
 
 
 # Unpickling  
#with open("X.pickle","rb") as f:
#     X = pickle.load(f)
#     
#with open("y.pickle","rb") as f:
#    y = pickle.load(f)
 #  Creating The Corpus 
corpus = []
for i in range (0,len(X)):
    review = re.sub(r"\W"," ",str(X[i]))
    review = review.lower()
    review = re.sub(r"\s+[a-z]\s+"," ",review)
    review = re.sub(r"^[a-z]\s+"," ",review)
    review = re.sub(r"\s+"," ",review)
    corpus.append(review)
    
    

##62 62 62 62 62 62 62 62
##Count vectorizer le histogram oluşturcam
from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=2000,min_df=3 , max_df=0.6, stop_words=stopwords.words("english"))
X= cv.fit_transform(corpus).toarray()


from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer()
X = transformer.fit_transform(X).toarray()
print(X.shape)

from sklearn.feature_extraction.text import TfidfVectorizer
cv=TfidfVectorizer(max_features=2000,min_df=3 , max_df=0.6, stop_words=stopwords.words("english"))
X= cv.fit_transform(corpus).toarray()



from sklearn.model_selection import train_test_split
X_train ,X_test , y_train , y_test = train_test_split(X,y,test_size = 0.3, random_state = 0)



from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(X_train,y_train)

y_pred = classifier.predict(X_test)


from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_pred,y_test)
print("From Logistic Regression:")
print(cm)

from sklearn.metrics import accuracy_score, precision_score, recall_score
print("Accuracy score: ", accuracy_score(y_test, y_pred))
print("Precision score: ", precision_score(y_test, y_pred))
print("Recall score: ", recall_score(y_test, y_pred))





##  Birde naive bayes için oluşturdum ama daha düşük yüzdeli başarı oranı var
from sklearn.naive_bayes import MultinomialNB
MNB = MultinomialNB()
MNB.fit(X_train , y_train)

y_pred2 =MNB.predict(X_test)    
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_pred2 , y_test)
print("from naive bayes")
print(cm)
#
#from sklearn.metrics import accuracy_score, precision_score, recall_score
#print("Accuracy score: ", accuracy_score(y_test, y_pred2))
#print("Precision score: ", precision_score(y_test, y_pred2))
#print("Recall score: ", recall_score(y_test, y_pred2))


#   Visualize etmek için bunu 
#from sklearn.metrics import confusion_matrix
#import matplotlib.pyplot as plt
#import seaborn as sns
#sns.heatmap(cm, square=True, annot=True, cmap="RdBu", cbar=False,xticklabels=["mert" , "seven"], yticklabels=["esesdfsdf","sevdigim"])
#plt.xlabel("true label")
#plt.ylabel("predicted label")
#


## Bu aşşağıda yaptııgm şeyler kısaca sunun ıcın ben bi model train ediyorum classifierim var
##twitter da mesela adlıgım verileri bu classifierı import ederek train edicem 


# Pickling The Classifier
with open ("classifier.pickle","wb") as f:
    pickle.dump(classifier,f)
        
    
# Pickling the vectorizer --> vectorizee 0 1 0 101
with open ("tfidfmodel.pickle" , "wb") as f:
    pickle.dump(cv , f)
    
    
    
    
    
# Unpickling the classifier and vectorizer        
    
with open ("classifier.pickle" , "rb") as f:
    clf = pickle.load(f)
    
    
with open ("tfidfmodel.pickle" , "rb") as f:
    tfidf = pickle.load(f)
    
print("after the pickle")


sample = ["Hello i really hate you ,you are a bad person i really say it"]
print(sample)
sample = tfidf.transform(sample).toarray()
print("calculating")
a =clf.predict(sample)

if a> 0.5:
    print("your Sentence is ",sample)
    print("And i classified your sentence  as POSİTİVE :) ")
else :
    print("your Sentence is ",sample)
    print("And i classified your sentence as negative :( ")


#
#import matplotlib.pyplot as plt
#import numpy
#
#objects = ["Positive", "Negative"]
#y_pos = np.arange(len(objects))
#
#plt.bar(y_pos , [total_pos ,total_neg],alpha = 0.5)
#plt.xticks(y_pos,objects)
#plt.ylabel("Number")
#plt.title("Number of Positive and Negative Tweets")



    

    
