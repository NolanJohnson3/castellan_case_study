## Nolan Johnson 
### Castellan Case Study 
#### 25 Nov 2024

import pandas as pd
import numpy as np
import yahooquery as yq

from scipy.stats import norm
### Black Scholes Formula

#S: current asset price
#K: strike price of the option
#T: expiration 
#r: risk free rate 
#sigma: volatility 

N = norm.cdf
def BS_CALL(S, K, T, r, sigma): 
    d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * N(d1) - K * np.exp(-r*T)* N(d2)

stock = "AAPL"
risk_free_rate = .045

from yahooquery import Ticker
aapl = Ticker('aapl')
# Get the options chain
options = aapl.option_chain
# Convert the calls to a DataFrame
options_df = options.reset_index()
# Create copy of DataFrame
calls_df = options_df[options_df['optionType'] == 'calls'].copy()
# Create mid_price column rounded to 3 decimal points (per given formula)
calls_df['mid_price'] = ((calls_df['bid'] + calls_df['ask']) / 2).round(3)
# Filter out mid_price where < 1
calls_df = calls_df[calls_df['mid_price'] > 1]

import datetime as dt
# Variable for today's date
today = dt.datetime.today()
# daysToExpiration column, formatting to days
calls_df['daysToExpiration'] = ((calls_df['expiration']) - today)
calls_df['daysToExpiration'] = calls_df['daysToExpiration'].dt.days

# Black Scholes Formula implementation using function above (rounded to 3 decimal points)
calls_df['black_scholes'] = BS_CALL(calls_df['lastPrice'], calls_df['strike'], calls_df['daysToExpiration'], risk_free_rate, calls_df['impliedVolatility']).round(3)
# difference_in_price calculated column (rounded to 3 decimal points)
calls_df['difference_in_price'] = (calls_df['mid_price'] - calls_df['black_scholes']).round(3)

# Drops 'unnecessary' columns
calls_df.drop(['currency', 'change', 'percentChange', 'volume', 'openInterest', 'contractSize', 'lastTradeDate', 'inTheMoney'], axis = 1, inplace = True)

# Reorders columns intuitively
calls_df = calls_df[['symbol', 'contractSymbol', 'expiration', 'daysToExpiration', 'strike', 'impliedVolatility', 'lastPrice', 'bid', 'ask', 'mid_price', 'black_scholes', 'difference_in_price']]
#calls_df

# Output csv file to current WD
calls_df.to_csv('out.csv', index = False)