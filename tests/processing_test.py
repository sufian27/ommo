import util.processing.logs_processing as lp
import numpy as np
from math import sqrt


def test_compute_avg__normal_input():
    """
    tests the compute_avg function in logs_processing with
    normal input
    """

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
    """
    tests the compute_max function in logs_processing with
    normal input
    """

    input = np.array(
        [
            [[3, 3, 0], [4, 0, 4]],  # Sample 1
            [[5, 5, 0], [3, 3, 0]],  # Sample 2
        ]
    )
    expected_output = np.array(
        [
            sqrt(5**2 + 5**2),  # Sensor 1
            sqrt(4**2 + 4**2),  # Sensor 2
        ]
    )
    assert (lp.compute_max(input) == expected_output).all() == True
