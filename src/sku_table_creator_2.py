import csv
import json

import numpy as np
import pandas as pd


def transform():
    converters = {'retail_price': to_f, 'price_attributable_for_royalty': to_f, 'retail_prices_in_currencies': to_dict}
    df = pd.read_csv('SKUs.csv', index_col='SKU', converters=converters)
    df['percent_attributable_for_royalty'] = (df.price_attributable_for_royalty / df.retail_price).fillna(0)
    df.retail_prices_in_currencies.fillna(df.retail_price.apply(lambda v: {'USD': v}), inplace=True)

    df_retail_prices_in_currencies = pd.DataFrame(df.retail_prices_in_currencies.tolist(), index=df.index)
    columns = ['percent_attributable_for_royalty', 'subscription_periods', 'comment']
    df3 = df[columns].join(df_retail_prices_in_currencies).reset_index()
    df3 = pd.melt(df3, id_vars=['SKU'] + columns, value_name="retail_price", var_name='currency_code').dropna()
    df3['price_attributable_for_royalty'] = np.round(df3.retail_price * df3.percent_attributable_for_royalty, 4)

    df3.drop('percent_attributable_for_royalty', axis=1, inplace=True)
    df3 = df3[
        ["currency_code", "retail_price", "price_attributable_for_royalty", "SKU", "subscription_periods", "comment"]]
    df3.sort_values(['SKU', 'currency_code']).to_csv('sku_table.csv', index=False, quoting=csv.QUOTE_ALL)


def to_f(v):
    return float(v.strip('$'))


def to_dict(v):
    return {c: float(p) for k, (c, p) in json.loads(v).items() if len(k) == 3} if v else None


def equote(v):
    try:
        float(v)
        return v
    except ValueError:
        return "'{}'".format(v)


def transform_csv_to_cte(path, fields):
    with open(path) as fin, open('skus_cte.sql', 'w') as fout:
        reader = csv.DictReader(fin)
        rows = [", ".join([equote(line[k]) for k in fields]) for line in reader]
        select_row = ['\tselect {}'.format(row) for row in rows]
        cte = 'with skus({columns}) as (\n{sql_body}\n)'.format(
            columns=','.join(fields),
            sql_body=' union all\n'.join(select_row)
        )
        fout.write(cte)


if __name__ == '__main__':
    p = transform()
    # transform_csv_to_cte(p, ['SKU', 'currency_code', 'price_attributable_for_royalty', 'subscription_periods'])
