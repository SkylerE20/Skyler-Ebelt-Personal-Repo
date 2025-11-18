""""""  		  	   		 	 	 			  		 			     			  	 
"""  		  	   		 	 	 			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		 	 	 			  		 			     			  	 
  		  	   		 	 	 			  		 			     			  	 
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
  		  	   		 	 	 			  		 			     			  	 
import datetime as dt
import numpy as np
import random
from BagLearner import BagLearner
from RTLearner import RTLearner
import indicators as ind


import pandas as pd  		  	   		 	 	 			  		 			     			  	 
from util import get_data

def author():
  return 'sebelt3'

def studygroup():
    return "sebelt3"
  		  	   		 	 	 			  		 			     			  	 
class StrategyLearner(object):
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		 	 	 			  		 			     			  	 
        """  		  	   		 	 	 			  		 			     			  	 
        Constructor method  		  	   		 	 	 			  		 			     			  	 
        """  		  	   		 	 	 			  		 			     			  	 
        self.verbose = verbose  		  	   		 	 	 			  		 			     			  	 
        self.impact = impact  		  	   		 	 	 			  		 			     			  	 
        self.commission = commission
        self.learner = BagLearner(
            learner=RTLearner,
            kwargs = {"leaf_size": 8},
            bags = 40,
            boost = False,
            verbose = verbose
        )

    def add_evidence(
            self,
            symbol="IBM",
            sd=dt.datetime(2008, 1, 1),
            ed=dt.datetime(2009, 1, 1),
            sv=10000,
    ):
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

        prices = prices_all[syms].copy()
        prices = prices.fillna(method='ffill').fillna(method='bfill')

        bbm = ind.bol_band(prices, window=15, type='Median')
        bbl = ind.bol_band(prices, window=15, type='Lower')
        bbu = ind.bol_band(prices, window=15, type='Upper')
        roc = ind.roc(prices)
        sma_short = ind.sma(prices, 10)
        sma_long = ind.sma(prices, 20)

        features = pd.DataFrame(index=prices.index)
        features['bb_lower'] = bbl
        features['bb_median'] = bbm
        features['bb_upper'] = bbu
        features['roc'] = roc
        features['sma_short'] = sma_short
        features['sma_long'] = sma_long

        features.fillna(method='bfill', inplace=True)
        features.fillna(method='ffill', inplace=True)

        future_returns = prices.shift(-5) / prices - 1
        future_returns = future_returns.loc[features.index]

        threshold = 0.02
        y = np.zeros(future_returns.shape)
        y[future_returns > threshold + self.impact] = 1
        y[future_returns < -threshold - self.impact] = -1

        X = features.values
        y = y.flatten()

        self.learner.add_evidence(X, y)

        self.feature_names = features.columns

    def testPolicy(
            self,
            symbol="IBM",
            sd=dt.datetime(2009, 1, 1),
            ed=dt.datetime(2010, 1, 1),
            sv=10000,
    ):

        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = get_data(syms, dates)
        prices = prices_all[syms].copy()
        prices = prices.fillna(method='ffill').fillna(method='bfill')

        bbm = ind.bol_band(prices, type='Median')
        bbl = ind.bol_band(prices, type='Lower')
        bbu = ind.bol_band(prices, type='Upper')
        roc = ind.roc(prices)
        sma_short = ind.sma(prices, 10)
        sma_long = ind.sma(prices, 20)

        features = pd.DataFrame(index=prices.index)
        features['bb_lower'] = bbl
        features['bb_median'] = bbm
        features['bb_upper'] = bbu
        features['roc'] = roc
        features['sma_short'] = sma_short
        features['sma_long'] = sma_long

        features.fillna(method='bfill', inplace=True)
        features.fillna(method='ffill', inplace=True)

        X = features.values
        predictions = self.learner.query(X)

        trades = pd.DataFrame(0, index=features.index, columns=[symbol])

        current_position = 0

        for i in range(len(predictions)):
            date = features.index[i]
            pred = predictions[i]

            action = 0
            if pred > 0 and current_position <= 0:
                action = 1000 + (-1000 * current_position)
                current_position = 1
            elif pred < 0 and current_position >= 0:
                action = -1000 - (1000 * current_position)
                current_position = -1

            if action != 0:
                trades.loc[date, symbol] = action

        all_trades = pd.DataFrame(0, index=prices.index, columns=[symbol])
        all_trades.update(trades)

        return all_trades


if __name__ == "__main__":  		  	   		 	 	 			  		 			     			  	 
    pass
