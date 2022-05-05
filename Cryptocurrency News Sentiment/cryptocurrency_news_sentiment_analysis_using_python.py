

#Description: This program analysis the sentiment of cryptocurrency news headlines

#Import the libraries
import pandas as pd
import numpy as np
from textblob import TextBlob
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

# Load the data
from google.colab import files
uploaded = files.upload()

#Store the data
#df = pd.read_csv('Crypto_News.csv', encoding= 'unicode_escape')
df = pd.read_csv('Cryptocurrency_News.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

# Create a function to get the polarity
def getPolarity(text):
   return  TextBlob(text).sentiment.polarity

# Create one new column called 'Polarity'
df['Polarity'] = df['Headline'].apply(getPolarity)

# Show the new dataframe with the new column called 'Polarity'
df

# Create a function to compute negative (-1), neutral (0) and positive (+1) sentiments
def getSentiment(score):
  if score < 0:
    return 'Negative'
  elif score == 0:
    return 'Neutral'
  else:
    return 'Positive'

#Create a new column to store sentiment string
df['Sentiment'] = df['Polarity'].apply(getSentiment)
# Show the dataframe
df

# Plotting and visualizing the counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('Counts')
df['Sentiment'].value_counts().plot(kind = 'bar')
plt.show()

#Compute and show the sum of the polarity for each date
polarity = df.groupby(['Date']).sum()['Polarity']
polarity

#Visually show the sum of the polarity for each date
plt.figure(figsize=(12.33,4.5))
plt.title('Sentiment Sum Over Time')
plt.plot(polarity.index, polarity)
plt.show()

#Get and show the number of articles or count in the data set for each day
polarity_count = df.groupby(['Date']).count()['Polarity']
polarity_count

#Show the average sentiment for each day
polarity/polarity_count

#Plot the average sentiment over time
plt.figure(figsize=(12.33,4.5))
plt.title('Sentiment Average Over Time')
plt.plot(polarity.index, polarity/polarity_count)
plt.show()

#Show another way to plot the average sentiment over time
polarity_avg = df.groupby(['Date']).mean()['Polarity']
plt.figure(figsize=(12.33,4.5))
plt.title('Sentiment Average Over Time')
plt.plot(polarity_avg.index, polarity_avg)
plt.show()