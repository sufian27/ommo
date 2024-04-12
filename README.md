# OMMO PROJECT

This is a Python library for dealing with HDF5 (Hierarchical Data Format version 5) files and sensor data. 

## About the project

Given an input directory of hdf5 files, outputs two CSV files:

- File 1: contains the average x, y, and z coordinates for each sensor's samples.
- File 2: contains the maximum euclidian distance for each sensor's samples.

## Getting started

### Dependencies

Libraries used:

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

- [h5py](https://pypi.org/project/h5py/)
```bash
pip install h5py
```
- os
- csv
- numpy
```bash
pip install numpy
```

### Installation

1. Clone the repository
```bash
git clone https://github.com/Hassanmushtaq524/ommo.git
```
2. Install the dependencies

### Usage

Use python3 to run the code, providing input and output directory paths that should already exist.

```bash
python3 logs_processor_main.py <input_path> <output_path>
```





