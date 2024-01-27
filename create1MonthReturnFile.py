import pandas as pd

data = pd.read_csv("raw_stock_test.csv")
df = pd.DataFrame()
df['1mR'] = data['return_1m']
df.to_csv("1MonthReturn.csv", index=False)