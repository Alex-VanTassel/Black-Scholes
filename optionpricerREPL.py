'''
Implementation of the Black-Scholes equation to price options

The Black-Scholes equation is used to compute the price of an option given a variety of inputs. Namely:
    1) volitility 
    2) stock price 
    3) strike price 
    4) time to expirery 
    5) interest rate
'''

from yahooquery import Ticker
import sys
from helper import compute_Call

# Input Collection

ticker = input("Please enter the ticker symbol of the stock: ")
info = Ticker(ticker)
price = info.price[ticker]['regularMarketPrice'] # Queries the Yahoo Finance database for live stock price (assuming program is run during market hours)
print(f"\n The current price of {ticker} is ${price} \n")

try:    
    strike_price = float(input("Please enter a strike price for the option: "))
    volitility = float(input("Please enter the volitility of the option: "))
    expires = float(input("Please enter the number of months until the the option expires: "))
    expires = expires / 12 # To get the expiration in years
    interest_rate = float(input("Please enter the interest rate as a % (Don't include the '%' sign): "))
except:
    print("Value Error")
    sys.exit(1)

print(round(compute_Call(price, strike_price, expires, interest_rate, volitility), 2))

