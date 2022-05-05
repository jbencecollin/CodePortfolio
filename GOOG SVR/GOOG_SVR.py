
#Description: This program predicts the price of Google stock for a specific day

#import the libraries
from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')

#Load the data
from google.colab import files
uploaded = files.upload()

#Store and show the data
df = pd.read_csv('GOOG_Stock.csv')
df

#Get the number of rows and columns
df.shape

#Get and print the last row of data
actual_price = df.tail(1)
actual_price

#prepare the data for training the SVR models 
#Get all of the data except for the last row
df = df.head(len(df)-1)
#Print the new data set
print(df)

#Create empty lists to store the independent and dependent data
days = list()
adj_close_prices = list()

#Get the dates and adjusted close prices
df_days = df.loc[:, 'Date']
df_adj_close = df.loc[:, 'Adj Close Price']

#Create the independent data set
for day in df_days:
  days.append( [int(day.split('/')[1])] )

#Create the dependent data set
for adj_close_price in df_adj_close:
  adj_close_prices.append( float(adj_close_price) )

#Print the days and the adj close prices
print(days)
print(adj_close_prices)

#Create the 3 Support Vector Regression Models

#Create and train a SVR model using a linear kernel
lin_svr = SVR(kernel='linear', C=1000.0)
lin_svr.fit(days, adj_close_prices)

#Create and train a SVR model using a polynomial kernel
poly_svr = SVR(kernel='poly', C=1000.0, degree = 2)
poly_svr.fit(days, adj_close_prices)

#Create and train a SVR model using a rbf kernel
rbf_svr = SVR(kernel='rbf', C=1000.0, gamma = 0.15)
rbf_svr.fit(days, adj_close_prices)

#plot the models on a graph to see which has the best fit to the original data
plt.figure(figsize=(16,8))
plt.scatter(days, adj_close_prices, color = 'red', label = 'Data')
plt.plot(days, rbf_svr.predict(days), color = 'green', label = 'RBF Model')
plt.plot(days, poly_svr.predict(days), color = 'orange', label = 'Polynomial Model')
plt.plot(days, lin_svr.predict(days), color = 'blue', label = 'Linear Model')
plt.legend()
plt.show()

#Show the predicted price for the given day
day = [[30]]

print('The RBF SVR predicted:', rbf_svr.predict(day))
print('The Linear SVR predicted:', lin_svr.predict(day))
print('The Polynomial SVR predicted:', poly_svr.predict(day))

#Print the actual price of teh stock on day 31
print('The actual price:', actual_price['Adj Close Price'][20])