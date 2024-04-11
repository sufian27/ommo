import h5py
import tempfile


tf = tempfile.TemporaryFile()
with h5py.File(tf, 'w') as file:
    incorrect_grp = file.create_dataset("device_1", (1000, 2, 3)) # not a group instance 

    for device, obj in file.items():
        print(f"{device} : {obj}")