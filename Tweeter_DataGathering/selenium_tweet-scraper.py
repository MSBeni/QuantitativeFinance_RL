import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

twitter_username = "JamesSilman"
browser = webdriver.Chrome('/home/i-sip_iot/s_vv/chromedriver')
browser.get("https://twitter.com/" + twitter_username)

time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 10

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

twitter_elm = browser.find_elements_by_class_name("tweet")

for post in twitter_elm:
    username = post.find_element_by_class_name("username")
    if username.text.lower() == "@" + twitter_username.lower():
        tweet = post.find_element_by_class_name("tweet-text")
        print(tweet.text)

browser.quit()

