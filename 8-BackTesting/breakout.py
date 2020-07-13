import numpy as np
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import copy


def ATR(DF, n):
    "function to calculate True Range and Average True Range"
    df = DF.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    # df['ATR'] = df['TR'].ewm(span=n,adjust=False,min_periods=n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2['ATR']


def cagr(dataframe):
    """function to calculate the Cumulative Annual Growth Rate of a trading strategy"""
    df = dataframe.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    n = len(df) / (252 * 78)
    CAGR = (df["cum_return"].tolist()[-1]) ** (1 / n) - 1
    return CAGR


def volatility(dataframe):
    """function to calculate annualized volatility of a trading strategy"""
    df = dataframe.copy()
    vol = df["ret"].std() * np.sqrt(252 * 78)
    return vol


def sharpe(dataframe, rf):
    """function to calculate sharpe ratio ; rf is the risk free rate"""
    df = dataframe.copy()
    sr = (cagr(df) - rf) / volatility(df)
    return sr


def max_dd(dataframe):
    """function to calculate max drawdown"""
    df = dataframe.copy()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd


# Download historical data (monthly) for selected stocks

tickers = ["MSFT", "AAPL", "FB", "AMZN", "INTC", "CSCO", "VZ", "IBM", "QCOM", "LYFT"]

ohlc_intraday = {}  # directory with ohlc value for each stock
key_path = "/home/i-sip_iot/s_vv/AlphaVantage.txt"
ts = TimeSeries(key=open(key_path, 'r').read(), output_format='pandas')

################################Backtesting####################################

# calculating ATR and rolling max price for each stock and consolidating this info by stock in a separate dataframe
ohlc_dict = copy.deepcopy(ohlc_intraday)
tickers_signal = {}
tickers_ret = {}
for ticker in tickers:
    print("calculating ATR and rolling max price for ", ticker)
    ohlc_dict[ticker]["ATR"] = ATR(ohlc_dict[ticker], 20)
    ohlc_dict[ticker]["roll_max_cp"] = ohlc_dict[ticker]["High"].rolling(20).max()
    ohlc_dict[ticker]["roll_min_cp"] = ohlc_dict[ticker]["Low"].rolling(20).min()
    ohlc_dict[ticker]["roll_max_vol"] = ohlc_dict[ticker]["Volume"].rolling(20).max()
    ohlc_dict[ticker].dropna(inplace=True)
    tickers_signal[ticker] = ""
    tickers_ret[ticker] = []

# identifying signals and calculating daily return (stop loss factored in)
for ticker in tickers:
    print("calculating returns for ", ticker)
    for i in range(len(ohlc_dict[ticker])):
        if tickers_signal[ticker] == "":
            tickers_ret[ticker].append(0)
            if ohlc_dict[ticker]["High"][i] >= ohlc_dict[ticker]["roll_max_cp"][i] and \
                    ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["roll_max_vol"][i - 1]:
                tickers_signal[ticker] = "Buy"
            elif ohlc_dict[ticker]["Low"][i] <= ohlc_dict[ticker]["roll_min_cp"][i] and \
                    ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["roll_max_vol"][i - 1]:
                tickers_signal[ticker] = "Sell"

        elif tickers_signal[ticker] == "Buy":
            if ohlc_dict[ticker]["Adj Close"][i] < ohlc_dict[ticker]["Adj Close"][i - 1] - ohlc_dict[ticker]["ATR"][i -
                                                                                                                    1]:
                tickers_signal[ticker] = ""
                tickers_ret[ticker].append(((ohlc_dict[ticker]["Adj Close"][i - 1] - ohlc_dict[ticker]["ATR"][i - 1]) /
                                            ohlc_dict[ticker]["Adj Close"][i - 1]) - 1)
            elif ohlc_dict[ticker]["Low"][i] <= ohlc_dict[ticker]["roll_min_cp"][i] and \
                    ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["roll_max_vol"][i - 1]:
                tickers_signal[ticker] = "Sell"
                tickers_ret[ticker].append(((ohlc_dict[ticker]["Adj Close"][i - 1] - ohlc_dict[ticker]["ATR"][i - 1]) /
                                            ohlc_dict[ticker]["Adj Close"][i - 1]) - 1)
            else:
                tickers_ret[ticker].append(
                    (ohlc_dict[ticker]["Adj Close"][i] / ohlc_dict[ticker]["Adj Close"][i - 1]) - 1)

        elif tickers_signal[ticker] == "Sell":
            if ohlc_dict[ticker]["Adj Close"][i] > ohlc_dict[ticker]["Adj Close"][i - 1] + ohlc_dict[ticker]["ATR"][i -
                                                                                                                    1]:
                tickers_signal[ticker] = ""
                tickers_ret[ticker].append((ohlc_dict[ticker]["Adj Close"][i - 1] / (
                            ohlc_dict[ticker]["Adj Close"][i - 1] + ohlc_dict[ticker]["ATR"][i - 1])) - 1)
            elif ohlc_dict[ticker]["High"][i] >= ohlc_dict[ticker]["roll_max_cp"][i] and \
                    ohlc_dict[ticker]["Volume"][i] > 1.5 * ohlc_dict[ticker]["roll_max_vol"][i - 1]:
                tickers_signal[ticker] = "Buy"
                tickers_ret[ticker].append((ohlc_dict[ticker]["Adj Close"][i - 1] / (
                            ohlc_dict[ticker]["Adj Close"][i - 1] + ohlc_dict[ticker]["ATR"][i - 1])) - 1)
            else:
                tickers_ret[ticker].append(
                    (ohlc_dict[ticker]["Adj Close"][i - 1] / ohlc_dict[ticker]["Adj Close"][i]) - 1)

    ohlc_dict[ticker]["ret"] = np.array(tickers_ret[ticker])

# calculating overall strategy's KPIs
strategy_df = pd.DataFrame()
for ticker in tickers:
    strategy_df[ticker] = ohlc_dict[ticker]["ret"]
strategy_df["ret"] = strategy_df.mean(axis=1)
cagr(strategy_df)
sharpe(strategy_df, 0.025)
max_dd(strategy_df)

# vizualization of strategy return
(1 + strategy_df["ret"]).cumprod().plot()

# calculating individual stock's KPIs
cagr = {}
sharpe_ratios = {}
max_drawdown = {}
for ticker in tickers:
    print("calculating KPIs for ", ticker)
    cagr[ticker] = cagr(ohlc_dict[ticker])
    sharpe_ratios[ticker] = sharpe(ohlc_dict[ticker], 0.025)
    max_drawdown[ticker] = max_dd(ohlc_dict[ticker])

KPI_df = pd.DataFrame([cagr, sharpe_ratios, max_drawdown], index=["Return", "Sharpe Ratio", "Max Drawdown"])
KPI_df.T


