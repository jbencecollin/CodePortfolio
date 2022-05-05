

#Description This program determines if BTC is over bought or over sold

#Import the dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from google.colab import files # Use to load data on Google Colab
files.upload() # Use to load data on Google Colab

#Get and show the data
#Store the data
df = pd.read_csv('BTC.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Look at the data
df

#Create and plot the graph
plt.figure(figsize=(12.2,4.5)) #width = 12.2in, height = 4.5
plt.plot( df.index,df['Close'],  label='Close')#plt.plot( X-Axis , Y-Axis, line_width, alpha_for_blending,  label)
plt.title('Close Price History')
plt.xlabel('May 20, 2019 - May 20, 2020',fontsize=18)
plt.ylabel('Price USD ($)',fontsize=18)
plt.show()

#Calculate the RSI
delta = df['Close'].diff(1) #Use diff() function to find the discrete difference over the column axis with period value equal to 1
delta = delta.dropna() # or delta[1:]
up =  delta.copy() #Make a copy of this object’s indices and data
down = delta.copy() #Make a copy of this object’s indices and data
up[up < 0] = 0 #Change all of the values within up that are less than 0 to 0
down[down > 0] = 0 #Change all of the values that are greater than 0 in down to 0
time_period = 14
AVG_Gain = up.rolling(window=time_period).mean() #Get the average gain
AVG_Loss = abs(down.rolling(window=time_period).mean()) #Get the average loss
RS = AVG_Gain / AVG_Loss #Calculate the Relative Strength
RSI = 100.0 - (100.0/ (1.0 + RS)) #Get the Relative Strength Index

#Plot the RSI
plt.figure(figsize=(12.2,4.5))
RSI.plot()
plt.show()

#Plot the RSI with Overbought and Oversold RSI lines/levels
fig, ax = plt.subplots(1,1,figsize=(15,5))
ax0 = RSI.plot(ax=ax)
ax0.axhline(30, color = 'green')
ax0.axhline(70, color = 'green')
ax0.axhline(20, color = 'orange')
ax0.axhline(80, color = 'orange')
ax0.axhline(10, color = 'red')
ax0.axhline(90, color = 'red')