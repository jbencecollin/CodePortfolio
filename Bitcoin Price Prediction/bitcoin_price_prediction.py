#Description: This program predicts the price of Bitcoin for the next 30 days

import numpy as np 
import pandas as pd

#Load the data
from google.colab import files # Use to load data on Google Colab
uploaded = files.upload() # Use to load data on Google Colab

#Store the data into the variable df
df = pd.read_csv('BitcoinPrice.csv')
df.head(7)

#Remove the Date column
df.drop(['Date'], 1, inplace=True)

#Show the first 7 rows of the new data set
df.head(7)

#A variable for predicting 'n' days out into the future
prediction_days = 30 #n = 30 days

#Create another column (the target or dependent variable) shifted 'n' units up
df['Prediction'] = df[['Price']].shift(-prediction_days)

#Show the first 7 rows of the new data set
df.head(7)

#Show the last 7 rows of the new data set
df.tail(7)

#CREATE THE INDEPENDENT DATA SET (X)

# Convert the dataframe to a numpy array and drop the prediction column
X = np.array(df.drop(['Prediction'],1))

#Remove the last 'n' rows where 'n' is the prediction_days
X= X[:len(df)-prediction_days]
print(X)

#CREATE THE DEPENDENT DATA SET (y)

# Convert the dataframe to a numpy array (All of the values including the NaN's)
y = np.array(df['Prediction'])

# Get all of the y values except the last 'n' rows
y = y[:-prediction_days]
print(y)

# Split the data into 80% training and 20% testing
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Set prediction_days_array equal to the last 30 rows of the original data set from the price column
prediction_days_array = np.array(df.drop(['Prediction'],1))[-prediction_days:]
print(prediction_days_array)

from sklearn.svm import SVR
# Create and train the Support Vector Machine (Regression) using the radial basis function
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.00001)
svr_rbf.fit(x_train, y_train)

# Testing Model: Score returns the accuracy of the prediction. 
# The best possible score is 1.0
svr_rbf_confidence = svr_rbf.score(x_test, y_test)
print("svr_rbf accuracy: ", svr_rbf_confidence)

# Print the predicted value
svm_prediction = svr_rbf.predict(x_test)
print(svm_prediction)

#Print the actual values
print(y_test)

# Print the model predictions for the next 'n' days
svm_prediction = svr_rbf.predict(prediction_days_array)
print(svm_prediction)

#Print the actual price for the next 'n' days, n=prediction_days=30 
df.tail(prediction_days)
