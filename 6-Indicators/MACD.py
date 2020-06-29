import pandas_datareader.data as pdr
import datetime

ticker = 'MSFT'
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1025), datetime.date.today())

df = ohlcv.copy()
df["MA_Fast"] = df["Adj Close"].ewm(span=12, min_periods=12).mean()
df["MA_Slow"] = df["Adj Close"].ewm(span=26, min_periods=26).mean()
df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
df["Signal"] = df["MACD"].ewm(span=9, min_periods=9).mean()
print(df["Signal"])
