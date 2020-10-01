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
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)

# Getting the first elements
# element = browser.find_element_by_xpath("html/*")

# Getting all elements
elements = browser.find_elements_by_xpath("html/*")

for el in elements:
    print(el.tag_name)
    # print(el.text)
    print(el.get_attribute('textContent'))

browser.quit()
