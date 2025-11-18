""""""
"""MC1-P2: Optimize a portfolio.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
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
  		  	   		 	 	 			  		 			     			  	 
Student Name: Skyler Ebelt (replace with your name)  		  	   		 	 	 			  		 			     			  	 
GT User ID: sebelt3 (replace with your User ID)  		  	   		 	 	 			  		 			     			  	 
GT ID: 904077010(replace with your GT ID)  		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import datetime as dt  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import numpy as np  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
import matplotlib.pyplot as plt  		  	   		 	 	 			  		 			     			  	 
import pandas as pd  		  	   		 	 	 			  		 			     			  	 
from util import get_data, plot_data
import scipy.optimize as sco
  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
# This is the function that will be tested by the autograder  		  	   		 	 	 			  		 			     			  	 
# The student must update this code to properly implement the functionality
def optimize_portfolio(  		  	   		 	 	 			  		 			     			  	 
    sd=dt.datetime(2008, 1, 1),  		  	   		 	 	 			  		 			     			  	 
    ed=dt.datetime(2009, 1, 1),  		  	   		 	 	 			  		 			     			  	 
    syms=["GOOG", "AAPL", "GLD", "XOM"],  		  	   		 	 	 			  		 			     			  	 
    gen_plot=False,  		  	   		 	 	 			  		 			     			  	 
):  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		 	 	 			  		 			     			  	 
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		 	 	 			  		 			     			  	 
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		 	 	 			  		 			     			  	 
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		 	 	 			  		 			     			  	 
    statistics.  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		 	 	 			  		 			     			  	 
    :type sd: datetime  		  	   		 	 	 			  		 			     			  	 
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		 	 	 			  		 			     			  	 
    :type ed: datetime  		  	   		 	 	 			  		 			     			  	 
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		 	 	 			  		 			     			  	 
        symbol in the data directory)  		  	   		 	 	 			  		 			     			  	 
    :type syms: list  		  	   		 	 	 			  		 			     			  	 
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		 	 	 			  		 			     			  	 
        code with gen_plot = False.  		  	   		 	 	 			  		 			     			  	 
    :type gen_plot: bool  		  	   		 	 	 			  		 			     			  	 
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		 	 	 			  		 			     			  	 
        standard deviation of daily returns, and Sharpe ratio  		  	   		 	 	 			  		 			     			  	 
    :rtype: tuple  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)  		  	   		 	 	 			  		 			     			  	 
    prices_all = get_data(syms, dates)  # automatically adds SPY  		  	   		 	 	 			  		 			     			  	 
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
    normpricesspy = prices_SPY/prices_SPY[0]
    n = len(syms)
    prices= prices/prices.iloc[0,:]
  		  	   		 	 	 			  		 			     			  	 
    # find the allocations for the optimal portfolio  		  	   		 	 	 			  		 			     			  	 
    # note that the values here ARE NOT meant to be correct for a test case
    # add code here to find the allocations


    initallocs = [1/n] * n

    for i in range(n):
        prices.iloc[:,i] *= initallocs[i]

    totaldaily = (prices.sum(axis=1))
    dailyreturn = totaldaily.pct_change(1) #pandas functionality and documentation proves to be incredibly helpful here: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pct_change.html this functions measures net change from last entry

    cr, adr, sddr, sr = [
        totaldaily[-1] - totaldaily[1], #subtract last value from first to give cr
        np.mean(dailyreturn), #average/mean of the daily return
        np.std(dailyreturn), #standard deviation "" "" "" ""
        np.sqrt(252) * (np.mean(dailyreturn) / np.std(dailyreturn)) #Sharpe ratio formula, pulled from lesson 01-07 8
    ]  # add code here to compute stats

    cons = {"type": "eq", "fun": lambda initallocs: 1.0 - np.sum(initallocs)} #used the example on the project 2 report rubric to create this
    bo = tuple((0.0,1.0) for i in range(n))

    allocs = sco.minimize(calculatesharpe, initallocs, method="SLSQP", args = prices, constraints=cons, bounds= bo).x #see previous note


    # Get daily portfolio value
    port_val = prices.sum(axis = 1)  # add code here to compute daily portfolio values
  		  	   		 	 	 			  		 			     			  	 
    # Compare daily portfolio value with SPY using a normalized plot  		  	   		 	 	 			  		 			     			  	 
    if gen_plot:  		  	   		 	 	 			  		 			     			  	 
        # add code to plot here  		  	   		 	 	 			  		 			     			  	 
        df_temp = pd.concat(  		  	   		 	 	 			  		 			     			  	 
            [port_val, normpricesspy], keys=["Portfolio", "SPY"], axis=1
        )
        df_temp.plot()
        plt.xlabel("Date")
        plt.ylabel("Price: Normalized")
        plt.title("Portfolio vs SPY Performance")
        plt.grid(True)
        #plt.show()
        plt.savefig("figure1.png")
        pass  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    return allocs, cr, adr, sddr, sr

    # Establish sharpe ratio, then optimize fun to find ideal allocs:
    #This will be called by sco.minimizer
def calculatesharpe(allocs,prices):
    prices = prices/prices.iloc[0,:] #borrowed calculations from above
    prices *= allocs
    totaldaily = (prices.sum(axis=1))
    dailyreturn = totaldaily.pct_change(1)
    cr, adr, sddr, sr = [
        totaldaily[-1] - totaldaily[1],  # subtract last value from first to give cr
        np.mean(dailyreturn),  # average/mean of the daily return
        np.std(dailyreturn),  # standard deviation "" "" "" ""
        np.sqrt(252) * (np.mean(dailyreturn) / np.std(dailyreturn))  # Sharpe ratio formula, pulled from lesson 01-07 8
    ]
    return -sr #return inverse

def test_code():  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
    This function WILL NOT be called by the auto grader.  		  	   		 	 	 			  		 			     			  	 
    """  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD", "JPM"]
  		  	   		 	 	 			  		 			     			  	 
    # Assess the portfolio  		  	   		 	 	 			  		 			     			  	 
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		 	 	 			  		 			     			  	 
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )
    print()
    # Print statistics
    print(f"Start Date: {start_date}")  		  	   		 	 	 			  		 			     			  	 
    print(f"End Date: {end_date}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Symbols: {symbols}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Allocations:{allocations}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Sharpe Ratio: {sr}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Average Daily Return: {adr}")  		  	   		 	 	 			  		 			     			  	 
    print(f"Cumulative Return: {cr}")

  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
if __name__ == "__main__":  		  	   		 	 	 			  		 			     			  	 
    # This code WILL NOT be called by the auto grader  		  	   		 	 	 			  		 			     			  	 
    # Do not assume that it will be called  		  	   		 	 	 			  		 			     			  	 
    test_code()  		  	   		 	 	 			  		 			     			  	 
