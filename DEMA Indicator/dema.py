#Description: This program uses the Double Exponential Moving Average (DEMA) to determine when to buy and sell stock

#Import the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from google.colab import files # Use to load data on Google Colab
files.upload() # Use to load data on Google Colab

#Store the data
df = pd.read_csv('AMZN_Stock_Data.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

#Visually show the close price
df['Close'].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('Close Price for AMZN ')
plt.ylabel('USD Price ($)')
plt.xlabel('Date')
plt.show();

#Create a function to calculate the Double Exponential Moving Average (DEMA)
def DEMA(data, time_period, column):
  #Calculate the Exponential Moving Average for some time_period (in days)
  EMA = data[column].ewm(span=time_period, adjust=False).mean()
  #Calculate the DEMA
  DEMA = 2*EMA - EMA.ewm(span=time_period, adjust=False).mean()

  return DEMA

#Store the short term (20 day period) and the long term (50 day period) DEMA's in the data set for the strategy 
#When the short Term DEMA (20 day period) crosses above the long term DEMA (50 day period) this would be an indication to (buy)
#When the short term DEMA (20 day period) crosses below the long term DEMA (50 day period) this would be an indication to (sell)
df['DEMA_short'] = DEMA(df, 20, 'Close') #Store the short term DEMA
df['DEMA_long'] = DEMA(df, 50, 'Close') #Store the long term DEMA

#Plot the chart
#Create a list of columns to keep
column_list = ['DEMA_short', 'DEMA_long', 'Close']
df[column_list].plot(figsize=(12.2,6.4)) #Plot the data
plt.title('DEMA for AMZN')
plt.ylabel('USD Price ($)')
plt.xlabel('Date')
plt.show();

#Create a function to buy and sell the stock (The trading strategy)

#When the short Term DEMA (20 day period) crosses above the long term DEMA (50 day period) this is an indication to (buy)
#When the short Term DEMA (20 day period) crosses below the long term DEMA (50 day period) this is an indication to (sell)

def DEMA_Strategy(data):
  buy_list = [] #Create a list to store the price at which to buy
  sell_list = [] #Create a list to store the price at which to sell
  flag =  False #Create a flag to determine when the indicators cross
  #Loop through the data
  for i in range(0,len(data)):
      #Check if the Short Term DEMA crosses above the Long Term DEMA
      if data['DEMA_short'][i]  > data['DEMA_long'][i] and flag == False:
          buy_list.append(data['Close'][i])
          sell_list.append(np.nan)
          flag = True
      #Check if the Short Term DEMA crosses below the Long Term DEMA    
      elif data['DEMA_short'][i]  < data['DEMA_long'][i] and flag == True:
          buy_list.append(np.nan)
          sell_list.append(data['Close'][i])
          flag = False
      else:#Else they didn't cross
          buy_list.append(np.nan)
          sell_list.append(np.nan)
  #Store the Buy and Sell signals in the data set
  data['Buy'] = buy_list
  data['Sell'] = sell_list

#Run the Strategy to get the buy and sell signals
DEMA_Strategy(df)

# Visually Show The Stock Buy and Sell Signals
#Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
plt.scatter(df.index, df['Buy'], color = 'green', label='Buy Signal', marker = '^', alpha = 1) #Plot the buy signal
plt.scatter(df.index, df['Sell'], color = 'red', label='Sell Signal', marker = 'v', alpha = 1) #Plot the sell signal
plt.plot( df['Close'],  label='Close Price', alpha = 0.35)#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
plt.plot( df['DEMA_short'],  label='DEMA_short', alpha = 0.35) #plot the Short Term DEMA
plt.plot( df['DEMA_long'],  label='DEMA_long', alpha = 0.35) #plot the Long Term DEMA
plt.xticks(rotation=45)#Rotate the dates 45 degrees
plt.title('Close Price History Buy / Sell Signals')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD ($)',fontsize=18)
plt.legend( loc='upper left')
plt.show()
