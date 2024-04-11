import util.verification.verification as ver
import h5py
import tempfile


def test_verify_structure__normal_input():  
    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        grp = file.create_group("device_1") # device group
        grp.create_dataset("Position", (1000, 2, 3), dtype=float) # dataset
        try:
            ver.verify(grp.name, grp, file)
            # no exception raised
            assert True
        except Exception as e:
            # exception raised
            assert False, f"verify({grp.name}, {grp}, {file}) raised an exception: {e}"


def test_verify_not_group_instance():
    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        incorrect_grp = file.create_dataset("device_1", (1000, 2, 3)) # not a group instance 
        expected_err = f"{incorrect_grp.name} is not a group of datasets"
        try:
            ver.verify(incorrect_grp.name, incorrect_grp, file)
            # no exception raised
            assert False, f"verify({incorrect_grp.name}, {incorrect_grp}, {file}) did not raise exception"
        except Exception as e:
            # exception raised
            assert (str(e) == expected_err) == True


def test_verify_no_position_key():
    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        grp = file.create_group("device_1") # device group
        grp.create_dataset("Speed", (1000, 2, 1), dtype=float) # not position dataset
        expected_err = f"Position is not a dataset for {grp.name}"
        try:
            ver.verify(grp.name, grp, file)
            # no exception raised
            assert False, f"verify({grp.name}, {grp}, {file}) did not raise exception"
        except Exception as e:
            # exception raised
            assert (str(e) == expected_err) == True


def test_verify_not_dataset_instance():
    tf = tempfile.TemporaryFile()
    with h5py.File(tf, 'w') as file:
        grp = file.create_group("device_1") # device group
        grp.create_group("Position") # a position group
        expected_err = f"Position is not a dataset in the group: {grp.name}"
        try:
            ver.verify(grp.name, grp, file)
            # no exception raised
            assert False, f"verify({grp.name}, {grp}, {file}) did not raise exception"
        except Exception as e:
            # exception raised
            assert (str(e) == expected_err) == True