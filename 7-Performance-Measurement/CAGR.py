# Import necesary libraries
import pandas_datareader.data as pdr
# import numpy as np
import datetime
import matplotlib.pyplot as plt

# Download historical data for required stocks
ticker = "^GSPC"
SnP = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())
# SnP["Adj Close"].plot()


def caqr(dataframe):
    DF = dataframe.copy()
    DF["daily return"] = DF["Adj Close"].pct_change()
    DF["Cumulative Return"] = (1 + DF["daily return"]).cumprod()
    n = len(DF)/252   # 252 is the number of total working days in a year
    CAQR = (DF["Cumulative Return"][-1])**(1/n) - 1
    return CAQR


print(caqr(SnP))
plt.show()

