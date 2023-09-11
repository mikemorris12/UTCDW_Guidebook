# 1.1 Setting Up Your Python Environment

The programming language used in the UTCDW is the latest version of Python 3, with the Anaconda3 package/environment manager. This guide will assume basic familiarity with Python, but not necessarily the packages used for analysis. If you do not have Python/Anaconda installed on your machine, [you can follow the instructions here](https://docs.anaconda.com/anaconda/install/).

Once you have Anaconda installed, you must create an environment in which you will install all the necessary packages. Because one of the packages you need to install (ec3, used for downloading weather station observational data from Environment and Climate Change Canada) is a custom package from a personal channel, the following commands will need to be run for conda to be able to find the package:

`conda config --prepend channels conda-forge`

`conda config --append channels claut`

Now you are ready to set up your Conda environemnt. To ensure version compatability, we have provided files which can be used to install all of the required Python packages with the versions used for development of the guidebook. Set up the environment by entering the following command into your command line terminal (on MacOS or Linux) or from the Anaconda Prompt.

* `conda env create -f UTCDW_env_Linux.yml` (Linux)
* `conda env create -f UTCDW_env_MacOS.yml` (MacOS with Apple Silicon chip)

Once set up, you can activate the environment using the command:

`conda activate UTCDW`

Most, but not all, of the packages used for this guidebook are listed below. If you prefer to work in your pre-existing conda environment, or if you are having issues setting up your environment using the provided `.yml` files, you can install them using

`conda install <package names>`

Where `<package names>` is to be replaced by the following package names, each separated by a space. Installing all packages at once helps ensure version consistency for packages that depend on others (e.g. `pandas` and `xarray` have dependencies on `numpy` and `scipy`, `cartopy` has a dependency on `matplotlib`, etc.). Anaconda attempts to ensure that there are no dependency issues with existing packages when installing a new one, but sometimes error can arise when installing packages one-by-one.

List of environments:

* `numpy` (used for arrays and other mathematical operations)
* `scipy` (additional scientific and mathematical operations)
* `matplotlib` (for making plots)
* `cartopy` (for plotting maps)
* `nc-time-axis` (for plotting time series)
* `pandas` (tabular data analysis and other useful functions)
* `jupyterlab` and/or `notebook` (for working in Jupyter notebooks)
* `xarray` (workhorse package for netCDF data and arrays with coordinates)
* `netCDF4` (backend package for xarray's netCDF file handling)
* `zarr` (backend package for handling zarr data store files)
* `ec3` (for downloading Canadian weather station observational data)
* `esgf-pyclient` (for downloading climate model data)
* `gcsfs` (for accessing climate model data stores on Google Cloud Services)
* `siphon` (for downloading data files)
* `requests` (another package for downloading data files)
* `tqdm` (progress bar for downloading data)
* `dask` (for speeding up xarray operations via parallel computing)
* `dask-ml` (regression functions for use with `dask.array` data types)
* `xesmf` (for re-gridding climate data)
* `xclim` (workhorse package for statistical downscaling and other climate analysis)
* `libpysal` and `esda` (for calculating spatial autocorrelations)

Once you've set up your Python environment, you will be able to run the examples in this book, and eventually, to get started on working with climate data in Python.