import tempfile
import util.io.io as io

def test_get_hdf5_files__normal_input():
    # temporary directory with files



    hdf5_list = io.get_hdf5_files(input_path)
    expected_hdf5_list = ["1.hdf5", "2.hdf5", "3.hdf5"]

