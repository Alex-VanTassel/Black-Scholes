"""
Implementation of the Black-Scholes equation to price options

The Black-Scholes equation is used to compute the price of an option given a variety of inputs. Namely:
    1) volitility 
    2) stock price 
    3) strike price 
    4) time to expirery 
    5) interest rate
"""

# Importing necessary libraries
import numpy as np
from scipy.stats import norm

# function to compute option price based on aforementioned parameters
def compute_Call(S, K, T, r, sigma, type = "call"):
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r*T)* norm.cdf(d2)
    else:
        return K*np.exp(-r*T)*norm.cdf(-d2) - S*norm.cdf(-d1)