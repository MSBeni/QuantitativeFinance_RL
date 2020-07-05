# Import necesary libraries
import pandas_datareader.data as pdr
import numpy as np

# Download historical data for required stocks
# ticker = "^GSPC"
# SnP = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())
# SnP["Adj Close"].plot()


def caqr(df):
    DataFrame = df.copy()
    DataFrame["daily return"] = DataFrame["Adj Close"].pct_change()
    DataFrame["Cumulative Return"] = (1 + DataFrame["daily return"]).cumprod()
    n = len(DataFrame)/252   # 252 is the number of total working days in a year
    CAQR = (DataFrame["Cumulative Return"][-1])**(1/n) - 1
    return CAQR


def volatility(dataframe):
    DF = dataframe.copy()
    DF["daily return"] = DF["Adj Close"].pct_change()
    vol = DF["daily return"].std() * np.sqrt(252)
    return vol

