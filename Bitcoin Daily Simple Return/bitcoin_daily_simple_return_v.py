
#Description: This program gets BTC's daily simple return

#Import the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data set
from google.colab import files
files.upload()

#Store the data into the data frame
df = pd.read_csv('BTC_Data.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#show the data frame
df

#Visually show and plot the close price 
plt.figure(figsize=(16,8))
plt.title('Close Price', fontsize=18)
plt.plot(df['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close Price USD ($)',fontsize=18)
plt.show()

#Calculate and show the Daily Simple Returns
DSR = df['Close'].pct_change(1)
#Show the daily simple return
DSR

#Get some statistics on the Daily Simple Return

#Here the expected daily return is about .1502% .
#The biggest daily drop within this data set was about 37.16%
#The biggest daily gain within this data set was about 18.74%
DSR.describe()

#Visually show and plot the daily simple return
plt.figure(figsize=(12,4))
plt.plot(DSR.index, DSR, label = 'DSR', lw = 2, alpha = .7)
plt.title('Daily Simple Returns')
plt.ylabel('Percentage (in decimal form)')
plt.xlabel('Days')
plt.xticks(rotation=45)
#Now we can visually see the daily drop of about 37.16%
# and we can visually see the highest percentage increase in price at about 18.74%

#Let's put the two plots together
#First plot Close price
top = plt.subplot2grid((4,4), (0,0), rowspan=3, colspan=4)
top.plot(df.index, df['Close'], label= 'Close')
plt.title('Close Price')
plt.legend(loc='upper left')
#Second Plot the DSR
bottom = plt.subplot2grid((4,4), (3,0), rowspan=1, colspan=4)
plt.title('DSR')
bottom.bar(DSR.index, DSR)
plt.subplots_adjust(hspace=0.75)
plt.gcf().set_size_inches(15,8)
