#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 19:56:01 2020

@author: panjiasheng
"""

from pandas_datareader import data as pdr
import numpy as np
import pandas as pd
import statsmodels
from statsmodels.tsa.stattools import coint
import matplotlib.pyplot as plt

m = {
     'pair1': ['COKE','PEP'],
     'pair2': ['DPZ','PZZA']
     }

start_date = '2010-01-01'
end_date = '2020-09-10'

class ETF:
    
    def __init__(self, code:str, start_date:str, end_date:str):
        self.code = code
        self.start_date = start_date
        self.end_date = end_date
    
    def prices(self):
        data = pdr.get_data_yahoo(self.code, start=self.start_date, end=self.end_date)
        data = data.reset_index()
        self.data = data.loc[:, ['Date', 'Close']]
        return self
    
    def prices_data(self):
        self.prices()
        data = self.data
        data[self.code] = data['Close']
        data = (data.dropna(axis=0, how='any')).reset_index(drop=True)
        data = data.drop(columns='Close')
        return data
    
    def cal_daily_return(self):
        self.prices()
        data = self.data
        data[self.code] = data['Close']/data['Close'].shift(1)-1
        data = (data.dropna(axis=0, how='any')).reset_index(drop=True)
        data = data.drop(columns='Close')
        return data
    
def all_returns(start = start_date, end = end_date):
    '''This returns all returns for ETF
    '''
    etf = ETF('SPY', start, end)
    df = etf.cal_daily_return()
    
    for k, v in m.items():
        for i in v:
            temp = ETF(i, start, end)
            new = temp.cal_daily_return()
            # df = pd.DataFrame(new)
            df = pd.merge(left= df, right=new,left_index = False, how='left')
    df = df.drop(columns = ['SPY'])
    return df



if __name__ == '__main__':
    print(all_returns())
    # etf = ETF('SPY', start, end)
    # df = etf.cal_daily_return()
    
    # code_list = ['XLB', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY']   
    # for code in code_list:
    #     temp = ETF(code, start, end)
    #     new = temp.cal_daily_return()
    #     df = pd.merge(left= df, right=new, how='left')
    # return df












