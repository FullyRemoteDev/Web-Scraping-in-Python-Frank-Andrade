from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

website_url = 'https://twitter.com/TwitterSupport/status/1578008801357209601'
chrome_driver_path = 'G:\\Downloads\\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_path)
driver.get(website_url)
driver.maximize_window()

def get_tweet(element):
    try:
        user = element.find_element_by_xpath(".//span[contains(text(), '@')]").text
        text = element.find_element_by_xpath(".//div[@lang]").text
        tweets_data = [user, text]
    except:
        tweets_data = ['user', 'text']
    return tweets_data


user_data = []
text_data = []
tweet_ids = set()

scrolling = True

while scrolling:
    tweets = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '//article['
                                                                                           '@role="article"]')))
    for tweet in tweets:
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)

        user_data.append(tweet_list[0])
        text_data.append(" ".join(tweet_list[1].split()))

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        # if new_height == last_height:
        #     scrolling = False
        #     break
        if len(user_data) > 100:
            scrolling = False
            break
        else:
            last_height = new_height
            break

driver.quit()

df_tweets = pd.DataFrame({'User': user_data, 'Tweet': text_data})
df_tweets.to_csv('tweets-infinite.csv', index=False)
