# -*- coding: utf-8 -*-
"""
Created on Sept 2019

@author: Sagar_Paithankar
"""

import os
path = r'G:\Anaconda_CC\spyder\_dummy_my\other'
os.chdir(path)
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
loadmet = pd.read_pickle('dummy_data')
scada = loadmet.copy()
scada = scada[['datetime','load']]
scada.set_index('datetime', inplace=True)
scada = scada.load.resample('D').mean().to_frame()
scada['load'].plot()
scada.reset_index(inplace=True)


#try this with diff models
df = pd.DataFrame()
df['yr2016'] = list(scada[(datetime(2017,1,1,0,0,0) > scada['datetime']) & (scada['datetime'] >= datetime(2016,9,1,0,0,0))]['load'])
df['yr2017'] = list(scada[(datetime(2018,1,1,0,0,0) > scada['datetime']) & (scada['datetime'] >= datetime(2017,9,1,0,0,0))]['load'])
df['yr2018'] = list(scada[(datetime(2019,1,1,0,0,0) > scada['datetime']) & (scada['datetime'] >= datetime(2018,9,1,0,0,0))]['load'])
a = scada[scada['datetime'] > datetime(2019,9,1,0,0,0)]['load'].to_frame()
#deepyr2018 = scada[(scada.index.month > 9) & (scada.index.year == 2016)]
x = range(1, 123)
plt.plot( x, 'yr2016', data=df, marker='', color='blue')
plt.plot( x, 'yr2017', data=df, marker='', color='green')
plt.plot( x, 'yr2018', data=df, marker='', color='red')
plt.plot( range(1, 53), 'load', data=a, marker='', color='black')
plt.legend()



scada = loadmet.copy()
scada = scada[['datetime','load']]
scada.set_index('datetime', inplace=True)
scada = scada.load.resample('12H').mean().to_frame()
scada.reset_index(inplace=True)

df = pd.DataFrame()
df['yr2016'] = list(scada[(datetime(2016,11,1,0,0,0) > scada['datetime']) & (scada['datetime'] > datetime(2016,9,1,0,0,0))]['load'])
df['yr2017'] = list(scada[(datetime(2017,11,1,0,0,0) > scada['datetime']) & (scada['datetime'] > datetime(2017,9,1,0,0,0))]['load'])
df['yr2018'] = list(scada[(datetime(2018,11,1,0,0,0) > scada['datetime']) & (scada['datetime'] > datetime(2018,9,1,0,0,0))]['load'])
a = scada[scada['datetime'] > datetime(2019,9,1,0,0,0)]['load'].to_frame()
#deepyr2018 = scada[(scada.index.month > 9) & (scada.index.year == 2016)]
x = range(1, 122)
plt.plot( x, 'yr2016', data=df, marker='', color='blue')
plt.plot( x, 'yr2017', data=df, marker='', color='green')
plt.plot( x, 'yr2018', data=df, marker='*', color='red')
plt.plot( range(1, 58), 'load', data=a, marker='.', color='black')
plt.show()


