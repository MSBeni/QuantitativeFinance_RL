import pandas as pd
import os
import errno
import pandas_datareader.data as pdr
import datetime


def ensure_directory_exists(base_directory):
    """
    Makes a directory if it does not exist
    """
    try:
        os.makedirs(base_directory)
    except OSError as ex:
        if ex.errno != errno.EEXIST:
            raise ex


tickers = ["MSFT", "AMZN", "AAPL", "CSCO", "IBM", "FB"]

close_prices = pd.DataFrame()
attempt = 0
drop = []
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if j not in drop]
    for i in range(len(tickers)):
        try:
            temp = pdr.get_data_yahoo(tickers[i], datetime.date.today()-datetime.timedelta(3650), datetime.date.today())
            temp.dropna(inplace=True)
            close_prices[tickers[i]] = temp['Adj Close']
            drop.append(tickers[i])

        except:
            print(tickers[i], ":Failed to fetch the data ... try again!!!")
            continue

close_prices.fillna(method='bfill', axis=0, inplace=True)

daily_return = close_prices.pct_change()   # equal to: (close_prices/close_prices.shift(1)) - 1
# print(daily_return)
ensure_directory_exists('data')
daily_return.to_csv('./data/daily_return.csv')
daily_return.to_json('./data/daily_return.json')
print(daily_return.mean())
print(daily_return.median())
print(daily_return.std())
