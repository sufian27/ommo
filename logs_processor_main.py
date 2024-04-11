import h5py
import numpy as np
import sys
import util.processing.logs_processing as lp
import util.verification.verification as ver
import util.io.io as io


def main():
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

    output_avg = dict()
    output_max = dict()
    # Perform computations on each file
    for file_path in files:
        print(f"COMPUTING FOR: {file_path}")
        file_avg, file_max = compute(file_path)
        output_avg[file_path] = file_avg
        output_max[file_path] = file_max

    # output the result
    io.output_to_csv(output_dir, output_avg, "file1.csv")
    io.output_to_csv(output_dir, output_max, "file2.csv")


"""
    file_path: the path to the hdf5 file
    output_avg: the output dictionary for avg positions
    output_max: the output dictionary for max position 
    return: a list with average positions for each sensor for a device
"""


def compute(file_path: str):
    output_avg = dict()
    output_max = dict()
    # open file
    with h5py.File(file_path, "r") as file:
        # check if the hdf5 is formatted correctly and calculate average position
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

            # TODO: Make this into a helper method
            # create output rows
            output_avg["file"] = file_path
            output_max["file"] = file_path

            for i, lis in enumerate(avg_list):
                output_avg[f"{device}_S{i}_x"] = lis[0]
                output_avg[f"{device}_S{i}_y"] = lis[1]
                output_avg[f"{device}_S{i}_z"] = lis[2]

            for i, val in enumerate(max_list):
                output_max[f"{device}_S{i}_max"] = val

    return output_avg, output_max


if __name__ == "__main__":
    main()
