from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


url = "https://ca.finance.yahoo.com/quote/AAPL/history?p=AAPL"

# please install and reference the latest version of chromedriver from the website bellow
# http://chromedriver.chromium.org/downloads
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

# browser.find_elements_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/svg')[0].click()
Bottom_element = WebDriverWait(browser, 30).\
    until(EC.visibility_of_element_located((
    By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div'))).click()


# start Date
# '//*[@id="dropdown-menu"]/div/div[1]/input'
_element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dropdown-menu"]/div/div[1]/input')))
# _element = browser.find_elements_by_xpath('//*[@id="dropdown-menu"]/div/div[1]/input')

# browser.execute_script("document.getElementByName('startDate')[0].value = '2016-10-07'")
# print(_element.get_attribute("textContent"))
# browser.execute_script("arguments[0].value = '2016'", _element.click())
browser.execute_script("arguments[0].innerText = '2016-10-07'", _element.click())
print(_element.get_attribute("textContent"))
# End Date
# '//*[@id="dropdown-menu"]/div/div[2]/input'
# _element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dropdown-menu"]/div/div[2]/input')))
# print(_element.get_attribute("textContent"))
# print(elem[0].get_attribute("textContent"))

# Press OK bottom
element_ = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dropdown-menu"]/div/div[3]/button[1]'))).click()

Final_el = browser.find_elements_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')[0]
Final_el.click()