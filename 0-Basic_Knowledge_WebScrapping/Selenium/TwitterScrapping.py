from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json

url = "https://twitter.com/search?q=(%23AAPL)%20until%3A2020-10-07%20since%3A2020-10-06&src=typed_query"
# url = "https://twitter.com/search?q=(%23AAPL)%20until%3A2020-10-07%20since%3A2020-10-06&src=typed_query"
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# pathToChromeDriver = ""

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)
# elements = browser.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/div/div/article/div/div/div/div[2]/div[2]/div[2]/div[1]/div/span[3]")
# element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div')))
element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div/div[2]/div/div/section/div')))
# element_ = browser.find_elements_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div')

# print(element_.getText())
print(element_.get_attribute("textContent"))
print("\n", "@@@@@@@@@@@@@@@@@@@")
print(element_.getText())
print("\n")


browser.execute_script("window.scrollTo(0, 1080)")
element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div')))
print(element_.get_attribute("textContent"))
print("\n")


browser.execute_script("window.scrollTo(0, 10080)")
element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div')))
print(element_.get_attribute("textContent"))
print("\n")

# for el in elements:
#     print(el.get_attribute("textContent"))

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


# target = "#AAPL"
# Start_element = browser.find_element_by_xpath("html")
# Path = FindElementByTarget("html", target, Start_element)
#
# print("The final path is:", Path)