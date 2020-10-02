from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
        print("Final Text>>>> ", el.get_attribute("textContent"))
    else:
        index += 1

browser.quit()
