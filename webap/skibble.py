import random
import numpy as np
import pandas as pd

from . import utilities




# recsys code euclidean
from numpy.linalg import norm
import numpy as np

#
def euc(x, df):
    x = np.array(x)
    multi = np.array([5, 4, 3, 2])
    energy = x.dot(multi)
    similarity = []
    for i in range(len(df)):
        row = df.loc[i][:4].values
        diff = x - row
        diffsq = diff * diff
        simval = 1 / (1 + np.sqrt(np.sum(diffsq)))
        similarity.append(simval)
    df['similarity'] = similarity
    df.sort_values(by='similarity', ascending=False, inplace=True)
    return df.iloc[0]['plans']


def recommend(h, f, l, b):
    df = utilities.load_df_from_mysql('recommendation_dataset')
    x = list(map(int, [h, f, l, b]))
    p = euc(x)
    return p
