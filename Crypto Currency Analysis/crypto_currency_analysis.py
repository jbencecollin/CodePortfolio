#Description: This is a python program for crypto currency analysis


#Import the libraries
import numpy as np
import pandas as pd

# Load the data
from google.colab import files
uploaded = files.upload()

# Store the data into dataframes
#Note the data starts from 366 days ago as of today (just download relevant info here)
df_btc = pd.read_csv('BTC_USD_2019-03-22_2020-03-21-CoinDesk.csv')
df_eth = pd.read_csv('ETH_USD_2019-03-22_2020-03-21-CoinDesk.csv')
df_ltc = pd.read_csv('LTC_USD_2019-03-22_2020-03-21-CoinDesk.csv')

# Print the data for BTC
df_btc.head()

# Print the first 5 rows of data for ETH'
df_eth.head()

# Print the first 5 rows of LTC
df_ltc.head()

# Create a new dataframe that holds teh closing price of all 3 crypto currencies
df = pd.DataFrame({'BTC': df_btc['Closing Price (USD)'],
                   'ETH': df_eth['Closing Price (USD)'],
                   'LTC': df_ltc['Closing Price (USD)']
                   
    
})

#Show the new dataframe
df

#Get statistics on the data 
df.describe()

#Visualize the cryptocurrency closing prices 
import matplotlib.pyplot as plt 
plt.style.use('fivethirtyeight')

my_crypto = df
plt.figure(figsize = (12.2, 4.5))
for c in my_crypto.columns.values:
  plt.plot(my_crypto[c], label = c)

plt.title('Cryptocurrency Graph')
plt.xlabel('Days')
plt.ylabel(' Crypto Price ($)')
plt.legend(my_crypto.columns.values, loc= 'upper left')
plt.show()

#Scale the data 
#the min-max scaler method scales the dataset so that all the input features lie between 0 and 100 inclusive
from sklearn import preprocessing 
min_max_scaler = preprocessing.MinMaxScaler(feature_range=(0, 100))
scaled = min_max_scaler.fit_transform(df)
scaled

# Convert the scaled data into a dataframe
df_scale = pd.DataFrame(scaled, columns = df.columns)

#Visualize the scaled data
my_crypto = df_scale

plt.figure(figsize=(12.4, 4.5))
for c in my_crypto.columns.values: 
  plt.plot(my_crypto[c], label=c)

plt.title('Cryptocurrency Scaled Graph')
plt.xlabel('Days')
plt.ylabel('Crypto Scaled Price ($)')
plt.legend(my_crypto.columns.values, loc = 'upper left')
plt.show()

#Get the daily simple return 
DSR = df.pct_change(1)
DSR

#Visualize the daily simple returns 
plt.figure(figsize=(12, 4.5))

for c in DSR.columns.values:
  plt.plot(DSR.index, DSR[c], label = c, lw = 2, alpha = .7)

plt.title('Daily Simple Returns')
plt.ylabel('Percentage (in decimal form')
plt.xlabel('Days')
plt.legend(DSR.columns.values, loc= 'upper right')
plt.show()

# Print the volatility /standard deviation σ (or sqrt(variance)) for daily simple returns
print('The cryptocurrency volatility:')
DSR.std()

#Show the mean / average daily simple return 
DSR.mean()

#Get the correlation
#Correlation is used to determine when a change in one variable can result in a change in another.
DSR.corr()

# Visualize the correlation
import seaborn as sns

plt.subplots(figsize= (11,11))
sns.heatmap(DSR.corr(), annot= True, fmt= '.2%')

#Get the daily cumulative simple returns 
DCSR = (DSR+1).cumprod()

#Show 
DCSR

#Visualize the daily cumulative simple returns 
plt.figure(figsize=(12.2, 4.5))
for c in DCSR.columns.values:
  plt.plot(DCSR.index, DCSR[c], lw=2, label= c)

plt.title('Daily Cumulative Simple Return')
plt.xlabel('Days')
plt.ylabel('Growth of $1 investment')
plt.legend(DCSR.columns.values, loc = 'upper left', fontsize = 10)
plt.show()