from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = Options()
options.headless = False
# options.add_argument('window-size=1920x1080')

website_url = 'https://www.audible.in/adblbestsellers'
chrome_driver_path = 'G:\\Downloads\\chromedriver.exe'
driver = webdriver.Chrome(chrome_driver_path, options=options)

driver.get(website_url)
driver.maximize_window()

pagination = driver.find_element_by_xpath('//ul[contains(@class, "pagingElements")]')
pages = pagination.find_elements_by_tag_name('li')
last_page = int(pages[-2].text)

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:
    # time.sleep(2)
    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                               'adbl-impression-container ')))
    # container = driver.find_element_by_class_name('adbl-impression-container ')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './/li[contains('
                                                                                                '@class, '
                                                                                                '"productListItem")]')))
    # products = container.find_elements_by_xpath('.//li[contains(@class, "productListItem")]')

    for product in products:
        book_title.append(product.find_element_by_xpath('.//h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element_by_xpath('.//li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element_by_xpath('.//li[contains(@class, "runtimeLabel")]').text)

    current_page += 1

    try:
        next_page = driver.find_element_by_xpath('//span[contains(@class, "nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame({'Title': book_title, 'Author': book_author, 'Length': book_length})
df_books.to_csv('audible_books.csv', index=False)
