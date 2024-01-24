import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
import  yfinance as yf
import datetime as dt
from MACD import MACD
import time
from scrapper import collect_data

stocks = []
collect_data('https://stockanalysis.com/stocks/', stocks)
print(len(stocks))
flat_stocks = [item[0] for item in stocks]
start_date = "2023-01-01"
end_date = "2023-12-31"

# gmo = yf.Ticker("MSFT")
#
# hist = gmo.history(start=start_date, end=end_date)
# print(gmo.history_metadata)
#
# print(gmo.actions)
# print(gmo.dividends)
# print(gmo.splits)
# print(gmo.capital_gains)
all_stock_data = pd.DataFrame()


for stock in flat_stocks[:5000]:
    stock_data = yf.download(stock, start=start_date, end=end_date, interval='1h')
    if not stock_data.empty:
     # stock_data['Date'] = stock_data.index
     #stock_data['Ticker_ID'] = stock
     if(len(stock_data) == 1742):

         stock_data = stock_data.drop('Adj Close', axis=1)

         # stock_data = stock_data.drop('Datetime', axis=1)
         stock_data = MACD(stock_data)
         all_stock_data = pd.concat([all_stock_data, stock_data], ignore_index=True)
         print(stock_data)
print(len(all_stock_data))
all_stock_data.to_csv("raw_stock_test.csv", index=False)