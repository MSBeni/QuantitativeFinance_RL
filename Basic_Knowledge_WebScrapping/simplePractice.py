import requests as re
import pandas as pd

url = "https://webscraper.io/test-sites/tables"

txt = re.get(url).text
txt = (txt.split('Table without thead tag')[0]).split('Table selector automatically detects header and data rows.')[1]
All_data = txt.split('<td>')
data_ = []
data_dict = {"#": [], "First Name": [], "Last Name": [], "Username": []}
for el in All_data:
    info = el.split('</td>')[0]
    if len(info) < 20:
        data_.append(info)

for i in range(len(data_)):
    try:
        hashtag = int(data_[i])
        data_dict["#"].append(data_[i])
        data_dict["First Name"].append(data_[i+1])
        data_dict["Last Name"].append(data_[i+2])
        data_dict["Username"].append(data_[i+3])
    except:
        print("ValueError: invalid literal for int()...")

FinalData = pd.DataFrame(data_dict)

print(FinalData)