'''
This is the base for the streamlit application I am developing to house the option price tracker
'''

from helper import compute_Call
import streamlit as st
from yahooquery import Ticker
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Option():
    def __init__(self, spot, strike, expires, volatility, interest_rate):
        self.spot = spot
        self.strike = strike
        self.expires = expires # Measured in years
        self.volatility = volatility
        self.interest_rate = interest_rate

    def compute_prices(self):
        self.call_price = round(compute_Call(self.spot, self.strike, self.expires, self.interest_rate, self.volatility), 2)
        self.put_price = round(compute_Call(self.spot, self.strike, self.expires, self.interest_rate, self.volatility, type="Put"), 2)
        return self.call_price, self.put_price

    


ticker = ''
strike = int
expires = float
volatility = float
interest_rate = float
stock_price = 0

# Helper Functions
def price_lookup():
    if ticker == '':
        return 0
    try:
        info = Ticker(ticker)
        stock_price = float(info.price[ticker]['regularMarketPrice']) # Queries the Yahoo Finance database for live stock price (assuming program is run during market hours)
    except:
        stock_price = 0
        return 0
    
    return stock_price



def generate_heatmap(vol_range, spot_range, option, buy_price = 0):
    # vol_range = volitility range for the array
    # spot_range = spot range for the array
    # Option is taken in to provide other necessary information for computations
    # Strike is brought in for computation purposes
    # Net is an optional argument indicating whether to simply return the arrays of prices
    #   Or the arrays of net profits/losses given a buy price for an option
    call_prices = np.zeros((10, 10))
    put_prices = np.zeros((10, 10))

    for i in range(len(vol_range)):
        for j in range(len(spot_range)):
            temp = Option(spot_range[j], option.strike, option.expires, vol_range[i], option.interest_rate)
            temp.compute_prices()
            call_prices[i, j] = temp.call_price
            put_prices[i, j] = temp.put_price
            if buy_price:
                call_prices[i, j] -= buy_price
                put_prices[i, j] -= buy_price

    
    # Generating the heatmaps
    if not buy_price:
        fig_call, ax_call = plt.subplots(figsize=(10, 8))
        sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_call)
        ax_call.set_title('CALL')
        ax_call.set_xlabel('Spot Price')
        ax_call.set_ylabel('Volatility')

        # Plotting Put Price Heatmap
        fig_put, ax_put = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="viridis", ax=ax_put)
        ax_put.set_title('PUT')
        ax_put.set_xlabel('Spot Price')
        ax_put.set_ylabel('Volatility')
    else:
        fig_call, ax_call = plt.subplots(figsize=(10, 8))
        sns.heatmap(call_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_call)
        ax_call.set_title('CALL')
        ax_call.set_xlabel('Spot Price')
        ax_call.set_ylabel('Volatility')

        # Plotting Put Price Heatmap
        fig_put, ax_put = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_prices, xticklabels=np.round(spot_range, 2), yticklabels=np.round(vol_range, 2), annot=True, fmt=".2f", cmap="RdYlGn", ax=ax_put)
        ax_put.set_title('PUT')
        ax_put.set_xlabel('Spot Price')
        ax_put.set_ylabel('Volatility')

    return fig_call, fig_put





# Side bar for parameter inputs
with st.sidebar:
    st.title("Parameter Inputs")
    ticker = st.text_input("Stock Ticker")
    stock_price = float(price_lookup())
    st.metric(f"{ticker} Price", stock_price)

    strike = st.number_input("Strike Price", value = 100.0)
    expires = st.number_input("Enter the number of months until expirey", value=4) / 12.0
    volatility = float(st.slider("Volatility", min_value=0.0, max_value=1.0, step=.01, value=.3))
    interest_rate = st.slider("Risk Feee Interest rate", min_value=0.0, max_value=.1, step=.001, value=.035)
    st.divider()
    st.button("Heatmap Parameters")
    
    spot_max = st.number_input("Max Stock Price for Heatmap", value=stock_price + 20)
    spot_min = st.number_input("Min Stock Price for Heatmap", value=stock_price - 20)
    vol_max = st.number_input("Max Volatility for Heamap", 0.7)
    vol_min = st.number_input("Min Volatility for Heatmap", 0.3)
    purchase_price = st.number_input("Buy price of option")

    vol_range = np.linspace(vol_min, vol_max, 10)
    spot_range = np.linspace(spot_min, spot_max, 10)

st.title("Black-Scholes Options Pricing Model")
st.divider()


col1, col2 = st.columns(2)

with col1:
    if price_lookup() != 0:
        st.metric("Call Price", round(compute_Call(float(price_lookup()), strike, expires, interest_rate, float(volatility)), 2), delta_color="normal")

with col2:
    if price_lookup() != 0:
        st.metric("Put Price", round(compute_Call(float(price_lookup()), strike, expires, interest_rate, float(volatility), type="put"), 2), delta_color="inverse")

st.divider()
st.title("Call and Put Heatmap")
st.info("Observe how volatility and spot price can change the price of an option")

if stock_price:
    option = Option(stock_price, strike, expires, volatility, interest_rate)

    call_heatmap, put_heatmap = generate_heatmap(vol_range, spot_range, option)


    col1, col2 = st.columns(2)
    with col1: 
        st.subheader("Call Heatmap")
        st.pyplot(call_heatmap)

    with col2:
        st.subheader("Put Heatmap")
        st.pyplot(put_heatmap)

if purchase_price:
    st.title("Profit and Loss Heatmaps")
    st.info("Given a purchase price for an option, observe the profitability of each of the puts and calls in the above heatmaps")
    call_pl_heatmap, put_pl_heatmap = generate_heatmap(vol_range, spot_range, option, buy_price = purchase_price)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Call P&L Heatmap")
        st.pyplot(call_pl_heatmap)

    with col2:
        st.subheader("Put P&L Heatmap")
        st.pyplot(put_pl_heatmap)