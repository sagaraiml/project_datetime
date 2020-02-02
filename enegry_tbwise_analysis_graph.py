# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 13:32:00 2019

@author: Sagar Paithankar
"""

import os
import time
os.environ['TZ'] = 'Asia/Calcutta'
try:
    time.tzset()
except:
    pass
try:
    path = '/root/client'
    os.chdir(path)
except:
    path = os.getcwd()
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import pymysql
from datetime import datetime
from datetime import timedelta 
try:
    import magic
except:
    pass
import base64
import requests
import json
class DB(object):
        
    def getConnection(self):
        db = pymysql.connect("139.59.42.147","dummy","dummy123","energy_consumption")
        return db
    
    def getEngine(self):
        engine = create_engine('mysql+pymysql://dummy:dummy123@139.59.42.147:3306/energy_consumption', echo=False)
        return engine

db = DB().getConnection()
query = 'SELECT * FROM client_data WHERE date >=' + "'" + str(datetime.now().date()-timedelta(days=8)) + "' " + 'AND date <=' +  "'" + str(datetime.now().date()-timedelta(days=1)) + "'"
df = pd.read_sql(query,db)
df['time'] = 0
for i in range(len(df)):
    df['time'].iloc[i] = df['time_slot'].iloc[i].split('-')[0]
df['time'] = pd.to_datetime(df['time'])
df['time'] = df['time'].dt.time
df['date'] = df['date'].astype('str')
df['time'] = df['time'].astype('str')
df['datetime'] = pd.to_datetime(df['date']+' '+df['time'])
df = df[['datetime','block_load']]

db = DB().getConnection()
query = 'SELECT * FROM client_dayahead_forecast WHERE date >=' + "'" + str(datetime.now().date()-timedelta(days=8)) + "' " + 'AND date <=' +  "'" + str(datetime.now().date()-timedelta(days=1)) + "'"
df1 = pd.read_sql(query,db)
df1['time'] = pd.to_datetime(df1['start_time'])
df1['time'] = df1['time'].dt.time
df1['date'] = df1['date'].astype('str')
df1['time'] = df1['time'].astype('str')
df1['datetime'] = pd.to_datetime(df1['date']+' '+df1['time'])
df1 = df1[['datetime','version','forecast']]
for i in df1['version'].unique():
    print(i)
    ddf = df1[df1['version']==i]
    ddf = ddf[['datetime','forecast']]
    ddf.columns = ['datetime',i]
    df = pd.merge(df,ddf,on='datetime',how='left')
    df[i] = (np.abs(df['block_load']-df[i])/df['block_load'])*100
#df.drop(['v99','load'],axis=1,inplace=True)
df = df[['datetime','vrc','vrl','vrx','vvn','vn2']]
minimums = pd.DataFrame(np.min(df.iloc[:,2:],axis=1))
df.set_index('datetime',inplace=True)
df = df[str(datetime.now().date()-timedelta(days=1))]
df.reset_index(inplace=True)
df['time'] = df['datetime'].dt.time
df.drop('datetime',axis=1,inplace=True)
df.set_index('time',inplace=True)
#df['time'] = df['datetime'].dt.time
df.reset_index(inplace=True,drop=True)
df.reset_index(inplace=True)
df['TB'] = df['index'] + 1
df.drop('index',inplace=True,axis=1)
a = ['TB']
a.extend(df.columns[:-1])
df = df[a]
import chart_studio.plotly as py
import plotly.graph_objs as go
data = []
for i in range(1,df.shape[1]):
    trace = go.Scatter(
        x = np.array(df['TB']),
        y = np.array(df.iloc[:,i]),
        mode = 'lines',
        name = pd.DataFrame(df.iloc[:,i]).columns[0]
    )
    data.append(trace)
import plotly
plotly.offline.plot(data, filename = 'model_accuracies.html', auto_open=False)
try:
    mime = magic.Magic(mime=True)
    output_filename='model_accuracies.html'
    with open(output_filename, "rb") as content:
        encoded_string = content.read()
        s = base64.b64encode(encoded_string).decode(encoding="utf-8", errors="strict")
        attachment = [{'data': s, 'name': os.path.basename(output_filename),'mime': mime.from_file(output_filename)}]
    
    body_str = ""
    body_str += "<br>"
    body_str += "<br>"
    #data = {"to":["rohit.deshmukh@dummy.com"],"from":"mailbot@dummy.com","subject":"","body":""}
    data = {"to":["modeller@dummy.com","eds@dummy.com"],"from":"mailbot@dummy.com","subject":"","body":""}
    data['subject'] = "Timeblockwise analysis graph of all models for client for : "+str(datetime.now().date()-timedelta(days=1))
    data['body'] =body_str
    data['attachment'] = attachment
    data['type'] = 'html'
    jsdata = json.dumps(data)
    requests.post("http://api.dummy.com/index.php?r=notifications/send-email",
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}, data= jsdata)  
    print('Mailing success!')
except Exception as e:
    print(e)