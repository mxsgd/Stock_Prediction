import pandas as pd

df = pd.read_csv('combined_stock_data.csv')

added = 0
liczba_segmentow = 21

for i in range(251, len(df), 251):
    mean_below = df.iloc[i+added-7:i+added].mean()
    added+=1
    df.loc[i+added] = mean_below

temp_df = pd.DataFrame()
true_df = pd.DataFrame()

for i in range(len(df)):
    # if(i % 231 == 0 and i != 0):
    #     segment = df.iloc[i:i + liczba_segmentow-1, :].values.flatten()
    #     temp_df = pd.concat([temp_df, pd.Series(segment)], axis=1)
    # else:
    segment = df.iloc[i:i + liczba_segmentow, :].values.flatten()
    temp_df = pd.concat([temp_df, pd.Series(segment)], axis=1)

temp_df = temp_df.transpose().reset_index(drop=True)
for i in range(0, len(temp_df), liczba_segmentow):
    true_df = pd.concat([true_df, temp_df.iloc[i, :]], axis=1)

true_df = true_df.transpose().reset_index(drop=True)

# for i in range(12, len(true_df), 12):
#     for j in range(0, 119, 6):
#         for k in range(6):
#             true_df.at[i, 120 + k] = true_df.at[i, 120 + k] + true_df.at[i, j + k]
#         for z in range(6):
#             true_df.at[i, 120 + z] = true_df.at[i, 120 + z] / 20.0
true_df.to_csv("test.csv", index=False)