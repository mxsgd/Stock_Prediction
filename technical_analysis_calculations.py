import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas_ta
def Calculations(stock_data):
    df1 = stock_data
    df1['garman_klass_vol'] = ((np.log(df1['high']) - np.log(df1['low'])) ** 2) / 2 - (2 * np.log(2) - 1) * (
            (np.log(df1['adj close']) - np.log(df1['open'])) ** 2)

    df1['rsi'] = df1.groupby(level=1)['adj close'].transform(lambda x: pandas_ta.rsi(close=x, length=20))

    df1['bb_low'] = df1.groupby(level=1)['adj close'].transform(
        lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:, 0])

    df1['bb_mid'] = df1.groupby(level=1)['adj close'].transform(
        lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:, 1])

    df1['bb_high'] = df1.groupby(level=1)['adj close'].transform(
        lambda x: pandas_ta.bbands(close=np.log1p(x), length=20).iloc[:, 2])

    def compute_atr(stock_data):
        atr = pandas_ta.atr(high=stock_data['high'],
                            low=stock_data['low'],
                            close=stock_data['close'],
                            length=14)
        return atr.sub(atr.mean()).div(atr.std())

    df1['atr'] = df1.groupby(level=1, group_keys=False).apply(compute_atr)

    def compute_macd(close):
        macd = pandas_ta.macd(close=close, length=20).iloc[:, 0]
        return macd.sub(macd.mean()).div(macd.std())

    df1['macd'] = df1.groupby(level=1, group_keys=False)['adj close'].apply(compute_macd)

    df1['dollar_volume'] = (df1['adj close'] * df1['volume']) / 1e6
    return stock_data
