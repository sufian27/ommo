import numpy as np

"""
    Library that is used to help process logs. Currently only contains methods for computing average and maximum
"""


def compute_avg(dataset):
    return np.mean(dataset, axis=0)


"""
    Returns a numpy array with max
"""


def compute_max(dataset):
    return np.max(np.linalg.norm(dataset, axis=2), axis=0)
