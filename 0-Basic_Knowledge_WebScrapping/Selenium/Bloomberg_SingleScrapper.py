from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = 'https://www.bloomberg.com/markets/economics'

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(URL)

element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="hub_single_story_1"]/article/section')))

print(element_.get_attribute("textContent"))



