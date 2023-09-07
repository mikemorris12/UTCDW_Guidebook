# UTCDW Guidebook

*Michael Morris, Paul J. Kushner, and Karen L. Smith*

*Version 0.9 -- Last updated September 7 2023*

Welcome to the guidebook for the University of Toronto Climate Downscaling Workflow. If you're accessing these resources, it means you are interested in using data to study how climate change may affect a particular domain in the built or natural environment. The purpose of this guidebook is to help you develop the skills and knowledge needed to design and conduct a climate change impact analysis study and perform your own statistical downscaling of climate model data. This guidebook takes advantage of the [Jupyter Book](https://jupyterbook.org/en/stable/intro.html) format to intermix text explaining concepts and methods with code that demonstrates application.

## Who This Guide is For

The target audience for this guidebook is a researcher with little or no foundation in climate science, who studies a system that is sensitive to weather and climate. For example, an engineer who studies building energy use, which depends on climatic variables such as temperature and humidity. In order to quantitatively study how climate change might affect the system you study and properly interpret the results, you need some basic knowledge of the climate system and climate modeling.

 Users from outside of the climate science community may not be familiar with how climate change projections are produced, what sort of data is available, and how climate data is typically structured. Importantly, you also need to understand the limitations of climate change projections. Rarely are out-of-the-box climate model projections suitable for regional climate impact assessment, so post-processing must be applied to account for systematic biases and coarse spatial sampling, and make the data useful for practitioners or impact modelers. One must also appreciate the irreducible uncertainty inherent to future climate projections, due to factors like uncertain greenhouse gas emission pathways and natural climate variability. This guidebook will introduce you to all of these concepts while also showing code examples of how to access and analyze climate data.

## Limitations of the UTCDW Guidebook

The UTCDW provides educational material to help you design and conduct your own analyses, but we cannot give detailed guidance on any specific research problem. The guidebook provides general guidance and a few examples, but there are too many possible applications of climate downscaling to be exhaustive. Notably, we cannot tell you *how* your domain application is sensitive to climatic factors. As the expert on the system you study, it's up to you to have a sense of the important climate variables for your application, and how you might quantify the way weather and climate affect your study system. If you require climate data as inputs to a model (for example, a model that calculates building energy use as a function of outside temperature and humidity), then you should be familiar with which input variables are required, and at what spatial and temporal sampling. We call the quantity which depends on climate variables, and is relevant for your domain application, a "climate indicator", whether it's calculated using an analytic expression or a complex numerical model. Climate indicators will be discussed further in Chapter 5, but it's important to know from the start that this guide assumes you have a way to quantify how your study system depends on climatic factors.

## Issues, Feedback, and Support

If you encounter a problem with the guidebook, would like to make suggestions on how to improve it, or otherwise would like to contact the authors, please use the [Feedback page](https://utcdw.physics.utoronto.ca/feedback/) of the main UTCDW website. We invite you to contribute to the book by making a Pull Request through the [Github Repository](https://github.com/mikemorris12/UTCDW_Guidebook) that hosts the files that comprise the guidebook. If you're not familiar with Git, then you're welcome to use the Feedback page instead.

## Contributors

The contents of this guidebook were written predominantly by Michael Morris. This work was performed under he supervision of Professor Paul J. Kushner, who conceived of the project and provided feedback, and Professor Karen L. Smith, who provided content suggestions and feedback for most chapters. Special thanks to Aleksandra Elias Chereque, Cassandra Chanen and Lilian Chan who tested early iterations of the guidebook materials. Extra special thanks to Julian Comanean, who coded the [UTCDW website](https://utcdw.physics.utoronto.ca/) and the guided survey/flowchart generator, and designed the UTCDW logo. 

## Funding Acknowledgement

Funding for this project was provided by the [Centre for Climate Science and Engineering](https://uoftcse.ca/), [Climate Positive Energy](https://cpe.utoronto.ca/), and the University of Toronto [Data Sciences Institute](https://datasciences.utoronto.ca/).

## License

This work is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). You are free to copy, redistribute, and share this book, in any medium, or format. You may also adapt the book, improve it, and re-use it in your own materials. However, keep in mind that you must give credit where credit is due, and any works that you produce based on this work are subject to the same license. For more details, click the badge below.

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
