import pandas as pd

combined_financials_cy = pd.read_csv('combined_financials_cy_Revised1.csv')
combined_financials_py = pd.read_csv('combined_financials_py_Revised2.csv')
combined_financials_py2 = pd.read_csv('combined_financials_py2_Revised3.csv')

combined_financials_cy.set_index('Unnamed: 0', inplace=True)
combined_financials_py.set_index('Unnamed: 0', inplace=True)
combined_financials_py2.set_index('Unnamed: 0', inplace=True)

combined_financials_cy.fillna('0', inplace=True)
combined_financials_py.fillna('0', inplace=True)
combined_financials_py2.fillna('0', inplace=True)

# selecting relevant financial information for each stock using fundamental data
stats = ["Net Income Common Stockholders",
         "Total Assets",
         "Operating Cash Flow",
         "Total Debt",
         "Capital Lease Obligations",
         "Total current assets",
         "Total current liabilities",
         "Common Stock Equity",
         "Total Revenue",
         "Gross Profit"]  # change as required

indx = ["NetIncome", "TotAssets", "CashFlowOps", "LTDebt", "OtherLTDebt",
        "CurrAssets", "CurrLiab", "CommStock", "TotRevenue", "GrossProfit"]


tickers = combined_financials_cy.columns
# print(tickers)
# temp = combined_financials_cy['AXP']
# # print(temp)
# ticker_stats = []
# ticker_stats.append(int(temp.loc['Total Assets'].replace(",", "")) -
#                     (int(temp.loc['Net Tangible Assets'].replace(",", "")) +
#                      int(temp.loc['Invested Capital'].replace(",", "")) +
#                      int(temp.loc['Tangible Book Value'].replace(",", ""))))
#
# ticker_stats.append(int(temp.loc['Gross Profit']))
#
# print(ticker_stats)

# temp = combined_financials_cy['AXP']
# print(temp)
ticker_stats = []
# for stat in stats:
#     if stat == 'Total current assets':
#         ticker_stats.append(int(temp.loc['Total Assets'].replace(",", "")) -
#                             (int(temp.loc['Net Tangible Assets'].replace(",", "")) +
#                              int(temp.loc['Invested Capital'].replace(",", "")) +
#                              int(temp.loc['Tangible Book Value'].replace(",", ""))))
#
#     elif stat == 'Total current liabilities':
#         ticker_stats.append(int(temp.loc['Total Debt'].replace(",", "")) -
#                             int(temp.loc['Net Debt'].replace(",", "")))
#     else:
#         ticker_stats.append(int(temp.loc[stat].replace(",", "")))
#
# print(ticker_stats)

# all_stats['{}'.format(ticker)] = ticker_stats

def info_filter(df, stats, indx):
    """function to filter relevant financial information for each
       stock and transforming string inputs to numeric"""
    tickers = df.columns
    all_stats = {}
    for ticker in tickers:
        try:
            temp = df[ticker]
            ticker_stats = []
            for stat in stats:
                if stat == 'Total current assets':
                    ticker_stats.append(int(temp.loc['Total Assets'].replace(",", "")) -
                                        (int(temp.loc['Net Tangible Assets'].replace(",", "")) +
                                         int(temp.loc['Invested Capital'].replace(",", "")) +
                                         int(temp.loc['Tangible Book Value'].replace(",", ""))))

                elif stat == 'Total current liabilities':
                    ticker_stats.append(int(temp.loc['Total Debt'].replace(",", "")) -
                                        int(temp.loc['Net Debt'].replace(",", "")))
                else:
                    ticker_stats.append(int(temp.loc[stat].replace(",", "")))

            all_stats['{}'.format(ticker)] = ticker_stats
        except:
            print("can't read data for ", ticker)

    all_stats_df = pd.DataFrame(all_stats, index=indx)

    # cleansing of fundamental data imported in dataframe
    # all_stats_df[tickers] = all_stats_df[tickers].replace({',': ''}, regex=True)
    # for ticker in all_stats_df.columns:
    #     all_stats_df[ticker] = pd.to_numeric(all_stats_df[ticker].values, errors='coerce')
    return all_stats_df

print(info_filter(combined_financials_cy, stats, indx))