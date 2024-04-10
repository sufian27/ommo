import numpy as np


def compute_avg(dataset):
    """
    Returns numpy array with averages
    """
    return np.mean(dataset, axis=0)


def compute_max(dataset):
    """
    Returns a numpy array with max
    """
    return np.max(np.linalg.norm(dataset, axis=2), axis=0)
