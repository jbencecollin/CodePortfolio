
import plotly.graph_objects as go
import pandas as pd

#Load the data 
from google.colab import files # Use to load data on Google Colab 
uploaded = files.upload() # Use to load data on Google Colab

#Store the data into the df variable
df = pd.read_csv('AMZN.csv')
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
df

fig = go.Figure(data=[go.Candlestick(x=df.index,
open=df['Open Price'],
high=df['High Price'],
low=df['Low Price'],
close=df['Close Price'],
increasing_line_color='green',
decreasing_line_color = 'red'
)])
fig.show()