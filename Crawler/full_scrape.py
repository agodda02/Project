from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from datetime import date, datetime, timedelta

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

def get_links(date_to_check):
    url = 'https://hansard.parliament.uk/Commons/' + str(date_to_check)
    page = get_page(url)
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find_all('a', class_='card-section')
    return links    

def update_pmq_sessions_list(links):
    for link in links:
        check_link = link['href'][len("/Commons/"):]
        if "OralAnswer" in check_link:
            inner_page = get_page('https://hansard.parliament.uk/Commons/' + str(check_link))
            if "Contribution by The Prime Minister" in inner_page:
                pmq_sessions.append(check_link)        
                
def write_to_file(pmq_sessions):
    with open("pmq_links.txt", "w") as f:
        for pmq_session in pmq_sessions:
            f.writelines(pmq_session+'\n')

def tuesday_or_thursday(date_to_check):
    day_of_week = date_to_check.strftime('%A')
    
    if day_of_week == "Tuesday":
        date_to_check += timedelta(days = 2)        
    elif day_of_week == "Thursday":
        date_to_check += timedelta(days = 5)
        
    return date_to_check

start_time = datetime.now()

date_to_check = date(1961, 7, 18) 
move_to_wednesdays = date(1997, 5, 20)
end = date(2022, 6, 29) 
pmq_sessions = list()

while date_to_check <= move_to_wednesdays:    
    links = get_links(date_to_check)
    update_pmq_sessions_list(links)
    date_to_check = tuesday_or_thursday(date_to_check)

    if len(pmq_sessions) == 200:
        write_to_file(pmq_sessions)
        pmq_sessions.clear()

date_to_check = date(1997, 5, 21)

while date_to_check <= end:
    links = get_links(date_to_check)
    update_pmq_sessions_list(links)
    date_to_check += timedelta(days = 7)    

    if len(pmq_sessions) == 200:
        write_to_file(pmq_sessions)
        pmq_sessions.clear()

write_to_file(pmq_sessions)

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))