import numpy as np


def compute_avg(dataset):
    """
    
    Returns numpy array with averages

    Parameters
    ----------
    dataset : np.array
        the dataset of float x, y, z values, with shape (samples, sensors, 3)
    
    Returns
    -------
    np.array
        numpy array with average x, y, z for each sensor
    """

    return np.mean(dataset, axis=0)


def compute_max(dataset):
    """

    Returns numpy array with maximum distances

    Parameters
    ----------
    dataset : np.array
        the dataset of float x, y, z values, with shape (samples, sensors, 3)
    
    Returns
    -------
    np.array
        numpy array with maximum distance for each sensor
    """
    
    return np.max(np.linalg.norm(dataset, axis=2), axis=0)


def get_avg_rows(avg_list, device_name) -> dict:
    """
    
    Creates a dictionary of rows with averages for each sensor
    
    Parameters
    ----------
    avg_list : np.array
        the list of average values
    device_name : str
        the name of the device

    Returns
    -------
    avg_rows : dict
        the dictionary with average position for every sensor in the hdf5 file
    """

    avg_rows = dict()
    for sensor_index, value in enumerate(avg_list):
        avg_rows[f"{device_name}_S{sensor_index}_x"] = value[0]
        avg_rows[f"{device_name}_S{sensor_index}_y"] = value[1]
        avg_rows[f"{device_name}_S{sensor_index}_z"] = value[2]

    return avg_rows


def get_max_rows(max_list, device_name) -> dict:
    """
    
    Creates a dictionary of rows with maximum distances for each
    sensor
    
    Parameters
    ----------
    max_list : np.array
        the list of maximum distance values
    device_name : str
        the name of the device

    Returns
    -------
    max_rows : dict
        the dictionary with maximum distances for every sensor in the hdf5 file
    """
    
    max_rows = dict()
    for sensor_index, value in enumerate(max_list):
        max_rows[f"{device_name}_S{sensor_index}_max"] = value

    return max_rows
