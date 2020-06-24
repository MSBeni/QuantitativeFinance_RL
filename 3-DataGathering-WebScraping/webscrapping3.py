import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ["AAPL", "MSFT"]  # list of tickers whose financial data needs to be extracted
financial_dir = {}

for ticker in tickers:
    # getting balance sheet data from yahoo finance for the given ticker
    temp_dir = {}
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class": "rw-expnded"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]] = list(row.get_text(separator='|').split("|")[i]
                                                                       .replace(',', '') for i
                                                                       in range(1, len(row.get_text(separator='|')
                                                                                       .split("|"))))

    # getting income statement data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class": "rw-expnded"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]] = list(row.get_text(separator='|').split("|")[i]
                                                                       .replace(',', '') for i
                                                                       in range(1, len(row.get_text(separator='|')
                                                                                       .split("|"))))

    # getting cashflow statement data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for t in tabl:
        rows = t.find_all("div", {"class": "rw-expnded"})
        for row in rows:
            temp_dir[row.get_text(separator='|').split("|")[0]] = list(row.get_text(separator='|').split("|")[i]
                                                                       .replace(',', '') for i
                                                                       in range(1, len(row.get_text(separator='|')
                                                                                       .split("|"))))

    financial_dir[ticker] = temp_dir

combined_financials = pd.DataFrame(financial_dir)
# print(combined_financials)
tickers = combined_financials.columns
for ticker in tickers:
    combined_financials = combined_financials[~combined_financials[ticker].str.contains("[a-z]").fillna(False)]

print(combined_financials)