import numpy as np
from alpha_vantage.timeseries import TimeSeries
import copy
import talib

talib.get_function_groups()  # get a list of talib functions by group

tickers = ["MSFT", "AAPL", "FB", "AMZN", "INTC", "CSCO", "VZ", "IBM", "QCOM", "LYFT"]

# Extract OHLCV data for the tickers
ohlc_tech = {}  # directory with ohlc value for each stock
key_path = "/home/i-sip_iot/s_vv/AlphaVantage.txt"
ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')

attempt = 0  # initializing passthrough variable
drop = []  # initializing list to store tickers whose close price was successfully extracted
while len(tickers) != 0 and attempt <= 100:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)):
        try:
            ohlc_tech[tickers[i]] = ts.get_daily(symbol=tickers[i], outputsize='full')[0]
            ohlc_tech[tickers[i]].columns = ["Open", "High", "Low", "Adj Close", "Volume"]
            drop.append(tickers[i])
        except:
            print(tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1

print(ohlc_tech)
