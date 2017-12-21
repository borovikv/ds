import os
import pandas as pd
import matplotlib.pyplot as plt

import ds.settings as s

base_path = s.path('02', 'movielens')

unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table(os.path.join(base_path, 'users.dat'), sep='::', header=None, names=unames, engine='python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table(os.path.join(base_path, 'ratings.dat'), sep='::', header=None, names=rnames, engine='python')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table(os.path.join(base_path, 'movies.dat'), sep='::', header=None, names=mnames, engine='python')

data = pd.merge(pd.merge(ratings, users), movies)
mean_ratings = data.pivot_table('rating', index='title', columns='gender')

ratings_by_title = data.groupby('title').size()
active_titles = ratings_by_title.index[ratings_by_title >= 250]
mean_ratings = mean_ratings.ix[active_titles]
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)
# print(top_female_ratings[:10])

mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
new_mean_raiting = mean_ratings.sort_values(by='diff')
# print(new_mean_raiting[:10])
# print(new_mean_raiting[::-1][:10])

rating_std_by_title = data.groupby('title')['rating'].std()
rating_std_by_title = rating_std_by_title.ix[active_titles]
less_despersion_titles = rating_std_by_title.sort_values(ascending=False)[:10]
print(less_despersion_titles)

plt.show(True)
