"""
Student Name: Skyler Ebelt
GT User ID: sebelt3
GT ID: 904077010
"""

import datetime as dt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals
from StrategyLearner import StrategyLearner


def author():
    return "sebelt3"


def studygroup():
    return "sebelt3"


def run_experiment():
    symbol = "JPM"
    sv = 100000
    commission = 0.0

    impacts = [0.0, 0.005, 0.01]

    in_sd = dt.datetime(2008, 1, 1)
    in_ed = dt.datetime(2009, 12, 31)

    portvals_norm_list = []

    for impact in impacts:
        learner = StrategyLearner(verbose=False, impact=impact, commission=commission)
        learner.add_evidence(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)


        trades = learner.testPolicy(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)

        if 'Symbol' not in trades.columns:
            orders_df = pd.DataFrame(index=trades.index)
            orders_df['Symbol'] = symbol
            orders_df['Order'] = ['BUY' if x > 0 else 'SELL' for x in trades[symbol].values]
            orders_df['Shares'] = abs(trades[symbol].values)

            orders_df = orders_df[orders_df['Shares'] > 0]
            portvals = compute_portvals(orders_df, sv, commission, impact)
        else:
            portvals = compute_portvals(trades, sv, commission, impact)

        portvals_norm = portvals / portvals.iloc[0]
        portvals_norm_list.append(portvals_norm)


    plt.figure(figsize=(10, 6))
    for i, impact in enumerate(impacts):
        plt.plot(portvals_norm_list[i], label=f'Impact: {impact}')

    plt.title('Portfolio Values with Different Market Impacts')
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('experiment2_portfolio_values.png')

if __name__ == "__main__":
    run_experiment()