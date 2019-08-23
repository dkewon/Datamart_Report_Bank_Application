# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 23:26:55 2018

@author: dkewon
"""
#installing packages and importing data
import pandas as pd
import numpy as np
import datetime
import matplotlib
import matplotlib.pyplot as plt
account = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\account.asc', sep=';')
card = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\card.asc', sep=';')
client = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\client.asc', sep=';')
disp = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\disp.asc', sep=';')
order = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\order.asc', sep=';')
trans = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\trans.asc', sep=';', low_memory=False)
loan = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\loan.asc', sep=';')
district = pd.read_csv('C:\\Users\\dkewon\\Documents\\GitHub\\Python-Group-Project\\data\\data_berka\\district.asc', sep=';')

#Debbie_ demographics, loan and dipositions


#cleaning demographics (district data)
#Renaming columns
district.columns = ['district_id','district_name','region', 'total_inhabitants','num_munipalities_less_499','500_to_1999','2000_to_9999','greater_than_10000','num_cities','ratio_urban','avg_salary','unemp_rate_95','unemp_rate_96','enterpreneurs_per_1000','num_crimes95','num_crimes96']

print(district.dtypes)

#unemp_rate_95 and num_crimes95 can't be object. There is also a ? mark on numcrimes95 column. changing types and replacing ? with -1
def convert_question_marks(x, typ):
    if x == '?':
        return -1
    elif typ == 'float':
        return float(x)
    else:
        return int(x)
    
district['unemp_rate_95'] = district['unemp_rate_95'].apply(convert_question_marks, args=('float',))
district['num_crimes95'] = district['num_crimes95'].apply(convert_question_marks, args=('int',))

print(district.dtypes)
district.to_csv("cleaned_district.csv", index=False)

#cleaning loan dataset
# convert loan date to integer.

def get_year(x):
    return int(x/10000)

def get_mid2_dig(x):
    return int(x/100) % 100

def get_month(x):
    mth = get_mid2_dig(x)
    if mth > 50:
        return mth - 50
    else:
        return mth

def get_day(x):
    return x % 100

def convert_int_to_date(x):
    yr = get_year(x) + 1900
    mth = get_month(x)
    day = get_day(x)
    return datetime.datetime(yr, mth, day)

loan['date'] = loan['date'].map(convert_int_to_date)

# function to convert a date to days after start_date.
# reference dates.
start_date = datetime.datetime(1993,1,1)
end_date = datetime.datetime(2000,1,1)

def convert_date_to_days(x):
    td = x - start_date
    return td.days

loan['num_days_since_grant'] = loan['date'].map(convert_date_to_days)
del loan['date']

loan = loan.rename(columns={'amount': 'loan_amount', 'duration':'loan_duration', 'payments':'monthly_loan_payment', 'status':'loan_status'})
loan.to_csv("cleaned_loan.csv", index=False)

# cleaning dipositions
typecount = disp['type'].value_counts()
disp.to_csv("cleaned_disp.csv", index=False)