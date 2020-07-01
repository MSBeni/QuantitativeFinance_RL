import pandas_datareader.data as pdr
import datetime
import matplotlib.pyplot as plt
import os
import errno


def ensure_directory_exists(base_directory):
    """
    Makes a directory if it does not exist
    """
    try:
        os.makedirs(base_directory)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise ex


def macd(dataframe, a, b, c):
    """function to calculate MACD
       typical values a = 12; b =26, c =9"""
    _df = dataframe.copy()
    _df["MA_Fast"] = _df["Adj Close"].ewm(span=a, min_periods=a).mean()
    _df["MA_Slow"] = _df["Adj Close"].ewm(span=b, min_periods=b).mean()
    _df["MACD"] = _df["MA_Fast"]-_df["MA_Slow"]
    _df["Signal"] = _df["MACD"].ewm(span=c, min_periods=c).mean()
    _df.dropna(inplace=True)
    return _df
#
# ticker = 'MSFT'
# ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1025), datetime.date.today())


"""
Doing the same steps via calling the macd function:
    df = ohlcv.copy()
    df["MA_Fast"] = df["Adj Close"].ewm(span=12, min_periods=12).mean()
    df["MA_Slow"] = df["Adj Close"].ewm(span=26, min_periods=26).mean()
    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span=9, min_periods=9).mean()
"""
# df = macd(ohlcv, 12, 26, 9)
#
# ensure_directory_exists('data')
# df.to_csv("./data/MSFT-MACDData.csv")
#
# plt.plot(df.iloc[:, [5, 8, 9]])
# plt.show()
