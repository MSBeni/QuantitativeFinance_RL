from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url = "https://ca.finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA"
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# pathToChromeDriver = ""

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

print(browser.page_source)


# "marketCap"


def FindElementByTarget(path, target, element):
    if target in element.get_attribute("textContent") and el.tag_name == 'script':
        return path

    New_Elements = element.find_elements_by_xpath("./*")
    for _element in New_Elements:
        print("New Path is >>>>>> ", path + "/" + _element.tag_name)
        finalPath = FindElementByTarget(path + "/" + _element.tag_name, target, _element)
        if finalPath != "":
            return finalPath
    return ""


elements = browser.find_elements_by_xpath("html/*")
# print(elements)
for el in elements:
    print(el.get_attribute("textContent"))

# browser.quit()
