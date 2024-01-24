import pandas as pd
import numpy as np
data = pd.read_csv('raw_stock_test.csv')

data['Above'] = data['High'] - data['Open']
data['Below'] = data['Open'] - data['Low']
data['VolumeToPrice'] = data['Close'] / data['Volume']
data.to_csv("calculated_stock_test.csv", index=False)