import util.processing.logs_processing as lp
import numpy as np


def test_compute_avg__normal_input():
    input = np.array(
        [
            [[2, 2, 2], [3, 3, 3]],  # Sample 1
            [[4, 4, 4], [5, 5, 5]],  # Sample 2
        ]
    )
    expected_output = np.array(
        [
            [3, 3, 3],  # Sensor 1
            [4, 4, 4],  # Sensor 2
        ]
    )
    assert (lp.compute_avg(input) == expected_output).all() == True


def test_compute_max__normal_input():
    input = np.array(
        [
            [[1, 1, 1], [2, 2, 2]],  # Sample 1
            [[3, 3, 2], [4, 4, 1]],  # Sample 2
        ]
    )
    expected_output = np.array(
        [
            3,  # Sensor 1
            3,  # Sensor 2
        ]
    )
    assert (lp.compute_max(input) == expected_output).all() == True
