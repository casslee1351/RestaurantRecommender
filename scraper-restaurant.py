from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time


service = Service('C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=service)

driver.get('https://www.visitwichita.com/restaurants/')
time.sleep(10)

driver.quit()
