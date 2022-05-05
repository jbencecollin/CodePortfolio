"""
Original file is located at
    https://colab.research.google.com/drive/1RCCs60iv_FzLpC_gizs0wkRuVFcOWi_K
"""

#Description: This program shows how much you can make on BlockFi by consistently investing

#Import the libraries
import math 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

#Create a variable for your monthly deposits
monthly_saving = 200 # $200 USD
#Create a variable to store the interest rate
rate = 0.086 # 8.6% APY
#Create a variable to store the time or number of time periods elapsed
time = 1/12
#Create a variable to store the number of times the interest is applied per time period
num_compounded = 12
#Create a variable to store the number of months invested
num_months_saving = 240 # 12 months * 20 years = 240

#Create a function to mimic the compound formula 
def compound_interest(P, r, t, n):
  #Create the formula
  # A = P(1+r/n)^(tn)
  A = P * pow( (1+r/n), (t*n) )
  return A

#Create a function for the strategy
def investment_strategy():
  #Create empty lists to store the values
  compound_list = []
  monthly_deposit_list = []

  #Add the intital deposit or the 1st month savings to the lists
  compound_list.append(monthly_saving)
  monthly_deposit_list.append(monthly_saving)

  #Loop through the number of months - 1 
  for i in range(1, num_months_saving):
    Amount = compound_interest( compound_list[i-1], rate, time, num_compounded)
    compound_list.append( Amount + monthly_saving)
    monthly_deposit_list.append(monthly_saving)

  return (compound_list, monthly_deposit_list)

#Get and store the compound list
compound_list = investment_strategy()[0]
compound_list

#Show the total return on my investment
total_return = compound_list[num_months_saving - 1]
total_return

#Get the list of monthly deposits
monthly_deposit_list = investment_strategy()[1]

#Get the total deposit amount 
total_deposit = len(monthly_deposit_list) * monthly_saving
total_deposit

#Visually show the investments
plt.plot(compound_list, label='Comp')
plt.plot(monthly_deposit_list, label='Cash')
plt.title('Amount Gained Over Time')
plt.ylabel('USD Price')
plt.xlabel('Months')
plt.legend(loc='upper left')
plt.show()