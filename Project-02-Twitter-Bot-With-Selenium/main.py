from selenium import webdriver
from dotenv import load_dotenv
import time
import os

load_dotenv()

website_url = 'https://twitter.com/i/flow/login'
chrome_driver_path = 'G:\\Downloads\\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_path)
driver.get(website_url)
driver.maximize_window()

time.sleep(6)

username = driver.find_element_by_xpath('//input[@autocomplete="username"]')
twitter_username = os.environ.get("TWITTER_USERNAME")
username.send_keys(twitter_username)

next_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Next"]')
next_button.click()

time.sleep(2)

password = driver.find_element_by_xpath('//input[@name="password"]')
twitter_password = os.environ.get("TWITTER_PASSWORD")
password.send_keys(twitter_password)

login_button = driver.find_element_by_xpath('//div[@role="button"]//span[text()="Log in"]')
login_button.click()

# driver.quit()
