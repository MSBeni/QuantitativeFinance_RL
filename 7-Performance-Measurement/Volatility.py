# Import necesary libraries
import pandas_datareader.data as pdr
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Download historical data for required stocks
ticker = "^GSPC"
SnP = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())
# SnP["Adj Close"].plot()


def volatility(dataframe):
    DF = dataframe.copy()
    DF["daily return"] = DF["Adj Close"].pct_change()
    vol = DF["daily return"].std() * np.sqrt(252)
    return vol


print(volatility(SnP))


