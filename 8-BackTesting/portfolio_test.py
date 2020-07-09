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

monthly_ret = []
portfolio = ["MMM", "AXP", "T", "BA", "CAT", "CVX"]
return_df = pd.read_csv("return_dataframe.csv")

print(return_df[portfolio].iloc[12, :].mean())
bad_stocks = return_df[portfolio].iloc[12, :].sort_values(ascending=True)[:3].index.values.tolist()
print(bad_stocks)
portfolio = [t for t in portfolio if t not in bad_stocks]
# new_picks = return_df.iloc[12, :].sort_values(ascending=False)[:3].index.values.tolist()
new_picks = return_df.iloc[12, 1:].sort_values(ascending=False)[:3].index.values.tolist()
print(new_picks)
portfolio = portfolio + new_picks
print(portfolio)

def pflio(dataframe_, m, x):
    df = dataframe_.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(1, len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i, :].mean())
            bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i, 1:].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
    monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns=["mon_ret"])
    return monthly_ret_df


# cagr(pflio(return_df, 6, 3))
