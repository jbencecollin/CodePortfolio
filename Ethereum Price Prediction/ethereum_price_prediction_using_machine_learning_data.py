
#Description: Predict the price of Ethereum

#Import the dependencies
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

#Load the data
from google.colab import files # Use to load data on Google Colab
files.upload() # Use to load data on Google Colab

#Get and show the data
#Store the data
df = pd.read_csv('ETH.csv')
#Set the date as the index
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#Show the data
df

#Create a variable for predicting 'n' days out into the future
projection = 14 #'n=14' days
#Create another column (the target ) shifted 'n' units up
df['Prediction'] = df[['Close']].shift(-projection)
#print the new data set
print(df.tail())

### Create the independent data set (X)  #######
# Convert the dataframe to a numpy array
X = np.array(df[['Close']]) #np.array(df.drop(['Prediction'],1))
#Remove the last '14' rows
X = X[:-projection]
print(X)

### Create the dependent data set (y)  #####
# Convert the dataframe to an array 
y = df['Prediction'].values #np.array(df['Prediction'])
# Get all of the y values except the last '14' rows
y = y[:-projection]
print(y)

# Split the data into 85% training and 15% testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.15)

# Create and train the Linear Regression  Model
linReg = LinearRegression()
# Train the model
linReg.fit(x_train, y_train)

# Test the model using score which returns the coefficient of determination R^2 of the prediction. 
#R^2 coefficient of determination is a statistical measure of how well the regression predictions approximate the real data points. 
#An R2 of 1 indicates that the regression predictions perfectly fit the data.
#So, the best possible score is 1.0
linReg_confidence = linReg.score(x_test, y_test)
print("Linear Regression Confidence: ", linReg_confidence)

# Set x_projection equal to the last 14 rows of the original data set from the Close column
x_projection = np.array(df[['Close']])[-projection:] #np.array(df.drop(['Prediction'],1))[-projection:]
print(x_projection)

# Print the linear regression model predictions for the next '14' days
linReg_prediction = linReg.predict(x_projection)
print(linReg_prediction)
