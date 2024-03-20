---
title: 'The University of Toronto Climate Downscaling Workflow: Tools and Resources for Climate Change Impact Analysis'
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
date: March 2024
bibliography: paper.bib
---

# Summary

The University of Toronto Climate Downscaling Workflow (UTCDW) is a resource designed to teach users how to produce their own statistically downscaled climate projections for the purpose of climate change impact analysis. The target audience includes graduate students and practitioners in engineering, the physical, mathematical, and computational sciences, who are interested in how their subject of study is sensitive to climate change. The main component of the UTCDW is a [Jupyter Book](https://utcdw.physics.utoronto.ca/UTCDW_Guidebook/README.html) called the "UTCDW Guidebook". The Guidebook introduces users to basic climate science concepts and beginning-to-intermediate concepts in the application of statistical climate downscaling. It also works through the decisions that must be made when designing a climate change impact study. Finally, it demonstrates how to download climate data, do exploratory analysis and model validation, and provides examples of end-to-end workflows for small climate downscaling projects. The Guidebook was written for self-study by members of the target audience, though it may be included as a part of a course on climate change impact analysis for graduate students or upper-year undergraduate students in the applied sciences. All of the Guidebook source materials are accessible in the [UTCDW_Guidebook GitHub repository](https://github.com/mikemorris12/UTCDW_Guidebook).

# Statement of Need

Important natural and human-designed systems are sensitive to weather and climate conditions, and are therefore also sensitive to the impacts of anthropogenic climate change. Experts in these fields need to assess climate change risks, but unprocessed climate model output such as those from the CMIP6 [@eyring2016] archive is usually not fit for this purpose. Raw climate model outputs do not directly correspond to useful metrics for calculating loads and hazards, and are often not available on the required spatial or temporal scales. *Downscaling* refers to a set of procedures that adjust and map climate data to variables, times, and locations, relevant for discipline-specific applications. It involves physical reasoning and statistical bias-correction of climate model output using observations and analysis requirements for specific study domains. Unfortunately, there is no single accepted standard for downscaling, only a range of methods that are centred on the practice of different climate-service providers. This makes it hard for new researchers to get started and perform their own analysis, especially when existing downscaled data products do not suit their needs. The UTCDW documents state-of-the-art methods for statistical bias correction and downscaling and show users how to implement them. 

Other educational materials on climate change impact assessment are available, but they are either limited regarding the complexity of the methods [@anderson2021], lack code examples to help new users actually work with the data [@kotamarthi2021], or are too advanced for a first introduction to downscaling [@maraun2018]. The UTCDW Guidebook fills this gap by providing a basic introduction to concepts in climate science and including worked examples and code for downscaling methods appropriate for applications. This makes the UTCDW ideal for users who are new to these concepts and wish to be able to start doing data analysis for their impact study as quickly as possible.

# Guidebook Content

The UTCDW Guidebook consists of six chapters. The first four chapters introduce the reader the background knowledge required to perform downscaling. Chapter 1 serves as an introduction, and guides users in configuring their Python environment. Chapter 2 explains how climate change projections are made and what their limitations. Chapter 3 demonstrates how to access observational, reanalysis, and climate model data, and how to do exploratory analysis with observational and raw climate model data. Chapter 4 contains explanations of various methods of bias-correction and downscaling, and examples of how to validate historical downscaled model output and assess future projections. Python code for the downscaling methods is provided, leveraging the utility of ``xclim`` [@logan2023] and the [Pangeo](https://pangeo.io/packages.html) software ecosystem.

The next two chapters focus on applying the content of Chapters 1-4. Chapter 5 introduces the "Downscaling Workflow" part of the UTCDW. This chapter unpacks the decisions that must be made when designing a climate change impact study and breaks the analysis tasks down into digestible steps. Chapter 6 contains examples of the workflow. Each example demonstrates the process of stating a problem, acquiring the necessary data, producing calibrated climate projections, and quantifying uncertainty. The examples focus on Canadian regions and observational data products, though we include links to available observational and downscaled data products for additional regions as well as global data. We welcome user submission of additional worked examples to contribute to the gallery of examples to be included on the website, or future versions of the UTCDW Guidebook

The UTCDW also includes a [website](https://utcdw.physics.utoronto.ca/) that contains a guided survey that helps a user design their climate impact study and generates a flowchart that lays out the workflow. The flowcharts are featured in the worked examples to explain the procedure before conducting the analysis. We recommend that students use them to explain their projects to their instructors and peers, or even include them in publications produced using the Guidebook methods.

# Teaching Experience

The guidebook material has been used by students from three cohorts: two undergraduate reading courses and two summer research students. The progress of the students demonstrates the strength of the Guidebook as a learning resource. They each started with little or no background in climate science or Pangeo software, and by the end of their terms they were able to independently conduct their own climate change impact analysis projects. We also hosted a hackathon where 30 participants used the Guidebook and workflow to tackle climate change impact challenges related to irrigation water demand, snowfall, and extreme heat. Most participants came to the event with little experience working with climate data and left having successfully implemented the downscaling workflow, further proving that Guidebooks meets its purpose as a learning resource.

# Acknowledgements

We acknowledge Anson Cheung, Peikun Guo, Claire Pan, Cassandra Chanen, and Lilian Chan for testing the UTCDW Guidebook content during its development. We acknowledge funding from the University of Toronto's [Centre for Climate Science and Engineering](https://uoftcse.ca/), [Climate Positive Energy Initiative](https://cpe.utoronto.ca/), and [Data Sciences Institute](https://datasciences.utoronto.ca/).

# References