# Description: This programs classifies images

#Import the libraries
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout
from tensorflow.keras import layers
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Load the data
from keras.datasets import cifar10
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

#Print the data type of x_train
print(type(x_train))
#Print the data type of y_train
print(type(y_train))
#Print the data type of x_test
print(type(x_test))
#Print the data type of y_test
print(type(y_test))

#Get the shape of x_train (number of images (32x32 with depth = 3(RGB)))
print('x_train shape:', x_train.shape)
#Get the shape of y_train
print('y_train shape:', y_train.shape)
#Get the shape of x_train
print('x_test shape:', x_test.shape)
#Get the shape of y_train
print('y_test shape:', y_test.shape)

#Take a look at the first image as an array
index = 0
x_train[index]

#Show the image as a picture
img = plt.imshow(x_train[index])

#Print the image label
print('The image label is: ', y_train[index])

#Get the image classification
classification = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
#Print the image class
print('The image class is: ', classification[y_train[index][0]])

#Convert the labels into a set of 10 numbers to input into the neural network
y_train_one_hot = to_categorical(y_train)
y_test_one_hot = to_categorical(y_test)

#Print the new labels
print(y_train_one_hot)

#Print the new label for the image/picture above
print('The one hot label is:', y_train_one_hot[0])

#Normalize the pixels to be values between 0 and 1
x_train = x_train / 255
x_test = x_test / 255

#Create  the models architecture
model = Sequential()

#Add the first layer which will be the convolution layer to extract features from the input image and create thirty two 5x5 ReLu convoluted features or feature maps
model.add(Conv2D(32, (5, 5), activation='relu', input_shape=(32,32,3)))

#Add apooling layer with a 2x2 pixel filter to get the max element from the feature maps
model.add(MaxPooling2D(pool_size=(2, 2)))

#Add another convolution layer and create sixty four 5x5 feature maps
model.add(Conv2D(64, (5, 5), activation='relu'))

#Add another pooling layer with a 2x2 pixel filter to get the max element from the feature maps
model.add(MaxPooling2D(pool_size=(2, 2)))

#Add a flattening layer to reduce the image dimensionality to a linear array
model.add(Flatten())

#Add 1000 neurons with the relu activation function 
model.add(Dense(1000, activation='relu'))

#Add a drop out layer with a 50% drop out rate to reduce overfitting 
model.add(Dropout(0.5))

#Add 500 neurons with the relu activation function 
model.add(Dense(500, activation='relu'))

#Add a drop out layer with a 50% drop out rate to reduce overfitting 
model.add(Dropout(0.5))

#Add 2500 neurons with the relu activation function 
model.add(Dense(250, activation='relu'))

#Add 10 neurons with the softmax activation function 
model.add(Dense(10, activation='softmax'))

#Compile the model
model.compile(loss='categorical_crossentropy', 
              optimizer='adam',
              metrics=['accuracy'])

# Train the model
hist = model.fit(x_train, y_train_one_hot, 
           batch_size=256, epochs=10, validation_split=0.2 )

#Evaluate the model using the test data set
model.evaluate(x_test, y_test_one_hot)[1]

#Visualize the models accuracy
plt.plot(hist.history['accuracy'])
plt.plot(hist.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper left')
plt.show()

#Visualize the models loss
plt.plot(hist.history['loss'])
plt.plot(hist.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Val'], loc='upper right')
plt.show()

#Test the model with an example
#Load the data
from google.colab import files # Use to load data on Google Colab
uploaded = files.upload() # Use to load data on Google Colab
new_image = plt.imread("cat.4015.jpg") #Read in the image (3, 14, 20)

#Show the image
img = plt.imshow(new_image)

#Transform the data to be a 32x32 pixel image with depth = 3
from skimage.transform import resize
resized_image = resize(new_image, (32,32,3))
img = plt.imshow(resized_image)

#Get the predictions
predictions = model.predict(np.array( [resized_image] ))
#Show the predictions
predictions

#Sort the predictions from least to greatest
list_index = [0,1,2,3,4,5,6,7,8,9]
x = predictions
for i in range(10):
  for j in range(10):
    if x[0][list_index[i]] > x[0][list_index[j]]:
      temp = list_index[i]
      list_index[i] = list_index[j]
      list_index[j] = temp
#Show the sorted labels in order from highest probability to lowest
print(list_index)

#Print the first 5 most likely classes
i=0
for i in range(5):
  print(classification[list_index[i]], ':', round(predictions[0][list_index[i]] * 100, 2), '%')

#Save the model
model.save('my_model.h5')

#To load the model 
from keras.models import load_model
model = load_model('my_model.h5')