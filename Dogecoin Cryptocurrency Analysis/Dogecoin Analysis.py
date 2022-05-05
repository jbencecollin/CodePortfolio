#Description: This program analysis Dogecoin

#Import the libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data set
from google.colab import files
files.upload()

#Store the data into a variable
df = pd.read_csv('Crypto_Data.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Drop or remove the date column
df = df.drop(['Date'], axis=1)
#Look at the data
df

#Get some statistics on the data
df.describe()

#Visually show the price of the cryptocurrencies
my_crypto = df

plt.figure(figsize=(12.2, 4.5))
for c in my_crypto.columns.values:
  plt.plot(my_crypto[c], label=c)

plt.title('Crypto Price')
plt.xlabel('Days')
plt.ylabel('Crypto Price ($)')
plt.legend(my_crypto.columns.values, loc='upper left')
plt.show()

#Scale the data
from sklearn import preprocessing
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 100))
scaled = min_max_scaler.fit_transform(df)
#Show the scaled data
scaled

#Convert the scaled data to a data frame
df_scaled = pd.DataFrame(scaled, columns = df.columns)
#Set the date as the index
df_scaled = df_scaled.set_index(pd.DatetimeIndex(df.index))
#Show the scaled dataframe
df_scaled

#Visualize the scaled data
my_crypto = df_scaled

plt.figure(figsize=(12.2, 4.5))
for c in my_crypto.columns.values:
  plt.plot(my_crypto[c], label=c)

plt.title('Crypto Scaled Price')
plt.xlabel('Days')
plt.ylabel('Individual Cryptos Scaled Price From Min To Max')
plt.legend(my_crypto.columns.values, loc='upper left')
plt.show()

#Get the Daily Simple Return
DSR = df.pct_change(1)
DSR

#Visualize and show the Daily Simple Returns
my_crypto = DSR

plt.figure(figsize=(12.2, 4.5))
for c in my_crypto.columns.values:
  plt.plot(my_crypto[c], label=c, alpha = .7, lw=2)

plt.title('Daily Simple Returns')
plt.xlabel('Days')
plt.ylabel('Percentage (in decimal form)')
plt.legend(my_crypto.columns.values, loc='upper left')
plt.show()

#Print the crypto volatility
print('The cryptocurrency volatility:')
DSR.std()

#Show the mean or average daily simple return
DSR.mean()

#Get the correlation
DSR.corr()

#Graph the correlations as a heat map
import seaborn as sns
plt.subplots(figsize=(11,11))
sns.heatmap(DSR.corr(), annot= True, fmt = '.2%')

#Calculate the daily cumulative simple return 
DCSR = (DSR+1).cumprod()
DCSR

#Visualize the scaled data
my_crypto = DCSR

plt.figure(figsize=(12.2, 4.5))
for c in my_crypto.columns.values:
  plt.plot(my_crypto[c], label=c)

plt.title('Daily Cumulative Simple Return')
plt.xlabel('Days')
plt.ylabel('Growth of $1 investment')
plt.legend(my_crypto.columns.values, loc='upper left')
plt.show()