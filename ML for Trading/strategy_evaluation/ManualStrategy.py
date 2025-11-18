"""
Manual Strategy code
Student Name: Skyler Ebelt
GT User ID: sebelt3
GT ID: 904077010
"""

import datetime as dt
import indicators as ind
import pandas as pd
from util import get_data


class ManualStrategy(object):
    def __init__(self, verbose=False, commission=0, impact=0):
        self.verbose = verbose
        self.commission = commission
        self.impact = impact

    def testPolicy(self, symbol="JPM", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
        syms = [symbol]

        date_range = pd.date_range(sd, ed)
        all_prices = get_data(syms, date_range)
        prices = all_prices[syms].copy()

        if self.verbose:
            print(prices)

        prices.fillna(method='bfill', inplace=True)
        prices.fillna(method='ffill', inplace=True)

        bbm = ind.bol_band(prices, window=15, type='Median')
        bbl = ind.bol_band(prices, window=15, type='Lower')
        bbu = ind.bol_band(prices, window=15, type='Upper')

        roc = ind.roc(prices, window=10)

        short_moving_avg = ind.sma(prices, 10)
        long_moving_avg = ind.sma(prices, 20)

        trades_df = pd.DataFrame(0, index=prices.index, columns=[symbol])

        current_position = 0

        price_trend_direction = 0
        lookback = 10

        for day_index in range(lookback, len(prices)):
            current_price = prices.iloc[day_index].iloc[0]
            past_price = prices.iloc[day_index - lookback].iloc[0]

            if current_price > past_price:
                price_trend_direction = 1
            elif current_price < past_price:
                price_trend_direction = -1

            if not pd.isna(roc.iloc[day_index].iloc[0]):
                roc_value = roc.iloc[day_index].iloc[0]
            else:
                roc_value = 0

            have_sma_data = True
            if pd.isna(short_moving_avg.iloc[day_index].iloc[0]) or pd.isna(long_moving_avg.iloc[day_index].iloc[0]):
                have_sma_data = False

            sma_signal = 0
            if have_sma_data:
                if short_moving_avg.iloc[day_index].iloc[0] > long_moving_avg.iloc[day_index].iloc[0]:
                    sma_signal = 1
                else:
                    sma_signal = -1

            have_bb_data = True
            if (pd.isna(bbm.iloc[day_index].iloc[0]) or
                    pd.isna(bbu.iloc[day_index].iloc[0]) or
                    pd.isna(bbl.iloc[day_index].iloc[0])):
                have_bb_data = False

            bb_signal = 0
            if have_bb_data:
                today_price = prices.iloc[day_index].iloc[0]
                today_lower_band = bbl.iloc[day_index].iloc[0]
                today_upper_band = bbu.iloc[day_index].iloc[0]

                if today_price <= today_lower_band:
                    bb_signal = 1
                elif today_price >= today_upper_band:
                    bb_signal = -1

            final_signal = 0

            if price_trend_direction == 1:
                if roc_value > 0 or sma_signal == 1 or bb_signal == 1:
                    final_signal = 1

            elif price_trend_direction == -1:
                if roc_value < 0 or sma_signal == -1 or bb_signal == -1:
                    final_signal = -1

            if final_signal == 1:
                if current_position == -1000:
                    trades_df.iloc[day_index] = 2000
                    current_position = 1000
                elif current_position == 0:
                    trades_df.iloc[day_index] = 1000
                    current_position = 1000
            elif final_signal == -1:
                if current_position == 1000:
                    trades_df.iloc[day_index] = -2000
                    current_position = -1000
                elif current_position == 0:
                    trades_df.iloc[day_index] = -1000
                    current_position = -1000

        if self.verbose:
            print(trades_df)

        return trades_df

        return trades
    def author(self):
        return "sebelt3"

    def studygroup(self):
        return "sebelt3"