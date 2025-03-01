from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

url = 'https://es.wallapop.com/app/search?filters_source=search_box&keywords=retroid%20pocket%205&longitude=-3.69196&latitude=40.41956'
driver.get(url)

wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ItemCardList__item")))

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

items = soup.find_all(class_="ItemCardList__item")
for item in items:
    print(item.text)

driver.quit()