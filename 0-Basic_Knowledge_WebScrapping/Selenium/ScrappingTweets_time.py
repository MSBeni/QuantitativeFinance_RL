from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = 'https://twitter.com/search?q=(from%3AJoeBiden)%20min_retweets%3A10%20until%3A2020-11-19%20since%3A2020-11-18&' \
      'src=typed_query'

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(URL)

element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/'
               'div/div/article/div/div/div/div[2]')))

print("The Tweet is: ")
print(element_.get_attribute("textContent"))

element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[1]/'
               'div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a')))

print(element_.get_attribute("title"))
print("The time of the Tweet is: ")
print(element_.get_attribute("textContent"))
