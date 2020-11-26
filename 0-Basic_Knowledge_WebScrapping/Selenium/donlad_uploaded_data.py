from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


url = "https://gofile.io/d/7y0P5u"

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

# Drop Down Bottom
Bottom_element = WebDriverWait(browser, 30).\
    until(EC.visibility_of_element_located((
    By.XPATH, '//*[@id="datatable"]/tbody/tr[1]/td[4]/a[1]/button'))).click()

