import numpy as np
from statsmodels.regression.rolling import RollingOLS
import pandas as pd
import yfinance as yf
from technical_analysis_calculations import Calculations
import pandas_datareader.data as web
import statsmodels.api as sm
from sklearn.cluster import KMeans
import re

stocks = ["SOL-USD"]
flat_stocks = [item[0] for item in stocks]
start_date = "2012-01-01"
end_date = "2024-01-26"


# Collecting stocks with specified data length then adding date and ticker index names
all_stock_data = pd.DataFrame()
all_stock_data = yf.download(tickers=stocks,
                      start=start_date,
                      end=end_date).stack()

all_stock_data.index.names = ['date', 'ticker']
all_stock_data.columns = all_stock_data.columns.str.lower()


#calculating: garman_klass_vol, rsi, bb_low/mid/high, atr, macd and dollar volume
all_stock_data = Calculations(all_stock_data)

#getting technical analysis columns
last_cols = [c for c in all_stock_data.columns.unique(0) if c not in ['dollar_volume', 'volume', 'open',
                                                          'high', 'low', 'close']]

data = (pd.concat([all_stock_data.unstack('ticker')['dollar_volume'].resample('M').mean().stack('ticker').to_frame('dollar_volume'),
                   all_stock_data.unstack()[last_cols].resample('M').last().stack('ticker')],
                  axis=1)).dropna()

#discard low liquidity stocks
data['dollar_volume'] = (data.loc[:, 'dollar_volume'].unstack('ticker').rolling(5*12, min_periods=12).mean().stack())
data['dollar_vol_rank'] = (data.groupby('date')['dollar_volume'].rank(ascending=False))
data = data[data['dollar_vol_rank']<150].drop(['dollar_volume', 'dollar_vol_rank'], axis=1)


def calculate_returns(df):
    outlier_cutoff = 0.005
    lags = [1, 2, 3, 6, 9, 12]

    for lag in lags:
        df[f'return_{lag}m'] = (df['adj close']
                                .pct_change(lag)
                                .pipe(lambda x: x.clip(lower=x.quantile(outlier_cutoff),
                                                       upper=x.quantile(1 - outlier_cutoff)))
                                .add(1)
                                .pow(1 / lag)
                                .sub(1))
    return df


data = data.groupby(level=1, group_keys=False).apply(calculate_returns).dropna()

factor_data = web.DataReader('F-F_Research_Data_5_Factors_2x3',
                               'famafrench',
                               start='2010')[0].drop('RF', axis=1)


factor_data.index = factor_data.index.to_timestamp()
factor_data = factor_data.resample('M').last().div(100)
factor_data.index.name = 'date'
factor_data = factor_data.join(data['return_1m']).sort_index()
observations = factor_data.groupby(level=1).size()
valid_stocks = observations[observations >= 10]
factor_data = factor_data[factor_data.index.get_level_values('ticker').isin(valid_stocks.index)]

betas = (factor_data.groupby(level=1,
                            group_keys=False)
         .apply(lambda x: RollingOLS(endog=x['return_1m'],
                                     exog=sm.add_constant(x.drop('return_1m', axis=1)),
                                     window=min(24, x.shape[0]),
                                     min_nobs=len(x.columns)+1)
         .fit(params_only=True)
         .params
         .drop('const', axis=1)))

factors = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA']

data = (data.join(betas.groupby('ticker').shift()))

data.loc[:, factors] = data.groupby('ticker', group_keys=False)[factors].apply(lambda x: x.fillna(x.mean()))

data = data.drop('adj close', axis=1)

data = data.dropna()

target_rsi_values = [30, 45, 55, 70]

initial_centroids = np.zeros((len(target_rsi_values), 18))

initial_centroids[:, 6] = target_rsi_values
def get_clusters(df):
    df['cluster'] = KMeans(n_clusters=4,
                           random_state=0,
                           init=initial_centroids).fit(df).labels_
    return df

data = data.dropna().groupby('date', group_keys=False).apply(get_clusters)
data = data.drop(['return_12m', 'return_9m', 'return_6m', 'return_3m', 'return_2m'], axis=1)
data.to_csv("crypto_STOCK.csv", index=False)
