import crawler_functions
from Contribution import *

import sys
sys.path.append("..")
import database as db

def get_all_contributions(soup):
    return soup.find_all(class_ = 'debate-item-contributiondebateitem')

def get_contributor(contribution):
    contributor_markup = contribution.find(class_ = "primary-text")
    contributor = contributor_markup.get_text().strip()
    return contributor

def get_first_pm_contribution_index(contributions):
    for i in range(len(contributions)):
        contributor = get_contributor(contributions[i])
        if contributor == "The Prime Minister":
            return i

def get_last_pm_contribution_index(contributions):
    last_pm_index = -1
    
    for i in range(len(contributions)):
        contributor = get_contributor(contributions[i])
        if contributor == "The Prime Minister":
            last_pm_index = i
            
    return last_pm_index
    
def get_pmq_contributions_raw(contributions):
    start = get_first_pm_contribution_index(contributions)-1
    end = get_last_pm_contribution_index(contributions)+1
    return contributions[start:end]
    
def get_pmq_contribution_objects(soup, link):
    contributions = get_all_contributions(soup)
    contributions_raw = get_pmq_contributions_raw(contributions)
    contribution_objects = list()
    
    for contribution in contributions_raw:
        contribution_objects.append(Contribution(contribution, link))    
    
    return contribution_objects
    
def get_questions_and_answers(contributions):
    questions_and_answers = list()
    skip_next_contribution = False
    last_contribution_type = ''
    
    for i in range(len(contributions)):
        contribution = contributions[i]
        if last_contribution_type != contribution.get_contribution_type():
            if skip_next_contribution:
                skip_next_contribution = False
                pass        
            elif contribution.get_contribution_type() == 'question':
                questions_and_answers.append(contribution)
            elif contribution.get_contribution_type() == 'answer':
                questions_and_answers.append(contribution)
            else:
                if contributions[i-1].get_contributor() == contributions[i+1].get_contributor():
                    contributions[i-1].concatenate_with(contributions[i+1].get_paragraph())
                    skip_next_contribution = True
        elif contribution.get_contribution_type() == 'question':
            questions_and_answers[-1] = contribution # this is replacing the last item in the list with the present contribution if two questions have been asked in a row
        
        last_contribution_type = contribution.get_contribution_type()
            
    return questions_and_answers

def get(questions_and_answers, contribution_type):
    contributions = list()
    previous_contribution_type = ''

    for i in range(len(questions_and_answers)):
        contribution = questions_and_answers[i]
        if contribution.get_contribution_type() == previous_contribution_type:
            questions_and_answers[i-1].concatenate_with(contribution.get_paragraph())        
        elif contribution.get_contribution_type() == contribution_type:
            contributions.append(contribution)
        previous_contribution_type = contribution.get_contribution_type()
    
    return contributions    

def get_questions(questions_and_answers):
    return get(questions_and_answers, 'question')

def get_answers(questions_and_answers):
    return get(questions_and_answers, 'answer')
    
def get_question_answer_pairs(soup, link):
    contribution_objects = get_pmq_contribution_objects(soup, link)
    questions_and_answers = get_questions_and_answers(contribution_objects)
    questions = get_questions(questions_and_answers)
    answers = get_answers(questions_and_answers)
    return list(zip(questions, answers))

def insert_list_into_database(question_answer_pairs):
    mydb = db.connect()
    mycursor = mydb.cursor()
    sql = "INSERT INTO qa_pairs (question, author, answer, date) VALUES (%s, %s, %s, %s)"
    
    for pair in question_answer_pairs:
        val = (pair[0].get_paragraph(), pair[0].get_contributor(), pair[1].get_paragraph(), pair[0].get_date())
        mycursor.execute(sql, val)
        mydb.commit()

    print("records inserted.")

with open("pmq_links.txt", "r") as f:
    url = 'https://hansard.parliament.uk/Commons/'
    lines = f.readlines()
    
    for line in lines:
        try:
            link = url + line
            page = crawler_functions.get_page(link)
            soup = crawler_functions.get_soup(page)
            question_answer_pairs = get_question_answer_pairs(soup, line)
            insert_list_into_database(question_answer_pairs)
        except:
            # The script fails to get the page source intermittently but not twice in a row
            # so it was sufficient to catch the error and just repeat the process exactly in the except clause
            link = url + line
            page = crawler_functions.get_page(link)
            soup = crawler_functions.get_soup(page)
            question_answer_pairs = get_question_answer_pairs(soup, line)
            insert_list_into_database(question_answer_pairs)
