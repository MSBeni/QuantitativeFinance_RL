# Import necesary libraries
import pandas as pd
import pandas_datareader.data as pdr
import numpy as np
import datetime

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = pdr.get_data_yahoo(ticker,datetime.date.today()-datetime.timedelta(364),datetime.date.today())


def rsi(dataframe, n):
    """function to calculate RSI"""
    df = dataframe.copy()
    df['delta'] = df['Adj Close'] - df['Adj Close'].shift(1)
    df['gain'] = np.where(df['delta'] >= 0, df['delta'], 0)
    df['loss'] = np.where(df['delta'] < 0, abs(df['delta']), 0)
    avg_gain = []
    avg_loss = []
    gain = df['gain'].tolist()
    loss = df['loss'].tolist()
    for i in range(len(df)):
        if i < n:
            avg_gain.append(np.NaN)
            avg_loss.append(np.NaN)
        elif i == n:
            avg_gain.append(df['gain'].rolling(n).mean().tolist()[n])
            avg_loss.append(df['loss'].rolling(n).mean().tolist()[n])
        elif i > n:
            avg_gain.append(((n-1)*avg_gain[i-1] + gain[i])/n)
            avg_loss.append(((n-1)*avg_loss[i-1] + loss[i])/n)
    df['avg_gain'] = np.array(avg_gain)
    df['avg_loss'] = np.array(avg_loss)
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    return df['RSI']


# Calculating RSI without using loop
def rsi_noloop(df, n):
    """function to calculate RSI"""
    delta = df["Adj Close"].diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[n-1]] = np.mean(u[:n])  # first value is sum of avg gains
    u = u.drop(u.index[:(n-1)])
    d[d.index[n-1]] = np.mean(d[:n])  # first value is sum of avg losses
    d = d.drop(d.index[:(n-1)])
    rs = pd.stats.moments.ewma(u, com=n-1, adjust=False) / pd.stats.moments.ewma(d, com=n-1, adjust=False)
    return 100 - 100 / (1 + rs)


print(rsi(ohlcv, 12))
