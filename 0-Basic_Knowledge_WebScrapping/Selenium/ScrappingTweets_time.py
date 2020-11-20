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

print("The time of the Tweet is: ")
print(element_.get_attribute("textContent"))


element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
    (By.CSS_SELECTOR, '#react-root > div > div > div.css-1dbjc4n.r-18u37iz.r-13qz1uu.r-417010 > main > div > div > div > div.css-1dbjc4n.r-14lw9ot.r-1tlfku8.r-1ljd8xs.r-13l2t4g.r-1phboty.r-1jgb5lz.r-11wrixw.r-61z16t.r-1ye8kvj.r-13qz1uu.r-184en5c > div > div:nth-child(2) > div > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(1) > div > div > div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2 > a > time')))

print(element_)
print("The time of the Tweet is: ")
print(element_.get_attribute("textContent"))

