from alpha_vantage.cryptocurrencies import CryptoCurrencies
import matplotlib.pyplot as plt
from pprint import pprint
import os
import errno
import pandas as pd

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
cc = CryptoCurrencies(key=open(key_path, 'r').read(), output_format='pandas')
data, meta_data = cc.get_digital_currency_daily(symbol='BTC', market='CNY')

temp = pd.DataFrame(data)
ensure_directory_exists('data')
file_name_json = './data/' + "BTC" + '.json'
file_name_csv = './data/' + "BTC" + '.csv'
temp.to_json(file_name_json)
temp.to_csv(file_name_csv)

data['4b. close (USD)'].plot()
plt.tight_layout()
plt.title('Daily close value for bitcoin (BTC)')
plt.grid()
plt.show()

