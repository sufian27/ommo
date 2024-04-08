import h5py
import numpy as np
import sys
import os
import csv



def main():
    # check input format
    if (len(sys.argv) != 3):
        print("Incorrect command")
        print("Use: python3 main.py <INPUT DIR PATH> <OUTPUT DIR PATH>")
        sys.exit(-1)

    # get the input and output directory
    inputDir = sys.argv[1]
    outputDir = sys.argv[2]

    # check the input output path
    checkPath(inputDir)
    checkPath(outputDir)

    # get the hdf5 files in a list
    files = getHDF5Files(inputDir)

    # output storage
    outputAvg = dict()
    outputMax = dict()

    # Perform computations on each file
    for filePath in files: 
        print(f"COMPUTING FOR: {filePath}")  
        compute(filePath, outputAvg, outputMax)

    # output the result
    outputToCSV(outputDir, outputAvg, "file1.csv")
    outputToCSV(outputDir, outputMax, "file2.csv")
      


"""
    path: the directory path to verify
    return: void
"""    
def checkPath(path: str):

    try:
        # check if path exists
        if (not os.path.exists(path)):
            raise Exception(f"{path} does not exist")
        # check if it is a directory
        if (not os.path.isdir(path)):
            raise Exception(f"{path} is not a valid directory")
    except Exception as e:
        # exit the program if error
        print(e)
        sys.exit(-1)


"""
    path: the directory path to retreive hdf5 files from
    return: a list of .hdf5 file names in the path
"""                        
def getHDF5Files(path: str) -> list:

    try:
        allFiles = os.listdir(path)
    except Exception as e:
        print(f"Error opening {path}")
        sys.exit(-1)

    dir_list = [ f"{path}/{f}" for f in allFiles]
    # only grab the hdf5 files 
    hdf5List = list(filter(lambda file: file[-5:] == ".hdf5", dir_list))
    
    return hdf5List





"""
    filePath: the path to the hdf5 file
    outputAvg: the output dictionary for avg positions
    outputMax: the output dictionary for max position 
    return: a list with average positions for each sensor for a device
"""
def compute(filePath: str, outputAvg: dict, outputMax: dict) -> None:
    # open file
    with h5py.File(filePath, 'r') as f:
        outputAvg[filePath] = dict()
        outputMax[filePath] = dict()
        # check if the hdf5 is formatted correctly and calculate average position
        for device, obj in f.items():
            # verify the structure of the hdf5 file
            try:
                # check if the object in file is a group
                if (not isinstance(obj, h5py.Group)):
                    raise Exception(f"{device} is not a group of datasets")
                # check if the device group has a key "Position" 
                if ("Position" not in f[device]):
                    raise Exception(f"Position is not a dataset for {device}")
                # check if the device's "Position" key is a dataset
                if (not isinstance(f[device]["Position"], h5py.Dataset)):
                    raise Exception(f"Position is not a dataset in the group: {device}")                   
            except Exception as e:
                print(e)
                print(f"Skipping {device}. . .")
                continue
            
            # compute
            dset = np.array(f[device]["Position"])
            print(f"Device: {device}")

            # get the average
            avgList = np.mean(dset, axis=0)

            # get the maximum distance
            maxList = np.max(np.linalg.norm(dset, axis=2), axis=0)

            # create output rows
            outputAvg[filePath]["file"] = filePath 
            outputMax[filePath]["file"] = filePath

            for i, lis in enumerate(avgList):
                outputAvg[filePath][f"{device}_S{i}_x"] = lis[0]
                outputAvg[filePath][f"{device}_S{i}_y"] = lis[1]
                outputAvg[filePath][f"{device}_S{i}_z"] = lis[2]
            
            for i, val in enumerate(maxList):
                outputMax[filePath][f"{device}_S{i}_max"] = val



            
"""
    outputDir: the output csv files path
    outputDict: the dictionary of rows with each row being a dictionary
    with key-value pairs
    return: outputs to the CSV file at outputDir with name fileName
"""
def outputToCSV(outputDir: str, outputDict: dict, fileName: str) -> None:
    # get unique header list
    headers = set()
    for row in outputDict:
        for col in outputDict[row]:
            headers.add(col)

    headers = sorted(list(headers))
    # output to file
    with open(f"{outputDir}/{fileName}", "w") as f:
        csvWriter = csv.DictWriter(f, fieldnames=headers)
        # write the headers
        csvWriter.writeheader()
        # write each row
        for row in outputDict:
            csvWriter.writerow(outputDict[row])


if __name__ == "__main__":
    main()