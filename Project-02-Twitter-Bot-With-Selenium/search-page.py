from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

search_text = 'python'
website_url = f'https://twitter.com/search?q={search_text}&src=typed_query'
chrome_driver_path = 'G:\\Downloads\\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_path)
driver.get(website_url)
driver.maximize_window()

def get_tweets(element):
    try:
        user = element.find_element_by_xpath(".//span[contains(text(), '@')]").text
        text = element.find_element_by_xpath(".//div[@lang]").text
        tweets_data = [user, text]
    except:
        tweets_data = ['user', 'text']
    return tweets_data

# time.sleep(6)
# tweets = driver.find_elements_by_xpath('//article[@role="article"]')
tweets = WebDriverWait(driver, 6).until(EC.presence_of_all_elements_located((By.XPATH, '//article[@role="article"]')))

user_data = []
text_data = []

for tweet in tweets:
    tweets_list = get_tweets(tweet)
    user_data.append(tweets_list[0])
    text_data.append(" ".join(tweets_list[1].split()))

driver.quit()

df_tweets = pd.DataFrame({'User': user_data, 'Tweet': text_data})
df_tweets.to_csv('tweets-search.csv', index=False)
