"""
Skyler Ebelt
sebelt3
904077010

Code for testing output
"""
from matplotlib.lines import lineStyles

import marketsimcode as mkt
import TheoreticallyOptimalStrategy as tos
import indicators as ind
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import pandas as pd

from util import get_data, plot_data

def author():
  return 'sebelt3'

def studygroup(self):
    return "sebelt3"

def test_code():
    adjc = mkt.get_adjc()

    orders_test = tos.tos()
    orders_bench = tos.benchmark()

    pv_test = mkt.compute_portvals(ordersdf = orders_test, start_val= 100000, impact=0, commission=0)
    pv_bench = mkt.compute_portvals(ordersdf = orders_bench, start_val= 100000, impact=0, commission=0)

    pv_test = pv_test / pv_test.iloc[0]
    pv_bench = pv_bench / pv_bench.iloc[0]

    pv_test_f = pv_test.to_numpy()
    pv_bench_f = pv_bench.to_numpy()

    plt.clf()

    plt.plot(pv_test.index,  pv_test_f, label='TOS Portfolio Values', color='purple')
    plt.plot( pv_bench.index, pv_bench_f, label='Benchmark Portfolio Values', color='red')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value - Normalized')
    #plt.show()
    plt.savefig('Figure0.png')

    bbm = ind.bol_band(adjc, type = 'Median')
    bbu = ind.bol_band(adjc, type='Upper')
    bbl = ind.bol_band(adjc, type='Lower')

    bbm.fillna(method='bfill', inplace=True)
    bbm.fillna(method='ffill', inplace=True)

    bbu.fillna(method='bfill', inplace=True)
    bbu.fillna(method='ffill', inplace=True)

    bbl.fillna(method='bfill', inplace=True)
    bbl.fillna(method='ffill', inplace=True)

    plt.clf()
    plt.title('Price o Ticker W/ Bollinger Bands')
    plt.plot(adjc.index, adjc, label='Adj Close')
    plt.plot(adjc.index, bbm, label='BB Mean')
    plt.plot(adjc.index, bbu, label='BB Upper')
    plt.plot(adjc.index, bbl, label='BB Lower')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Ticker Value ($JPM)')
    #plt.show()
    #plt.savefig('Figure1.png')
#https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html for subplots

    plt.clf()
    cci = pd.DataFrame(ind.cci(orders_test))
    cci.fillna(method='bfill', inplace=True)
    cci.fillna(method='ffill', inplace=True)
    adjc2 = adjc.drop(adjc.index[0])
    cci.index = adjc2.index

    fig, (ax, ax1) = plt.subplots(2)
    fig.suptitle('Price of Ticker W/ CCI')
    #plt.plot(adjc2.index, adjc2.iloc[:,0], label='Adj Close')
    ax.plot(adjc.index, adjc, label='Adj Close')
    ax.legend(loc='best')
    ax.set_xlabel('Date')
    ax.set_ylabel('Ticker Value ($JPM)')
    ax1.plot(adjc2.index, cci, label='CCI')
    med = np.median(cci)

    ax1.axhline(y = med, color='r', ls = '--',label='Median')
    ax1.axhline(y=100, color='r', ls = '--',label='Upper Bound')
    ax1.axhline(y=-100, color='r', ls = '--',label='Lower Bound')
    ax1.legend()
    ax1.set_xlabel('Date')
    ax1.set_ylabel('CCI')
    #plt.show()
    #plt.savefig('Figure2.png')

    plt.clf()
    plt.title('Price of Ticker W/ SMA')
    sma = pd.DataFrame(ind.sma(adjc))
    plt.plot(adjc.index, adjc, label='Adj Close')
    plt.plot(adjc.index, sma, label='SMA')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Price of Ticker ($JPM)')
    #plt.show()
    #plt.savefig('Figure3.png')

    plt.clf()
    roc = ind.roc(adjc)
    fig, (ax, ax1) = plt.subplots(2)
    fig.suptitle('Price of Ticker W/ ROC')
    ax1.plot(adjc.index, roc, label='ROC')
    med = np.median(cci)
    ax1.axhline(y=med, color='r', ls = '--', label='Median')
    ax1.legend()
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Rate of Change (ROC)')
    ax.plot(adjc.index, adjc, label='Adjusted Close')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price of Ticker ($JPM)')
    #plt.show()
    #plt.savefig('Figure4.png')

    plt.clf()
    ppo = ind.ppo(adjc)
    fig, (ax, ax1) = plt.subplots(2)
    fig.suptitle('Price of Ticker W/ PPO')
    ax1.plot(adjc.index, ppo, label='PPO')
    ax1.legend()
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price of Ticker ($JPM)')
    ax.plot(adjc.index, adjc, label='Adjusted Close')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price of Ticker ($JPM)')
    #plt.show()
    #plt.savefig('Figure5.png')

    return

if __name__ == '__main__':
    test_code()