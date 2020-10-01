from selenium import webdriver
# We are using the ChromeDriverManagerto install the latest suitable Chrome Web Driver Based on Local Browser
from webdriver_manager.chrome import ChromeDriverManager

url = "https://ca.finance.yahoo.com/quote/TSLA/key-statistics?p=TSLA"
options = webdriver.ChromeOptions()
options.add_argument('headless')
pathToChromeDriver = ""

# please install and reference the latest version of chromedriver from the website bellow
# http://chromedriver.chromium.org/downloads
# browser = webdriver.Chrome(executable_path="/home/i-sip_iot/s_vv/chromedriver", options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(url)

driver.quit()
