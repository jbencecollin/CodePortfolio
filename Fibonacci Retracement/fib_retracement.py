
#Description: This program calculates and plots the Fibonacci Retracement Levels

#Import the libraries
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from google.colab import files
files.upload()

#Store the data
df = pd.read_csv('S&P500.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

#Plot the close price on a chart
plt.figure(figsize=(12.2, 4.5))
plt.plot(df.Close, color = 'blue')
plt.title('S&P 500 Close Price')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.show()

#Calculate the Fibonacci Retracement Level Prices with a non-Fibonacci Level/Ratio of 0.5 or 50%
#The Fibonacci Ratios are 0.236, 0.382, and 0.618

#First, get the maximum and minimum close price for the time period
maximum_price = df['Close'].max()
minimum_price = df['Close'].min()

difference = maximum_price - minimum_price
first_level = maximum_price - difference * 0.236
second_level = maximum_price - difference * 0.382
third_level = maximum_price - difference * 0.5 
fourth_level = maximum_price - difference * 0.618

#print the price at each level
print('Level Percentage Price ($)')
print('00.0%\t\t', maximum_price)
print('23.6%\t\t', first_level)
print('38.2%\t\t', second_level)
print('50.0%\t\t', third_level)
print('61.8%\t\t', fourth_level)
print('100.0%\t\t', minimum_price)

#Plot the Fibonacci Level prices along with the close price
new_df = df
plt.figure(figsize=(12.33, 4.5))
plt.title('Fibonacci Retracement Plot')
plt.plot(new_df.index, new_df['Close'])
plt.axhline(maximum_price, linestyle='--', alpha = 0.5, color='red')
plt.axhline(first_level, linestyle='--', alpha = 0.5, color='orange')
plt.axhline(second_level, linestyle='--', alpha = 0.5, color='yellow')
plt.axhline(third_level, linestyle='--', alpha = 0.5, color='green')
plt.axhline(fourth_level, linestyle='--', alpha = 0.5, color='blue')
plt.axhline(minimum_price, linestyle='--', alpha = 0.5, color='purple')
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()

#Create another plot of the Fibonacci levels along with the close price with levels filled
new_df = df
fig = plt.figure(figsize=(12.33, 4.5))
ax = fig.add_subplot(1,1,1)
plt.title('Fibonacci Retracement Plot')
plt.plot(new_df.index, new_df['Close'], color='black')
plt.axhline(maximum_price, linestyle='--', alpha = 0.5, color='red')
ax.fill_between(new_df.index, maximum_price, first_level, color='red')

plt.axhline(first_level, linestyle='--', alpha = 0.5, color='orange')
ax.fill_between(new_df.index, first_level, second_level, color='orange')

plt.axhline(second_level, linestyle='--', alpha = 0.5, color='yellow')
ax.fill_between(new_df.index, second_level, third_level, color='yellow')

plt.axhline(third_level, linestyle='--', alpha = 0.5, color='green')
ax.fill_between(new_df.index, third_level, fourth_level, color='green')

plt.axhline(fourth_level, linestyle='--', alpha = 0.5, color='blue')
ax.fill_between(new_df.index, fourth_level, minimum_price, color='blue')

plt.axhline(minimum_price, linestyle='--', alpha = 0.5, color='purple')


plt.xlabel('Date')
plt.ylabel('Price')
plt.show()