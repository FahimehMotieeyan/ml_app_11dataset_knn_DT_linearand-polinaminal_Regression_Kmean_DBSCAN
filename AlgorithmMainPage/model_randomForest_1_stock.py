import pandas as pd
import numpy as np

df = pd.read_csv('filles/stock_predict.csv', header=None, names=['raw_data'])
df[["quarter", "stock", "date", "open", "high", "low", "close", "volume", "percent_change_price", "percent_change_volume_over_last_wk", "previous_weeks_volume", "next_weeks_open", "next_weeks_close", "percent_change_next_weeks_price", "days_to_next_dividend", "percent_return_next_dividend"]] = (
    df['raw_data'].str.split(',', expand=True)
)
df.drop('raw_data', axis=1, inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')
df = df.drop(columns=['stock', 'date', 'open', 'high', 'low', 'close'])
# df['percent_change_volume_over_last_wk'].fillna(df['percent_change_volume_over_last_wk'].mean(), inplace=True)
# df['previous_weeks_volume'].fillna(df['previous_weeks_volume'].mean(), inplace=True)

print(df.head().to_string())
print(df.info())
print(df.describe().to_string())
print(df.isnull().sum())
print(df.shape)