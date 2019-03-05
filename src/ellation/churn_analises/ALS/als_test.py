# from sklearn.decomposition import NMF

import numpy as np
import pandas as pd

df_media = pd.read_csv('cr_media.csv')
df_media['mediaIdInt'] = np.arange(len(df_media))
df_viewerships = pd.read_csv('normalized_viewership.csv')

dfViewNormalizedWithMedia = pd.merge(df_viewerships, df_media, on='mediaId')

dfPopularity = dfViewNormalizedWithMedia[['mediaIdInt', 'mediaId']]
dfPopularity = dfPopularity.groupby(['mediaIdInt', 'mediaId']).size().reset_index(name='countMedia')
dfPopularity['fracPopular'] = dfPopularity['countMedia'] / dfPopularity['countMedia'].max()
dfPopularity['expPopular'] = np.exp(dfPopularity['fracPopular'] * -1)
dfPopularity = dfPopularity[['mediaIdInt', 'mediaId', 'expPopular', 'fracPopular']]

dfViewWithInvPop = pd.merge(dfViewNormalizedWithMedia, dfPopularity, on=['mediaIdInt', 'mediaId'])
dfViewWithInvPop['implicitRating'] = dfViewWithInvPop['avgFracViewed'] * dfViewWithInvPop['expPopular']
dfViewWithInvPop = dfViewWithInvPop[[
    'userId',
    'userIdInt',
    'mediaId',
    'mediaIdInt',
    'title',
    'implicitRating',
    'latestEventSent',
    'isCompletelyWatched'
]]
dfViewWithInvPop['recentRank'] = (
    dfViewWithInvPop.groupby('userId')["latestEventSent"].rank(method="dense", ascending=True))
recentViewershipLimit = 60
dfRecentViewership = dfViewWithInvPop[dfViewWithInvPop.recentRank <= recentViewershipLimit]

columns = ['userIdInt', 'mediaIdInt', 'implicitRating', 'latestEventSent']
dfViewForAls = pd.concat([dfViewWithInvPop[columns], dfRecentViewership[columns]])


