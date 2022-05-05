

#Description: This program predicts the price of FB stock for a specific day
#             using the Machine Learning algorithm called 
#             Support Vector Regression (SVR) Model

#Import the libraries
from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from google.colab import files # Use to load data on Google Colab
uploaded = files.upload() # Use to load data on Google Colab

#Store and show the data
df = pd.read_csv('FB_Stock.csv') 
df

#Get the number of rows and columns in the data set 
df.shape

#Print the last row of data (this will be the data that we test on)
actual_price = df.tail(1)
actual_price

#Prepare the data for training the SVR models
#Get all of the data except for the last row
df = df.head(len(df)-1)
#Print the new data frame
print(df)

#Create empty lists to store the independent 'X' and dependent 'y' data
days = list()
adj_close_prices = list()

#Get only the date or independent data and the adjusted close price or dependent data
df_days = df.loc[:,'Date'] 
df_adj_close = df.loc[:,'Adj Close Price']

#Create the independent data set 'X' as dates
for day in df_days:
  days.append( [int(day.split('/')[1]) ] )
  
#Create the dependent data set 'y' as prices
for adj_close_price in df_adj_close:
  adj_close_prices.append(float(adj_close_price))

#Print the days
print(days)

#Print the adj close prices
print(adj_close_prices)

#Create 3 Support Vector Regression Models

#Create and train an SVR model using a linear kernel
lin_svr = SVR(kernel='linear', C=1000.0)
lin_svr.fit(days,adj_close_prices)

#Create and train an SVR model using a polynomial kernel
poly_svr = SVR(kernel='poly', C=1000.0, degree=2)
poly_svr.fit(days, adj_close_prices)

#Create and train an SVR model using a RBF kernel
rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=0.15)
rbf_svr.fit(days, adj_close_prices)

#Plot the models on a graph to see which has the best fit
plt.figure(figsize=(16,8))
plt.scatter(days, adj_close_prices, color = 'black', label='Data')
plt.plot(days, rbf_svr.predict(days), color = 'green', label='RBF Model')
plt.plot(days, poly_svr.predict(days), color = 'orange', label='Polynomial Model')
plt.plot(days, lin_svr.predict(days), color = 'blue', label='Linear Model')
plt.xlabel('Days')
plt.ylabel('Adj Close Price')
plt.title('Support Vector Regression')
plt.legend()
plt.show()

#Show the predicted price for the given day
day = [[31]]
print('The RBF SVR predicted price:',rbf_svr.predict(day))
print('The linear SVR predicted price',lin_svr.predict(day))
print('The polynomial SVR predicted price',poly_svr.predict(day))

#Print the actual price of the stock on day 31 
print('The actual price:', actual_price['Adj Close Price'][21])