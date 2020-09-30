import requests as re

url = "https://ca.finance.yahoo.com/quote/TSLA?p=TSLA"

# txt = re.get(url).text
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
    splitList = htmlText.split(el)[1].split('/td></tr><tr')[0]
    if len(splitList.split('">')[:20]) == 2:
        FinalVal.append(((splitList.split('">')[:20])[1][:20].split('</span><')[0][:13]).split('<')[0])
    elif len(splitList.split('">')[:20]) == 3:
        FinalVal.append(((splitList.split('">')[:20])[2][:20].split('</span><')[0][:13]).split('<')[0])
    else:
        FinalVal.append(((splitList.split('">')[:20])[2][:20].split('</span><')[0][:13]).split('<')[0])

print(FinalVal)
print(len(FinalVal))
# afterFirstSplit = splitList[1].split("\">")[1]
# afterSecondSplit = afterFirstSplit.split("</td>")
# dataValue = afterSecondSplit[0]
# Indicators[indicator].append(dataValue)


# for indicator in Indicators:
#     splitList = htmlText.split(indicator)
#     afterFirstSplit = splitList[1].split("\">")[1]
#     afterSecondSplit = afterFirstSplit.split("</td>")
#     dataValue = afterSecondSplit[0]
#     Indicators[indicator].append(dataValue)

# print(Indicators)



# txt = txt.split('</span></td></tr></tbody></table></div></div></div></div></div><script>')[0]
# txt = txt.split('PREV_CLOSE-value')[1]
# txt = txt.split(') " data-reactid="')
#
# # print(txt)
# textF = []
# for el in txt:
#     textF.append(el.split('</td></tr><tr')[0])
#
# for el in textF:
#     print(el.split('">'))
