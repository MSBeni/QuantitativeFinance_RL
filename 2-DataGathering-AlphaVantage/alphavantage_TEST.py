from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from pprint import pprint

key_path = "/home/i-sip_iot/s_vv/AlphaVantage.txt"

ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')
data, meta_data = ts.get_intraday(symbol='MSFT', interval='1min', outputsize='full')
pprint(data.head(20))
print("\n")
print("meta_data: ", meta_data)
