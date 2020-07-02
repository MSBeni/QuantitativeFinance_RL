# Import necesary libraries
import pandas_datareader.data as pdr
import datetime
from stocktrends import Renko
from References.ATR_BollingerBand import atr

# Download historical data for required stocks
ticker = "AAPL"
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(364), datetime.date.today())


def renko_df(dataframe):
    """function to convert ohlc data into renko bricks"""
    df_ = dataframe.copy()
    df_.reset_index(inplace=True)
    df_ = df_.iloc[:, [0, 1, 2, 3, 5, 6]]
    df_.rename(columns={"Date": "date", "High": "high", "Low": "low", "Open": "open", "Adj Close": "close",
                        "Volume": "volume"}, inplace=True)
    df2 = Renko(df_)
    df2.brick_size = round(atr(dataframe, 120)["ATR"][-1], 0)
    # renko_df = df2.get_bricks() # if get_bricks() does not work try using get_ohlc_data() instead
    RENKO_df = df2.get_ohlc_data()
    return RENKO_df


