import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def MACD(stock_data):
    short_window = 12
    long_window = 26

    stock_data['Short_MA'] = stock_data['Close'].rolling(window=short_window, min_periods=1).mean()
    stock_data['Long_MA'] = stock_data['Close'].rolling(window=long_window, min_periods=1).mean()

    stock_data['MACD'] = stock_data['Short_MA'] - stock_data['Long_MA']

    signal_window = 9
    stock_data['Signal_Line'] = stock_data['MACD'].rolling(window=signal_window, min_periods=1).mean()
    return stock_data
