
'''
Description: This is a python program to predict Telco customer churn
'''

#Import the library
import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


#Load the data set
from google.colab import files
uploaded = files.upload()

#Load the data into the data frame
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
df.head(7)

#Get the number of rows and columns in the data set
df.shape

#Show all of the column names
df.columns.values

#Check for na or missing data
df.isna().sum()

#Show statistics on the current data (Only SeniorCitizen, tenure, & MonthlyCharges are numeric values)
df.describe()

#Get customer churn counts
df['Churn'].value_counts()

#Visualize the count of customer churn
sns.countplot(df['Churn'])

#What percentage of customers are leaving ?

retained = df[df.Churn == 'No']
churned = df[df.Churn == 'Yes']
num_retained = retained.shape[0]
num_churned = churned.shape[0]

#Print the percentage of customers that stayed and left
print( num_retained / (num_retained + num_churned) * 100 , "% of customers stayed with the company.")

#Print the percentage of customers that stayed and left
print( num_churned / (num_retained + num_churned) * 100,"% of customers left the company.")

#Visualize the churn count for both Males and Females
sns.countplot(x='gender', hue='Churn',data = df)

#Visualize the churn count for the internet service
sns.countplot(x='InternetService', hue='Churn', data = df)

numerical_features = ['tenure', 'MonthlyCharges']
fig, ax = plt.subplots(1, 2, figsize=(28, 8))
df[df.Churn == 'No'][numerical_features].hist(bins=20, color="blue", alpha=0.5, ax=ax)
df[df.Churn == 'Yes'][numerical_features].hist(bins=20, color="orange", alpha=0.5, ax=ax)

#DATA PROCESSING & CLEANING

#Remove the unnecessary column customerID
cleaned_df = df = df.drop('customerID', axis=1)

#Look at the number of rows and cols in the new data set
cleaned_df.shape

#Convert all the non-numeric columns to numerical data types
for column in cleaned_df.columns:
        if cleaned_df[column].dtype == np.number:
            continue
        cleaned_df[column] = LabelEncoder().fit_transform(cleaned_df[column])

#Check the new data set data types
cleaned_df.dtypes

#Show the first 5 rows of the new data set
cleaned_df.head()

#Scale the cleaned data to be values between 0 and 1 inclusively

X = cleaned_df.drop('Churn', axis = 1) #Feature Data
y = cleaned_df['Churn'] #Target Data

# Standardizing/scaling the features
X = StandardScaler().fit_transform(X)

#Split the data into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#Create the model
model = LogisticRegression()
#Train the model
model.fit(x_train, y_train)

predictions = model.predict(x_test)
#printing the predictions
print(predictions)

#Check precision, recall, f1-score
print( classification_report(y_test, predictions) )
