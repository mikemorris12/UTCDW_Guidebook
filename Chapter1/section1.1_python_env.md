# 1.1 Setting Up Your Python Environment

The programming language used in the UTCDW is the latest version of Python 3, with the Anaconda3 package/environment manager. The Guidebook assumes basic familiarity with Python, but not necessarily all of the packages used for analysis. If you do not have Python/Anaconda installed on your machine, [you can follow the instructions here](https://docs.anaconda.com/anaconda/install/).

Once you have Anaconda installed, you must create an environment in which you will install all the necessary packages. Because one of the packages you need to install (ec3, used for downloading weather station observational data from Environment and Climate Change Canada) is a custom package from a personal channel, the following commands will need to be run for conda to be able to find the package:

`conda config --prepend channels conda-forge`

`conda config --append channels claut`

Now you are ready to set up your Conda environment. To ensure version compatibility, we have provided files in the [UTCDW GitHub repository](https://github.com/mikemorris12/UTCDW_Guidebook) which can be used to install all of the required Python packages with the versions used for development of the Guidebook. Set up the environment by entering the following command into your command line terminal (on MacOS or Linux) or from the Anaconda Prompt (Windows), since Windows does not include a native Terminal application. 

* `conda env create -f UTCDW_env_Linux.yml` (Linux)
* `conda env create -f UTCDW_env_MacOS.yml` (MacOS with Apple Silicon chip)
* `conda env create -f UTCDW_env_Windows.yml` (Windows)

```{note}
The UTCDW_env_Windows.yml does not include certain packages available in the MacOS and Linux environment files, such as [xesmf](https://xesmf.readthedocs.io/en/latest/index.html), since they are not compatible with the Windows operating system. See [this page](https://xesmf.readthedocs.io/en/latest/installation.html#notes-for-windows-users) for further explanation, and possible workarounds. The xesmf package is primarily used within the [BCCA gridded downscaling code](https://github.com/mikemorris12/UTCDW_Guidebook/blob/master/downscaling_code/BCCA.py), used in the example in [Chapter 6.5](https://utcdw.physics.utoronto.ca/UTCDW_Guidebook/Chapter6/section6.5_gridded_DBCCA_example.html). Windows users will not be able to run this code without implementing one of the workarounds described in the xesmf documentation.
```

Once set up, you can activate the environment using the command:

`conda activate UTCDW-env`

Most, but not all, of the packages used for the UTCDW Guidebook are listed below. If you prefer to work in your pre-existing conda environment, or if you are having issues setting up your environment using the provided `.yml` files, you can install them using

`conda install <package names>`

Where `<package names>` is to be replaced by the following package names, each separated by a space. Installing all packages at once helps ensure version consistency for packages that depend on others (e.g. `pandas` and `xarray` have dependencies on `numpy` and `scipy`, `cartopy` has a dependency on `matplotlib`, etc.). Anaconda attempts to ensure that there are no dependency issues with existing packages when installing a new one, but sometimes errors can arise when installing packages one-by-one.

List of packages:

* `numpy` (used for arrays and other mathematical operations)
* `scipy` (additional scientific and mathematical operations)
* `matplotlib` (for making plots)
* `seaborn` (for styling plots)
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
* `scikit-learn` (regression functions with `numpy.array` data types)
* `xesmf` (for re-gridding climate data)
* `xclim` (workhorse package for statistical downscaling and other climate analysis)
* `xskillscore` (useful functions for climate data and xarray)
* `libpysal` and `esda` (for calculating spatial autocorrelations)

Once you've set up your Python environment, you will be able to run the examples in this Guidebook, and eventually, to get started on working with climate data in Python.