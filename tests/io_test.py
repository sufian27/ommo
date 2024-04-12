import util.io.io as io
import pytest
import csv
from contextlib import contextmanager

@contextmanager
def not_raises(exception):
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")
  

def test_get_hdf5_files(tmp_path):
    # temporary directory with files
    dir = tmp_path / "tmp_directory"
    dir.mkdir()

    for i in range(5):
        (dir / f"tmp_{i}.txt").touch()
    for i in range(5):
        (dir / f"tmp_{i}.hdf5").touch()
    for i in range(5):
        (dir / f"tmp_{i}hdf5").touch()
    for i in range(5):
        (dir / f"tmp_{i}.hdf4").touch()
    for i in range(5):
        (dir / f"tmp_{i}").mkdir()

    hdf5_list = io.get_hdf5_files(dir)
    expected_hdf5_list = [str(dir / f"tmp_{i}.hdf5") for i in range(5)]

    assert set(hdf5_list) == set(expected_hdf5_list)


def test_path_not_exists(tmp_path):
    # temporary directory
    dir = tmp_path / "tmp_directory"
    dir.mkdir()

    expected_err = f"{str(dir / "incorrect_directory")} does not exist"

    with pytest.raises(Exception, match=expected_err) as e_info:
        io.check_path(str(dir / "incorrect_directory"))   


def test_path_not_directory(tmp_path):
    # temporary file
    incorrect_dir = tmp_path / "tmp_directory"
    incorrect_dir.touch()

    expected_err = f"{str(incorrect_dir)} is not a valid directory"

    with pytest.raises(Exception, match=expected_err) as e_info:
        io.check_path(str(incorrect_dir))


@pytest.mark.parametrize("test_input, expected, expected_headers", [
    (
        {
            "input/1.hdf5": { "file": "input/1.hdf5", "device_1_S0_x": 3.1, "device_1_S0_y": 4.1, "device_1_S0_z": 5.1, "device_1_S1_x": 7.1, "device_1_S1_y": 12.1, "device_1_S1_z": -2.1 },
            "input/2.hdf5": { "file": "input/2.hdf5", "device_1_S0_x": 3.2, "device_1_S0_y": 4.2, "device_1_S0_z": 5.2}
        },
        {
            "input/1.hdf5": { "file": "input/1.hdf5", "device_1_S0_x": "3.1", "device_1_S0_y": "4.1", "device_1_S0_z": "5.1", "device_1_S1_x": "7.1", "device_1_S1_y": "12.1", "device_1_S1_z": "-2.1" },
            "input/2.hdf5": { "file": "input/2.hdf5", "device_1_S0_x": "3.2", "device_1_S0_y": "4.2", "device_1_S0_z": "5.2", "device_1_S1_x": "", "device_1_S1_y": "", "device_1_S1_z": "" }
        },
        ["file", "device_1_S0_x", "device_1_S0_y", "device_1_S0_z", "device_1_S1_x", "device_1_S1_y", "device_1_S1_z"]
    ),
    (
        {
            "input/1.hdf5": { "file": "input/1.hdf5", "device_1_S0_x": 3.1, "device_1_S0_y": 4.1, "device_1_S0_z": 5.1, "device_1_S1_x": 7.1, "device_1_S1_y": 12.1, "device_1_S1_z": -2.1 },
            "input/2.hdf5": { "file": "input/2.hdf5", "device_2_S0_x": 3.2, "device_2_S0_y": 4.2, "device_2_S0_z": 5.2}
        },
        {
            "input/1.hdf5": { "file": "input/1.hdf5", "device_1_S0_x": "3.1", "device_1_S0_y": "4.1", "device_1_S0_z": "5.1", "device_1_S1_x": "7.1", "device_1_S1_y": "12.1", "device_1_S1_z": "-2.1", "device_2_S0_x": "", "device_2_S0_y": "", "device_2_S0_z": "" },
            "input/2.hdf5": { "file": "input/2.hdf5", "device_2_S0_x": "3.2", "device_2_S0_y": "4.2", "device_2_S0_z": "5.2", "device_1_S0_x": "", "device_1_S0_y": "", "device_1_S0_z": "", "device_1_S1_x": "", "device_1_S1_y": "", "device_1_S1_z": "" }
        },
        ["file", "device_1_S0_x", "device_1_S0_y", "device_1_S0_z", "device_1_S1_x", "device_1_S1_y", "device_1_S1_z", "device_2_S0_x", "device_2_S0_y", "device_2_S0_z"] 
    )
])
def test_output__normal_input(tmp_path, test_input, expected, expected_headers):
    # temporary output directory
    output_dir = tmp_path / "tmp_output_dir"
    output_dir.mkdir()

    tmp_file = output_dir / "tmp_file.csv"
    tmp_file.touch()

    with not_raises(Exception):
        io.output_to_csv(str(output_dir), test_input, "tmp_file.csv")

    with open(str(tmp_file), 'r') as f:
        csvReader = csv.DictReader(f)
        # check if headers are correct
        assert (set(expected_headers) == set(csvReader.fieldnames))
        for row in csvReader:
            # every row must be the same
            assert expected[row["file"]] == row


            

