from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.google.com/"

# please install and reference the latest version of chromedriver from the website bellow
# http://chromedriver.chromium.org/downloads
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

elements = browser.find_elements_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')[0]

elements.send_keys("Yahoo Finance")
elements.submit()
Webelements = browser.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div/div[1]/a')[0]

Webelements.click()

# browser.quit()