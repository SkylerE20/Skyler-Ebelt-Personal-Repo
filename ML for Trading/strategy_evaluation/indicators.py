"""
Skyler Ebelt
sebelt3
904077010

Indicators:
Bollinger Bands
PPI
Momentum
SMA
ROC
"""
from util import get_data
import numpy as np
import datetime as dt
import pandas as pd

#https://edstem.org/us/courses/70660/discussion/5939683
def bol_band(data, window = 20, type = 'Median'): #https://www.britannica.com/money/bollinger-bands-indicator
    """
    Accepts PRICE data
    """

    median = data.rolling(window).mean()
    standev = data.rolling(window).std()

    l_bol = median - (standev * 2)
    u_bol = median + (standev * 2)

    if type == 'Median':
        return median
    if type == 'Lower':
        return l_bol
    if type == 'Upper':
        return u_bol
    else:
        pass



def cci(data, window = 20): #https://en.wikipedia.org/wiki/Commodity_channel_index pulled equation from here

    """
    Accepts the ORDERS file then does the rest
    It looks awful but these arrays need to match the length of our data - weekends and - holidays
    to enable them to be plotted on the same chart
    """
    symbol = [data.iloc[0,-1]]
    start_date = data.index[0]
    end_date = data.index[-1]
    cci_high = pd.DataFrame(
        get_data(symbol, pd.date_range(start_date, end_date, freq="B"), addSPY=False, colname="High"))
    cci_low = pd.DataFrame(
        get_data(symbol, pd.date_range(start_date, end_date, freq="B"), addSPY=False, colname="Low"))
    cci_close = pd.DataFrame(
        get_data(symbol, pd.date_range(start_date, end_date, freq="B"), addSPY=False, colname="Adj Close"))

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

    cci_high.drop(index=hdates, axis=0, inplace=True, errors='ignore')
    cci_low.drop(index=hdates, axis=0, inplace=True, errors='ignore')
    cci_close.drop(index=hdates, axis=0, inplace=True, errors='ignore')

    cci_high = cci_high.to_numpy()
    cci_low = cci_low.to_numpy()
    cci_close = cci_close.to_numpy()

    typ_price = (cci_high + cci_low + cci_close) / 3

    sma = np.zeros(len(typ_price))
    md = np.zeros(len(typ_price))
    cci = np.zeros(len(typ_price))
    cci[:window - 1] = np.nan


    for i in range(window - 1, len(typ_price)):
        win = typ_price[i - (window - 1):i + 1]
        sma[i] = np.mean(win)
        md[i] = np.mean(np.abs(win - sma[i]))
        cci[i] = (typ_price[i] - sma[i]) / (0.015 * md[i])

    return cci


def sma(data, window = 20): #source: this is common sense, no?

    sma = data.rolling(window).mean()

    return sma


def roc(data, window = 20): #https://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    """
    Accepts price data NOT orders
    """

    data = data.pct_change(periods=window) * 100

    return data


def ppo(data, win1 = 9, win2 = 26):
    #https://www.investopedia.com/articles/investing/051214/use-percentage-price-oscillator-elegant-indicator-picking-stocks.asp
    #and
    #https://www.investopedia.com/terms/e/ema.asp
    """
    Again, price data not orders
    """
    data = data.copy()
    data = data.to_numpy()

    emas = np.zeros(len(data))
    emal= np.zeros(len(data))

    emas[win1 - 1] = np.mean(data[:win1])
    emal[win2 - 1] = np.mean(data[:win2])

    als = 2.0 / (win1 + 1)
    al = 2.0 / (win2 + 1)

    for i in range(win1, len(data)):
        emas[i] = data[i] * als + emas[i - 1] * (1 - als)
    for i in range(win2, len(data)):
        emal[i] = data[i] * al + emal[i - 1] * (1 - al)
    for i in range(win2, len(data)):
        data[i] = ((emas[i] - emal[i]) / emal[i]) * 100

    return data

def author():
  return 'sebelt3'

def studygroup(self):
    return "sebelt3"