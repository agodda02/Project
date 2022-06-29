import pytest
from bs4 import BeautifulSoup
from Contribution import *

@pytest.fixture
def soup():
    with open("example.txt", "r") as f:
        data = f.read()
    soup = BeautifulSoup(data, 'html.parser')
    return soup  

def test_question(soup):
    contributions = soup.find_all(class_ = 'debate-item-contributiondebateitem')
    test = Contribution(contributions[0])
    assert test.contributor == "Mr. Ian Taylor"
    assert test.paragraph == "To ask the Prime Minister if he will list his official engagements for Wednesday 21 May. [340]"
    assert test.question_or_answer == "question"

def test_answer(soup):
    contributions = soup.find_all(class_ = 'debate-item-contributiondebateitem')
    test = Contribution(contributions[3])
    assert test.contributor == "The Prime Minister"
    assert test.paragraph == "I first have to say yes, indeed, we have had a busy day because this Government, unlike the last Government, are governing in the interests of the people of this country. Secondly, the windfall tax will not harm pensioners at all. What did, however, harm pensioners was the last Government's imposition of VAT on fuel. It is precisely for that reason that we propose cutting it."
    assert test.question_or_answer == "answer"
    