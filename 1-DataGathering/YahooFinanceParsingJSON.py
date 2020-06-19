# Please check this repository and install yahoofinancials library
# https://github.com/JECSand/yahoofinancials
import pandas as pd
from yahoofinancials import YahooFinancials
import datetime

all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "INTC"]

# extracting stock data (historical close price) for the stocks identified
close_prices = pd.DataFrame()
end_date = (datetime.date.today()).strftime('%Y-%m-%d')
beg_date = (datetime.date.today()-datetime.timedelta(1825)).strftime('%Y-%m-%d')
cp_tickers = all_tickers
attempt = 0
drop = []

for ticker in all_tickers:
    try:
        yahoo_financials = YahooFinancials(ticker)
        # You can ask for weekly or yearly data as well
        json_obj = yahoo_financials.get_historical_price_data(beg_date, end_date, "daily")
        prices = json_obj[ticker]['prices']
        temp = pd.DataFrame(prices)[["formatted_date", "adjclose", "open", "high", "low"]]
        # temp = pd.DataFrame(prices)[["formatted_date", "adjclose"]]
        temp.set_index("formatted_date", inplace=True)
        # we do not look for the duplicated values -- just get rid of them
        temp2 = temp[~temp.index.duplicated(keep='first')]
        close_prices[ticker] = temp2["adjclose"]
        file_name_json = ticker + '.json'
        file_name_csv = ticker + '.csv'
        temp2.to_json(file_name_json)
        temp2.to_csv(file_name_csv)
    except:
        print(ticker, " :failed to fetch data...retrying")
        continue

print(temp2)


