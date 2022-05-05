
#Import the libraries
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

#Load the data set
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

#View a training image
img_index = 2 # <<<<<  You can update this value to look at other images
img = train_images[img_index]
print("Image Label: " + str(train_labels[img_index]))
plt.imshow(img)

#Print the shape 
print(train_images.shape)# 60,000 rows of 28 x 28 pixel images
print(test_images.shape) # 10,000 rows of 28 x 28 pixel images

#Create the neural network model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28,28)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(10, activation=tf.nn.softmax)
])

#Compile the model
model.compile(optimizer=tf.train.AdamOptimizer(), loss='sparse_categorical_crossentropy', metrics = ['accuracy'])

#Train the model
model.fit(train_images, train_labels, epochs=5, batch_size=32)

#Evaluate the model
model.evaluate(test_images, test_labels)

#Make a prediction
predictions = model.predict(test_images[:5])
#Print the predicted labels
print(np.argmax(predictions, axis=1))
#Print the actual labels
print(test_labels[:5])

for i in range(0,5):
  first_image = test_images[i]
  first_image = np.array(first_image, dtype='float')
  pixels = first_image.reshape((28, 28))
  plt.imshow(pixels, cmap='gray')
  plt.show()

test_labels[:5]