#This program uses the Machine Learning Algorithm called a Decision Tree to classify a car 


# Import the dependencies / libraries
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

#Create a dataframe from the cars dataset / csv file
df = pd.read_csv('car_integer_exceptY.csv')

#print the first 5 rows of the data set
print(df.head())

# Split your data into the independent variable(s) and dependent variable
X_train = df.loc[:,'buying':'safety'] #Gets all the rows in the dataset from column 'buying' to column 'safety'
Y_train = df.loc[:,'values'] #Gets all of the rows in the dataset from column 'values'

# The actual decision tree classifier
tree = DecisionTreeClassifier(max_leaf_nodes=3, random_state=0)

# Train the model
tree.fit(X_train, Y_train)

# Make your prediction
# input:buying=v-high, main=high, doors=2, persons=2, lug_boot=med, safety=3
# integer conversion of input: 4,3,2,2,2,3
prediction = tree.predict([[4,3,2,2,2,3]])

#Print the prediction
print('Printing the prediction: ')
print(prediction)
