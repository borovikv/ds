import pandas as pd


df = pd.read_csv('words/many_line_1.csv')
df2 = df[df.text.str.contains('/')]
df2.to_csv('examine_2.csv', index=False)
