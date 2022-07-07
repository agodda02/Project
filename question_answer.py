from bs4 import BeautifulSoup
from Contribution import *

def get_soup(data):
    soup = BeautifulSoup(data, 'html.parser')
    return soup

def get_contributor(contribution):
    contributor_markup = contribution.find(class_ = "primary-text")
    contributor = contributor_markup.get_text().strip()
    return contributor

def get_first_pm_contribution_index(soup):
    contributions = soup.find_all(class_ = 'debate-item-contributiondebateitem')
    for i in range(len(contributions)):
        contributor = get_contributor(contributions[i])
        if contributor == "The Prime Minister":
            return i

def get_last_pm_contribution_index(soup):
    contributions = soup.find_all(class_ = 'debate-item-contributiondebateitem')
    last_pm_index = -1
    for i in range(len(contributions)):
        contributor = get_contributor(contributions[i])
        if contributor == "The Prime Minister":
            last_pm_index = i
            
    return last_pm_index
            
def get_first_pmq(soup):
    return get_first_pm_contribution_index(soup) - 1
    
def get_number_of_pm_contributions(soup):
    contributions = soup.find_all(class_ = 'debate-item-contributiondebateitem')
    start = get_first_pm_contribution_index(soup)
    count = 0
    for i in range(start, len(contributions)):
        contributor = get_contributor(contributions[i])
        if contributor == "The Prime Minister":
            count += 1
    
    return count
    
def get_pmq_contributions_raw(soup):
    contributions = soup.find_all(class_ = 'debate-item-contributiondebateitem')
    start = get_first_pm_contribution_index(soup) - 1
    end = get_last_pm_contribution_index(soup)+1
    return contributions[start:end]
    
def get_pmq_contribution_objects(contributions, link):
    contribution_objects = list()
    for contribution in contributions:
        contribution_objects.append(Contribution(contribution, link))
        
    return contribution_objects