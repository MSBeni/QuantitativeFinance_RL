import pandas_datareader.data as pdr
import datetime

# Download historical data for required stocks
ticker = "MSFT"
ohlc = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())
