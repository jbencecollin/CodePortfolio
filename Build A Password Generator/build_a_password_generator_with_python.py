
#Description: Generate a random password using python

#import the libraries
import string
import random

#Get information on what you need to generate the password 
while True:
  num_min_characters = int(input('Minimum number of characters:'))
  num_cap_letters = int(input('Number of capital letter(s):'))
  num_punctuations = int(input('Number of punctuation(s):'))
  num_digits = int(input('Number of digits:'))
  pass_len = int(input('How many characters for your password:'))

  #Check if the number of minimum characters is greater than or equal to the required characters 
  #  and check if the length of the password is greater than or equal to the minimum number of characters needed
  if num_min_characters >= num_cap_letters + num_punctuations + num_digits and (pass_len >= num_min_characters):
    break
  else:
    print('The number of minimum characters does not match the number of capital letters + number of punctuations + number of digits or possibly the length of the password string')
    print()

#Get 'n' random capitalized letters
caps = []
for i in range(0, num_cap_letters):
  caps.append(random.choice(string.ascii_letters).upper())

#Get 'm' random punctuations
puncts = []
for i in range(0, num_punctuations):
  puncts.append(random.choice(string.punctuation))

#Get 'k' random digits
digits = []
for i in range(0, num_digits):
    digits.append(random.choice(string.digits))

#Create and show a list of required characters within the password
password_requirements = caps + puncts + digits
password_requirements

#Get random characters/letters to fill the rest of the spots within the password
pass_len = pass_len - num_min_characters
password = []
for i in range(0, pass_len ):
  password.append(random.choice(string.ascii_letters))

#Append the random characters/letters to the required characters
for char in password_requirements:
  password.append(char)

#Show the current password
password

#randomly shuffle the characters in the password
random.shuffle(password)

#Show the newly generated password
password
