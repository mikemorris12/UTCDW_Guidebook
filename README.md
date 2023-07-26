# UTCDW Guidebook
# Chapter 1: Introduction

*Last updated July 26 2023*

Welcome to the guidebook for the University of Toronto Climate Downscaling Workflow. If you're accessing these resources, it means you are interested in using data to study how climate change may affect a particular domain in the built or natural environment. The purpose of this guidebook is to help you develop the skills and knowledge needed to design and conduct a climate change impact analysis study. 

## Who This Guide is For

The target audience for this guidebook is a researcher with little or no foundation in climate science, who studies a system that is sensitive to weather and climate. For example, an engineer who studies building energy use, which depends on climatic variables such as temperature and humidity. In order to quantitatively study how climate change might affect the system you study and properly interpret the results, you need some basic knowledge of the climate system and climate modeling.

 Users from outside of the climate science community may not be familiar with how climate change projections are produced, what sort of data is available, and how climate data is typically structured. Importantly, you also need to understand the limitations of climate change projections. Rarely are out-of-the-box climate model projections suitable for regional climate impact assessment, so post-processing must be applied to account for systematic biases and coarse spatial sampling, and make the data useful for practitioners or impact modelers. One must also appreciate the irreducible uncertainty inherent to future climate projections, due to factors like uncertain greenhouse gas emission pathways and natural climate variability. This guidebook will introduce you to all of these concepts while also showing code examples of how to access and analyze climate data.

## How to Use This Guide

Before working through the material in this guide, we encourage users new to working with climate data to work through an online learning resource developed as a predecessor to the UTCDW: [Engineering in a Changing Climate: A Transdisciplinary Workshop Series for Engineering and Climate Science Students](https://edtech.engineering.utoronto.ca/project/engineering-changing-climate). Module 1 of the aforementioned resource (Introduction to Climate Science and Modelling) will introduce basic concepts in climate science and climate modeling. These topics will be expanded upon in Chapter 2 of this book. Chapter 3 will demonstrate to the user how to acquire and explore climate data, both from observations and climate model simulations, using the Python programming language.

Module 2 (Regional Downscaling) will discuss the basics of post-processing climate change projections to make them appropriate and useful for local-scale applications (i.e. for studying a particular region, city, or location). This processing step is called Downscaling (the "D" in UTCDW), and it is crucial for any climate change impact study. Chapter 4 of this book will expand upon the e-Learning module by discussing topics including methods for statistical downscaling in practice, and which methods are suitable for different applications.

The latter portion of this book will introduce the "W" in UTCDW. Chapter 5 will help make explicit the decisions and compromises that must be made during study design, and help the user develop a workflow for acquiring, processing, and analyzing climate change projection data tailored for their study application. Finally, Chapter 6 will lay out examples of implementing this workflow for several different downscaling methods.

## Limitations of the UTCDW Guidebook

The UTCDW provides educational material to help you design and conduct your own analyses, but we cannot give detailed guidance on any specific research problem. The guidebook provides general guidance and a few examples, but there are too many possible applications of climate downscaling to be exhaustive. Notably, we cannot tell you *how* your domain application is sensitive to climatic factors. As the expert on the system you study, it's up to you to have a sense of the important climate variables for your application, and how you might quantify the way weather and climate affect your study system. If you require climate data as inputs to a model (for example, a model that calculates building energy use as a function of outside temperature and humidity), then you should be familiar with which input variables are required, and at what spatial and temporal sampling. We call the quantity which depends on climate variables, and is relevant for your domain application, a "climate indicator", whether it's calculated using an analytic expression or a complex numerical model. Climate indicators will be discussed further in Chapter 5, but it's important to know from the start that this guide assumes you have a way to quantify how your study system depends on climatic factors.

## A Note About Computational Resource Requirements

The volume of data to be processed as a part of a climate impact study can be very large. Multiple decades of global climate model data for a single variable at daily time frequency (e.g., air temperature at 2 m height) can add up to tens or even hundreds of GB. Most data hosting services do not support spatial sub-setting before downloading the data, so for most use cases you will need significant data storage resources, if not significant computing (processor and memory) resources as well. This guide will assume you have access to such resources, either via your research group's in-house cluster, a HPC cluster such as [SciNet](https://www.scinethpc.ca/) at the University of Toronto, or a cloud computing service such as Amazon Web Services. Certain free-to-use climate analytics platforms are available, such as [PAVICS](https://pavics.ouranos.ca/index.html), but this guide aims to be independent of the computing platform you intend to use and does not provide support or guidance regarding their use.

## A Note about Statistics

The downscaling and analysis methods described and implemented in this guidebook make use of fundamental concepts in probability and statistics. As such, understanding of these concepts is necessary for understanding the methods presented in Chapter 4. Readers with little or no background in statistics are encouraged to review the textbook "Statistical Methods in the Atmospheric Sciences" (Wilks, 2019) ([UofT Libraries Permalink](https://librarysearch.library.utoronto.ca/permalink/01UTORONTO_INST/14bjeso/alma991106867754106196)), particularly Chapters 1-4. 

## Appendix: Setting Up Your Python Environment

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
