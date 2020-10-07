from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager

url = "https://ca.finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA"

# please install and reference the latest version of chromedriver from the website bellow
# http://chromedriver.chromium.org/downloads
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

element = browser.find_element_by_id("yfin-usr-qry")
# print(elements)
element.send_keys("AAPL")
element.submit()

# browser.quit()
