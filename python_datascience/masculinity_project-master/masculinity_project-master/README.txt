Masculinity Survey


My Python practice project from:


My Codecademy Masculinity Survey Project From The Data Scientist Path Foundations of Machine Learning: Unsupervised Learning.

Project Goal:
Find patterns in the way men view masculinity by utilizing the KMeans algorithm on a FiveThirtyEight masculinity survey data.

----------------------------------------------------------------------------------------

Project Requirements:

Knowledge, Machine Learning, Unsupervised Learning

Python v3 or later:
https://www.python.org/

scikit-learn
https://scikit-learn.org/

Pandas 
https://pandas.pydata.org/

Matplotlib
https://matplotlib.org/

Numpy
https://numpy.org/

Jupyter notebook:
https://jupyter.org/

----------------------------------------------------------------------------------------

Overview:

In this project, I investigated the way people think about masculinity by applying the KMeans algorithm to 
data from FiveThirtyEight. https://fivethirtyeight.com/features/what-do-men-think-it-means-to-be-a-man/
FiveThirtyEight is a popular website known for their use of statistical analysis in many of their stories.

FiveThirtyEight and WNYC studios used 'masculinity-survey.pdf' to get their male readers' thoughts on masculinity.
FiveThirtyEight's article What Do Men Think It Means To Be A Man? contains their major takeaways.

----------------------------------------------------------------------------------------

Links:

My Project Blog Presentation: 
https://www.alex-ricciardi.com/post/masculinity-survey

Project GitHub:
https://github.com/ARiccGitHub/masculinity_project

----------------------------------------------------------------------------------------

Project map:

Python Jupiter Notebook Code Lines File:
masculinity_project.ipynp

Python Code Lines Files:
masculinity_project.py
column_types.py
features_combinations.py
survey_questions.py

provided data/info:
masculinity.csv
masculinity-survey.pdf

data files:
data/*.csv

Graphs:
grah/*.png

Html Tables:
html_DataFrames/*.html

Code Presentation:
masculinity_project.html

----------------------------------------------------------------------------------------

My Project layout:

- Overview
- Libraries
- Investigate the Data
	The questions
	The responses data
- Mapping the Data
	The map_responses() function
	Mapping question 7 responses
- Plotting Question 7 Data
	Question 7 sub-questions
	The plot_features() function
	Plotting question 7
- K-Means Model
	Training model with selected question 7 sub-question response	
- Separating by clusters
	Adding model classifications results to the q0007_responses DataFrame
	Separating question 7 responses data by clusters
	Plotting Question 7 Clusters
	Separating the survey data by Clusters
- Investigate the Cluster Members
	The investigate_member() function
	Responses investigation results
	Answering the demographic question
	All the features investigation result
	

