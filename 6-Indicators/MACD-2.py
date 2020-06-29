# Import necesary libraries
import pandas_datareader.data as pdr
import datetime
import matplotlib.pyplot as plt
from References.MACD import macd

# Download historical data for required stocks
ticker = "MSFT"
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today()-datetime.timedelta(1825), datetime.date.today())


# Visualization - plotting MACD/signal along with close price and volume for last 100 data points
df = macd(ohlcv, 12, 26, 9)

plt.subplot(311)
plt.plot(df.iloc[-100:, 4])
plt.title('MSFT Stock Price')
plt.xticks([])

plt.subplot(312)
plt.bar(df.iloc[-100:, 5].index, df.iloc[-100:, 5].values)
plt.title('Volume')
plt.xticks([])

plt.subplot(313)
plt.plot(df.iloc[-100:, [-2, -1]])
plt.title('MACD')
plt.legend(('MACD', 'Signal'), loc='lower right')

plt.show()


# Visualization - Using object orient approach
# Get the figure and the axes
fig, (ax0, ax1) = plt.subplots(nrows=2, ncols=1, figsize=(10, 6), gridspec_kw={'height_ratios': [2.5, 1]})
df.iloc[-100:, 4].plot(ax=ax0)
ax0.set(ylabel='Adj Close')

df.iloc[-100:, [-2, -1]].plot(ax=ax1)
ax1.set(xlabel='Date', ylabel='MACD/Signal')

# Title the figure
fig.suptitle('Stock Price with MACD', fontsize=14, fontweight='bold')

plt.show()
