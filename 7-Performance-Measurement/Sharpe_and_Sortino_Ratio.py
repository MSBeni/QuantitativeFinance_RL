# Import necesary libraries
import pandas_datareader.data as pdr
import numpy as np
import datetime
from References.Performance_Measurements import cagr, volatility

# Download historical data for required stocks
ticker = "^GSPC"
SnP = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())


def sharpe(dataframe, risk_free_rate):
    df = dataframe.copy()
    Sharperate = (cagr(df) - risk_free_rate)/volatility(df)
    return Sharperate


def sortino(df, rf):
    """function to calculate sortino ratio ; rf is the risk free rate"""
    df = df.copy()
    df["daily_ret"] = df["Adj Close"].pct_change()
    neg_vol = df[df["daily_ret"] < 0]["daily_ret"].std() * np.sqrt(252)
    sr = (cagr(df) - rf)/neg_vol
    return sr


RFR = 0.022
print(sortino(SnP, RFR))
