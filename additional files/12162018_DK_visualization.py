# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 23:26:55 2018

@author: dkewon
"""
#installing packages and importing data
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt 

import matplotlib

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

##############################data visualization##########################
#import geoplotlib
#import pyglet
#geoplotlib.dots(district)
#geoplotlib.show()
import seaborn as sns
from collections import Counter
from matplotlib import pyplot 

#distirct id and population
f = plt.figure(1)
y = district['total_inhabitants']
x = district['district_id']
y_pos = np.arange(len(x))
plt.bar(y_pos, y, color=(0.2, 0.4, 0.6, 0.6))
# Custom Axis title
plt.xlabel('District ID', fontweight='bold', color = 'blue', fontsize='10', horizontalalignment='center')
plt.title('District vs Population')
plt.savefig('fig_'+str('district_avgsal_pop1')+'.png', dpi=200)
plt.show()

#district id and avg_salary
g = plt.figure(2)
y = district['avg_salary']
x = district['district_id']
y_pos = np.arange(len(x))
plt.bar(y_pos, y, color=(0.2, 0.4, 0.6, 0.6))
# Custom Axis title
plt.xlabel('District ID', fontweight='bold', color = 'red', fontsize='10', horizontalalignment='center')
plt.title('District vs Average Salary')
plt.savefig('fig_'+str('district_avgsal_pop2')+'.png', dpi=200)
plt.show()

#urban ratio
b = district['ratio_urban']
a = district['district_id']
y_pos = np.arange(len(a))
plt.bar(y_pos, b, color=(0.2, 0.4, 0.6, 0.6))
# Custom Axis title
plt.xlabel('District ID', fontweight='bold', color = 'red', fontsize='10', horizontalalignment='center')
plt.title('District vs Ratio of Urban Inhabitants ')
plt.savefig('fig_'+str('district_urbanratio')+'.png', dpi=200)
plt.show()




#unemp rate_trend
import plotly.plotly as py
import plotly.graph_objs as go


unemployment_rate95 = go.Scatter(
    x=district['district_id'],
    y=district['unemp_rate_95'],name='unemployment rate 95'
)
unemployment_rate96 = go.Scatter(
    x=district['district_id'],
    y=district['unemp_rate_96'],name='unemployment rate 96'
)
data = [unemployment_rate95, unemployment_rate96]
py.plot(data, filename='unemp')

#crime_number_trend-same-not very useful/important
crime95 = go.Scatter(
    x=district['district_id'],
    y=district['num_crimes95'],name='Number of Crimes 95'
)
crime96 = go.Scatter(
    x=district['district_id'],
    y=district['num_crimes96'],name='Number of Crimes 96'
)
data2 = [crime95, crime96]
py.plot(data2, filename='crime')


#Loan Amount vs. Monthly payment and Duration
df=pd.DataFrame({'x': loan['loan_amount'], 'y':loan['monthly_loan_payment'] , 'z': loan['loan_duration'] })
 
# Cut your window in 1 row and 2 columns, and start a plot in the first part
ax1=plt.subplot(121)
plt.plot( 'x', 'y', data=df, marker='o', alpha=0.4)
plt.xlabel("Loan Amount")
ax1.set_title('Loan Amount vs Monthly Payment')

# And now add something in the second part:
ax2=plt.subplot(122)
plt.plot( 'x','z', data=df, linestyle='none', marker='o', color="orange", alpha=0.3)
plt.xlabel("Loan Amount")
ax2.set_title('Loan Duration')
plt.savefig('fig_'+str('loan_monpayment_duration')+'.png', dpi=200)
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=5, hspace=None)

# frequency- loan status
loan_status_num=Counter(loan['loan_status'])
loan_status_freq = pd.DataFrame.from_dict(loan_status_num, orient='index')
loan_status_freq.plot(kind='bar')
plt.xlabel('Loan Status', fontweight='bold', color = 'blue', fontsize='10',horizontalalignment='center')
plt.xticks(rotation=30)
plt.savefig('fig_'+str('loan_status')+'.png', dpi=200)
plt.show()

#loan status vs avg loan amount
from astropy.table import Table, Column
loan2 = loan.drop(loan.columns[[0, 1]], axis=1)
Table([loan['loan_status'], loan['loan_amount']])
loan2[loan2['loan_status']=='A'].mean()
loan2[loan2['loan_status']=='B'].mean()
loan2[loan2['loan_status']=='C'].mean()
loan2[loan2['loan_status']=='D'].mean()

ax = loan2.groupby(by=['loan_status']).mean().plot.bar(legend=True)
ax.set_ylabel("Amount")
plt.xticks(rotation=30)
plt.savefig('fig_'+str('loan_status_amount')+'.png', dpi=200,bbox_inches="tight")


#DISP
disp['type'].value_counts().plot(kind='bar', subplots=True)
plt.savefig('fig_'+str('num_owner')+'.png', dpi=200,bbox_inches="tight")
plt.show()

#Combine datasets with client - more insights
byclient = pd.merge(client,district, how="outer", on="district_id")
byclient = pd.merge(byclient,disp, how="outer", on="client_id")
byclient = pd.merge(byclient,loan, how="outer", on="account_id")

# not everyone has loans 
byclientloan=Counter(byclient['loan_status'])
byclientloan_freq = pd.DataFrame.from_dict(byclientloan, orient='index')
graph=byclientloan_freq.plot(kind='bar')
plt.xlabel('Loan Status', fontweight='bold', color = 'blue', fontsize='10',horizontalalignment='center')
plt.xticks(rotation=30)
for p in graph.patches:
    graph.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
    
#graph.text(1, 2000, 'nan: 4542, C: 493, A: 258, B: 31, D: 45', fontsize=15)
plt.savefig('fig_'+str('num_borrowers')+'.png', dpi=200,bbox_inches="tight")
plt.show()