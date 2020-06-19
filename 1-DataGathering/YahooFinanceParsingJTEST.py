# Please check this repository and install yahoofinancials library
# https://github.com/JECSand/yahoofinancials
from yahoofinancials import YahooFinancials

ticker = 'AAPL'
yahoo_financials = YahooFinancials(ticker)

# balance_sheet_data_qt = yahoo_financials.get_financial_stmts('quarterly', 'balance')
# income_statement_data_qt = yahoo_financials.get_financial_stmts('quarterly', 'income')
# all_statement_data_qt = yahoo_financials.get_financial_stmts('quarterly', ['income', 'cash', 'balance'])
# apple_earnings_data = yahoo_financials.get_stock_earnings_data()
# apple_net_income = yahoo_financials.get_net_income()

# You can ask for weekly or yearly data as well
historical_stock_prices = yahoo_financials.get_historical_price_data('2018-09-15', '2019-09-15', 'daily')

print("Apple historical stock prices: ", historical_stock_prices)
