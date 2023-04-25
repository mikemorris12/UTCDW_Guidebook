# UTCDW Guidebook 

# Section 1: Introduction

Welcome to the guidebook for the University of Toronto Climate Downscaling Workflow. If you're accessing these resources, it means you are interested in using data to study how climate change may affect a particular domain in the built or natural environment. The purpose of this guidebook is to help you develop the skills and knowledge needed to design and conduct a climate change impact analysis study. 

Users from outside of the climate science community may not be familiar with how climate change projections are produced, what sort of data is available, and how climate data is typically structured. For this reason, we encourage users new to working with climate data to work through an online learning resource developed as a predecessor to the UTCDW: [Engineering in a Changing Climate: A Transdisciplinary Workshop Series for Engineering and Climate Science Students](https://edtech.engineering.utoronto.ca/project/engineering-changing-climate).

Module 1 (Introduction to Climate Science and Modelling) will introduce basic concepts in climate science and climate modeling. This topic will be expanded upon in Section 2 of this book. Section 3 will demonstrate to the user how to acquire and explore climate data, both from observations and climate model simulations, using the Python programming language.

Module 2 (Regional Downscaling) will discuss the basics of post-processing climate change projections to make them appropriate and useful for local-scale applications (i.e. for studying a particular region, city, or location). This processing step is called Downscaling (the "D" in UTCDW), and it is crucial for any climate change impact study. Section 4 of this book will expand upon the e-Learning module by discussing topics including methods for statistical downscaling in practice, and which methods are suitable for different applications.

The latter portion of this book will introduce the "W" in UTCDW. Section 5 will help make explicit the decisions and compromises that must be made during study design, and help the user develop a workflow for acquiring, processing, and analyzing climate change projection data tailored for their study application. Finally, Section 6 will lay out examples of implementing this workflow for several different downscaling methods.

A Note About Computational Resource Requirements

The volume of data to be processed as a part of a climate impact study can be very large. Multiple decades of global climate model data for a single variable at daily time frequency (e.g., air temperature at 2 m height) can add up to tens or even hundreds of GB. Most data hosting services do not support spatial sub-setting before downloading the data, so for most use cases you will need significant data storage resources, if not significant computing (processor and memory) resources as well. This guide will assume you have access to such resources, either via your research group's in-house cluster, a HPC cluster such as SciNet at the University of Toronto, or a cloud computing service such as Amazon Web Services. Certain free-to-use climate analytics platforms are available, such as [PAVICS](https://pavics.ouranos.ca/index.html), but this guide aims to be independent of the computing platform you intend to use and does not provide support or guidance regarding their use.

### A Note about Statistics

The downscaling methods described and implemented in this guidebook make use of fundamental concepts in probability and statistics. As such, understanding of these concepts is necessary for understanding the methods presented in Section 4. Readers with little or no background in statistics are encouraged to review the textbook "Statistical Methods in the Atmospheric Sciences" (Wilks, 2019) ([UofT Libraries Permalink](https://librarysearch.library.utoronto.ca/permalink/01UTORONTO_INST/14bjeso/alma991106867754106196)), particularly Chapters 1-4. 

### Appendix 1a: Setting Up Your Python Environment

The programming language used in the UTCDW is the latest version of Python 3, with the Anaconda3 package/environment manager. This guide will assume basic familiarity with Python, but not necessarily the packages used for analysis. If you do not have Python/Anaconda installed on your machine, [you can follow the instructions here](https://docs.anaconda.com/anaconda/install/).

Once you have Anaconda installed, you must create an environment in which you will install all the necessary packages. Do this using by entering the following command into your command line terminal (on MacOS or Linux) or from the Anaconda Prompt.

conda create -n UTCDW python=3.9

Next, activate the environment using:

`conda activate UTCDW`

Because one of the packages you need to install (ec3, used for downloading weather station observational data from Environment and Climate Change Canada) is a custom package from a personal channel, the following commands will need to be run for conda to be able to find the package:

`conda config --prepend channels conda-forge`

`conda config --append channels claut`

And install the following packages, each using the command:

`conda install <package name>`

* `numpy` (used for arrays and other mathematical operations)
* `scipy` (additional scientific and mathematical operations)
* `matplotlib` (for making plots)
* `cartopy` (for plotting maps)
* `pandas` (tabular data analysis and other useful functions)
* `jupyterlab` (for working in Jupyter notebooks)
* `xarray` (workhorse package for netCDF data and arrays with coordinates)
* `netcdf4` (backend package for xarray's netCDF file handling)
* `ec3` (for downloading Canadian weather station observational data)
* `esgf-pyclient` (for downloading climate model data)
* `requests` (another package for downloading data files)
* `tdqm` (progress bar for downloading data)
* `dask` (for speeding up xarray operations via parallel computing)
* `xesmf` (for re-gridding climate data)
* `xclim` (workhorse package for statistical downscaling and other climate analysis)

Once you've installed each of these packages, your Python environment will be ready for you to run the examples in this book, and eventually, to get started on working with climate data in Python.