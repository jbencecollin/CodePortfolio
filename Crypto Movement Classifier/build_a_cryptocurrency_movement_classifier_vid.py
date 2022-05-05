'''
Build A Crypto Movement Classifier Using Machine Learning
'''

#Import the libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

#Load the data
from google.colab import files
files.upload()

#Read in the file
df = pd.read_csv('BTC_Data.csv')

#Show the data
df

#Create the Exponential Moving Average Indicator
#This gives more importance to recent price data
def EMA(data, period=20, column='Close'):
  return data[column].ewm(span=period, adjust=False).mean()

#Create a function to calculate the Relative Strength Index (RSI)
#This measure how quickly people are bidding the price of Bitcoin up or down
def RSI(data, period = 14, column = 'Close'):
  delta = data[column].diff(1) #Use diff() function to find the discrete difference over the column axis with period value equal to 1
  delta = delta.dropna() # or delta[1:]
  up =  delta.copy() #Make a copy of this object’s indices and data
  down = delta.copy() #Make a copy of this object’s indices and data
  up[up < 0] = 0 
  down[down > 0] = 0 
  data['up'] = up
  data['down'] = down
  AVG_Gain = EMA(data, period, column='up')#up.rolling(window=period).mean()
  AVG_Loss = abs(EMA(data, period, column='down'))#abs(down.rolling(window=period).mean())
  RS = AVG_Gain / AVG_Loss
  RSI = 100.0 - (100.0/ (1.0 + RS))
  
  data['RSI'+str(period)] = RSI
  return data

#Add the indicators to the data set
#Creating the data set 
RSI(df, 7)
RSI(df, 14)
RSI(df, 20)
df['EMA15'] = EMA(df, 15)
df['EMA20'] = EMA(df, 20)
df['EMA50'] = EMA(df, 50)
#Show the data
df

#Create the target column to determine if tomorrows price will be greater than todays price represented by 1 or less than todays price represented by 0
df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0) # if tomorrows price is greater than todays price put 1 else put 0

#Show the data
df

#Remove the first 1 row of data
df = df[1:]
#Show the data set
df

#Split the data set into a feature or independent data set (X) and a target or dependent data set (Y)
#Get a list of columns to keep
keep_columns = df.drop(['Date','High',	'Low',	'Open',	'Volume',	'Adj Close','Close', 'up', 'down','Target'], axis=1).columns#['Close', 'MACD', 'Signal_Line', 'RSI', 'SMA', 'EMA']
X = df[keep_columns].values
Y = df['Target'].values

#Split the data again but this time into 80% training and 20% testing data sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2)

#Create the random forest classifier model
from sklearn.ensemble import RandomForestClassifier
forest = RandomForestClassifier(n_estimators = 132, criterion = 'entropy', random_state = 34)
forest.fit(X_train, Y_train)

#See how well the model did on the test data by getting the score
forest.score(X_test, Y_test)

#Show the models predictions
forest_prediction = forest.predict(X_test)
print(forest_prediction)

#Show the actual values from the test data set
Y_test