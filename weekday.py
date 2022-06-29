import pandas as pd

def get_day(date):
    month_dict = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 
              'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    items = date.split()
    converted_date = str(items[2]) + '-' + str(month_dict[items[1]]) + '-' + str(items[0])
    temp = pd.Timestamp(converted_date)
    return temp.day_name()