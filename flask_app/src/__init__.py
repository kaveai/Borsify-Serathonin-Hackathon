from flask import Flask, render_template, make_response, request, redirect
import pandas as pd
import numpy as np
import time
app = Flask(__name__)
from os.path import join, dirname, realpath
import pickle 
import os
from shutil import copyfile
import json
from pandas.io.json import json_normalize
from sklearn.datasets import load_files
import nltk
import bs4 as bs
import urllib.request
nltk.download('stopwords')
from snowballstemmer import stemmer
import datetime
import tweepy
import re
import random
import sys
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

copyfile("C:/Users/yemre/Desktop/flask_app/src/static/uploads/safe_zone/db.sqlite3", "C:/Users/yemre/Desktop/flask_app/src/db.sqlite3")

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')


kokbul1 = stemmer('turkish')
filename = UPLOADS_PATH+'/model.sav'
filenamev2 = UPLOADS_PATH+'/vectorizer.sav'
loaded_model = pickle.load(open(filename, 'rb'))
loaded_vectorizer = pickle.load(open(filenamev2, 'rb'))
################ Kisaltma #############################
def get_links(url = "ASELS"):
    basliklar = []
    linkler = []
    detay = []
    tarihler =[] 
    source = urllib.request.urlopen('https://www.bloomberght.com/liste/arama?ara='+url)
    soup = bs.BeautifulSoup(source,'lxml')
    for url in soup.findAll('a', class_="searchResultsHeadline"):
        basliklar.append(url.getText())
    for url in soup.findAll('a', class_="searchResultsHeadline"):
        linkler.append(url.get("href"))
    for url in soup.findAll('a', class_="searchResultsSpot"):
        detay.append(url.getText())
    for url in soup.findAll('a', class_="searchResultsDate"):
        tarihler.append(url.getText())
    return basliklar,linkler,detay,tarihler
#######################################################
################ Chatter BOT ###############
def preprocessing(text):
    text = text.lower()
        # get rid of non-alphanumerical characters
    text = re.sub(r'\W', ' ', text)
        # get rid of spaces
    text = re.sub(r'\s+', ' ', text)
        # Correct mistakes
        # and do the stemming
    return " ".join([word for word in kokbul1.stemWords(text.split())])

def predicting(x):
    test_sample = []
    for i in range(len(x)):
        test_sample.append(preprocessing(x[i]))
    sample = loaded_vectorizer.transform(test_sample).toarray()
    result = loaded_model.predict(sample)
    return result

def tweetSearch(query, limit = 1000, language = "en", remove = []):
    auth = tweepy.OAuthHandler("b31NqruIj0m3D6mzOk4glEfz7", "yAku57PMlQ9V6MVxUrrzkGxI4izrwGCzvI8Q5OwPwyFeLCR0oT")
    auth.set_access_token("352938901-hH3mCRnw7ir8acB7oFQwfsu9gaboZeu20Hbm2jWi", "t2vYixvZemUibVI95QuapcqwEUCITki7xWFK6DjLTvGce")
    api = tweepy.API(auth)
        #Create a blank variable
    texts = []
    back_up_text = []

        #Iterate through Twitter using Tweepy to find our query in our language, with our defined limit
        #For every tweet that has our query, add it to our text holder in lower case
    for tweet in tweepy.Cursor(api.search, q=query, lang=language).items(limit):
        back_up_text.append(tweet.text.replace("\n",""))
        texts.append(preprocessing(tweet.text.lower()))
        
        #Twitter has lots of links, we need to remove the common parts of links to clean our data
        #Firstly, create a list of terms that we want to remove. This contains https & co, alongside any words in our remove list
    removeWords = ["https","co"]
    removeWords += remove
        
        #For each word in our removeWords list, replace it with nothing in our main text - deleting it
        #for word in removeWords:
        #    text = text.replace(word, "")
        
        #return our clean text
    return texts,back_up_text

def GetTweets(username,count):
        # Twitter API Settings
        #auth = tweepy.OAuthHandler("b31NqruIj0m3D6mzOk4glEfz7", "yAku57PMlQ9V6MVxUrrzkGxI4izrwGCzvI8Q5OwPwyFeLCR0oT")
        #auth.set_access_token("352938901-hH3mCRnw7ir8acB7oFQwfsu9gaboZeu20Hbm2jWi", "t2vYixvZemUibVI95QuapcqwEUCITki7xWFK6DjLTvGce")
        #api = tweepy.API(auth)

        # Get Tweets
    tweets = []
        #fetched_tweets = api.user_timeline(screen_name=username, count=100, include_rts=True)

        #for tweet in fetched_tweets:
        #    tweets.append(preprocessing(tweet.text))
    tweets,back_up_text = tweetSearch(username,limit=count)
    result = predicting(tweets)

    x, y, c = [], [], []

    x = list(pd.DataFrame(result)[0].value_counts().values)
    y = list(pd.DataFrame(result)[0].value_counts().index)
    inv_sentiment =dict(zip(y, x))
    c = pd.DataFrame(x, y, columns=[0]).T
    return inv_sentiment, back_up_text[:20]

def Twitter(username="kuveytturk",count=10):
    # Modellerin İçeri Alınması
    kokbul1 = stemmer('turkish')
    filename = UPLOADS_PATH+'/model.sav'
    filenamev2 = UPLOADS_PATH+'/vectorizer.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    loaded_vectorizer = pickle.load(open(filenamev2, 'rb'))

    c,tweets = GetTweets(username,count)
    return c,tweets
##############################################

def get_deger(sembol):
    data = pd.read_excel(UPLOADS_PATH+sembol+'.xlsx')
    data = data[['Close']]
    deger = data.iloc[-1].values[0]
    return str(deger)
def get_Excel(sembol="KCHOL"):
    data = pd.read_excel(UPLOADS_PATH+sembol+'.xlsx')
    data = data[['Close']]
    return (((data.iloc[-1].values - data.iloc[-7].values) / data.iloc[-1].values)[0]*100).round(3),(((data.iloc[-1].values - data.iloc[-15].values) / data.iloc[-1].values)[0]*100).round(3),(((data.iloc[-1].values - data.iloc[-30].values) / data.iloc[-1].values)[0]*100).round(3)

from chatterbot import ChatBot

# Create a new chat bot named Charlie
chatbot = ChatBot(
    'Charlie',
    trainer='chatterbot.trainers.ListTrainer',
    read_only=True
)

@app.route('/')
def entry_page()->'html':
    bist_100_data,tweets = Twitter("Bist100",count=100)
    data = pd.read_excel(UPLOADS_PATH+"BIST100.xlsx")
    data = data[['Close']]
    clf = pickle.load(open(UPLOADS_PATH+'model-BIST100.pkl', 'rb'))
    # Önümüzdeki 7 Gün için Tahmin yapma
    base = list(data.Close.values[-7:])
    symbol_data,tweets = Twitter("Bist100",10)
    for i in range(7):
        base.append(clf.predict(np.array([base[i:]]))[0].round(2))
    sample_Data = data.Close.values[-28:]
    predict_data = base[-7:]
    percantege_data = (((predict_data[-1] - sample_Data[-1])/ sample_Data[-1])*100).round(2)
    x,y,z,v = get_links("Bist100")
    bloomerg = []
    for i in range(0,4):
        bloomerg.append({"baslik":x[i],"linkler":y[i],"detay":z[i],"tarihler":v[i]})
    return render_template('index.html',yazilar=bloomerg, son_durum="1 Gündür Düşüşte",analiz_baslik= "Twitter'da BIST100 Hakkında atılan Tweetlerin Analizi",infos = bist_100_data, kap=tweets, kap_2="Bloomberg" ,infos_list = list(bist_100_data.keys()),sample_Data = sample_Data, hacim="5.510.509.915 TL",predict_data=predict_data,percantege_data=percantege_data,symbol_name="BIST100")


@app.route('/detail_view/<symbol_name>')
def detail_analytics(symbol_name):
    data = pd.read_excel(UPLOADS_PATH+symbol_name+".xlsx")
    kap = pd.read_excel(UPLOADS_PATH+"KAP_DATA.xlsx")
    kap_3 = kap[kap.Class == symbol_name].Text.values[-5:]
    kap = kap[kap.Class == symbol_name].Text.values[np.random.randint(0,50)]
    symbol_data,tweets = Twitter(symbol_name,10)

    results = predicting(kap_3)
    
    x = list(pd.DataFrame(results)[0].value_counts().values)
    y = list(pd.DataFrame(results)[0].value_counts().index)
    inv_sentiment =dict(zip(y, x))
    print(y)
    
    data = data[['Close']]
    clf = pickle.load(open(UPLOADS_PATH+'model-'+symbol_name+'.pkl', 'rb'))
    base = list(data.Close.values[-7:])
    for i in range(7):
        base.append(clf.predict(np.array([base[i:]]))[0].round(2))
    sample_Data = data.Close.values[-28:]
    predict_data = base[-7:]
    percantege_data = (((predict_data[-7] - sample_Data[-2])/ predict_data[-7])*100).round(2)

    if symbol_name == "VESTL":
        hacim = "7.856.722 TL"
        son_durum = "3 Gündür Düşüşte"
    elif symbol_name == "FROTO":
        hacim = "20.860.079 TL"
        son_durum = "5 Gündür Yükselmekte"
    elif symbol_name == "GARAN":
        hacim = "48.790.854 TL"
        son_durum = "2 Gündür Düşüşte"
    elif symbol_name == "ASELS":
        hacim ="27.343.402 TL"
        son_durum = "2 Gündür Yükselmekte"
    elif symbol_name == "THYAO":
        hacim = "77.107.648 TL"
        son_durum = "2 Gündür Yükselmekte"
    else:
        hacim = "1.792.778 TL"
        son_durum = "5 Gündür Yükselmekte"
    
    x,y,z,v = get_links(symbol_name)
    bloomerg = []
    try:
        for i in range(0,4):
            bloomerg.append({"baslik":x[i],"linkler":y[i],"detay":z[i],"tarihler":v[i]})
    except:
        print("hata")
    return render_template('index.html',yazilar=bloomerg,  analiz_baslik= "Son 5 KAP Açıklamasının Duygusal Analizi", son_durum=son_durum,infos = inv_sentiment, infos_list = list(inv_sentiment.keys()),sample_Data = sample_Data ,hacim=hacim,kap=tweets,kap_2="Bloomberg",predict_data=predict_data,percantege_data=percantege_data,symbol_name=symbol_name)


@app.route('/listele')
def list_page()->'html':
    return render_template('list.html')

@app.route('/chat-bot')
def chat_bot()->'html':
    text = request.args.get('query')
    random_number = np.random.randint(0,3)
    response = chatbot.get_response(text,conversation_id=random_number)
    print(random_number)
    if "teşekkürler" in text:
        return {"result":{"fulfillment":{"speech":"Rica ederim, başka öneri istersen bu hisselerin ilgini çekebileceğini düşünüyorum. Bana Güven 😉","messages":["VESTL'in durumu","KCHOL'in durumu","GARAN'in durumu"]}}}
    elif "merhaba" in text.lower():
        return {"result":{"fulfillment":{"speech":"Merhaba 🖐, nasıl yardımcı olabilirim?"}}} 
    else:
        return {"result":{"fulfillment":{"speech":response.text}}}
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=37000)