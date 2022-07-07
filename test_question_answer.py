import pytest
from question_answer import *
from Contribution import *

@pytest.fixture
def soup_1975():
    with open("example_1975.txt", "r") as f:
        data = f.read()
    return get_soup(data)  
    
@pytest.fixture
def soup_2022_06_22():
    with open("example_2022_06_22.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)

@pytest.fixture
def soup_2022_06_15():
    with open("example_2022_06_15.txt", "r", encoding="utf8") as f:
        data = f.read()
    return get_soup(data)    

def test_question(soup_1975):
    link = '1975-01-14/debates/e0279e7f-6655-463f-ae5a-e39aa443a117/OralAnswersToQuestions'
    contributions = soup_1975.find_all(class_ = 'debate-item-contributiondebateitem')
    test = Contribution(contributions[0], link)
    assert test.contributor == "Mr. Biggs-Davison"
    assert test.paragraph == "asked the Secretary of State for Defence whether he will make a statement about the progress of military operations in Northern Ireland."
    assert test.contribution_type == "question"
    assert test.date == date(1975, 1, 14)

def test_answer(soup_1975):
    link = '1975-01-14/debates/e0279e7f-6655-463f-ae5a-e39aa443a117/OralAnswersToQuestions'
    contributions = soup_1975.find_all(class_ = 'debate-item-contributiondebateitem')
    test = Contribution(contributions[126], link)
    assert test.contributor == "The Prime Minister"
    assert test.paragraph == "I did so on 9th December, Sir."
    assert test.contribution_type == "answer"
    assert test.date == date(1975, 1, 14)
    
def test_get_first_pm_contribution(soup_1975):
    first_pm_contribution_index = get_first_pm_contribution_index(soup_1975)
    assert first_pm_contribution_index == 126
    
def test_get_first_pmq(soup_1975):
    assert get_first_pmq(soup_1975) == 125

def test_get_number_of_pm_contributions(soup_2022_06_22):
    assert get_number_of_pm_contributions(soup_2022_06_22) == 28

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
        if contribution.contribution_type == 'answer':
            answers += 1
        if contribution.contribution_type == 'question':
            questions += 1
        if contribution.contribution_type == 'interruption':
            interruptions += 1
            
    assert interruptions == 6
    assert questions == 29    # Presumably an interruption broke a question into two contributions
    assert answers == 28
    

    
# def test_deal_with_speaker_pm_interruption(soup_22):
    # contributions = get_contributions(soup_22)
    
    # answer = 'This is the Government who love the railways and who invest in the railways. We are putting £96 billion into the integrated railway plan. I am proud to have built Crossrail, by the way, and we are going to build Northern Powerhouse Rail, but we have got to modernise our railways. It is a disgrace, when we are planning to make sure that we do not have ticket offices that sell fewer than one ticket every hour, that yesterday the right hon. and learned Gentleman had 25 Labour MPs out on the picket line, defying instructions—[Interruption.] There were 25 Labour MPs and the shadow deputy leader out on the picket line, backing the strikers, while we back the strivers.'
    