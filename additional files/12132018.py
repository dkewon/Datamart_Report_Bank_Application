# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 23:26:55 2018

@author: dkewon
"""
import pandas as pd
account = pd.read_csv('./data_berka/account.asc', sep=';')
card = pd.read_csv('./data_berka/card.asc', sep=';')
client = pd.read_csv('./data_berka/client.asc', sep=';')
disp = pd.read_csv('./data_berka/disp.asc', sep=';')
order = pd.read_csv('./data_berka/order.asc', sep=';')
trans = pd.read_csv('./data_berka/trans.asc', sep=';', low_memory=False)
loan = pd.read_csv('./data_berka/loan.asc', sep=';')
district = pd.read_csv('./data_berka/district.asc', sep=';')
import numpy as np

#merging based on account_id (two datasets at a time)
accountid_data = pd.merge(loan, order, how="outer", on="account_id")
accountid_data = pd.merge(accountid_data, trans, how="outer", on="account_id")
accountid_data = pd.merge(accountid_data, account, how="outer", on="account_id")
accountid_data = pd.merge(accountid_data, disp, how="outer", on="account_id")

#changing district column names 
district.columns = ['district_id','district name','region', 'total_inhabitants','less_than_499','500_to_1999','2000_to_9999','less_than_10000','cities','ratiourban','avgsalary','unemployment_rate_95','unemployment_rate_96','enterpreneurs_per_1000','crimes95','crimes96']

#merging based on district_id
districtid_data = pd.merge(district, client, how="outer", on="district_id")

#Length of credit history, Income,Payment history,Credit utilization,Current Loan...