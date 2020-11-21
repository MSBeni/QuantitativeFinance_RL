from selenium import webdriver
# We are using the ChromeDriverManager to install the latest suitable Chrome Web Driver Based on Local Browser
# pip install webdriver-manager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import re

URL = 'https://twitter.com/search?q=(from%3AJoeBiden)%20min_retweets%3A10%20until%3A2020-11-19%20since%3A2020-11-18&' \
      'src=typed_query'

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(URL)

tweet = {
    'date': None,
    'text': None,
    'user_id': None,
    'created_at': None,
    'retweets': 0,
    'likes': 0,
    'replies': 0
}

element_ = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[7]/'
               'div/div/article/div/div/div/div[2]')))

print("The Tweet is: ")
text_ = element_.get_attribute("textContent")
print(element_.get_attribute("textContent"))

# Extract UserName
element_ = WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[7]/'
               'div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[2]/div/span')))

print("The Username is: ")
user_id_ = element_.get_attribute("textContent")
print(element_.get_attribute("textContent"))

# Exporting the Time
element_ = WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[7]/'
               'div/div/article/div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/a')))

print("The time of the Tweet is: ")
time_ = element_.get_attribute("title")
time_ = re.sub('[,!@#$]', '', time_)
time_ = time_[:7]+' '+time_[9:]
print(element_.get_attribute("title"))
tweet_time_ = datetime.strptime(time_, '%I:%M %p %b %d %Y')
print(tweet_time_)

# Exporting the retweets
elements = WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/'
                                          'div/div/section/div/div/div[7]/div/div/article/div/div/div/div[2]/div[2]/'
                                          'div[2]/div[3]/div[2]/div/div/div[2]/span/span')))
print("The retweets of the Tweet is: ")
retweets_ = elements.get_attribute("textContent")
print(elements.get_attribute("textContent"))


# Exporting the replies
elements = WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[7]/'
               'div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[1]/div/div/div[2]/span/span')))
print("The replies on the Tweet is: ")
replies_ = elements.get_attribute("textContent")
print(elements.get_attribute("textContent"))


# Exporting the likes
elements = WebDriverWait(browser, 5).until(EC.visibility_of_element_located(
    (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[2]/div/div/section/div/div/div[7]/'
               'div/div/article/div/div/div/div[2]/div[2]/div[2]/div[3]/div[3]/div/div/div[2]/span/span')))
print("The Likes of the Tweet is: ")
likes_ = elements.get_attribute("textContent")
print(elements.get_attribute("textContent"))


tweet = {
    'date': str(tweet_time_.date()),
    'created_at': str(tweet_time_.time()),
    'text': text_,
    'user_id': user_id_,
    'retweets': retweets_,
    'likes': likes_,
    'replies': replies_
}

print(tweet)