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
