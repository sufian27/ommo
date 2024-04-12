import os
import csv


def get_hdf5_files(input_path: str) -> list:
    """
    
    Gets all the hdf5 files from an input directory path

    Parameters
    ----------
    input_path : str
        the directory path to retreive hdf5 files from

    Returns
    -------
    hdf5_list : list
        list of strings with hdf5 files in the input path
    """

    all_files = os.listdir(input_path)
    dir_list = [os.path.join(input_path, f) for f in all_files]
    # only grab the hdf5 files
    hdf5_list = list(filter(lambda file: file[-5:] == ".hdf5", dir_list))
    return hdf5_list



def check_path(path: str):
    """
    
    Checks if the directory path is valid

    Parameters
    ----------
    path : str
        the directory path to validate

    Raises
    ------
    Exception
        raises exception if the path does not exist or
        the path is not a valid directory
    """

    # check if path exists
    if not os.path.exists(path):
        raise Exception(f"{path} does not exist")
    # check if it is a directory
    if not os.path.isdir(path):
        raise Exception(f"{path} is not a valid directory")


def output_to_csv(output_dir: str, output_dict: dict, filename: str) -> None:
    """
    
    Outputs the output dictionary to the CSV file at output_dir with 
    filename
    
    Parameters
    ----------
    output_dir : str
        the directory path to output the csv files to
    output_dict : dict
        the dictionary of rows with each row being a dictionary
        with key-value pairs
    filename : str
        the csv file name to output
    """

    # get unique header list
    headers = set()
    for row in output_dict:
        for col in output_dict[row]:
            headers.add(col)

    headers = sorted(list(headers))
    # output to file
    with open(os.path.join(output_dir, filename), "w") as f:
        csvWriter = csv.DictWriter(f, fieldnames=headers)
        # write the headers
        csvWriter.writeheader()
        # write each row
        for row in output_dict:
            csvWriter.writerow(output_dict[row])
