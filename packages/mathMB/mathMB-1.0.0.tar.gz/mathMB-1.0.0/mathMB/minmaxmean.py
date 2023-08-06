import numpy as np


def minmaxmean(x):
    '''Wrapper to print np.min(), np.max(), np.mean() at once'''
    return np.nanmin(x), np.nanmax(x), np.nanmean(x)
