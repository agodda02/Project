import pytest
from question_answer import *
from Contribution import *

@pytest.fixture
def soup_1975():
    with open("test_data/example_1975.txt", "r") as f:
        data = f.read()
    return get_soup(data)  
    
@pytest.fixture
def soup_2022_06_22():
    with open("test_data/example_2022_06_22.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)

@pytest.fixture
def soup_2022_06_15():
    with open("test_data/example_2022_06_15.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)    

@pytest.fixture
def soup_1963():
    with open("test_data/example_1963.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)    

@pytest.fixture
def soup_1961():
    with open("test_data/example_1961.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)    

@pytest.fixture
def soup_1962_07_05():
    with open("test_data/example_1962_07_05.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)
    
@pytest.fixture
def soup_1980_04_24():
    with open("test_data/example_1980_04_24.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)    

def test_question(soup_1975):
    link = '1975-01-14/debates/e0279e7f-6655-463f-ae5a-e39aa443a117/OralAnswersToQuestions'
    contributions = soup_1975.find_all(class_ = 'debate-item-contributiondebateitem')
    test = Contribution(contributions[0], link)
    assert test.get_contributor() == "Mr. Biggs-Davison"
    assert test.get_paragraph() == "asked the Secretary of State for Defence whether he will make a statement about the progress of military operations in Northern Ireland."
    assert test.get_contribution_type() == "question"
    assert test.get_date() == date(1975, 1, 14)

def test_answer(soup_1975):
    link = '1975-01-14/debates/e0279e7f-6655-463f-ae5a-e39aa443a117/OralAnswersToQuestions'
    contributions = soup_1975.find_all(class_ = 'debate-item-contributiondebateitem')
    test = Contribution(contributions[126], link)
    assert test.get_contributor() == "The Prime Minister"
    assert test.get_paragraph() == "I did so on 9th December, Sir."
    assert test.get_contribution_type() == "answer"
    assert test.get_date() == date(1975, 1, 14)
    
def test_get_first_pm_contribution(soup_1975):
    first_pm_contribution_index = get_first_pm_contribution_index(soup_1975)
    assert first_pm_contribution_index == 126

def test_get_pmq_contributions_raw_1(soup_2022_06_22):
    assert len(get_pmq_contributions_raw(soup_2022_06_22)) == 63

def test_get_pmq_contributions_raw_2(soup_2022_06_15):
    assert len(get_pmq_contributions_raw(soup_2022_06_15)) == 67
    
def test_get_pmq_contributions(soup_2022_06_22):
    contributions = get_pmq_contributions_raw(soup_2022_06_22)
    link = '2022-06-22/debates/1825FDB2-5C11-4579-B1DA-94B80654D983/OralAnswersToQuestions'
    contribution_objects = get_pmq_contribution_objects(contributions, link)
    assert len(contribution_objects) == 63
    
    answers = 0
    questions = 0
    interruptions = 0
    
    for contribution in contribution_objects:
        if contribution.get_contribution_type() == 'answer':
            answers += 1
        if contribution.get_contribution_type() == 'question':
            questions += 1
        if contribution.get_contribution_type() == 'interruption':
            interruptions += 1
            
    assert interruptions == 6
    assert questions == 29
    assert answers == 28

def test_deal_with_interruption(soup_2022_06_22):
    contributions = get_pmq_contributions_raw(soup_2022_06_22)
    link = '2022-06-22/debates/1825FDB2-5C11-4579-B1DA-94B80654D983/OralAnswersToQuestions'
    previous_contribution = Contribution(contributions[9], link)
    contribution = Contribution(contributions[10], link)
    next_contribution = Contribution(contributions[11], link)    
    question = 'The Prime Minister has obviously not been to Wakefield recently. He has crashed the economy and he has put everybody’s tax up. The last Tory he sent up to Wakefield was convicted of a sexual assault. That is not much of a pitch, Prime Minister. Talking of people not up to the job, while the Transport Secretary spends his time working on his spreadsheet tracking the Prime Minister’s unpopularity, thousands of families have had their holiday flights cancelled, it takes forever to renew a driving licence or passport and now we have the biggest rail strike in 30 years. If the Prime Minister is genuine— If the Prime Minister is genuine about preventing strikes, will he tell this House how many meetings he or his Transport Secretary have had with rail workers this week to actually stop the strikes?'
    previous_contribution.concatenate_with(next_contribution.get_paragraph())
    assert previous_contribution.get_paragraph() == question

def test_get_questions_and_answers_1(soup_2022_06_22):
    contributions = get_pmq_contributions_raw(soup_2022_06_22)
    link = '2022-06-22/debates/1825FDB2-5C11-4579-B1DA-94B80654D##983/OralAnswersToQuestions'
    contribution_objects = get_pmq_contribution_objects(contributions, link)
    questions_and_answers = get_questions_and_answers(contribution_objects)
    questions = get_questions(questions_and_answers)
    answers = get_answers(questions_and_answers)
    assert len(questions_and_answers) == 54
    assert len(questions) == 27
    assert len(answers) == 27
    
def test_get_questions_and_answers_2(soup_2022_06_15):
    contributions = get_pmq_contributions_raw(soup_2022_06_15)
    link = '2022-06-15/debates/20D19FB5-2111-49A8-94A1-9E43AAC5CD38/OralAnswersToQuestions'
    contribution_objects = get_pmq_contribution_objects(contributions, link)
    questions_and_answers = get_questions_and_answers(contribution_objects)
    questions = get_questions(questions_and_answers)
    answers = get_answers(questions_and_answers)
    assert len(questions) == 26
    assert len(answers) == 26
        
def test_get_questions_and_answers_3(soup_1975):    
    contributions = get_pmq_contributions_raw(soup_1975)
    link = '1975-01-14/debates/e0279e7f-6655-463f-ae5a-e39aa443a117/OralAnswersToQuestions'
    contribution_objects = get_pmq_contribution_objects(contributions, link)
    questions_and_answers = get_questions_and_answers(contribution_objects)
    questions = get_questions(questions_and_answers)
    answers = get_answers(questions_and_answers)
    assert len(questions) == 13
    assert len(answers) == 13

def test_get_questions_and_answers_4(soup_1962_07_05):
    contributions = get_pmq_contributions_raw(soup_1962_07_05)
    link = '1962-07-05/debates/cf144f26-664f-4ef8-8f18-ba35e409bcfa/OralAnswersToQuestions'
    contribution_objects = get_pmq_contribution_objects(contributions, link)
    questions_and_answers = get_questions_and_answers(contribution_objects)
    questions = get_questions(questions_and_answers)
    answers = get_answers(questions_and_answers)
    assert len(questions) == 16
    assert len(answers) == 16
    
def test_get_questions_and_answers_5(soup_1980_04_24):
    contributions = get_pmq_contributions_raw(soup_1980_04_24)
    link = '1980-04-24/debates/7d7b15d8-398a-489e-94b0-01a685a4f205/OralAnswersToQuestions'
    contribution_objects = get_pmq_contribution_objects(contributions, link)
    questions_and_answers = get_questions_and_answers(contribution_objects)
    questions = get_questions(questions_and_answers)
    answers = get_answers(questions_and_answers)
    assert len(questions) == 16
    assert len(answers) == 16    
        
def test_get_question_answer_pairs(soup_1975):
    link = '1975-01-14/debates/e0279e7f-6655-463f-ae5a-e39aa443a117/OralAnswersToQuestions'
    question_answer_pairs = get_question_answer_pairs(soup_1975, link)
    assert len(question_answer_pairs) == 13
    
def test_get_question_answer_pairs_2(soup_1963):
    link = '1975-01-14/debates/e0279e7f-6655-463f-ae5a-e39aa443a117/OralAnswersToQuestions'
    question_answer_pairs = get_question_answer_pairs(soup_1963, link)
    assert len(question_answer_pairs) == 16
    
    question = "asked the Prime Minister if he will take steps to set up a Department of Disarmament with a senior Minister in charge of it."
    answer = "No, Sir. Disarmament is closely linked with the fundamental responsibilities of the Foreign Secretary and the Minister of Defence.  My hon. Friend the Minister of State for Foreign Affairs already has special responsibility, under the Foreign Secretary, for disarmament and devotes a very large part of his time to it."
    
    assert question_answer_pairs[10][0].get_paragraph() == question
    assert question_answer_pairs[10][1].get_paragraph() == answer
    
def test_regex():
    head = 'https://hansard.parliament.uk/Commons/'
    link = '1961-07-18/debates/adf428ba-7690-44bf-999c-635b980254fe/OralAnswersToQuestions'
    page = get_page(head + link)
    soup = get_soup(page)
    question_answer_pairs = get_question_answer_pairs(soup, link)    
    answer = 'My right hon. Friend the Lord Privy Seal has visited  Nicosia for this purpose, and had talks with Cyprus Ministers.'
    assert question_answer_pairs[2][1].get_paragraph() == answer