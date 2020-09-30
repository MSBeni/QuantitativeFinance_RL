import requests as re

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

txt = re.get(url).text
LimitedTXT = txt.split('0001555280')[0]
tickers = ['Symbol', 'Security', 'SEC filings',	'GICS Sector', 'GICS Sub Industry', 'Headquarters Location',
           'Date first added', 'CIK',	'Founded']
LimitedTXT = LimitedTXT.split('<th>Security</th>')[1]
LimitedTXT = LimitedTXT.split('<th><a href="/wiki/Central_Index_Key" title="Central Index Key">CIK</a></th>')[1]
LimitedTXT = LimitedTXT.split('<td><a rel="nofollow" class="external text" href=')
nameslst = []
for el in LimitedTXT:
    try:
        if el[:6] == '"https':
           ticker = el.split('"https://www.nyse.com/quote/XNYS:')[1]
           nameslst.append(ticker)
        else:
            ticker2 = el.split('"http://www.nasdaq.com/symbol/')[1]
            nameslst.append(ticker2)
    except:
        print("NOT A RIGHT OPERATION...")

FinalTickers = []
for el in nameslst:
    TICK = el.split('">')[0]
    TICK_Size = len(TICK)
    FinalTickers.append(el.split('">')[1][:TICK_Size])


for ticker in FinalTickers:
    # New_url = "https://ca.finance.yahoo.com/quote/" + ticker + "/history?p=" + ticker + "&.tsrc=fin-tre-srch"
    url = "https://ca.finance.yahoo.com/quote/"+ ticker +"?p="+ ticker
    Indicators = {"Previous Close": [],
                  "Open": [],
                  "Bid": [],
                  "Ask": [],
                  "Day&#x27;s Range": [],
                  "52 Week Range": [],
                  "Volume": [],
                  "Avg. Volume": [],
                  "Market Cap": [],
                  "Beta": [],
                  "PE Ratio (TTM)": [],
                  "EPS (TTM)": [],
                  "Earnings Date": [],
                  "Dividend &amp; Yield": [],
                  "Ex-Dividend Date": [],
                  "1y Target Est": []}

    htmlText = re.get(url).text
    # print(htmlText)
    FinalVal = []
    for el in Indicators.keys():
        try:
            splitList = htmlText.split(el)[1].split('/td></tr><tr')[0]
            if len(splitList.split('">')[:20]) == 2:
                FinalVal.append(((splitList.split('">')[:20])[1][:20].split('</span><')[0][:13]).split('<')[0])
            elif len(splitList.split('">')[:20]) == 3:
                FinalVal.append(((splitList.split('">')[:20])[2][:20].split('</span><')[0][:13]).split('<')[0])
            else:
                FinalVal.append(((splitList.split('">')[:20])[2][:20].split('</span><')[0][:13]).split('<')[0])
        except:
            print("Something goes wrong with this {} Indicators for {} stck".format(el, ticker))

        Indicators[el].append(FinalVal[-1])

    print(Indicators)