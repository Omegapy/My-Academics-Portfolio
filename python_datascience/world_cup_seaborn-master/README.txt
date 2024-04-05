
My Python Data Visualization with the Library Matplotlib and Seaborn Practice Project From:

Codecademy Data Science course Python, Data Visualization with Matplotlib
"Word Cup Data" project  
Introduction to Seaborn
Visualizing World Cup Data With Seaborn

----------------------------------------------------------------------------------------

Project Requirements:

Python v2 or later:
https://www.python.org/

pandas - Python Data Analysis Library:
https://pandas.pydata.org/

Matplotlib
https://matplotlib.org/

Seaborn
https://seaborn.pydata.org/
----------------------------------------------------------------------------------------

Overview:

Visualizing World Cup Data With Seaborn
For this project you will be exploring data from the Fifa World Cup from 1930-2014 to analyze trends and discover insights about the world’s game, fútbol!

This Fifa World Cup data is from Kaggle. Kaggle is a platform for data science competitions that hosts many datasets online.

Using Seaborn you will create a series of plots that explore aggregates and distribution across the goals scored in World Cup games.
----------------------------------------------------------------------------------------

Project map:

Project Python code
world_cup_seaborn\world_cup.py

Project Data files
world_cup_seaborn\WorldCupMatches.csv
world_cup_seaborn\goal.csv

Project Presentation .pdf format				
world_cup_seaborn\world_cup_seaborn_presentation

----------------------------------------------------------------------------------------

links:
PowerPoint Visualizing World Cup Data With Seaborn Presentation
https://1drv.ms/p/s!AsKPX_vZuHCqg8YfHIi21C9i3VWbVQ?e=qu604D

----------------------------------------------------------------------------------------

Project:

1.
Import the modules that you’ll be using in this project:

	from matplotlib import pyplot as plt
	import pandas as pd
	import seaborn as sns

2.
Inspect the raw CSV files that you will be using in this project by selecting them in the file navigator.

3.
Load WorldCupMatches.csv into a DataFrame called df. This will allow you to eventually plot the DataFrame with Seaborn.

4.
It is usually a good idea to check any new DataFrame to make sure the results are as expected.
Inspect the DataFrame using .head(). Make sure to use print() to wrap any output you want to inspect.

5.
The data in WorldCupMatches.csv has the goals scored in each match broken up by goals for the home team and goals for the away team. We want to visualize the total number of goals scored in each match.
Create a new column in df named Total Goals, and set it equal to the sum of the columns Home Team Goals and Away Team Goals.
Print the results of df.head() to confirm your new column.

6.
You are going to create a bar chart visualizing how many goals were scored each year the World Cup was held between 1930-2014.
Set the style of your plot to be whitegrid . This will add gridlines to the plot which will make it easier to read the visualization. 

7.
To make the text in your visualization bigger and easier to read, set the context to be "poster".
If you would like to further adjust the font size of your plot, you can pass sns.set_context() a second optional argument using the keyword font_scale. 

8.
Create a figure and axes for your plot using the syntax:
f, ax = plt.subplots()
Inside of plt.subplots(), set the size of the figure to be 12 inches wide and 7 inches tall.

9.
Using the data in df and the syntax:
ax = sns.barplot()
visualize the columns Year and Total Goals as a bar chart.
Year should be on the x-axis, and Total Goals should be on the y-axis.

10.
Render your bar chart so you can see it.

11.
Effective visualizations include a clear title.
Give your bar chart a meaningful title using ax.set_title().

12.
Now you are going to create a box plot so you can visualize the distribution of the goals data instead of just the average with a bar chart.
Load goals.csv into a DataFrame called df_goals, and take a quick look at the DataFrame using .head().

13.
Experimenting with different contexts and font scales can help you decide on the best context and font scale for the particular visualization.
Try setting the context of the plot to be notebook and the font_scale to be 1.25.

14.
create a figure for your second plot.
Set the variables f, ax2 and instantiate a figure that is 12 inches wide and 7 inches tall.

15.
Set ax2 equal to a box plot with the color palette Spectral that visualizes the data in the DataFrame df_goals with the column year on the x-axis and goals on the y-axis.

16.
Give your box plot a meaningful and clear title.

17.
Render your box plot so you can see it.

