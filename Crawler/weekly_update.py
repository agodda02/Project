from datetime import date, datetime, timedelta
import crawler_functions

url = 'https://hansard.parliament.uk/Commons/'

with open("next_session.txt", "r") as f:
    next_date = f.readline()

datetime_object = datetime.strptime(next_date, '%Y-%m-%d')

url = 'https://hansard.parliament.uk/Commons/' + next_date
page = crawler_functions.get_page(url)
soup = crawler_functions.get_soup(page)
links = soup.find_all('a', class_='card-section')

pmq_sessions = list()

for link in links:
    check_link = link['href'][len("/Commons/"):]
    if "OralAnswer" in check_link:
        inner_page = crawler_functions.get_page('https://hansard.parliament.uk/Commons/' + str(check_link))
        if "Contribution by The Prime Minister" in inner_page:
            pmq_sessions.append(check_link) 
            
if len(pmq_sessions) > 0:
    with open("pmq_links.txt", "w") as f:
        for pmq_session in pmq_sessions:
            f.writelines(pmq_session+'\n')
    
datetime_object += timedelta(days = 7)

with open("next_session.txt", "w") as f:
    f.write(datetime_object.strftime("%Y-%m-%d"))