"""
Student Name: Skyler Ebelt
GT User ID: sebelt3
GT ID: 904077010
"""

import datetime as dt
import pandas as pd
import numpy as np
import experiment1
import experiment2
import ManualStrategy as ms
import marketsimcode as msim
import matplotlib.pyplot as plt


def convert_trades_to_orders(trades_df, symbol):
    orders_list = []

    for date, row in trades_df.iterrows():
        shares = row[0]
        if shares == 0:
            continue

        order_type = 'BUY' if shares > 0 else 'SELL'
        orders_list.append({
            'Symbol': symbol,
            'Order': order_type,
            'Shares': abs(shares)
        })

    if not orders_list:
        return pd.DataFrame(columns=['Symbol', 'Order', 'Shares'])

    orders_df = pd.DataFrame(orders_list)
    orders_df.index = trades_df.loc[trades_df.iloc[:, 0] != 0].index

    return orders_df


def run_manual_strategy():
    symbol = 'JPM'
    sv = 100000
    commission = 9.95
    impact = 0.005

    in_sd = dt.datetime(2008, 1, 1)
    in_ed = dt.datetime(2009, 12, 31)

    out_sd = dt.datetime(2010, 1, 1)
    out_ed = dt.datetime(2011, 12, 31)

    manual_strategy = ms.ManualStrategy(verbose=False, commission=commission, impact=impact)

    ms_trades_in = manual_strategy.testPolicy(symbol=symbol, sd=in_sd, ed=in_ed, sv=sv)
    ms_trades_out = manual_strategy.testPolicy(symbol=symbol, sd=out_sd, ed=out_ed, sv=sv)

    ms_orders_in = convert_trades_to_orders(ms_trades_in, symbol)
    ms_orders_out = convert_trades_to_orders(ms_trades_out, symbol)

    benchmark_in = msim.benchmark(sym=[symbol], sd=in_sd, ed=in_ed)
    benchmark_out = msim.benchmark(sym=[symbol], sd=out_sd, ed=out_ed)

    ms_portvals_in = msim.compute_portvals(ms_orders_in, start_val=sv, commission=commission, impact=impact)
    benchmark_portvals_in = msim.compute_portvals(benchmark_in, start_val=sv, commission=commission, impact=impact)

    ms_portvals_out = msim.compute_portvals(ms_orders_out, start_val=sv, commission=commission, impact=impact)
    benchmark_portvals_out = msim.compute_portvals(benchmark_out, start_val=sv, commission=commission, impact=impact)

    plt.figure(figsize=(10, 6))
    plt.plot(ms_portvals_in/ ms_portvals_in.iloc[0], color='red', label='Manual Strategy')
    plt.plot(benchmark_portvals_in / benchmark_portvals_in.iloc[0], color='purple', label='Benchmark')

    plt.title(f'In-Sample Manual Strategy vs Benchmark:')
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('manual_strategy_in_sample.png')

    plt.figure(figsize=(10, 6))
    plt.plot(ms_portvals_out, color='red', label='Manual Strategy')
    plt.plot(benchmark_portvals_out, color='purple', label='Benchmark')


    plt.title(f'Out-of-Sample Manual Strategy vs Benchmark:')
    plt.xlabel('Date')
    plt.ylabel('Normalized Portfolio Value')
    plt.legend()
    plt.grid(True)
    plt.savefig('manual_strategy_out_sample.png')

def author():
    return "sebelt3"


def studygroup():
    return "sebelt3"


if __name__ == "__main__":
    np.random.seed(904077010)
    run_manual_strategy()
    experiment1.run_experiment1()
    experiment2.run_experiment()
