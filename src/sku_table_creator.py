import json

import numpy as np
import pandas as pd

df = pd.read_csv('SKUs.csv')

df.retail_price = df.retail_price.str.strip('$').astype(float)
df.price_attributable_for_royalty = df.price_attributable_for_royalty.str.strip('$').astype(float)
df.retail_prices_in_currencies[df.retail_prices_in_currencies.isnull()] = df.retail_price
df.retail_prices_in_currencies = df.retail_prices_in_currencies.fillna(df.retail_price)
df['percent_attributable_for_royalty'] = (df.price_attributable_for_royalty / df.retail_price).fillna(0)


def p(d):
    try:
        return json.loads(d)
    except:
        return {"USD": ["USD", d]}


df.retail_prices_in_currencies = df.retail_prices_in_currencies.dropna().apply(p)

df2 = pd.DataFrame(df.retail_prices_in_currencies.tolist())
df2 = df2[df2.columns[df2.columns.str.len() == 3]]


def get_amount(v):
    try:
        return v[1]
    except:
        return np.nan


df2 = df2.applymap(get_amount)
df2['SKU'] = df['SKU']


# df2 = df2.set_index('SKU')

def currency_by_sku(row):
    sku = row.pop('SKU')
    df = pd.DataFrame([row]).transpose().reset_index()
    df.columns = ['currency_code', 'retail_price']
    df['SKU'] = sku
    return df


df3 = pd.concat(currency_by_sku(row) for row in df2.to_dict('records'))
df5 = df[['SKU', 'percent_attributable_for_royalty', 'subscription_periods', 'comment']]
df4 = df5.set_index('SKU').join(df3.set_index('SKU'))
# df4['price_attributable_for_royalty'] = df4['retail_price'] * df4['percent_attributable_for_royalty']
print(df4[:5])

# df3 = df.join(df2).drop('retail_prices_in_currencies', axis=1)
#
# sc = ['SKU',
#       'retail_price',
#       'percent_attributable_for_royalty',
#       'price_attributable_for_royalty',
#       'subscription_periods',
#       'comment']
# df4 = df3[sc].to_dict('records')
# result = []
# for i, row in enumerate(df4):
#     for column in df3.columns:
#         if len(column) == 3 and column != 'SKU':
#             row1 = deepcopy(row)
#             result.append(row1)
#             row1['currency_code'] = column
#             row1['retail_price'] = df3[column][i]
#             try:
#                 row1['price_attributable_for_royalty'] = float(row1['retail_price']) * row1[
#                     'percent_attributable_for_royalty']
#             except:
#                 row1['price_attributable_for_royalty'] = 0
#
# df5 = pd.DataFrame(result)
# df5 = df5[pd.notnull(df5['retail_price'])]
# df5.drop('percent_attributable_for_royalty', inplace=True, axis=1)
# print(df5[:5])
# df5.to_csv('out.csv', index=False)
