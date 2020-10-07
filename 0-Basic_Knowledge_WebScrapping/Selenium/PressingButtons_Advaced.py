from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


url = "https://www.google.com/"

# please install and reference the latest version of chromedriver from the website bellow
# http://chromedriver.chromium.org/downloads
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

elements = browser.find_elements_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')[0]

elements.send_keys("Yahoo Finance")
elements.submit()
# element = WebDriverWait(browser,10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="Rzn5id"]/div/a[2]'))).click()
Webelements = browser.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div/div[1]/a')[0]

Webelements.click()
element = browser.find_elements_by_id("yfin-usr-qry")[0]
element.send_keys("AAPL")
element.submit()

element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="quote-nav"]/ul/li[5]/a'
                                                                            ))).click()

element_ = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/span')))

# element_.textContent = "Oct. 07, 2016 - Oct. 07, 2020"

# In order to edit the element inner text data
# browser.execute_script()
browser.execute_script("arguments[0].innerText = 'Oct. 07, 2016 - Oct. 07, 2020'", element_)
print(element_.get_attribute("textContent"))

# element_ = browser.find_elements_by_xpath('//*[@id="dropdown-menu"]/div/div[3]/button[1]')[0]
# //*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div/div/svg/path
# Drop Down Bottom
Bottom_element = WebDriverWait(browser, 10).\
    until(EC.visibility_of_element_located((
    By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/div[1]/div/div'))).click()
# actions.move_to_element(Bottom_element[0]).perform()

# Bottom_element[0].click()

# # start Date
# # '//*[@id="dropdown-menu"]/div/div[1]/input'
# _element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dropdown-menu"]/div/div[1]/input')))
# print(_element.get_attribute("textContent"))
# # End Date
# # '//*[@id="dropdown-menu"]/div/div[2]/input'
# _element = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dropdown-menu"]/div/div[2]/input')))
# print(_element.get_attribute("textContent"))
# # print(elem[0].get_attribute("textContent"))

element_ = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button'))).click()
element_ = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[1]/button'))).click()

Final_el = browser.find_elements_by_xpath('//*[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[1]/div[2]/span[2]/a')[0]
Final_el.click()
# browser.quit()