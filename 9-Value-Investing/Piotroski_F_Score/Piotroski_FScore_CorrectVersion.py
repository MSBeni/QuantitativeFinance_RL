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

combined_financials_cy.replace('-', '0', inplace=True)
combined_financials_py.replace('-', '0', inplace=True)
combined_financials_py2.replace('-', '0', inplace=True)

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
    return all_stats_df

# print(info_filter(combined_financials_cy, stats, indx))


def piotroski_f(df_cy, df_py, df_py2):
    """function to calculate f score of each stock and output information as dataframe"""
    f_score = {}
    tickers = df_cy.columns
    for ticker in tickers:
        ROA_FS = int(df_cy.loc["NetIncome", ticker] / (
                    (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2) > 0)
        CFO_FS = int(df_cy.loc["CashFlowOps", ticker] > 0)
        ROA_D_FS = int(
            df_cy.loc["NetIncome", ticker] / (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2 >
            df_py.loc["NetIncome", ticker] / (df_py.loc["TotAssets", ticker] + df_py2.loc["TotAssets", ticker]) / 2)
        CFO_ROA_FS = int(
            df_cy.loc["CashFlowOps", ticker] / df_cy.loc["TotAssets", ticker] > df_cy.loc["NetIncome", ticker] / (
                        (df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2))
        LTD_FS = int((df_cy.loc["LTDebt", ticker] + df_cy.loc["OtherLTDebt", ticker]) < (
                    df_py.loc["LTDebt", ticker] + df_py.loc["OtherLTDebt", ticker]))
        CR_FS = int((df_cy.loc["CurrAssets", ticker] / df_cy.loc["CurrLiab", ticker]) > (
                    df_py.loc["CurrAssets", ticker] / df_py.loc["CurrLiab", ticker]))
        DILUTION_FS = int(df_cy.loc["CommStock", ticker] <= df_py.loc["CommStock", ticker])
        GM_FS = int((df_cy.loc["GrossProfit", ticker] / df_cy.loc["TotRevenue", ticker]) > (
                    df_py.loc["GrossProfit", ticker] / df_py.loc["TotRevenue", ticker]))
        ATO_FS = int(
            df_cy.loc["TotRevenue", ticker] / ((df_cy.loc["TotAssets", ticker] + df_py.loc["TotAssets", ticker]) / 2) >
            df_py.loc["TotRevenue", ticker] / ((df_py.loc["TotAssets", ticker] + df_py2.loc["TotAssets", ticker]) / 2))
        f_score[ticker] = [ROA_FS, CFO_FS, ROA_D_FS, CFO_ROA_FS, LTD_FS, CR_FS, DILUTION_FS, GM_FS, ATO_FS]
    f_score_df = pd.DataFrame(f_score,
                              index=["PosROA", "PosCFO", "ROAChange", "Accruals", "Leverage", "Liquidity", "Dilution",
                                     "GM", "ATO"])
    return f_score_df


# Selecting stocks with highest Piotroski f score
transformed_df_cy = info_filter(combined_financials_cy, stats, indx)
transformed_df_py = info_filter(combined_financials_py, stats, indx)
transformed_df_py2 = info_filter(combined_financials_py2, stats, indx)

print(transformed_df_cy)
print(transformed_df_py)
print(transformed_df_py2)

f_score_df = piotroski_f(transformed_df_cy, transformed_df_py, transformed_df_py2)
print(f_score_df.sum().sort_values(ascending=False))
