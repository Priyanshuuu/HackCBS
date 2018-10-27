from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer
import time
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
app = Flask(__name__)

nltk.download('stopwords')
stops=set(stopwords.words('english'))
punct=list(string.punctuation)
stops.update(punct)

stops = set(stopwords.words('english'))
punctuations = list(string.punctuation)
stops.update(punctuations)

def  Remove_stop_words(x):
    l=len(x)
    #print(l)
    y=[]
   
    for i in range(l):
        if x[i] not in stops :
            y.append(x[i])
    #print(len(y))
    return y

def lower_casing(words): 
    text=[]
    for i in words :
        text.append(i.lower())
    return text


def adding(b):
    
    txt=''
    for i in range(len(b)):
        txt+=' '+b[i]
    textdocument.append(txt)

df=pd.read_csv(r'finaldataset.csv')

x=df.copy()


lt=['Category', 'StateName', 'DistrictName', 'BlockName', 'CreatedOn']
for i in lt:
    x.drop(i, axis=1,inplace = True)


len(x)
X = x.iloc[:,0:5]
Y = pd.DataFrame(x.iloc[:,5])


new_data=pd.get_dummies(X,columns=['Season','Sector','Crop','QueryType'])

X=new_data.iloc[:,1:]
from sklearn import model_selection
xtrain,xtest,ytrain,ytest=model_selection.train_test_split(X,Y,random_state=0)
#print(len(xtrain))
#print(len(xtest))
#print(len(ytrain))
#print(len(ytest))






from sklearn.linear_model import LogisticRegression

clf=LogisticRegression(C=0.06)
clf.fit(xtrain,ytrain)

y1_pred=clf.predict(xtest)





from gtts import gTTS
import speech_recognition as sr
import os
import re
import time
from weather import Weather, Unit

def rep():
    a=mycommand()
    talkToMe(a) 
    while True:
        if(a=='exit'):
            break
        else:
            a=mycommand()
            #talkToMe(a)

def talkToMe(audio):
    tts=gTTS(text=audio,lang='hi')
    tts.save('hello.mp3')
    os.system('hello.mp3')

from yandex import Translater
def transl(file):
    tr = Translater()
    tr.set_key('trnsl.1.1.20181027T064233Z.3eb896622966c6cb.3685096a854ebdc502d7d01bdecdf7d490e88f9d') # Api key found on https://translate.yandex.com/developers/keys
    tr.set_text(file)
    tr.set_from_lang('en')
    tr.set_to_lang('hi')
    l=tr.translate()
    print(l)
    talkToMe(l)

import goslate
def trans(file):
    gs = goslate.Goslate()
    translatedText = gs.translate(file,'hi')
    print(translatedText)
    talkToMe(translatedText)

def mycommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Now please enter your command")
        r.pause_threshold=1
        r.adjust_for_ambient_noise(source,duration=1)
        audio=r.listen(source)
        try:
            command=r.recognize_google(audio, language="en-IN") #hi-IN
            print("you said: " +command+"\n")
            if 'current weather in' in command:
                reg_ex = re.search('current weather in (.*)', command)
                if reg_ex:
                    city = reg_ex.group(1)
                    weather = Weather(unit=Unit.CELSIUS)
                    location = weather.lookup_by_location(city)
                    condition = location.condition
                    forecasts = location.forecast
                    for i in range(1):
                        print(forecasts[i].text)
                        print(forecasts[i].date)
                        print(forecasts[i].high)
                        print(forecasts[i].low)
                        #x="On " + forecast.date + ", the weather will be " + forecast.text
                        #y=" with estimated maximum temperature as " + forecast.high + "degree celsius and with estimated minimum temperature as " + forecast.low + " degree celsius"
                        z='On %s the weather will be %s with estimated maximum temperature as %s degree' % (forecasts[i].date, forecasts[i].text, forecasts[i].high)
                        a='celsius and with estimated minimum temperature as %s degree celsius ' % (forecasts[i].low)
                        #talkToMe(x)
                        trans(z)
                        #talkToMe(z)
                        time.sleep(6)
                        #talkToMe(a)
                        trans(a)
                        time.sleep(6)
                        
                        
                    
                    
        except sr.UnknownValueError:
            #assistant(mycommand())
            print("Your command couldn't be heard")
            command = myCommand();
    return command












@app.route('/')
def render_static():
    return render_template('index.html')
 
@app.route('/background_process_test')
def background_process_test():
    print("Hello")
    rep()
    return "nothing"


if __name__ == '__main__':
    app.run()