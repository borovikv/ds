import csv
import json

import numpy as np
import pandas as pd


def transform():
    df = pd.read_csv('SKUs.csv', converters={'retail_price': to_f, 'price_attributable_for_royalty': to_f})
    df['percent_attributable_for_royalty'] = (df.price_attributable_for_royalty / df.retail_price).fillna(0)

    prices = df.retail_prices_in_currencies.dropna().apply(to_dict).tolist()
    df2 = pd.DataFrame(prices, index=df.SKU[df.retail_prices_in_currencies.notnull()]).reset_index()
    df2 = pd.melt(df2, id_vars=["SKU"], value_name="retail_price", var_name='currency_code').dropna()

    df3 = df.set_index('SKU').join(df2.set_index('SKU'), lsuffix='_orig', how='left').reset_index()
    df3.retail_price = df3.retail_price.combine_first(df3.retail_price_orig)
    df3.currency_code = df3.currency_code.fillna('USD')
    df3.price_attributable_for_royalty = np.round(df3.retail_price * df3.percent_attributable_for_royalty, 2)

    cols = ['currency_code', 'retail_price', 'price_attributable_for_royalty', 'SKU', 'subscription_periods', 'comment']
    df3[cols].to_csv('out.csv', index=False, quoting=csv.QUOTE_ALL, quotechar="'")
    return 'out.csv'


def to_f(v):
    return float(v.strip('$'))


def to_dict(r):
    return {c: float(a) for k, (c, a) in json.loads(r).items() if len(k) == 3}


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
