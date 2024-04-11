import os
import csv

"""
    input_path: the directory path to retreive hdf5 files from
    return: a list of .hdf5 file names in the path
"""


def get_hdf5_files(input_path: str) -> list:
    all_files = os.listdir(input_path)
    dir_list = [os.path.join(input_path, f) for f in all_files]
    # only grab the hdf5 files
    hdf5_list = list(filter(lambda file: file[-5:] == ".hdf5", dir_list))
    return hdf5_list


"""
    path: the directory path to verify
    return: void
"""


def check_path(path: str):
    # check if path exists
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")
    # check if it is a directory
    if not os.path.isdir(path):
        raise Exception(f"{path} is not a valid directory")


"""
    output_dir: the output csv files path
    output_dict: the dictionary of rows with each row being a dictionary
    with key-value pairs
    return: outputs to the CSV file at output_dir with name filename
"""


def output_to_csv(output_dir: str, output_dict: dict, filename: str) -> None:
    # get unique header list
    headers = set()
    for row in output_dict:
        for col in output_dict[row]:
            headers.add(col)

    headers = sorted(list(headers))
    # output to file
    with open(f"{output_dir}/{filename}", "w") as f:
        csvWriter = csv.DictWriter(f, fieldnames=headers)
        # write the headers
        csvWriter.writeheader()
        # write each row
        for row in output_dict:
            csvWriter.writerow(output_dict[row])
