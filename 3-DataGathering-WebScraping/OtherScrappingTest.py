import requests
from bs4 import BeautifulSoup
import pandas as pd


names = []
prices = []
changes = []
percentChanges = []
marketCaps = []
totalVolumes = []
circulatingSupplys = []

CryptoCurrenciesUrl = "https://in.finance.yahoo.com/currencies"
r = requests.get(CryptoCurrenciesUrl)
data = r.text
soup = BeautifulSoup(data)

counter = 40
for i in range(40, 404, 14):
    for listing in soup.find_all('tr', attrs={'data-reactid': i}):
        for name in listing.find_all('td', attrs={'data-reactid': i + 3}):
            names.append(name.text)
        for price in listing.find_all('td', attrs={'data-reactid': i + 4}):
            prices.append(price.text)
        for change in listing.find_all('td', attrs={'data-reactid': i + 5}):
            changes.append(change.text)
        for percentChange in listing.find_all('td', attrs={'data-reactid': i + 7}):
            percentChanges.append(percentChange.text)
print(pd.DataFrame({"Names": names, "Prices": prices, "Change": changes, "% Change": percentChanges}))
