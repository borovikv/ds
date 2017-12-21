import json
import os

import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame

import ds.settings as s


def parse_records(path):
    abspath = os.path.join(s.RESOURCE_ROOT, path)
    return [json.loads(line) for line in open(abspath)]


path = 'ch02/usagov_bitly_data2012-03-16-1331923249.txt'
records = parse_records(path)

frame = DataFrame(records)

cframe = frame[frame.a.notnull()]
systems = np.where(cframe['a'].str.contains('Windows'), 'Windows', 'Not Windows')
by_tz_os = cframe.groupby(['tz', systems])
agg_counts = by_tz_os.size().unstack().fillna(0)
indexer = agg_counts.sum(1).argsort()
count_subset = agg_counts.take(indexer)[-10:]
count_subset.div(count_subset.sum(1), axis=0).plot(kind='barh', stacked=True)




#
# clean_tz = frame['tz'].fillna('Missing')
# clean_tz[clean_tz == ''] = 'Unknown'
# tz_counts = clean_tz.value_counts()
# tz_counts[:10].plot(kind='barh', rot=0)
plt.show(True)
