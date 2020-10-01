import requests as re

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

txt = re.get(url).text
txtsplitted = txt.split("</td></tr>")

All_Com = []
for el in txtsplitted:
    All_Com.append(el.split("title=")[1])

_CompanyNames = []
for el in All_Com:
    _CompanyNames.append(el.split("</a></td>")[0])

FinalCompanyNames = []
for CompanyString in _CompanyNames:
    try:
        CName = CompanyString.split("\">")[1]
        if len(CName) < 30:
            FinalCompanyNames.append(CompanyString.split("\">")[1])
    except:
        print('Gush, such a wrong idea, your list is out of range ...')


print(FinalCompanyNames)
print(len(FinalCompanyNames))
