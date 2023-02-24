# Crypto_Data_Analysis
Project for statistical analysis of crypto currencies. Looking at several coins and trying to find a correlation between them.

The objective of this project is to allow a user to input two currencies whose historical data will pulled from an API. Afterwards, that pulled data will be clean and repurposed by functions we've created in order run statistical analysis on the currencies.


Questions to answer: 
  1. What is the correlation between the chosen currencies?
We can identitfy correlation between the chosen currencies using the pulled data by running applying the .corr method to a dataframe containing both currencies historical data.

  2. What useful statistical analysis can be run on the currencies?
We settled on looking correlation, volume, min/max, and predictive systems.

  3. How have the currencies fluctuate over time?
An hvplot can implemented to directly compare how both coin's fluctuate

  4. What is total volume of the currencies over time?
We can visualize this using hvplot and a combined dataframe.

  5. What is the Sharpe Ratio of the currencies?
By implementing the Sharpe Ratio formula into a function, we can look at risks of the chosen currencies compared to others.

  6. How can we predict future prices?
We implemented a Monte Carlo simulation to simulate where the prices may be in the future and can expound upon the simulation to say with 95% confidence the price will reside between x and y, where x is the minimun and y is the maximum

  7. How do we visualize our findings?
We used hvplots, bar graphs and heatmaps as a means of visualizing our findings.

  8. How do we make money?
  We don't believe we will be capable of making money using our program just yet but potentially in the future we could change it to make it a possibility.

# FINDINGS
Although there we some difficulties in writing the code capable of running the analytics in question, the most impactful portion for us would likely be discovering how to create a "master" code that calls functions we created for purpose of data analytics. 

  
