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


def get_avg_rows(dataset, device_name) -> dict:
    avg_rows = dict()
    for sensor_index, value in enumerate(dataset):
        avg_rows[f"{device_name}_S{sensor_index}_x"] = value[0]
        avg_rows[f"{device_name}_S{sensor_index}_y"] = value[1]
        avg_rows[f"{device_name}_S{sensor_index}_z"] = value[2]

    return avg_rows


def get_max_rows(max_list, device_name) -> dict:
    max_rows = dict()
    for sensor_index, value in enumerate(max_list):
        max_rows[f"{device_name}_S{sensor_index}_max"] = value

    return max_rows
