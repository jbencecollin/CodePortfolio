'''
The cryptocurrency data dates are from '2019-12-08' to '2021-05-27'
(Crypto_Dashboard.py)

'''
# Description: A Cryptocurrency Dashboard Web Application

# Import the libraries
import streamlit as st
import pandas as pd
import datetime
import plotly.graph_objects as go
from PIL import Image  # Python Imaging library


# Add a title and an image
st.write("""
# Cryptocurrency Dashboard Application
Visually show data on crypto (BTC, DOGE, & ETH) from **'2019-12-08' to '2021-05-27'**
""")
image = Image.open("crypto_image3.png")  # Open the image
st.image(image, use_column_width=True)  # Display the image

# Create a sidebar header
st.sidebar.header('User Input')


# Create a function to get the users input
def get_input():
    start_date = st.sidebar.text_input("Start Date", '2020-01-01')
    end_date = st.sidebar.text_input("End Date", '2020-08-01')
    crypto_symbol = st.sidebar.text_input("Crypto Symbol", 'BTC')
    return start_date, end_date, crypto_symbol


# Create a function to get the cryptocurrency name correlating to the symbol
def get_crypto_name(symbol):
    symbol = symbol.upper()
    if symbol == 'BTC':
        return 'Bitcoin'
    elif symbol == 'ETH':
        return 'Ethereum'
    elif symbol == 'DOGE':
        return 'Dogecoin'
    else:
        return 'None'


# Create a function to get the proper data and the proper timeframe from the start date to the end date
def get_data(symbol, start, end):
    # Load the data
    symbol = symbol.upper()
    if symbol == 'BTC':  # if the symbol is BTC then load the BTC.csv data set
        df = pd.read_csv('BTC.csv')
    elif symbol == 'ETH':  # if the symbol is ETH then load the ETH.csv data set
        df = pd.read_csv('ETH.csv')
    elif symbol == 'DOGE':  # if the symbol is DOGE then load the DOGE.csv data set
        df = pd.read_csv('DOGE.csv')
    else:
        df = pd.DataFrame(columns=['Date', 'Close', 'Open', 'Volume', 'Adj Close'])

    # Get the date range
    # convert the start and end dates to datetime data types
    start = pd.to_datetime(start)  # Convert start to datetime
    end = pd.to_datetime(end)  # Convert end to datetime

    # Set the index to be the date
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    # return the dataframe within the users date range
    return df.loc[start:end]


# Get the users input
start, end, symbol = get_input()
# Get the data
df = get_data(symbol, start, end)
# Get the crypto name
crypto_name = get_crypto_name(symbol)

# Create a candle interactive stock chart figure!
fig = go.Figure(data=[go.Candlestick(x=df.index,
open=df['Open'],
high=df['High'],
low=df['Low'],
close=df['Close'],
increasing_line_color='green',
decreasing_line_color = 'red'
)])

# Display the data
st.header(crypto_name +' Data')
st.write(df)

# Get statistics on the data
st.header('Data Statistics')
st.write(df.describe())

# Display the Close Price
st.header(crypto_name + " Close Price\n")
st.line_chart(df['Close'])

# Display the Volume
st.header(crypto_name + " Volume\n ")
st.bar_chart(df['Volume'])

# Display the Candle Stick
st.header(crypto_name +' Candle Stick')
st.plotly_chart(fig)


# Run The Program in command prompt using a similar command structure:
# streamlit run "<Directory>/Crypto_Dashboard.py"

