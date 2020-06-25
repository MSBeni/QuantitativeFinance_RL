import pandas as pd
import os
import errno
import pandas_datareader.data as pdr
import datetime
import matplotlib.pyplot as plt


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
# close_prices.plot()

daily_return = close_prices.pct_change()   # equal to: (close_prices/close_prices.shift(1)) - 1
# print(daily_return)

Rolling_DailyReturn_mean = daily_return.rolling(window=20, min_periods=1).mean()  # Simple moving average
Rolling_DailyReturn_std = daily_return.rolling(window=20).std()

ewm_DailyReturn_mean = daily_return.ewm(span=20, min_periods=20).mean()  # exponential moving average
ewm_DailyReturn_std = daily_return.ewm(span=20, min_periods=20).std()

cp_standardized = (close_prices - close_prices.mean())/close_prices.std()
cp_standardized.plot()
cp_standardized.plot(subplots=True, layout=(3, 2), title="Stock price evolution", grid=True)
# plt.plot(cp_standardized)
plt.show()


# print(Rolling_DailyReturn_mean)
# print(Rolling_DailyReturn_std)
# print(ewm_DailyReturn_mean)
# print(ewm_DailyReturn_std)

# ensure_directory_exists('data')
# Rolling_daily_return.to_csv('./data/Rolling_daily_return.csv')
# Rolling_daily_return.to_json('./data/Rolling_daily_return.json')