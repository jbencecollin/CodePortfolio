#Description: Create and Plot Multiple Technical Indicators

#Import the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from google.colab import files # Use to load data on Google Colab
files.upload() # Use to load data on Google Colab

#Store the data 
df = pd.read_csv('TSLA_Stock_Data.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

#Create functions to calculate the SMA, & the EMA
#Create the Simple Moving Average Indicator
#The most common time periods used in moving averages are 15, 20, 30, 50, 100, and 200 days. 
def SMA(data, period=30, column='Close'):
  return data[column].rolling(window=period).mean()

#Create the Exponential Moving Average Indicator
def EMA(data, period=20, column='Close'):
  return data[column].ewm(span=period, adjust=False).mean()

#Calculate the MACD and the Signal Line
"""
MACD, short for moving average convergence/divergence, 
is a trading indicator used in technical analysis of stock prices.

    period_long: the longer period EMA (26 days recommended)
    period_short: the shorter period EMA (12 days recommended)
    period_signal: signal line EMA (9 days recommended)

"""
def MACD(data, period_long=26, period_short=12, period_signal=9, column='Close'):
    #Calculate the Short Term Exponential Moving Average
    ShortEMA = EMA(data, period_short, column=column) #AKA Fast moving average
    #Calculate the Long Term Exponential Moving Average
    LongEMA = EMA(data, period_long, column=column) #AKA Slow moving average
    #Calculate the Moving Average Convergence/Divergence (MACD)
    data['MACD'] = ShortEMA - LongEMA
    #Calcualte the signal line
    data['Signal_Line'] = EMA(data, period_signal, column='MACD')#data['MACD'].ewm(span=period_signal, adjust=False).mean()
        
    return data

#Create a function to compute the Relative Strength Index (RSI) technical indicator
'''
Relative Strength Index (RSI) is a technical indicator, which is used in the analysis of
 financial markets to determine if a stock is being over bought or over sold

A common time period to use for RSI is 14 days. 
'''
def RSI(data, period = 14, column = 'Close'):
  delta = data[column].diff(1) #Use diff() function to find the discrete difference over the column axis with period value equal to 1
  delta = delta.dropna() # or delta[1:]
  up =  delta.copy() #Make a copy of this object’s indices and data
  down = delta.copy() #Make a copy of this object’s indices and data
  up[up < 0] = 0 
  down[down > 0] = 0 
  data['up'] = up
  data['down'] = down
  AVG_Gain = SMA(data, period, column='up')#up.rolling(window=period).mean()
  AVG_Loss = abs(SMA(data, period, column='down'))#abs(down.rolling(window=period).mean())
  RS = AVG_Gain / AVG_Loss
  RSI = 100.0 - (100.0/ (1.0 + RS))
  
  data['RSI'] = RSI
  return data

#Creating the data set 
MACD(df)
RSI(df)
df['SMA'] = SMA(df)
df['EMA'] = EMA(df)
#Show the data
df

#Plot the chart
#Create a list of columns to keep
column_list = ['MACD','Signal_Line']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('MACD for TSLA')
plt.show();

#Plot the chart
#Create a list of columns to keep
column_list = ['SMA','Close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('SMA for TSLA')
plt.ylabel('USD Price ($)')
plt.show();

#Plot the chart
#Create a list of columns to keep
column_list = ['EMA','Close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('EMA for TSLA')
plt.ylabel('USD Price ($)')
plt.show();

#Plot the chart
#Create a list of columns to keep
#Sell: RSI = 70 or greater
#Buy: RSI = 30 or lower
column_list = ['RSI']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('RSI for TSLA')
plt.show()
