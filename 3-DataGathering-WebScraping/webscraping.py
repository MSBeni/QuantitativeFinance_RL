import requests
from bs4 import BeautifulSoup
import pandas as pd

tickers = ['AAPL', 'MSFT']
financial_dir = {}

for ticker in tickers:
    temp_dir = {}
    financial_list = []
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/balance-sheet?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    table = soup.find_all("div", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for row in table:
        for i in range(len(row.get_text(separator='|'))):
            try:
                financial_list.append(row.get_text(separator='|').split("|")[i].replace(',', ''))
            except:
                continue


    # getting income statement data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/financials?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("table", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for row in table:
        for i in range(len(row.get_text(separator='|'))):
            try:
                financial_list.append(row.get_text(separator='|').split("|")[i].replace(',', ''))
            except:
                continue



    # getting cashflow statement data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/cash-flow?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.find_all("table", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for row in table:
        for i in range(len(row.get_text(separator='|'))):
            try:
                financial_list.append(row.get_text(separator='|').split("|")[i].replace(',', ''))
            except:
                continue



    # getting key statistics data from yahoo finance for the given ticker
    url = 'https://in.finance.yahoo.com/quote/' + ticker + '/key-statistics?p=' + ticker
    page = requests.get(url)
    page_content = page.content
    soup = BeautifulSoup(page_content, 'html.parser')
    tabl = soup.findAll("table", {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})
    for row in table:
        for i in range(len(row.get_text(separator='|'))):
            try:
                financial_list.append(row.get_text(separator='|').split("|")[i].replace(',', ''))
            except:
                continue




                # class ="rw-expnded"

    #combining all extracted information with the corresponding ticker
    financial_dir[ticker] = financial_list

print(financial_dir)
