
#Description: This program determines if a stock is under or over valued

#Import the libraries
import pandas as pd
import numpy as np

#Load the data
from google.colab import files
files.upload()

#Store the data
df = pd.read_csv('Information Technology Stocks.csv')
#Set the tickers as the index
df = df.set_index('Tickers')
#Show the data
df

#Calculate & show the mean P/E Ratio
PE_Ratio_Mean = df.PE_Ratio.mean()
#Show the data
PE_Ratio_Mean

#Calculate and show the fiar market value
df['Fair_Market_Value'] = PE_Ratio_Mean * df['Earnings_Per_Share']
#Show the data
df

#Calculate and show a companies value ratio to determine if that company is over valued or under valued
df['Over_Under_Ratio'] = df['Current_Price'] / df['Fair_Market_Value']
#Show the data
df

#Create a new column to store and show a label of under valued and over valued stocks.
df['Value_Label'] = np.where(df['Over_Under_Ratio'] < 1.0, 'Under Valued', 'Fair or Over Valued')
#Show the data
df

#Show the percventage that the stock is over or under valued
df['Value_Percentage'] = abs(df['Over_Under_Ratio'] - 1)* 100
#Show the data
df

#Show only a list of stocks that are considered under valued
df[df.Value_Label == 'Under Valued'].index