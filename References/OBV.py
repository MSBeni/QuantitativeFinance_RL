# Import necesary libraries
import pandas_datareader.data as pdr
import numpy as np
import datetime

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(364), datetime.date.today())

def obv(df):
    """function to calculate On Balance Volume"""
    df = df.copy()
    df['daily_ret'] = df['Adj Close'].pct_change()  # Calculate pct_change of each value to previous entry in group.
    df['direction'] = np.where(df['daily_ret'] >= 0, 1, -1)
    df['direction'][0] = 0
    df['vol_adj'] = df['Volume'] * df['direction']
    df['obv'] = df['vol_adj'].cumsum()
    return df['obv']


# print(obv(ohlcv))
