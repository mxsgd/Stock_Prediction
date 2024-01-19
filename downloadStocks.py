import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
import datetime as dt
import mplfinance as mpf
import time
from scrapper import collect_data

stocks = []
collect_data('https://stockanalysis.com/stocks/', stocks)
print(len(stocks))
flat_stocks = [item[0] for item in stocks]
start_date = "2022-01-01"
end_date = "2022-12-31"

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


for stock in flat_stocks:
    stock_data = yf.download(stock, start=start_date, end=end_date, interval='1d')
    if not stock_data.empty:
     #stock_data['Ticker_ID'] = stock
     all_stock_data = pd.concat([all_stock_data, stock_data], ignore_index=True)
     print(stock_data)
all_stock_data.to_csv("combined_stock_data.csv", index=False)