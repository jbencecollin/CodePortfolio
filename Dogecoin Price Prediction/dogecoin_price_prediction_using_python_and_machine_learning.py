

#Description: This program attempts to predict the future price of Dogecoin

#Import the libraries
import numpy as np 
import pandas as pd

#Load the data
from google.colab import files # Use to load data on Google Colab
uploaded = files.upload() # Use to load data on Google Colab

#Store the data 
df = pd.read_csv('Doge.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

#Get the close price
df = df[['Close']]
#Show the data
df

#Create a variable to store the number of days into the future that we want to predict
prediction_days = 1 #n = 1 day(s)

#Create a new column called Prediction (the target or dependent variable) shifted 'n' units up
df['Prediction'] = df[['Close']].shift(-prediction_days)
#Show the data set
df

#CREATE THE INDEPENDENT DATA SET (X)
# Convert the dataframe to a numpy array and drop the prediction column
X = np.array(df.drop(['Prediction'],1))
#Remove the last 'n+1' rows where 'n' is the prediction_days
X= X[:len(df)-prediction_days-1]
#Show the data
print(X)

#CREATE THE DEPENDENT DATA SET (y) 
# Convert the dataframe to a numpy array (All of the values including the NaN's) 
y = np.array(df['Prediction'])  
# Get all of the y values except the last 'n+1' row(s) 
y = y[:-prediction_days-1] 
print(y)

# Split the data into 80% training and 20% testing
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Use RandomForestRegressor for the model
from sklearn.ensemble import RandomForestRegressor
forest = RandomForestRegressor(n_estimators = 2, random_state = 587)
forest.fit(x_train, y_train)
print(forest.score(x_test, y_test)) #Print the score (aka  the coefficient of determination R^2 of the prediction.) of the test data

#Show how close the predicted and actual test values are
#Create a variable to store the predicted test values
prediction = forest.predict(x_test)
# Print the predicted test value(s)
print(prediction)
#print a new line
print() 
#Print the actual values
print(y_test)

#Get the validation data for the model
#Create a variable to store all of the rows in the data set except the last 'n' rows where n is prediction days
temp_df = df[:-prediction_days]
# Create a variable to store the independent price value that will be used when making future predictions (Note this data has not been seen by the model before)
x_val = temp_df.tail(1)['Close'][0]
#Show the data
print(x_val)

#Use x_val (data that the model hasn't seen before) to validate the models prediction 
#Create a variable to Store the predicted value
prediction = forest.predict([[x_val]])
#Print the price of Dogecoin for the next 'n' days
print('The price of Dogecoin in', prediction_days, 'day(s) is predicted to be',prediction)
#Print the actual price for the next 'n' days, n=prediction_days=1 
print('The actual price was', temp_df.tail(1)['Prediction'][0])

