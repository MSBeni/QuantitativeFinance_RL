import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["MMM", "AXP", "AAPL", "BA", "CAT", "CVX", "CSCO", "KO", "DIS", "DWDP",
           "XOM", "GE", "GS", "HD", "IBM", "INTC", "JNJ", "JPM", "MCD", "MRK",
           "MSFT", "NKE", "PFE", "PG", "TRV", "UTX", "UNH", "VZ", "V", "WMT"]
# tickers = ["MMM", "AXP"]

# list of tickers whose financial data needs to be extracted
financial_dir = {}

for ticker in tickers:
    # getting balance sheet data from yahoo finance for the given ticker
    temp_dir = {}
    url = 'https://finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
    print(url)
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class": "W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
    # print(tabl)
    for t in tabl:
        # print("t: ", t)
        # print("################")
        rows = t.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        # print("rows: ", rows)
        for row in rows:
            # print("row", row)
            if len(row.get_text(separator='|').split("|")[0:2]) > 1:
                # print("name: ", row.get_text(separator='|').split("|")[0])
                # print("value: ", row.get_text(separator='|').split("|")[1])
                # print("###########################")
                temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]

    # getting income statement data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class": "W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
    for t in tabl:
        rows = t.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2]) > 1:
                temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]

    # getting cashflow statement data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class": "W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
    for t in tabl:
        rows = t.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2]) > 1:
                temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[1]

    # getting key statistics data from yahoo finance for the given ticker
    url = 'https://finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class": "W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)"})
    for t in tabl:
        rows = t.find_all("div", {"class": "D(tbr) fi-row Bgc($hoverBgColor):h"})
        for row in rows:
            if len(row.get_text(separator='|').split("|")[0:2]) > 0:
                temp_dir[row.get_text(separator='|').split("|")[0]] = row.get_text(separator='|').split("|")[-1]

                # combining all extracted information with the corresponding ticker
    financial_dir[ticker] = temp_dir

df = pd.DataFrame(financial_dir)
df.to_csv("Com_Finance_data.csv")

# print(financial_dir)