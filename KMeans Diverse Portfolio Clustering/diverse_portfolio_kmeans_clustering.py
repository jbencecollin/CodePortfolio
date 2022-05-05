

#Description: StockMarket Clustering with K-means using Python

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from google.colab import files
files.upload()

df = pd.read_csv('NASDAQ.csv')
#Remove the date column
df.drop(['Date'], axis=1, inplace=True)
#Show the data
df

#Calculate the annual mean returns and variances
daily_returns = df.pct_change()
annual_mean_returns = daily_returns.mean() * 252
annual_return_variance = daily_returns.var() * 252

#Create a new dataframe
df2 = pd.DataFrame(df.columns, columns=['Stock_Symbols'])
df2['Variances'] = annual_return_variance.values
df2['Returns'] = annual_mean_returns.values
#Show the data
df2

#Use the Elbow method to determine the number of clusters to use to group the stocks
#Get and store the annual returns and annual variances
X = df2[['Returns', 'Variances']].values
inertia_list = []
for k in range(2,16):
  #Create and train the model 
  kmeans = KMeans(n_clusters=k)
  kmeans.fit(X)
  inertia_list.append(kmeans.inertia_)

#Plot the data
plt.plot(range(2,16), inertia_list)
plt.title('Elbow Curve')
plt.xlabel('Number of Clusters')
plt.ylabel('Inertia or Sum Squared Error (SSE)')
plt.show()

#Get and show the labels / groups
kmeans = KMeans(n_clusters=4).fit(X)
labels = kmeans.labels_
labels

df2['Cluster_Labels'] = labels
df2

#Plot and show the different clusters
plt.scatter(X[:,0], X[:,1], c = labels, cmap = 'rainbow')
plt.title('K-Means Plot')
plt.xlabel('Returns')
plt.ylabel('Variances')
plt.show()

#Create a function to build a simple diversed portfolio
def diversed_port():
  for i in range(0, 4):
    symbol = df2[ df2['Cluster_Labels'] == i].head(1)
    print(symbol[['Stock_Symbols', 'Cluster_Labels']])

diversed_port()