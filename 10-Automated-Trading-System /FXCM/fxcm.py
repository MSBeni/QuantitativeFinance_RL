import fxcmpy
import socketio


# initiating API connection and defining trade parameters
token_path = "/home/i-sip_iot/s_vv/FXCM.txt"

con = fxcmpy.fxcmpy(access_token=open(token_path, 'r').read()[:-1], log_level='error', server='demo')
pair = 'EUR/USD'
# print(con.get_instruments())

# get historical data
data = con.get_candles(pair, period='m5', number=250)
"""periods can be m1, m5, m15 and m30, H1, H2, H3, H4, H6 and H8, D1, W1, M1"""

# print(data)

#streaming data
"for streaming data, we first need ti subscribe to a currency pair"
con.subscribe_market_data('EUR/USD')
# con.get_last_price('EUR/USD')
# con.get_prices('EUR/USD')
# con.unsubscribe_market_data('EUR/USD')

print("get_last_price EUR/USD: ")
print(con.get_last_price('EUR/USD'))
print("get_prices EUR/USD: ")
print(con.get_prices('EUR/USD'))
print("unsubscribe_market_data EUR/USD: ")
print(con.unsubscribe_market_data('EUR/USD'))


# trading account data
# GetAccounts = con.get_accounts().T
#
# GetOpenPositions = con.get_open_positions().T
# GetOpenPositionsSummary = con.get_open_positions_summary().T
#
# GetClosedPositions = con.get_closed_positions(kind='dataframe').T

print("get_accounts: ")
print(con.get_accounts().T)
print("get_open_positions: ")
print(con.get_open_positions().T)
print("get_open_positions_summary: ")
print(con.get_open_positions_summary().T)
print("get_closed_positions: ")
print(con.get_closed_positions(kind='dataframe').T)
#
# con.get_closed_positions()
print("et_closed_positions: ")
print(con.get_closed_positions())
#
# con.get_orders()
print("get_orders: ")
print(con.get_orders())
#
# orders
# con.create_market_buy_order('EUR/USD', 10)
print("Create market buy order 'EUR/USD': ")
print(con.create_market_buy_order('EUR/USD', 10))
# con.create_market_buy_order('USD/CAD', 10)
print("Create market buy order 'USD/CAD': ")
print(con.create_market_buy_order('USD/CAD', 10))
# con.create_market_sell_order('USD/CAD', 20)
print("Create market buy order 'USD/CAD': ")
print(con.create_market_buy_order('USD/CAD', 20))
# con.create_market_sell_order('EUR/USD', 10)
print("Create market buy order 'EUR/USD': ")
print(con.create_market_buy_order('EUR/USD', 10))
# #
# #
# tradeId = con.get_open_trade_ids()[-1]
# print(tradeId)
# #
# order = con.open_trade(symbol='USD/CAD', is_buy=False,
#                        is_in_pips=True,
#                        amount=10, time_in_force='GTC',
#                        stop=-9, trailing_step=True,
#                        order_type='AtMarket', limit=9)
#
# con.close_trade(trade_id=tradeId, amount=1000)
# con.close_all_for_symbol('USD/CAD')
#
# #closing connection
# con.close()
