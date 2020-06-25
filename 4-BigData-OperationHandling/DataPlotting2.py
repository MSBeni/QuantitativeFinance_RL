# Import necesary libraries
import pandas as pd
import pandas_datareader.data as pdr
import datetime
import matplotlib.pyplot as plt

# Download historical data for required stocks
tickers = ["MSFT", "AMZN", "AAPL", "CSCO", "IBM", "FB"]

close_prices = pd.DataFrame()  # dataframe to store close price of each ticker
attempt = 0  # initializing passthrough variable
drop = []  # initializing list to store tickers whose close price was successfully extracted
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if
               j not in drop]  # removing stocks whose data has been extracted from the ticker list
    for i in range(len(tickers)):
        try:
            temp = pdr.get_data_yahoo(tickers[i], datetime.date.today() - datetime.timedelta(3650),
                                      datetime.date.today())
            temp.dropna(inplace=True)
            close_prices[tickers[i]] = temp["Adj Close"]
            drop.append(tickers[i])
        except:
            print(tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1

# Handling NaN Values
close_prices.fillna(method='bfill', axis=0,
                    inplace=True)  # Replaces NaN values with the next valid value along the column
daily_return = close_prices.pct_change()  # Creates dataframe with daily return for each stock

# Data vizualization
close_prices.plot()  # Plot of all the stocks superimposed on the same chart

cp_standardized = (close_prices - close_prices.mean()) / close_prices.std()  # Standardization
cp_standardized.plot()  # Plot of all the stocks standardized and superimposed on the same chart

close_prices.plot(subplots=True, layout=(3, 2), title="Tech Stock Price Evolution", grid=True)  # Subplots of the stocks

# Pyplot demo
fig, ax = plt.subplots()
plt.style.available
plt.style.use('ggplot')
ax.set(title="Daily return on tech stocks", xlabel="Tech Stocks", ylabel="Daily Returns")
plt.bar(daily_return.columns, daily_return.mean())
plt.show()