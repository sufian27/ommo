import util.verification.verification as ver
import h5py
import tempfile
import pytest
from contextlib import contextmanager

@contextmanager
def not_raises(exception):
  try:
    yield
  except exception:
    raise pytest.fail(f"DID RAISE {exception}")
  

def test_verify_structure__normal_input():  
    """
    tests the verify function in verification with
    normal input - No exception should be raised
    """

    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        grp = file.create_group("device_1") # device group
        grp.create_dataset("Position", (1000, 2, 3), dtype=float) # dataset
        with not_raises(Exception):
            ver.verify(grp.name, grp, file)


def test_verify_not_group_instance():
    """
    tests whether the verify function in verification raises
    the correct exception
    """

    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        incorrect_grp = file.create_dataset("device_1", (1000, 2, 3)) # not a group instance 
        expected_err = f"{incorrect_grp.name} is not a group of datasets"
        with pytest.raises(Exception, match=expected_err) as e_info:
            ver.verify(incorrect_grp.name, incorrect_grp, file)


def test_verify_no_position_key():
    """
    tests whether the verify function in verification raises
    the correct exception
    """
    
    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        grp = file.create_group("device_1") # device group
        grp.create_dataset("Speed", (1000, 2, 1), dtype=float) # not position dataset
        expected_err = f"Position is not a dataset for {grp.name}"
        with pytest.raises(Exception, match=expected_err) as e_info:
            ver.verify(grp.name, grp, file)


def test_verify_not_dataset_instance():
    """
    tests whether the verify function in verification raises
    the correct exception
    """

    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        grp = file.create_group("device_1") # device group
        grp.create_group("Position") # a position group
        expected_err = f"Position is not a dataset in the group: {grp.name}"
        with pytest.raises(Exception, match=expected_err) as e_info:
            ver.verify(grp.name, grp, file)