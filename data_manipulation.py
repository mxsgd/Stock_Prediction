import pandas as pd
import numpy as np
df = pd.read_csv('raw_stock_test.csv')

added = 0
liczba_segmentow = 134

# del_df = pd.DataFrame()

# for i in range(len(df)):
#     if (i % 250 == 0 and i != 0):
#         added+=1
#         segment = df.loc[i,:].values
#         temp_df = pd.concat([temp_df, pd.Series(segment)], axis=1)
#         temp_df = pd.concat([temp_df, pd.Series(segment)], axis=1)
#     else:
#         segment = df.loc[i, :].values
#         temp_df = pd.concat([temp_df, pd.Series(segment)], axis=1)
#         print(i)
# temp_df = temp_df.transpose().reset_index(drop=True)
true_df = pd.DataFrame()
control = 0
for i in range(0, len(df), liczba_segmentow):
    # if(int(i - added*7) % 245 == 0 and i != 0 and control == 0):
    #     segment = df.iloc[i-added:i-added + liczba_segmentow-1, :].values.flatten()
    #     true_df = pd.concat([true_df, pd.Series(segment)], axis=1)
    #     added +=1
    #     control = 1
    # else:
    print(i)
    segment = df.iloc[i-added:i-added + liczba_segmentow, :].values.flatten()
    true_df = pd.concat([true_df, pd.Series(segment)], axis=1)
    control = 0

# for i in range(0, len(temp_df), liczba_segmentow):
#     true_df = pd.concat([true_df, temp_df.iloc[i, :]], axis=1)
#     print(i)
true_df = true_df.transpose().reset_index(drop=True)

# for i in range(12, len(true_df), 12):
#     for j in range(0, 119, 6):
#         for k in range(6):
#             true_df.at[i, 120 + k] = true_df.at[i, 120 + k] + true_df.at[i, j + k]
#         for z in range(6):
#             true_df.at[i, 120 + z] = true_df.at[i, 120 + z] / 20.0
# true_df['Label'] = np.where(true_df['40'].shift(-1) > true_df['40'], 1, 0)
#
# for i in range(len(true_df)):
#     if (i % 36 != 0):
#         segment = true_df.loc[i, :].values
#         del_df = pd.concat([del_df, pd.Series(segment)], axis=1)
#         print(f"last{i}")
true_df.to_csv("combined_test.csv", index=False)
