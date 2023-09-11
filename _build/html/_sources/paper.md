--
title: The University of Toronto Climate Downscaling Workflow: Tools and Resources for Climate Change Impact Analysis

authors:
- name: Michael Morris
  affiliation: 1
- name: Paul J. Kushner
  orcid: 0000-0002-6404-4518
  affiliation: 1
- name: Karen L. Smith
  orcid: 0000-0002-4652-6310
  affiliation: 2
affiliations:
- name: Department of Physics, University of Toronto
  index: 1
- name: Department of Physical and Environmental Sciences, University of Toronto Scarborough
  index: 2
date: 2023
bibliography: paper.bib
--

# Summary

The University of Toronto Climate Downscaling Workflow (UTCDW) is a resource designed to teach users how to produce their own statistically downscaled climate projections for the purpose of climate change impact analysis. The target audience is graduate students or practitioners who may work outside the field of climate science, but are interested in how their subject of study is sensitive to climate change. The main component of the UTCDW is a [Jupyter Book](https://utcdw.physics.utoronto.ca/UTCDW_Guidebook/README.html) we call the "UTCDW Guidebook". The guidebook book introduces users to fundamental topics of climate science and downscaling, and unpacks the decisions that must be made when designing a climate change impact study. It demonstrates how to download climate data, do exploratory analysis and model validation, and provides examples of end-to-end workflows for small climate downscaling projects. All of the guidebook source materials (Jupyter Notebooks, markdown files, and Python scripts) are accessible in the [UTCDW_Guidebook GitHub repository](https://github.com/mikemorris12/UTCDW_Guidebook). The UTCDW also includes a [website](https://utcdw.physics.utoronto.ca/) that contains a guided survey that helps a user design their climate impact study and generated a flowchart image that lays out the steps for the workflow. While this website is separate from the JOSE submission, the flowcharts are featured in the worked examples (Chapter 6) to explain the process of study design and analysis before acquiring, analyzing, and interpreting the data.

# Statement of Need

Important natural and human-designed systems in disciplines such as ecology, engineering, and public health are sensitive to weather and climate conditions. This means these systems are also sensitive to the impacts of anthropogenic global warming and climate change. As climate change intensifies, climate-sensitive entities are set to become more vulnerable to climate risk. Therefore we need to answer important questions about design, risk assessment, and practical solutions to mitigate damaging climate change. However, available climate data from weather-station observations, satellites, gridded observational products, and climate models, usually don’t directly meet the requirements of end users. Models are imperfect and observations contain errors, so model output is typically not consistent with the observed climate. In addition, available climate information doesn’t directly correspond to useful metrics for calculating loads and hazards, for example, not being available on the required spatial scales and time scales. Generally, climate data is not specific to a given site or set of sites such as a residential area, an electric power grid, or a watershed. Downscaling refers to a set of procedures that adjust and map climate data to variables, times, and locations, relevant for applications. It involves a calibration, using statistics, physical reasoning, and modelling, of climate model output using observations and analysis requirements for specific study domains. Downscaling is enriched with expertise on understanding of the climate system and subject matter expertise. Engineering firms, government departments, and non-profit organizations carry out downscaling routinely to help various clients and stakeholders adapt to a changing climate and seek effective solutions to the dangerous effects of climate change. 

Unfortunately, there is no single accepted standard for downscaling, only a range of methods that are centred on the practice of different climate-service providers. This makes it hard for new researchers to get started and perform their own analysis, especially when existing downscaled data products do not suit their needs. The UTCDW documents state-of-the-art methods for statistical bias correction and downscaling that are easy for technically competent users to implement, and helps users build this technical competence in the early guidebook chapters. Other educational materials on climate change impact assessment are available, but they are either limited regarding the complexity of the methods covered [@anderson_narrative_2021], lack code examples to help new users actually work with the data they need [@kotamarthi_downscaling_2021], or are too advanced for a first introduction to downscaling [@maraun_statistical_2018]. The UTCDW Guidebook fills this gap by providing a basic introduction to concepts in climate science and including worked examples and code for downscaling methods appropriate for research applications. This makes the UTCDW ideal for users who are new to these concepts and wish to be able to start doing data analysis for their impact study as quickly as possible.

# Guidebook Content

The UTCDW guidebook consistents of six chapters. The first four chapters teach the reader the background knowledge required to do downscaling. Chapter 1 discusses the purpose of the book, points to some prerequisite material, and explains how to set up the Python computing environment. Chapter 2 is an introduction to climate science and climate modeling, so readers build an understanding of how climate change projections are made and what their limitations are. Chapter 3 is where the book begins to work with real climate data, and shows how one can access observational, reanalysis, and climate model data to use for an impact study. Chapter 4 contains explanations of various methods of bias-correction and downscaling methods, and examples of how to validate historical downscaled model output and assess future projections. The next two chapters puts together



Chapter 6 contains worked examples of the UTCDW, building on the material and methods covered in the earlier chapters. The examples implement both bias-adjustment of one-dimensional time series representing data for a single location, and gridded downscaling methods to enhance the spatial resolution of model projections over an extended region. For users who do not wish to use pre-processed downscaled data, the guidebook also shows users how to access ready-to-use downscaled model output for Canada from the Pacific Climate Impacts Consortium [@pacific_climate_impacts_consortium_statistically_2021] and links to other publicly available downscaled data products for additional regions or the globe. In either case, the examples demonstrate the end-to-end process of stating a problem, acquiring the necessary data, producing calibrated projections of the relevant metrics, and quantifying uncertainty.