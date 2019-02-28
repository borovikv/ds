import pandas as pd


df = pd.read_csv('/Users/vborovic/Downloads/svod_by_media.csv')
# print(df.groupby('m').sum())
df.to_csv('/Users/vborovic/Downloads/svod_by_media_1.csv', index=False)
# df1 = pd.read_csv('/Users/vborovic/Downloads/svod_by_media_1.csv')
# print(df1.groupby('m').sum())



# df = pd.read_csv('/Users/vborovic/Downloads/svod_by_user.csv')
# df.to_csv('/Users/vborovic/Downloads/svod_by_user_1.csv', index=False)
# print('loaded')

# print(df.groupby('m').sum())
