from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import json

url = "https://ca.finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA"
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# pathToChromeDriver = ""

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)


# "marketCap"
def FindElementByTarget(path, target, element):
    if target in element.get_attribute("textContent") and element.tag_name == 'script':
        return path

    New_Elements = element.find_elements_by_xpath("./*")
    for _element in New_Elements:
        print("New Path is >>>>>> ", path + "/" + _element.tag_name)
        finalPath = FindElementByTarget(path + "/" + _element.tag_name, target, _element)
        if finalPath != "":
            return finalPath
    return ""


def JsonPathFinder(jsonobj, path, target, matchtype):
    if type(jsonobj) == matchtype:
        if target in jsonobj:
            return path
        for newKey in jsonobj:
            print("JSON Path: ", path)
            result = JsonPathFinder(jsonobj[newKey], path + "," + newKey, target, matchtype)
            if result != "":
                return result
    return ""


target = "marketCap"
Start_element = browser.find_element_by_xpath("html")
Path = FindElementByTarget("html", target, Start_element)

print("The final path is:", Path)

# html index to find the place where the target is in different same paths
index = 1

FinalElement = browser.find_elements_by_xpath(Path)
for el in FinalElement:
    if target in el.get_attribute("textContent"):
        print("index_num: ", index)
        print("The real final path is: ", Path + "[" + str(index) + "]")
        Final_json = json.loads((el.get_attribute("textContent").split("(this));\n")[0]).split("root.App.main = ")[1]
                                [:-3])
    else:
        index += 1

print(Final_json)
print(type(Final_json))
# print(Final_json["context"].keys())
# print(Final_json["context"]["dispatcher"]["stores"])

MatchType = type(Final_json)
Final_JSON_Path = JsonPathFinder(Final_json, "", "marketCap", MatchType)
print("Final JSON PATH is: ", Final_JSON_Path)

JsonSplittedPath = Final_JSON_Path.split(",")
print("JsonSplittedPath: ", JsonSplittedPath)

WholeJSON = Final_json
for el in JsonSplittedPath:
    if el != "":
        data_ = WholeJSON[el]
        WholeJSON = data_

print(data_)
final_DATA = pd.DataFrame(data_)
print(final_DATA)

browser.quit()
