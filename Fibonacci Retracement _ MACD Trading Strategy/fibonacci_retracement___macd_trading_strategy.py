
#Description: This program uses Fibonacci Retracement Levels and MACD to indicate when to buy and sell stock.

#Import the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from google.colab import files
files.upload()

#Get and show the data
df = pd.read_csv('AAPL.csv')
#Set the date as the index 
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

#Plot the data 
plt.figure(figsize=(12,4))
plt.plot(df.Close)
plt.title('Close Price')
plt.xlabel('Date')
plt.ylabel('Price ($USD)')
plt.xticks(rotation=45)
plt.show()

#Calculate the Fibonacci Retracement Levels
max_price = df['Close'].max()
min_price = df['Close'].min()

difference = max_price - min_price
first_level = max_price - difference * 0.236
second_level = max_price - difference * 0.382
third_level = max_price - difference * 0.5
fourth_level = max_price - difference * 0.618

#Calculate the MACD Line and the Signal Line indicators
#Calculate the Short Term Exponential Moving Average
ShortEMA = df.Close.ewm(span=12, adjust=False).mean()
#Calculate the Long Term Exponential Moving Average
LongEMA = df.Close.ewm(span=26, adjust= False).mean()
#Calculate the Moving Average Convergence/Divergence (MACD)
MACD = ShortEMA - LongEMA
#Calculate the Signal Line
signal = MACD.ewm(span=9, adjust =False).mean()

#Plot the Fibonacci Levels along with the close price and the MACD and Signal Line
new_df = df

#plot the Fibonacci Levels
plt.figure(figsize=(12.33, 9.5))
plt.subplot(2,1,1)
plt.plot(new_df.index, new_df['Close'])
plt.axhline(max_price, linestyle= '--', alpha=0.5, color='red')
plt.axhline(first_level, linestyle= '--', alpha=0.5, color='orange')
plt.axhline(second_level, linestyle= '--', alpha=0.5, color='yellow')
plt.axhline(third_level, linestyle= '--', alpha=0.5, color='green')
plt.axhline(fourth_level, linestyle= '--', alpha=0.5, color='blue')
plt.axhline(min_price, linestyle= '--', alpha=0.5, color='purple')
plt.ylabel('Fibonacci')
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)

#Plot the MACD Line and the Signal Line
plt.subplot(2,1,2)
plt.plot(new_df.index, MACD)
plt.plot(new_df.index, signal)
plt.ylabel('MACD')
plt.xticks(rotation=45)

plt.savefig('Fig1.png')

#Create new columns for the data frame
df['MACD'] = MACD
df['Signal Line'] = signal
#Show the new data
df

#Create a function to be used in our strategy to get the upper Fibonacci Level and the Lower Fibonacci Level of the current price.
def getLevels(price):
  if price >= first_level:
    return (max_price, first_level)
  elif price >= second_level:
    return (first_level, second_level)
  elif price >= third_level:
    return (second_level, third_level)
  elif price >= fourth_level:
    return (third_level, fourth_level)
  else:
    return (fourth_level, min_price)

#Create a function for the trading strategy

#The Strategy
#If the signal line crosses above the MACD Line and the current price crossed above or below the last Fibonacci Level then buy
#If the signal line crosses below the MACD Line and the current price crossed above or below the last Fibonacci Level then sell
#Never sell at a price that's lower then I bought

def strategy(df):
  buy_list =[]
  sell_list=[]
  flag = 0 
  last_buy_price = 0

  #Loop through the data set
  for i in range(0, df.shape[0]):
    price = df['Close'][i]
    #If this is the first data point within the data set, then get the level above and below it. 
    if i == 0:
      upper_lvl, lower_lvl = getLevels(price)
      buy_list.append(np.nan)
      sell_list.append(np.nan)
    #Else if the current price is greater than or equal to the upper_lvl, or less than or equal to the lower_lvl, then we know the price has 'hit' or crossed a new Fibonacci Level
    elif price >= upper_lvl or price <= lower_lvl:

      #Check to see if the MACD line crossed above or below the signal line
      if df['Signal Line'][i] > df['MACD'][i] and flag == 0:
        last_buy_price = price
        buy_list.append(price)
        sell_list.append(np.nan)
        #Set the flag to 1 to signal that the share was bought
        flag = 1
      elif df['Signal Line'][i] < df['MACD'][i] and flag == 1 and price >= last_buy_price:
        buy_list.append(np.nan)
        sell_list.append(price)
        #Set the flag to 0 to signal that the share was sold
        flag = 0
      else:
        buy_list.append(np.nan)
        sell_list.append(np.nan)
    else:
      buy_list.append(np.nan)
      sell_list.append(np.nan)

    #Update the new levels
    upper_lvl, lower_lvl = getLevels(price)

  return buy_list, sell_list

#Create buy and sell columns
buy, sell = strategy(df)
df['Buy_Signal_Price'] = buy
df['Sell_Signal_Price'] = sell 
#Show the data
df

#Plot the Fibonacci Levels along with the close price and with the Buy and Sell signals
new_df = df

#plot the Fibonacci Levels
plt.figure(figsize=(12.33, 4.5))
plt.plot(new_df.index, new_df['Close'], alpha=0.5)
plt.scatter(new_df.index, new_df['Buy_Signal_Price'], color='green', marker='^', alpha=1)
plt.scatter(new_df.index, new_df['Sell_Signal_Price'], color='red', marker='v', alpha=1)
plt.axhline(max_price, linestyle= '--', alpha=0.5, color='red')
plt.axhline(first_level, linestyle= '--', alpha=0.5, color='orange')
plt.axhline(second_level, linestyle= '--', alpha=0.5, color='yellow')
plt.axhline(third_level, linestyle= '--', alpha=0.5, color='green')
plt.axhline(fourth_level, linestyle= '--', alpha=0.5, color='blue')
plt.axhline(min_price, linestyle= '--', alpha=0.5, color='purple')
plt.ylabel('Close Price in USD')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.show()