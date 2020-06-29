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


ticker = 'MSFT'
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1025), datetime.date.today())

df = ohlcv.copy()
df["MA_Fast"] = df["Adj Close"].ewm(span=12, min_periods=12).mean()
df["MA_Slow"] = df["Adj Close"].ewm(span=26, min_periods=26).mean()
df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
df["Signal"] = df["MACD"].ewm(span=9, min_periods=9).mean()
ensure_directory_exists('data')
df.to_csv("./data/MSFT-MACDData.csv")
# df.dropna(inplace=True)
# print(df["Signal"])
print(df)
plt.plot(df.iloc[:, [5, 8, 9]])
plt.show()
