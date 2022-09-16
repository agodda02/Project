import pytest
from datetime import date, datetime, timedelta
from get_date import *

def test_get_date():
    datefrom = date(2022, 9, 1)
    dateto = date(2022, 9, 6)
    target_date = get_nearest_date(datefrom, dateto)
    
    db_date = date(2022, 9, 7)
    assert db_date == target_date