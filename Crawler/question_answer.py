from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from Contribution import *

import sys
sys.path.append("..")
import database as db

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
    
def get_questions_and_answers(contributions):
    questions_and_answers = list()
    skip_next_contribution = False
    last_contribution_type = ''
    
    for i in range(len(contributions)):
        contribution = contributions[i]
        if last_contribution_type != contribution.contribution_type:
            if skip_next_contribution:
                skip_next_contribution = False
                pass        
            elif contribution.contribution_type == 'question':
                questions_and_answers.append(contribution)
            elif contribution.contribution_type == 'answer':
                questions_and_answers.append(contribution)
            else:
                if contributions[i-1].contributor == contributions[i+1].contributor:
                    contributions[i-1].concatenate_with(contributions[i+1].paragraph)
                    skip_next_contribution = True
        elif contribution.contribution_type == 'question':
            questions_and_answers[-1] = contribution
        
        last_contribution_type = contribution.contribution_type
            
    return questions_and_answers

def get_questions(questions_and_answers):
    questions = list()
    previous_contribution_type = ''
    for i in range(len(questions_and_answers)):
        contribution = questions_and_answers[i]
        if contribution.contribution_type == previous_contribution_type:
            questions_and_answers[i-1].concatenate_with(contribution.paragraph)        
        elif contribution.contribution_type == 'question':
            questions.append(contribution)
        previous_contribution_type = contribution.contribution_type
    
    return questions

def get_answers(questions_and_answers):
    answers = list()
    previous_contribution_type = ''
    for i in range(len(questions_and_answers)):
        contribution = questions_and_answers[i]
        if contribution.contribution_type == previous_contribution_type:
            questions_and_answers[i-1].concatenate_with(contribution.paragraph)        
        elif contribution.contribution_type == 'answer':
            answers.append(contribution)
        previous_contribution_type = contribution.contribution_type
    
    return answers
    
def get_question_answer_pairs(soup, link):
    contributions = get_pmq_contributions_raw(soup)
    contribution_objects = get_pmq_contribution_objects(contributions, link)
    questions_and_answers = get_questions_and_answers(contribution_objects)
    questions = get_questions(questions_and_answers)
    answers = get_answers(questions_and_answers)
    return list(zip(questions, answers))

def insert_list_into_database(question_answer_pairs):
    mydb = db.connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO qa_pairs (question, author, answer, date) VALUES (%s, %s, %s, %s)"
    
    for pair in question_answer_pairs:
        val = (pair[0].paragraph, pair[0].contributor, pair[1].paragraph, pair[0].date)
        mycursor.execute(sql, val)

        mydb.commit()

    print("records inserted.")

with open("pmq_links.txt", "r") as f:
    url = 'https://hansard.parliament.uk/Commons/'
    lines = f.readlines()
    
    for line in lines:
        link = url + line
        page = get_page(link)
        soup = get_soup(page)
        question_answer_pairs = get_question_answer_pairs(soup, line)
        insert_list_into_database(question_answer_pairs)
    
