import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "DIS", "DOW", "XOM",
           "HD", "IBM", "INTC", "JNJ", "KO", "MCD", "MMM", "MRK", "MSFT",
           "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WMT", "WBA"]

# list of tickers whose financial data needs to be extracted
financial_dir_cy = {}  # directory to store current year's information
financial_dir_py = {}  # directory to store last year's information
financial_dir_py2 = {}  # directory to store last to last year's information

for ticker in tickers:
    try:
        print("scraping financial statement data for ", ticker)
        temp_dir = {}
        temp_dir2 = {}
        temp_dir3 = {}
        # getting balance sheet data from yahoo finance for the given ticker
        url = 'https://finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
        page = requests.get(url)
        page_content = page.content
        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.find_all("div", {"class": "W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
        for t in tabl:
            rows = t.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
            for row in rows:
                temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]
                temp_dir2[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[2]
                temp_dir3[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[3]

        # getting income statement data from yahoo finance for the given ticker
        url = 'https://finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
        page = requests.get(url)
        page_content = page.content
        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.find_all("div", {"class": "W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
        for t in tabl:
            rows = t.find_all("div", {"class": "rw-expnded"})
            for row in rows:
                temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]
                temp_dir2[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[2]
                temp_dir3[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[3]

        # getting cashflow statement data from yahoo finance for the given ticker
        url = 'https://finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker
        page = requests.get(url)
        page_content = page.content
        soup = BeautifulSoup(page_content, 'html.parser')
        tabl = soup.find_all("div", {"class": "M(0) Mb(10px) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
        for t in tabl:
            rows = t.find_all("div", {"class": "rw-expnded"})
            for row in rows:
                temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]
                temp_dir2[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[2]
                temp_dir3[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[3]

                # combining all extracted information with the corresponding ticker
        financial_dir_cy[ticker] = temp_dir
        financial_dir_py[ticker] = temp_dir2
        financial_dir_py2[ticker] = temp_dir3
    except:
        print("Problem scraping data for ", ticker)

# storing information in pandas dataframe
combined_financials_cy = pd.DataFrame(financial_dir_cy)
combined_financials_cy.dropna(how='all', axis=1, inplace=True)  # dropping columns with all NaN values
combined_financials_cy.to_csv("combined_financials_cy_Revised1.csv")

combined_financials_py = pd.DataFrame(financial_dir_py)
combined_financials_py.dropna(how='all', axis=1, inplace=True)
combined_financials_py.to_csv("combined_financials_py_Revised2.csv")

combined_financials_py2 = pd.DataFrame(financial_dir_py2)
combined_financials_py2.dropna(how='all', axis=1, inplace=True)
combined_financials_py2.to_csv("combined_financials_py2_Revised3.csv")

tickers = combined_financials_cy.columns  # updating the tickers list based on only those tickers whose values were successfully extracted

# selecting relevant financial information for each stock using fundamental data
stats = ["Net Income available to common shareholders",
         "Total assets",
         "Net cash provided by operating activites",
         "Long-term debt",
         "Other long-term liabilities",
         "Total current assets",
         "Total current liabilities",
         "Common stock",
         "Total revenue",
         "Gross profit"]  # change as required

indx = ["NetIncome", "TotAssets", "CashFlowOps", "LTDebt", "OtherLTDebt",
        "CurrAssets", "CurrLiab", "CommStock", "TotRevenue", "GrossProfit"]


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
                ticker_stats.append(temp.loc[stat])
            all_stats['{}'.format(ticker)] = ticker_stats
        except:
            print("can't read data for ", ticker)

    all_stats_df = pd.DataFrame(all_stats, index=indx)

    # cleansing of fundamental data imported in dataframe
    all_stats_df[tickers] = all_stats_df[tickers].replace({',': ''}, regex=True)
    for ticker in all_stats_df.columns:
        all_stats_df[ticker] = pd.to_numeric(all_stats_df[ticker].values, errors='coerce')
    return all_stats_df


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

f_score_df = piotroski_f(transformed_df_cy, transformed_df_py, transformed_df_py2)
f_score_df.sum().sort_values(ascending=False)