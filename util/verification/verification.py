import h5py


def verify(device, obj, file):
    """
    
    Helper method to verify hdf5 structure
    
    Parameters
    ----------
    device : str
        the device name
    obj : h5py.Group
        the instance of hdf5 group to verify
    file : h5py.File
        the hdf5 file instance to verify

    Raises
    ------
    Exception
        if the obj parameter is not an instance of hdf5 group
    Exception
        if the Position key is not the group obj
    Exception
        if the Position key in the group is not an instance of hdf5
        dataset
    """

    # check if the object in file is a group
    if not isinstance(obj, h5py.Group):
        raise Exception(f"{device} is not a group of datasets")
        # check if the device group has a key "Position"
    if "Position" not in file[device]:
        raise Exception(f"Position is not a dataset for {device}")
        # check if the device's "Position" key is a dataset
    if not isinstance(file[device]["Position"], h5py.Dataset):
        raise Exception(f"Position is not a dataset in the group: {device}")
