import pytest
from weekday import *

def test_thursday():
    date = '7 June 1962'
    assert get_day(date) == 'Thursday'
    
def test_tuesday():
    date = '7 May 1974'
    assert get_day(date) == 'Tuesday'
    