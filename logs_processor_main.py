import h5py
import numpy as np
import sys
import util.processing.logs_processing as lp
import util.verification.verification as ver
import util.io.io as io


def main():
    """
    
    Gets all the hdf5 files in the input directory, and stores the average
    position and maximum euclidian distance of each sensor as rows
    in output dictionaries. Outputs the data into two separate CSV files.

    * File 1: contains the average x, y, and z coordinates for each sensor's samples.
    * File 2: contains the maximum euclidian distance for each sensor's samples.
      
    Usage: python3 logs_processing_main.py <INPUT DIR PATH> <OUTPUT DIR PATH>
    """

    # check input format
    if len(sys.argv) != 3:
        print("Incorrect command")
        print("Use: python3 logs_processing_main.py <INPUT DIR PATH> <OUTPUT DIR PATH>")
        sys.exit(-1)

    # get the input and output directory
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    # check the input output path and get all files
    try:
        io.check_path(input_dir)
        io.check_path(output_dir)
        files = io.get_hdf5_files(input_dir)
    except Exception as e:
        # exit the program if error
        print(e)
        sys.exit(-1)

    avg_rows = dict()
    max_rows = dict()
    # Perform computations on each file
    for file_path in files:
        print(f"COMPUTING FOR: {file_path}")
        file_avg, file_max = compute(file_path)
        avg_rows[file_path] = file_avg
        max_rows[file_path] = file_max

    # output the result
    io.output_to_csv(output_dir, avg_rows, "file1.csv")
    io.output_to_csv(output_dir, max_rows, "file2.csv")


def compute(file_path: str):
    """
    
    Loops through the device groups in hdf5 file and computes the average
    position and maximum euclidian distance for all sensors in the device

    Parameters
    ----------
    file_path : str
        the path to the hdf5 file

    Returns
    -------
    avg_rows : dict
        the dictionary with average position for every sensor in the hdf5 file
    max_rows : dict
        the dictionary with maximum euclidian distance for every sensor in the hdf5 file
    """

    with h5py.File(file_path, "r") as file:
        for device, obj in file.items():
            # verify the structure of the hdf5 file
            try:
                ver.verify(device, obj, file)
            except Exception as e:
                print(e)
                print(f"Skipping {device}. . .")
                continue

            # compute
            print(f"Device: {device}")
            dataset = np.array(file[device]["Position"])

            # get the average
            avg_list = lp.compute_avg(dataset)
            # get the maximum distance
            max_list = lp.compute_max(dataset)

            # create output rows
            avg_rows = lp.get_avg_rows(avg_list, device)
            avg_rows["file"] = file_path
            max_rows = lp.get_max_rows(max_list, device)
            max_rows["file"] = file_path

    return avg_rows, max_rows


if __name__ == "__main__":
    main()
