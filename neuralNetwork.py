import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow import Sequential
from tensorflow import LSTM, Dense

data = pd.read_csv("combined_stock_data.csv")

data['Label'] = np.where(data['Close'].shift(-1) > data['Close'], 1, 0)

features = ['Open', 'High', 'Low', 'Close', 'Volume', 'Ticker_ID']