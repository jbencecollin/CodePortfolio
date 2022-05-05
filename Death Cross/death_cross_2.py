
#Description: A Death Cross Program

#Import the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the Bitcoin data
from google.colab import files # Use Googles library to load the data on Google Colab
files.upload() # Use to load data on Google Colab

#Store the data 
df = pd.read_csv('BTC.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

#Use a Simple moving average to create the death cross 
#Create a function to get the Simple Moving Average 
def SMA(data, period=30, column='Close'):
  return data[column].rolling(window=period).mean()

#Create new columns to store the Short Term SMA and the Long Term SMA
df['ShortSMA'] = SMA(df,period=50)
df['LongSMA'] = SMA(df,period=200)

#Plot the chart
#Create a list of columns to show
column_list = ['ShortSMA', 'LongSMA', 'Close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('Death/Golden Cross')
plt.show();

#Create a function to see the dates of each Death cross and Golden cross within the data set
#If Short Term Moving AVG crosses below the Long Term Moving AVG then this indicates prices are going to drop lower long term
#If Short Term Moving AVG crosses above the Long Term Moving AVG then this indicates prices are going to increase higher long term
def death_golden_cross():

  first_cross = 0
  #Loop through the length of the data set
  for i in range(0, len(df)):
    if df['ShortSMA'][i] < df['LongSMA'][i] and first_cross == 0:
      print('DEATH CROSS on day', df.index[i])
      first_cross = 1
    elif df['ShortSMA'][i] > df['LongSMA'][i] and first_cross == 1:
      print('GOLDEN CROSS on day', df.index[i])
      first_cross = 0

#Show the dates of each Death cross and Golden cross within the data set
death_golden_cross()
