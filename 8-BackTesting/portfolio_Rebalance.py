import numpy as np
import pandas as pd
import pandas_datareader.data as pdr
import datetime
import copy
import matplotlib.pyplot as plt


def cagr(dataframe):
    """function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
    df = dataframe.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    n = len(df)/12
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR


def volatility(dataframe):
    """function to calculate annualized volatility of a trading strategy"""
    df = dataframe.copy()
    vol = df["mon_ret"].std() * np.sqrt(12)
    return vol


def sharpe(dataframe, rf):
    """function to calculate sharpe ratio ; rf is the risk free rate"""
    df = dataframe.copy()
    sr = (cagr(df) - rf)/volatility(df)
    return sr


def max_dd(DF):
    """function to calculate max drawdown"""
    df = DF.copy()
    df["cum_return"] = (1 + df["mon_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd


# Download historical data (monthly) for DJI constituent stocks
tickers = ["MMM", "AXP", "T", "BA", "CAT", "CVX", "CSCO", "KO", "XOM", "GE", "GS", "HD",
           "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK", "MSFT", "NKE", "PFE", "PG", "TRV",
           "UTX", "UNH", "VZ", "V", "WMT", "DIS"]

ohlc_mon = {}  # directory with ohlc value for each stock
attempt = 0  # initializing passthrough variable
drop = []  # initializing list to store tickers whose close price was successfully extracted
while len(tickers) != 0 and attempt <= 5:
    tickers = [j for j in tickers if
               j not in drop]  # removing stocks whose data has been extracted from the ticker list
    for i in range(len(tickers)):
        try:
            ohlc_mon[tickers[i]] = pdr.get_data_yahoo(tickers[i], datetime.date.today() - datetime.timedelta(1900),
                                                      datetime.date.today(), interval='m')
            ohlc_mon[tickers[i]].dropna(inplace=True)
            drop.append(tickers[i])
        except:
            print(tickers[i], " :failed to fetch data...retrying")
            continue
    attempt += 1

tickers = ohlc_mon.keys()  # redefine tickers variable after removing any tickers with corrupted data


# ###############################Backtesting####################################

# ###############################Backtesting####################################

# calculating monthly return for each stock and consolidating return info by stock in a separate dataframe
ohlc_dict = copy.deepcopy(ohlc_mon)
return_df = pd.DataFrame()
for ticker in tickers:
    print("calculating monthly return for ", ticker)
    ohlc_dict[ticker]["mon_ret"] = ohlc_dict[ticker]["Adj Close"].pct_change()
    return_df[ticker] = ohlc_dict[ticker]["mon_ret"]

# dataframe = return_df.to_csv("return_dataframe.csv")


# function to calculate portfolio return iteratively
def pflio(dataframe_, m, x):
    """Returns cumulative portfolio return
    dataframe_ = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = dataframe_.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(1, len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i, :].mean())
            bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i, :].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
        print(portfolio)
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns=["mon_ret"])
    return monthly_ret_df


# calculating overall strategy's KPIs
cagr(pflio(return_df, 6, 3))
sharpe(pflio(return_df, 6, 3), 0.025)
max_dd(pflio(return_df, 6, 3))


# calculating KPIs for Index buy and hold strategy over the same period
DJI = pdr.get_data_yahoo("^DJI", datetime.date.today()-datetime.timedelta(1900), datetime.date.today(), interval='m')
DJI["mon_ret"] = DJI["Adj Close"].pct_change()
cagr(DJI)
sharpe(DJI, 0.025)
max_dd(DJI)

# visualization
fig, ax = plt.subplots()
plt.plot((1+pflio(return_df, 6, 3)).cumprod())
plt.plot((1+DJI["mon_ret"][2:].reset_index(drop=True)).cumprod())
plt.title("Index Return vs Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return", "Index Return"])

plt.show()