import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import copy


def ATR(DF, n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    # df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2['ATR']


def cagr(dataframe):
    """function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
    df = dataframe.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df) / (252 * 78)
    CAGR = (df["cum_return"].tolist()[-1]) ** (1 / n) - 1
    return CAGR


def volatility(dataframe):
    """function to calculate annualized volatility of a trading strategy"""
    df = dataframe.copy()
    vol = df["ret"].std() * np.sqrt(252 * 78)
    return vol


def sharpe(dataframe, rf):
    """function to calculate sharpe ratio ; rf is the risk free rate"""
    df = dataframe.copy()
    sr = (cagr(df) - rf) / volatility(df)
    return sr


def max_dd(dataframe):
    """function to calculate max drawdown"""
    df = dataframe.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd


# Download historical data (monthly) for selected stocks

tickers = ["MSFT", "AAPL", "FB", "AMZN", "INTC", "CSCO", "VZ", "IBM", "QCOM", "LYFT"]

ohlc_intraday = {}  # directory with ohlc value for each stock
key_path = "/home/i-sip_iot/s_vv/AlphaVantage.txt"
ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')


