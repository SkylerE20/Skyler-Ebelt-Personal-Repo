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
#import TheoreticallyOptimalStrategy as tos
import datetime as dt  		  	   		 	 	 			  		 			     			  	 
import os  #I think this file came with this imported: I didnt import this, dont want to remove it, sorry if thats wrong
  		  	   		 	 	 			  		 			     			  	 
import numpy as np  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import pandas as pd  		  	   		 	 	 			  		 			     			  	 
from util import get_data, plot_data



def compute_portvals(  		  	   		 	 	 			  		 			     			  	 
    ordersdf = None,
    start_val=1000000,  		  	   		 	 	 			  		 			     			  	 
    commission=0,
    impact=0,
):  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    Computes the portfolio values.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		 	 	 			  		 			     			  	 
    :type orders_file: str or file object  		  	   		 	 	 			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		 	 	 			  		 			     			  	 
    :type start_val: int  		  	   		 	 	 			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		 	 	 			  		 			     			  	 
    :type commission: float  		  	   		 	 	 			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		 	 	 			  		 			     			  	 
    :type impact: float  		  	   		 	 	 			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		 	 	 			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		 	 	 			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		 	 	 			  		 			     			  	 
    # code should work correctly with either input  		  	   		 	 	 			  		 			     			  	 
    # TODO: Your code here

###############################################################################################
    """
    Read in data/General preprocessing 
    """

    start_date = ordersdf.index[0]
    end_date = ordersdf.index[-1]
    dates = pd.DataFrame(pd.date_range(start_date, end_date,freq = "B"))
    temp = pd.DataFrame(np.zeros(shape = (dates.shape[0],2)))
    temp.loc[:, 0] = dates
    symbols = np.unique(ordersdf['Symbol'].values).tolist()#orginally used .unique() but needed to add on the .tolist() otherwise it wasnt able to work with get_data

    adjc = pd.DataFrame(
        get_data(symbols, pd.date_range(start_date, end_date, freq="B"), addSPY=False, colname="Adj Close"))
    adjc.fillna(method='bfill', inplace=True)
    adjc.fillna(method='ffill', inplace=True)
    #adjc = adjc.astype(np.float64)

    #print(adjc_cci)
    #print(adjc)
###############################################################################################
    """
    Create a dataframe which will store stock allocations, 
    this will allow for computations of port_val
    """

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
              ]#Hell.

    cols = []
    for symbol in symbols:
        cols.append(symbol)
    cols.append('Cash')
    cols.append('Equity')
    cols.append('Total')

    adjc.drop(index=hdates, axis=0, inplace=True, errors='ignore')


###############################################################################################
    #rewrote code - simplified
    totals_per_date = pd.DataFrame(0,index=adjc.index, columns=symbols)
    cash = pd.Series(start_val, index=adjc.index)

    #iterate through each row/col in orders
    for date, col in ordersdf.iterrows():
        sym = col['Symbol']
        order_type = col['Order']
        qty = int(col['Shares'])

        price = adjc.loc[date, sym]

        if order_type == 'BUY':
            adj = price * (1 + impact)
            totals_per_date.loc[date:, sym] += qty
            ci = ((adj * qty) + commission)*-1
        elif order_type == 'SELL':
            adj= price * (1 - impact)
            totals_per_date.loc[date:, sym] -= qty
            ci = (adj * qty) - commission

        cash.loc[date:] += ci


    pos_val = totals_per_date.multiply(adjc)
    portval = pos_val.sum(axis=1) + cash



    portvals = pd.DataFrame(portval, columns=['Total'])
    pd.set_option('display.max_rows', None)

    return portvals


"""def test_code():
     		  	   		 	 	 			  		 			     			  	 
    #Helper function to test code  		  	   		 	 	 			  		 			     			  	 
     		  	   		 	 	 			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		 	 	 			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		 	 	 			  		 			     			  	 
    # Define input parameters  		  	   		 	 	 			  		 			     			  	 

    #of = "./orders/orders-06.csv"
    of = tos.tos()
    #of2 = tos.benchmark()
    #print(of2)
    #o = pd.read_csv(of, index_col='Date', parse_dates=True, na_values=['nan'])  # pulled this from project outline
    #o = o.sort_index(axis=0)

    sv = 100000
  		  	   		 	 	 			  		 			     			  	 
    # Process orders  		  	   		 	 	 			  		 			     			  	 
    portvals = compute_portvals(ordersdf = of, start_val=sv, impact=0, commission=0)
    if isinstance(portvals, pd.DataFrame):  		  	   		 	 	 			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		 	 	 			  		 			     			  	 
    else:  		  	   		 	 	 			  		 			     			  	 
        "warning, code did not return a DataFrame"

        # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		 	 	 			  		 			     			  	 
    orders = tos.tos()
    start_date = orders.index[0]
    end_date = orders.index[-1]
    #print(of)
    #print(portvals)


    syms = ['SPY']

    dates = pd.date_range(start_date, end_date)
    prices= get_data(syms, dates)
    #print(prices.iloc[0,0])

    dailyreturn = portvals.pct_change(1)
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [
        portvals[-1] - portvals[1],  # subtract last value from first to give cr
        np.mean(dailyreturn),  # average/mean of the daily return
        np.std(dailyreturn),  # standard deviation "" "" "" ""
        np.sqrt(252) * (np.mean(dailyreturn) / np.std(dailyreturn))
        # Sharpe ratio formula, pulled from lesson 01-07 8
    ]

    dailyreturn = prices.pct_change(1)

    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [
        prices.iloc[-1,0] - prices.iloc[1,0],  # subtract last value from first to give cr
        np.mean(dailyreturn),  # average/mean of the daily return
        np.std(dailyreturn),  # standard deviation "" "" "" ""
        np.sqrt(252) * (np.mean(dailyreturn) / np.std(dailyreturn))  # Sharpe ratio formula, pulled from lesson 01-07 8
    ]


    # Compare portfolio against $SPX
    '''print(f"Date Range: {start_date} to {end_date}")  		  	   		 	 	 			  		 			     			  	 
    print()  		  	   		 	 	 			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		 	 	 			  		 			     			  	 
    print()  		  	   		 	 	 			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		 	 	 			  		 			     			  	 
    print()  		  	   		 	 	 			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		 	 	 			  		 			     			  	 
    print()  		  	   		 	 	 			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		 	 	 			  		 			     			  	 
    print()  		  	   		 	 	 			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")'''

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

    return adjc"""

def benchmark(sym = ['JPM'],sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):
    #sd = dt.datetime(2008, 1, 1)
    dates = [sd, ed]
    bench = pd.DataFrame({'Order':['BUY', 'SELL'], 'Shares':[1000, 1000], 'Symbol':[str(sym[0]),str(sym[0])]}, index=dates)

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
