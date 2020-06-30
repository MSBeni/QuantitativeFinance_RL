import pandas_datareader.data as pdr
import datetime

# Download historical data for required stocks
ticker = "MSFT"
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())


def atr(dataframe, n):
    """function to calculate True Range and Average True Range"""
    df = dataframe.copy()
    df['H-L'] = abs(df['High']-df['Low'])
    df['H-PC'] = abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low']-df['Adj Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    # df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2


print(atr(ohlcv, 20))

