import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import ds.settings as s


def load_names():
    years = range(1880, 2011)
    names = ['name', 'sex', 'births']
    pieces = []
    for year in years:
        frame = pd.read_csv(s.path('02', 'names', f'yob{year}.txt'), names=names)
        frame['year'] = year
        pieces.append(frame)
    return pd.concat(pieces, ignore_index=True)


def add_prop(group):
    # При целочисленном делении производится округление с недостатком
    births = group.births.astype(float)
    group['prop'] = births / births.sum()
    return group


names = load_names().groupby(['year', 'sex']).apply(add_prop)


def plot_by_names(all_names, subset_names):
    total_berths = all_names.pivot_table('births', index='year', columns='name', aggfunc=sum)
    subset = total_berths[subset_names]
    subset.plot(subplots=True, figsize=(12, 10), grid=False, title="Number of births per year")


# plot_by_names(names, ['John', 'Harry', 'Mary', 'Marilyn', 'Vladimir'])


def get_top1000(group):
    return group.sort_values(by='births', ascending=False)[:1000]


def plot_names_most_common_1000_tendency(top1000):
    table = top1000.pivot_table('prop', index='year', columns='sex', aggfunc=sum)
    table.plot(title='Sum of table.prop by year and sex', yticks=np.linspace(0, 1.2, 13), xticks=range(1880, 2020, 10))


top1000 = names.groupby(['year', 'sex']).apply(get_top1000)


# plot_names_most_common_1000_tendency(top1000)


def get_quantile_count(group, q=0.5):
    group = group.sort_values(by='prop', ascending=False)
    return group.prop.cumsum().searchsorted(q) + 1


def names_diversity():
    diversity = top1000.groupby(['year', 'sex']).apply(get_quantile_count)
    diversity = diversity.unstack('sex').astype(float)
    diversity.plot(title="Number of popular names in top 50%")


# names_diversity()

# Извлекаем последнюю букву имени в столбце name
get_last_letter = lambda x: x[-1]
last_letters = names.name.map(get_last_letter)
last_letters.name = 'last letter'
table = names.pivot_table('births', index=last_letters, columns=['sex', 'year'], aggfunc=sum)


def last_letter_diversity(start, stop, step):
    subtable = table.reindex(columns=list(range(start, stop, step)), level='year')
    letter_prop = subtable / subtable.sum().astype(float)
    fig, axes = plt.subplots(2, 1, figsize=(10, 8))
    letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
    letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female', legend=False)


# last_letter_diversity(1910, 2011, 50)

def last_letter_tendency(letters, sex):
    letter_prop = table / table.sum().astype(float)
    dny_ts = letter_prop.ix[letters, sex].T
    dny_ts.plot()


# last_letter_tendency(['d', 'n', 'y'], 'M')


def name_tendency(group, name_mask):
    all_names = group.name.unique()
    mask = np.array([name_mask in x.lower() for x in all_names])
    mask_name_like = all_names[mask]
    filtered = group[group.name.isin(mask_name_like)]
    table = filtered.pivot_table('births', index='year', columns='sex', aggfunc='sum')
    table = table.div(table.sum(1), axis=0)
    table.plot(style={'M': 'k-', 'F': 'k--'})


name_tendency(names, 'vlad')

plt.show(True)
