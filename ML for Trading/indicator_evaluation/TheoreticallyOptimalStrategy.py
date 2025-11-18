"""
Skyler Ebelt
sebelt3
904077010

Code for testing the theoretically optimal strategy.
"""
import datetime as dt

import numpy as np

import pandas as pd
from util import get_data, plot_data

def author():
  return 'sebelt3'

def studygroup(self):
    return "sebelt3"

def cond_df(data): #takes instances of multiple orders of the same type, finds the optimal order to keep and removes other orders
    data['order_change'] = (data['JPM'] != data['JPM'].shift(1))

    data['group'] = data['order_change'].cumsum()

    groups = data.groupby(['group', 'JPM'])

    cons = []
    #https://pandas.pydata.org/docs/reference/api/pandas.core.groupby.DataFrameGroupBy.idxmax.html
    #Also see idxmin
    for name, group in groups:
        order_type = name[1]

        if order_type == 'Buy':
            best_row = group.loc[group['b'].idxmin()].copy()
        else:
            best_row = group.loc[group['b'].idxmax()].copy()

        cons.append(best_row)

    con_df = pd.DataFrame(cons).drop(['order_change', 'group'], axis=1)

    con_df = con_df.sort_index()

    return con_df #Unlimted leverage = dont do this???? now nets $300k+ instead of about $200k

def get_local_extrema(data, window = 3, ret_data = "Maxima"): #Here I manually played with window vals to find the one that netted the largest portval
    maxima = data.rolling(window).max()
    minima = data.rolling(window).min()

    if ret_data == "Maxima":
        return maxima
    if ret_data == "Minima":
        return minima
    else:
        pass

def tos(sym = ['JPM'], sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):
    hdates = [
              dt.datetime(2008, 1, 21), dt.datetime(2008, 2, 18), dt.datetime(2008, 3, 21),
              dt.datetime(2008, 5, 26), dt.datetime(2008, 6, 19), dt.datetime(2008, 7, 4),
              dt.datetime(2008, 9, 1), dt.datetime(2007, 11, 27), dt.datetime(2008, 12, 25),
              dt.datetime(2009, 1, 1), dt.datetime(2009, 1, 19), dt.datetime(2009, 2, 16), dt.datetime(2009, 4, 10),
              dt.datetime(2009, 5, 25), dt.datetime(2009, 7, 3),
              dt.datetime(2009, 9, 7), dt.datetime(2009, 11, 26), dt.datetime(2009, 12, 25),
              ]

    adjc = pd.DataFrame(
        get_data(sym, pd.date_range(sd, ed, freq="B"), addSPY=False, colname="Adj Close"))

    adjc.drop(index=hdates, axis=0, inplace=True, errors='ignore')

    pd.set_option('display.max_rows', None)
    trade_max = get_local_extrema(adjc, ret_data="Maxima")
    trade_max = trade_max.drop_duplicates()

    trade_max_copy = get_local_extrema(adjc, ret_data="Maxima")
    trade_max_copy = trade_max_copy.drop_duplicates()

    trade_max.iloc[:, 0] = "SELL"

    trade_min = get_local_extrema(adjc, ret_data="Minima")
    trade_min = trade_min.drop_duplicates()

    trade_min_copy = get_local_extrema(adjc, ret_data="Minima")
    trade_min_copy = trade_min_copy.drop_duplicates()

    trade_min.iloc[:,0] = "BUY"

    trade_mm = pd.concat([trade_max, trade_min])
    trade_mm = trade_mm.sort_index()

    trade_mm_copy = pd.concat([trade_max_copy, trade_min_copy])
    trade_mm_copy = trade_mm_copy.sort_index()

    trade_mm = trade_mm.assign(b=trade_mm_copy)

    trade_mm = trade_mm.assign(c= 1000)

    trade_mm = trade_mm.assign(d=str(sym[0]))

    trade_mm.fillna(method='bfill', inplace=True)
    trade_mm.fillna(method='ffill', inplace=True)

    trade_final = cond_df(trade_mm) #trade_mm
    trade_final = trade_final.drop(['b'], axis=1)
    trade_final.rename(columns={'JPM':'Order', 'c':'Shares', 'd':'Symbol'}, inplace=True)
    #print(trade_final.head())
    return trade_final

def benchmark(sym = ['JPM'],sd = dt.datetime(2008, 1, 1), ed = dt.datetime(2009, 12, 31)):
    #sd = dt.datetime(2008, 1, 1)
    dates = [sd, ed]
    bench = pd.DataFrame({'Order':['BUY', 'SELL'], 'Shares':[1000, 1000], 'Symbol':[str(sym[0]),str(sym[0])]}, index=dates)

    return bench
if __name__ == "__main__":
    tos()