import h5py


def verify(device, obj, file):
    """
    Helper method to help verify hdf5 structure
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
