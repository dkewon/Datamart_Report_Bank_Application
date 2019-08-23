# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 19:43:33 2018

@author: Chris
"""
import numpy as np               # Arrary
import pandas as pd              # DataFrame
import datetime
import matplotlib.pyplot as plt  # Visualization
import seaborn as sns 

basetable= pd.read_csv('./data/basetable.csv', sep=',', index_col=0)
print(list(basetable))
basetable.columns = basetable.columns.str.replace(r'.1', '')
basetable.columns = basetable.columns.str.replace(r'.2', '')
basetable.columns = basetable.columns.str.replace(r'.3', '')
print(list(basetable))
sns.set(style="darkgrid")

order_cols = [col for col in basetable.columns if 'order' in col]
for col in order_cols:
    g = sns.jointplot("client_age", col, data=basetable, kind="reg", color="m", height=7)