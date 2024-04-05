
My Python Data Analysis Capstone Project From:

Codecademy Data Science course Python, Statistics with NumPy and Hypothesis Testing with SciPy section.

Project:
Analysis an A/B test from MuscleHub dataset. 

----------------------------------------------------------------------------------------

Project Requirements:

Python v3 or later:
https://www.python.org/

SciPy – Statistics Library:
https://docs.scipy.org/doc/scipy/reference/stats.html l

Pandas - Python Data Analysis Library:
https://pandas.pydata.org/

Matplotlib
https://matplotlib.org/

Jupyter notebook:
https://jupyter.org/

----------------------------------------------------------------------------------------

Overview:

Help MuscleHub analyze an A/B test and choose a business strategy

Currently, when a visitor to MuscleHub is considering buying a membership, he or she follows the following steps:

- Take a fitness test with a personal trainer
- Fill out an application for the gym
- Send in their payment for their first month’s membership

Janet, the manager of MuscleHub, thinks that the fitness test intimidates some prospective members, so she has set up an A/B test.

Visitors will randomly be assigned to one of two groups:

- Group A will still be asked to take a fitness test 
with a personal trainer
- Group B will skip the fitness test and proceed directly to the application

Janet’s hypothesis is that visitors assigned to Group B will be more likely to eventually purchase a membership to MuscleHub.

----------------------------------------------------------------------------------------

Links:
MuscleHub Blog Presentation
https://www.alex-ricciardi.com/post/musclehub-a-b-test

----------------------------------------------------------------------------------------

Project map:

Python Jupiter code lines file:
musclehub.ipynb

SQL local library python code lines:
SQL.lib.py

data files:
data/*.csv
data/sql_tables.db

chart images:
graph/*.png

----------------------------------------------------------------------------------------

Project:

Step 1. Embedded SQL 
Like most businesses, Janet keeps her data in a SQL database. 
Download the data from her database to a csv file, and then load it into a Jupyter Notebook using Pandas.
For this project, I use a special Codecademy library that lets you type SQL queries directly into this Jupyter notebook. 
See SQL.lib.py

Step 2. Explore dataset using SQL and create a DataFrame from the dataset 

Step 3. Investigate the A and B groups

Step 4. Investigate funnel stages for both A and B tests
- Visitor to Applicant 
- Applicant to Member 
- Visitor to Member
        

Step 5. Summarize the acquisition funnel with charts
	    	


