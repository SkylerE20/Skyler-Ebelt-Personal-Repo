""""""
"""MC2-P1: Market simulator.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	 	 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	 	 			  		 			     			  	 
All Rights Reserved  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	 	 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	 	 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	 	 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	 	 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	 	 			  		 			     			  	 
or edited.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	 	 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	 	 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	 	 			  		 			     			  	 
GT honor code violation.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
Student Name: Skyler Ebelt  		  	   		 	 	 			  		 			     			  	 
GT User ID: sebelt3   	 	   		 	 	 			  		 			     			  	 
GT ID: 904077010 		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 

"""
This code has been modified from project 5 to accept a df rather than read a file to 
produce a df. I cleaned up the file as well so there will be discrepancies in this file from
the project 5 submission, however everything else has been preserved and is essentially the same file
"""

import datetime as dt  		  	   		 	 	 			  		 			     			  	 
import os  #I think this file came with this imported: I didnt import this, dont want to remove it, sorry if thats wrong
  		  	   		 	 	 			  		 			     			  	 
import numpy as np  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import pandas as pd  		  	   		 	 	 			  		 			     			  	 
from util import get_data, plot_data


def compute_portvals(
        ordersdf=None,
        start_val=1000000,
        commission=0,
        impact=0,
):
    """Computes the portfolio values."""
    # This is the function the autograder will call to test your code

    # Read in data/General preprocessing
    start_date = ordersdf.index[0]
    end_date = ordersdf.index[-1]
    dates = pd.DataFrame(pd.date_range(start_date, end_date, freq="B"))
    temp = pd.DataFrame(np.zeros(shape=(dates.shape[0], 2)))
    temp.loc[:, 0] = dates

    if 'Symbol' in ordersdf.columns:
        symbols = np.unique(ordersdf['Symbol'].values).tolist()
    else:
        # In this case, symbol is the column name
        symbols = ordersdf.columns.tolist()

    adjc = pd.DataFrame(
        get_data(symbols, pd.date_range(start_date, end_date, freq="B"), addSPY=False, colname="Adj Close"))
    adjc.fillna(method='bfill', inplace=True)
    adjc.fillna(method='ffill', inplace=True)

    # Drop holiday dates
    hdates = [dt.datetime(2007, 1, 20), dt.datetime(2007, 2, 19),
              # ... other dates as in your original code
              dt.datetime(2012, 9, 3), dt.datetime(2012, 11, 22), dt.datetime(2012, 12, 25)]

    adjc.drop(index=hdates, axis=0, inplace=True, errors='ignore')

    # Initialize portfolio dataframe
    totals_per_date = pd.DataFrame(0, index=adjc.index, columns=symbols)
    cash = pd.Series(start_val, index=adjc.index)

    # IMPORTANT FIX: Iterate through orders and only process if date exists in adjc
    for date, col in ordersdf.iterrows():
        # Skip dates that don't exist in our price data
        if date not in adjc.index:
            continue

        sym = col['Symbol']
        order_type = col['Order']
        qty = int(col['Shares'])

        price = adjc.loc[date, sym]

        if order_type == 'BUY':
            adj = price * (1 + impact)
            totals_per_date.loc[date:, sym] += qty
            ci = ((adj * qty) + commission) * -1
        elif order_type == 'SELL':
            adj = price * (1 - impact)
            totals_per_date.loc[date:, sym] -= qty
            ci = (adj * qty) - commission

        cash.loc[date:] += ci

    pos_val = totals_per_date.multiply(adjc)
    portval = pos_val.sum(axis=1) + cash

    portvals = pd.DataFrame(portval, columns=['Total'])
    pd.set_option('display.max_rows', None)

    return portvals

def get_adjc(sym = ['JPM'], sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):#Need to get polished adjc data for indicators, I'm lazy and dont wanna change marketsim except for duplicating these functions to allow for ind calcs
    hdates = [dt.datetime(2007, 1, 20), dt.datetime(2007, 2, 19),
              dt.datetime(2007, 3, 21), dt.datetime(2007, 4, 6),
              dt.datetime(2007, 5, 28), dt.datetime(2007, 7, 4),
              dt.datetime(2007, 9, 3), dt.datetime(2007, 11, 22), dt.datetime(2007, 12, 25),
              dt.datetime(2008, 1, 21), dt.datetime(2008, 2, 18), dt.datetime(2008, 3, 21),
              dt.datetime(2008, 5, 26), dt.datetime(2008, 6, 19), dt.datetime(2008, 7, 4),
              dt.datetime(2008, 9, 1), dt.datetime(2007, 11, 27), dt.datetime(2008, 12, 25),
              dt.datetime(2009, 1, 1), dt.datetime(2009, 1, 19), dt.datetime(2009, 2, 16), dt.datetime(2009, 4, 10),
              dt.datetime(2009, 5, 25), dt.datetime(2009, 7, 3),
              dt.datetime(2009, 9, 7), dt.datetime(2009, 11, 26), dt.datetime(2009, 12, 25),
              dt.datetime(2010, 1, 1), dt.datetime(2010, 1, 18), dt.datetime(2010, 2, 15), dt.datetime(2010, 4, 2),
              dt.datetime(2010, 5, 31), dt.datetime(2010, 7, 5),
              dt.datetime(2010, 9, 6), dt.datetime(2010, 11, 25), dt.datetime(2010, 12, 24),
              dt.datetime(2011, 1, 17), dt.datetime(2011, 2, 21), dt.datetime(2011, 4, 22),
              dt.datetime(2011, 5, 30), dt.datetime(2011, 7, 4),
              dt.datetime(2011, 9, 5), dt.datetime(2011, 11, 24), dt.datetime(2011, 12, 26),
              dt.datetime(2012, 1, 16), dt.datetime(2012, 2, 20), dt.datetime(2012, 4, 6),
              dt.datetime(2012, 5, 28), dt.datetime(2012, 7, 4),
              dt.datetime(2012, 9, 3), dt.datetime(2012, 11, 22), dt.datetime(2012, 12, 25)
              ]  # Hell.

    adjc = pd.DataFrame(
        get_data(sym, pd.date_range(sd, ed, freq="B"), addSPY=False, colname="Adj Close"))
    adjc.fillna(method='bfill', inplace=True)
    adjc.fillna(method='ffill', inplace=True)

    adjc.drop(index=hdates, axis=0, inplace=True, errors='ignore')

    return adjc


def benchmark(sym = ['JPM'],sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):
    #sd = dt.datetime(2008, 1, 1)
    dates = [sd, ed]
    bench = pd.DataFrame({'Order':['BUY', 'SELL'], 'Shares':[1000, 1000], 'Symbol':[str(sym[0]),str(sym[0])]}, index=dates)


    return bench

def author():
    """  		  	   		 	 	 			  		 			     			  	 
    :return: The GT username of the student  		  	   		 	 	 			  		 			     			  	 
    :rtype: str  		  	   		 	 	 			  		 			     			  	 
    """
    return "sebelt3"  # Change this to your user ID

def studygroup(self):
    return "sebelt3"

if __name__ == "__main__":  		  	   		 	 	 			  		 			     			  	 
    pass
