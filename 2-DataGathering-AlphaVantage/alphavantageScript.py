from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os
import errno
from alpha_vantage.timeseries import TimeSeries


def ensure_directory_exists(base_directory):
    """
    Makes a directory if it does not exist
    """
    try:
        os.makedirs(base_directory)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise ex


key_path = "/home/i-sip_iot/s_vv/AlphaVantage.txt"
ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')

all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN"]
# all_tickers = ["PCLN"]

data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')[0]
data.columns = ["open", "high", "low", "close", "volume"]

# extracting stock data for the stocks identified in all tickers
for ticker in all_tickers:
    try:
        ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')
        data = ts.get_intraday(symbol=ticker, interval='1min', outputsize='full')[0]
        data.columns = ["open", "high", "low", "close", "volume"]
        temp = pd.DataFrame(data)
        ensure_directory_exists('data')
        file_name_json = './data/' + ticker + '.json'
        file_name_csv = './data/' + ticker + '.csv'
        temp.to_json(file_name_json)
        temp.to_csv(file_name_csv)
    except:
        print(ticker, " :failed to fetch data...retrying")
        continue


