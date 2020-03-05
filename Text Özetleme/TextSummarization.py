# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 18:00:08 2020

@author: MERT
"""

import bs4 as bs#beatiful soup library
import urllib.request
import re
import nltk
import heapq
nltk.download("stopwords")


# Fetchin data from Web(Wikiden almayı düşünüyorm)
source = urllib.request.urlopen("https://tr.wikipedia.org/wiki/Solucandeli%C4%9Fi")

soup = bs.BeautifulSoup(source,"lxml")
#lxml dedigimiz şey parser bi cok parser var diğerlerinide kullanabilirsin ama lxml bi sıkıntı yaratmadı

text = ""
for paragraph in soup.find_all("p"):
    #bu p html de ki <p> tagi burası baska bı sıtede <h> olmadı cunku <div> lede yazılmış olabilir yani eğer baska bi siteden cekerken <div> <span> deniyebilirsin
    text += paragraph.text
    
    
 #Preprocessing yapıyorum mertooooooo
text =re.sub(r'\[[0-9]*\]',' ',text) #bu [1 2 3 leri felan kaldırmaya calısıyorum kaldırmak derken " " le replace etmeyi broooo]
text = re.sub(r'\s+'," ",text)
clean_text = text.lower()
clean_text = re.sub(r"\W"," ",clean_text)
clean_text = re.sub(r"\d"," ",clean_text)
clean_text = re.sub(r"\s+"," " ,clean_text)


#clean_texti su yuzden yazdım belki numaralar onemlıdiir numberlar cunku tarihi bişeylerde önemli olabiir


# Tokenizing string (Split le de yapabilirim ama ondan sonra " ".join felan yapıcam)
sentences = nltk.sent_tokenize(text) # paragrapı sentence sentence ayırdım
stopd_words = nltk.corpus.stopwords.words("turkish")


#create the histogram   éééé83-84-85 "hands-on kitabı"
word2count = {}
for word in nltk.word_tokenize(clean_text):
    if word not in stopd_words:
        if word not in word2count.keys():
            word2count[word] =1
        else:
            word2count[word] +=1
            
            
word3count = {}
word3count = word2count
            
            
for key in word2count.keys():
    word2count[key]=word2count[key]/max(word2count.values())



#   Sentence score hesaplamaya çalışıyorum
    
sent2score = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word2count.keys():
            if len(sentence.split(" ")) <25: #bunu yapmadakı amacım cok uzun kelimler alırsak özetn özetliliği kalmaz 
                if sentence not in sent2score.keys():
                    sent2score[sentence] = word2count[word]
                else:
                    sent2score[sentence] +=word2count[word]
                    
                    
#en yüksek scorlü 7 cümleyi cektim                    
best_sentences=heapq.nlargest(7,sent2score,key=sent2score.get)

print("------------------------------------------------------")
word2 = heapq.nlargest(4 , word3count,key=word3count.get) # en yükse score lu 4 kelime

stringtitle = ""
print("Paragrafın Başlığı :")
for stringeceviriyom in word2:
    stringtitle =stringtitle + stringeceviriyom +" "
print(stringtitle.upper())
print("  ")

for sentence in best_sentences:
    print(sentence) 



                    

