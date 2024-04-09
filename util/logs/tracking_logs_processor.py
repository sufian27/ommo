import numpy as np

"""
    Class that is used to help process logs
"""
class TrackingLogsProcessor:

    """
        Returns a numpy array with averages
    """
    def compute_avg(self, dataset):
        return np.mean(dataset, axis=0)
    
    """
        Returns a numpy array with max
    """
    def compute_max(self, dataset):
        return np.max(np.linalg.norm(dataset, axis=2), axis=0)