
#Parkinson's disease is a progressive nervous system disorder that affects movement. 
#Symptoms start gradually, sometimes starting with a barely noticeable tremor in just one hand. 
#Tremors are common, but the disorder also commonly causes stiffness or slowing of movement. 
#-https://www.mayoclinic.org/diseases-conditions/parkinsons-disease/symptoms-causes/syc-20376055

#This program detects if an individual has of Parkinson’s disease.

#Get the dependencies
import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.preprocessing import  MinMaxScaler
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import seaborn as sns

# Load the data 
from google.colab import files
uploaded = files.upload()

#Load the data
df=pd.read_csv('parkinsons.data')
df.head()

#Check for any missing data
df.isnull().values.any()

#Get the count of the number of rows and cols
df.shape

#Get Target counts
df['status'].value_counts()

print('If I guess the individual did not have Parkinson’s disease, I would be correct',48/(147+48)*100,'% of the time.')
print('If I guess the individual had Parkinson’s disease, I would be correct',147/(147+48) *100, '% of the time.')

#Visualize this count
sns.countplot(df['status'],label="Count")

#Get the data types in the data set
df.dtypes

#Create the feature data set
X = df.drop(['name'],1)
X = np.array(X.drop(['status'],1))

#Create the target data set
y = np.array(df['status'])

# Split the data into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#Transform features by scaling each feature to a given range.
sc = MinMaxScaler(feature_range=(0,1))
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)

#Create the XGBClassifier model
# XGBoost stands for eXtreme Gradient Boosting and is based on decision trees. 
# XGBoost is a new Machine Learning algorithm designed with speed and performance in mind.
model = XGBClassifier().fit(x_train, y_train)

#Get the models predictions/classifications and print them
predictions = model.predict(x_test)
predictions

#Get the models accuracy, precision, recall, and f1-score
print( classification_report(y_test, predictions) )
