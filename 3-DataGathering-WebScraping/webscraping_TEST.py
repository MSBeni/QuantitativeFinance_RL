import requests
from bs4 import BeautifulSoup


url = 'https://in.finance.yahoo.com/quote/MSFT/financials?p=MSFT'
page = requests.get(url)
PageContent = page.content
soup = BeautifulSoup(PageContent, 'html.parser')
# table = soup.find_all('div', {"class": "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)"})

# "class": "Pos(r)"
table = soup.find_all('div', {"class": "rw-expnded"})
print(type(table))
for div in table:
    print(div.get_text())

