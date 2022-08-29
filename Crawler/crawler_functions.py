from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

def get_driver():
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")
    service = Service('C:/Users/andre/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    return driver

def get_page(url):
    driver = get_driver()
    driver.get(url)
    source = driver.page_source
    driver.close()
    return source

def get_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup
