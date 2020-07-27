import requests
from bs4 import BeautifulSoup
import pandas as pd

combined_financials = pd.read_csv('Com_Finance_data_NEW.csv')
# updating the tickers list based on only those tickers whose values were successfully extracted
tickers = combined_financials.columns
tickers = tickers[1:]
# print(tickers)

NewIdx = combined_financials['Unnamed: 0']

combined_financials.drop(['Unnamed: 0'], axis=1, inplace=True)
combined_financials.set_index(NewIdx, inplace=True)
# print(combined_financials)

stats = ["Pretax Income",
         "Total Capitalization",
         "Total Revenue",
         "Invested Capital",
         "Net Income Common Stockholders",
         "Total Capitalization",
         "Operating Income",
         "Operating Expense"
         ]   # change as required


indx = ["Income", "TotRevenue", "InvCap", "NetInc", "TotCap", "OpeInc", "OpeExp"]
all_stats = {}
# try:
#         temp = combined_financials['MMM']
#         ticker_stats = []
#         for stat in stats:
#             ticker_stats.append(temp.loc['Total Assets'])
#         all_stats['{}'.format('MMM')] = ticker_stats
# except:
#         print("Fuck it !!!")
for ticker in tickers:
    try:
        temp = combined_financials[ticker]
        ticker_stats = []
        for stat in stats:
            ticker_stats.append(temp.loc[stat])
        all_stats['{}'.format(ticker)] = ticker_stats
    except:
        print("can't read data for ", ticker)

all_stats_df = pd.DataFrame(all_stats, index=indx)
# print(all_stats_df)



# cleansing of fundamental data imported in dataframe
all_stats_df.iloc[1, :] = [x.replace("M", "E+03") for x in all_stats_df.iloc[1, :].values]
all_stats_df.iloc[1, :] = [x.replace("B", "E+06") for x in all_stats_df.iloc[1, :].values]
all_stats_df.iloc[1, :] = [x.replace("T", "E+09") for x in all_stats_df.iloc[1, :].values]
all_stats_df.iloc[-1, :] = [str(x).replace("%", "E-02") for x in all_stats_df.iloc[-1,:].values]
all_stats_df[tickers] = all_stats_df[tickers].replace({',': ''}, regex=True)
for ticker in all_stats_df.columns:
    all_stats_df[ticker] = pd.to_numeric(all_stats_df[ticker].values, errors='coerce')

# calculating relevant financial metrics for each stock
transpose_df = all_stats_df.transpose()
final_stats_df = pd.DataFrame()
final_stats_df["EBIT"] = transpose_df["EBIT"]
final_stats_df["TEV"] = transpose_df["MarketCap"].fillna(0) \
                         +transpose_df["TotDebt"].fillna(0) \
                         +transpose_df["PrefStock"].fillna(0) \
                         +transpose_df["MinInterest"].fillna(0) \
                         -(transpose_df["CurrAsset"].fillna(0)-transpose_df["CurrLiab"].fillna(0))
final_stats_df["EarningYield"] = final_stats_df["EBIT"]/final_stats_df["TEV"]
final_stats_df["FCFYield"] = (transpose_df["CashFlowOps"]-transpose_df["Capex"])/transpose_df["MarketCap"]
final_stats_df["ROC"] = transpose_df["EBIT"]/(transpose_df["PPE"]+transpose_df["CurrAsset"]-transpose_df["CurrLiab"])
final_stats_df["BookToMkt"] = transpose_df["BookValue"]/transpose_df["MarketCap"]
final_stats_df["DivYield"] = transpose_df["DivYield"]


################################Output Dataframes##############################

# finding value stocks based on Magic Formula
final_stats_val_df = final_stats_df.loc[tickers, :]
final_stats_val_df["CombRank"] = final_stats_val_df["EarningYield"].rank(ascending=False,na_option='bottom') + \
                                 final_stats_val_df["ROC"].rank(ascending=False, na_option='bottom')
final_stats_val_df["MagicFormulaRank"] = final_stats_val_df["CombRank"].rank(method='first')
value_stocks = final_stats_val_df.sort_values("MagicFormulaRank").iloc[:, [2, 4, 8]]
print("------------------------------------------------")
print("Value stocks based on Greenblatt's Magic Formula")
print(value_stocks)


# finding highest dividend yield stocks
high_dividend_stocks = final_stats_df.sort_values("DivYield", ascending=False).iloc[:, 6]
print("------------------------------------------------")
print("Highest dividend paying stocks")
print(high_dividend_stocks)


# # Magic Formula & Dividend yield combined
final_stats_df["CombRank"] = final_stats_df["EarningYield"].rank(ascending=False, method='first') \
                              +final_stats_df["ROC"].rank(ascending=False, method='first')  \
                              +final_stats_df["DivYield"].rank(ascending=False, method='first')
final_stats_df["CombinedRank"] = final_stats_df["CombRank"].rank(method='first')
value_high_div_stocks = final_stats_df.sort_values("CombinedRank").iloc[:, [2, 4, 6, 8]]
print("------------------------------------------------")
print("Magic Formula and Dividend Yield combined")
print(value_high_div_stocks)



