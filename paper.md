--
title: The University of Toronto Climate Downscaling Workflow: Tools and Resources for Climate Change Impact Analysis

authors:
- name: Michael Morris
  orcid: 0000-0002-5758-2182
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

The University of Toronto Climate Downscaling Workflow (UTCDW) is a resource designed to teach users how to produce their own statistically downscaled climate projections for the purpose of climate change impact analysis. The target audience is graduate students or practitioners who may work outside the field of climate science, but are interested in how their subject of study is sensitive to climate change. The main component of the UTCDW is a [Jupyter Book](https://utcdw.physics.utoronto.ca/UTCDW_Guidebook/README.html) we call the "UTCDW Guidebook". The guidebook book introduces users to fundamental topics of climate science and downscaling, and unpacks the decisions that must be made when designing a climate change impact study. It demonstrates how to download climate data, do exploratory analysis and model validation, and provides examples of end-to-end workflows for small climate downscaling projects. All of the guidebook source materials (Jupyter Notebooks, markdown files, and Python scripts) are accessible in the [UTCDW_Guidebook GitHub repository](https://github.com/mikemorris12/UTCDW_Guidebook).

# Statement of Need

Important natural and human-designed systems studied under disciplines such as ecology, engineering, and public health are sensitive to weather and climate conditions. This means these systems are also sensitive to the impacts of anthropogenic global warming and climate change, and as climate change intensifies, they are set to become more vulnerable to climate risk. Therefore experts in these fields need to answer important questions about climate change risk assessment and adaptation. However, unprocessed climate model projections such as those from the CMIP6 [@eyring_overview_2016] archive usually don’t directly meet their requirements. Models are inherently imperfect, so their output is typically not consistent with observed local climates. In addition, raw climate data does not directly correspond to useful metrics for calculating loads and hazards, for example, not being available on the required spatial or temporal scales. Generally, climate data is not specific to a given site or set of sites such as a residential area, an electric power grid, or a watershed. Downscaling refers to a set of procedures that adjust and map climate data to variables, times, and locations, relevant for applications. It involves a calibration, using statistics, physical reasoning, and modelling, of climate model output using observations and analysis requirements for specific study domains. Downscaling is enriched with expertise on understanding of the climate system and subject matter expertise. Engineering firms, government departments, and non-profit organizations carry out downscaling routinely to help various clients and stakeholders adapt to a changing climate and seek effective solutions to the dangerous effects of climate change. 

Unfortunately, there is no single accepted standard for downscaling, only a range of methods that are centred on the practice of different climate-service providers. This makes it hard for new researchers to get started and perform their own analysis, especially when existing downscaled data products do not suit their needs. The UTCDW documents state-of-the-art methods for statistical bias correction and downscaling that are easy for technically competent users to implement, and helps users build this technical competence in the early guidebook chapters. Other educational materials on climate change impact assessment are available, but they are either limited regarding the complexity of the methods covered [@anderson_narrative_2021], lack code examples to help new users actually work with the data they need [@kotamarthi_downscaling_2021], or are too advanced for a first introduction to downscaling [@maraun_statistical_2018]. The UTCDW Guidebook fills this gap by providing a basic introduction to concepts in climate science and including worked examples and code for downscaling methods appropriate for research applications. This makes the UTCDW ideal for users who are new to these concepts and wish to be able to start doing data analysis for their impact study as quickly as possible.

# Guidebook Content

The UTCDW guidebook consists of six chapters. The first four chapters teach the reader the background knowledge required to do downscaling. Chapter 1 discusses the purpose of the book, points to some prerequisite material, and explains how to set up the Python computing environment. Chapter 2 is an introduction to climate science and climate modeling, so readers build an understanding of how climate change projections are made and what their limitations are. Chapter 3 is where the book begins to work with real climate data. It shows users how to access observational, reanalysis, and climate model data to use for an impact study, and how to do exploratory analysis with observational and raw climate model data. Chapter 4 contains explanations of various methods of bias-correction and downscaling methods, and examples of how to validate historical downscaled model output and assess future projections. The reccomended bias-correction methods are the quantile-mapping based methods proposed by @cannon_bias_2015 and implemented in the ``xclim`` package [@logan_xclim_2023], and the downscaling methods, which enhance the spatial resolution of gridded data, are the constructed-analogue (CA) based methods described in @werner_hydrologic_2016. Python code for the CA methods is not currently available in another open-source library, so we provide pre-written functions to implement spatial downscaling.

The next two chapters focus on applying the knowledge and methods covered in Chapters 1-4. Chapter 5 introduces the "Downscaling Workflow" part of the UTCDW. This chapter unpacks the decisions that must be made when designing a climate change impact study, and breaks the analysis tasks down into disgestible steps. Chapter 6 contains several simple examples of the workflow. The examples implement both bias-adjustment of one-dimensional time series representing data for a single location and spatial resolution-enhancing downscaling methods. For users who do not wish to use pre-processed downscaled data, the guidebook also shows users how to access ready-to-use downscaled model output for Canada from the Pacific Climate Impacts Consortium [@pacific_climate_impacts_consortium_statistically_2021] and links to other publicly available downscaled data products for additional regions or the globe. In either case, the examples demonstrate the end-to-end process of stating a problem, acquiring the necessary data, producing calibrated projections of metrics relevant to the application at hand, and quantifying uncertainty in the projections. We welcome user submission of additional worked examples to contribute to future versions of the UTCDW guidebook.

The UTCDW also includes a [website](https://utcdw.physics.utoronto.ca/) that contains a guided survey that helps a user design their climate impact study and generated a flowchart image that lays out the steps for the workflow. While this website is separate from the JOSE submission, the flowcharts are featured in the worked examples (Chapter 6) to explain the procedure before showing the steps of the analysis.

# Acknowledgements

We acknowledge contributions from Anson Cheung, Peikun Guo, and Claire Pan for their testing of very prelimiary versions of the UTCDW content as a part of an undergraduate research course at the University of Toronto, as well as Cassandra Chanen and Lilian Chan for testing of the UTCDW guidebook during its development. We acknowledge funding from the University of Toronto's [Centre for Climate Science and Engineering](https://uoftcse.ca/), [Climate Positive Energy Initiative](https://cpe.utoronto.ca/), and [Data Sciences Institute](https://datasciences.utoronto.ca/).

# References