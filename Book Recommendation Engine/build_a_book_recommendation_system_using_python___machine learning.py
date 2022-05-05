#Description: Build a book recommendation engine (more specifically a content based recommendation engine)

#Import the libraries
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

#Load the data 
from google.colab import files
files.upload()

#Store the data
df = pd.read_csv('books.csv',encoding= 'unicode_escape', error_bad_lines=False)

#Show the first 4 rows of data
df.head(4)

#Create a list of columns to keep that are important
columns = ['title', 'authors', 'publisher']

#Check for Null values
df[columns].isnull().values.any()

#Create a function to combine the important columns/features
def combine_features(data):
  features = []
  for i in range(0, data.shape[0]):
    features.append(data['title'][i]+ ' '+data['authors'][i]+ ' '+data['publisher'][i] )

  return features

#Create a new column with the combined features
df['combined_features'] = combine_features(df)

#Show the new column
df.head(4)

#Convert the text from the new column to a matrix/vector of word counts, and store it into a variable called cm
cm = CountVectorizer().fit_transform(df['combined_features'])

#Get the cosine similarity matrix from the count matrix 
# This will give us a nxn matrix of similarity scores for each book (row of data) to every other book in the data set (the columns) including itself.
cs = cosine_similarity(cm)
#Print the similarity score
print(cs)

#Get the title of the book the reader likes
Title = df['title'][1] #Harry Potter and the Order of the Phoenix (Harry Potter  #5)'

#Find the row id / book id of the book the user likes and store it into a variable.
book_id = df[df.title == Title]['book_id'].values[0]

#Create a list of tuples in the form (book_id, similarity score)
scores = list(enumerate(cs[book_id]))
print(scores)

#Sort the list of similar books according to the similarity scores in descending order.
sorted_scores= sorted(scores,key=lambda x:x[1],reverse=True)
#Since the most similar book is itself, we will discard the first element after sorting.
sorted_scores = sorted_scores[1:]

print(sorted_scores)

#Create a loop to print the first 7 books from the sorted similar books list
j=0
print('The 7 most recommended books to', Title, 'are:\n')
for item in sorted_scores:
  book_title = df[df.book_id == item[0]]['title'].values[0]
  print(j+1,book_title)
  j = j+1
  if j > 6:
    break
