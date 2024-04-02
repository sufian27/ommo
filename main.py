import h5py
import numpy as np
import sys
import os
import logging



def main():
    
    # check input format
    if (len(sys.argv) != 3):
        print("Incorrect command")
        print("Use: py main.py <INPUT PATH> <OUTPUT PATH>")
        sys.exit(-1)

    inputDir = sys.argv[1]
    outputDir = sys.argv[2]

    # check if input and output paths are correct
    checkPath(inputDir)
    checkPath(outputDir)
    
    # get the hdf5 files in a list
    files = getHDF5Files(inputDir)

    # Perform computations on each file
    for filePath in files: 
        print("COMPUTING FOR: " + filePath)  
        compute(filePath)
        


"""
    path: the directory path to verify
    return: void
"""    
def checkPath(path: str):

    # 
    # TODO
    # 
    try:
        
        if (not os.path.exists(path)):
            raise FileNotFoundError(path + " does not exist")
        
        if (not os.path.isdir(path)):
            raise Exception(path + " is not a valid directory")
    
    except (Exception, FileNotFoundError) as e:
        print(e)
        sys.exit(-1)

    return


"""
    path: the input directory path
    return: a list of .hdf5 file names in the path
"""                        
def getHDF5Files(path: str) -> list:
    allFiles = os.listdir(path)
    dir_list = [ path + "/" + f for f in allFiles]
    # only grab the hdf5 files 
    hdf5List = list(filter(lambda file: file[-5:] == ".hdf5", dir_list))
    
    return hdf5List



"""
    filePath: the path to the hdf5 file
    return: a list with average positions for each sensor for a device
"""
def compute(filePath: str) -> None:
    # open file
    with h5py.File(filePath, 'r') as f:
        # output storage
        outputDict = dict()
        # check if the hdf5 is formatted correctly and calculate average position
        for device, obj in f.items():
            # verify the structure of the hdf5 file
            # 
            # TODO
            # 
            try:


                if (not isinstance(obj, h5py.Group)):
                    raise TypeError("Not a group")

                if ("Position" not in f[device].keys()):
                    raise Exception("Position dataset is not in the group: " + device)

                if (not isinstance(f[device]["Position"], h5py.Dataset)):
                    raise TypeError("Position is not a dataset in the group: " + device)
                
            except TypeError as e:
                print(e)
                continue
            except Exception as e:
                print(e)
                sys.exit(-1)

            # perform computations
            dset = np.array(f[device]["Position"])
            numSensors = dset.shape[1]
            numSamples = dset.shape[0]

            print("Device: " + device)
            if (device not in outputDict.keys()):
                outputDict = {
                    device: {
                        "avgPosition": calculateAvgPosition(dset, numSensors, numSamples),
                        "maxDistance": calculateMaxDistance(dset, numSensors, numSamples)
                    }
                }
            
            print(outputDict)


"""
    dset: the dataset to calculate avg position for
    numSensors: the number of sensors for the device
    numSamples: the number of samples in the device for each sensor
    return: the list of avg positions for each sensor
"""
def calculateAvgPosition(dset: list[float], numSensors: int, numSamples: int) -> list[float]:

    avgList = np.zeros((numSensors, 3), dtype=float)

    #   loop through every sensor and calculate average
    for i in range(numSensors):
        for sample in dset:
            # x
            avgList[i][0] += sample[i][0]
            # y
            avgList[i][1] += sample[i][1]
            # z
            avgList[i][2] += sample[i][2]
        # compute
        avgList[i] = [ avgList[i][0] / numSamples, avgList[i][1] / numSamples, avgList[i][2] / numSamples]
    
    # return the list
    return avgList

"""
    dset: the dataset to calculate avg position for
    numSensors: the number of sensors for the device
    numSamples: the number of samples in the device for each sensor
    return: the list of maximum distances for each sensor
"""
def calculateMaxDistance(dset: list[float], numSensors: int, numSamples: int) -> list[float]:
    maxList = np.empty(numSensors, dtype=float)
    # loop through every sensor and grab the maximum distance
    for i in range(numSensors):
        maxDistance = float('-inf')
        for sample in dset:
            distance = ((sample[i][0] ** 2) + (sample[i][1] ** 2) + (sample[i][2] ** 2)) ** 0.5
            maxDistance = max(maxDistance, distance)
        # store the maximum distance
        maxList[i] = maxDistance
    
    return maxList
            


if __name__ == "__main__":
    main()