from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date, datetime, timedelta

def get_page(url):
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1080")

    service = Service('C:/Users/andre/chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    return driver.page_source        

start_time = datetime.now()

d = date(1997, 5, 21)
today = date.today()
pmq_sessions = list()

while d <= today:
    url = 'https://hansard.parliament.uk/Commons/' + str(d)
    page = get_page(url)
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find_all('a', class_='card-section')
    for link in links:
        if 'Engagements' in link['href']:
            pmq_sessions.append(link['href'])    
    d += timedelta(days = 7)
    
with open("pmq_links.txt", "w") as f:
    for pmq_session in pmq_sessions:
        f.writelines(pmq_session+'\n')
    
end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))