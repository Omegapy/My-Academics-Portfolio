
My Python Data Analysis with the Library Pandas Practice Project From:

Codecademy Data Science course Python, Data Analysis with Pandas
"This Is Jeopardy!" project  
Introduction to Pandas
Aggregates in Pandas

----------------------------------------------------------------------------------------

Prerequisites:

For Codacademy students.
In order to complete this project, 
you should have completed the Pandas lessons in the Analyze Data with Python Skill Path. 
You can also find those lessons in the Data Analysis with Pandas course.

Finally, the Practical Data Cleaning course may also be helpful.

----------------------------------------------------------------------------------------

Project Requirements:

Python v2 or later:
https://www.python.org/

pandas - Python Data Analysis Library:
https://pandas.pydata.org/

----------------------------------------------------------------------------------------

Overview:

This project is slightly different than others you have encountered thus far on Codecademy. 
Instead of a step-by-step tutorial, this project contains a series of open-ended requirements 
which describe the project you’ll be building. 
There are many possible ways to correctly fulfill all of these requirements, 
and you should expect to use the internet, Codecademy, 
and other resources when you encounter a problem that you cannot easily solve.

Project Goals.
You will work to write several functions that investigate a dataset of Jeopardy! 
questions and answers. Filter the dataset for topics that you’re interested in, 
compute the average difficulty of those questions, and train to become the next Jeopardy champion!

----------------------------------------------------------------------------------------

Project map:

SQL queries code lines
codecademy_sql\cooltshirts_attribution_queries\cooltshirts_attribution_queries.sql

Project Presentation .pdf format				
codecademy_sql\cooltshirts_attribution_queries\cooltshirts_attribution_queries_project_presentation.pdf 

----------------------------------------------------------------------------------------

links:
PowerPoint CoolTShirts Attribution Queries Presentation
https://onedrive.live.com/view.aspx?resid=AA70B8D9FB5F8FC2!54066&ithint=file%2cpptx&authkey=!ACCBvGKY1G_GkyM

----------------------------------------------------------------------------------------

Project:

2.
We’ve provided a csv file containing data about the game show Jeopardy! in a file named jeopardy.csv. 
Load the data into a DataFrame and investigate its contents. Try to print out specific columns.

3.
Write a function that filters the dataset for questions that contains all of the words in a list of words. 

4.
Test your original function with a few different sets of words to try to find some ways your function breaks. 
Edit your function so it is more robust.

5.
We may want to eventually compute aggregate statistics, like .mean() on the " Value" column. 
But right now, the values in that column are strings. 
Convert the " Value" column to floats. If you’d like to, you can create a new column with the float values.

6.
Write a function that returns the count of the unique answers to all of the questions in a dataset. 

7.
Explore from here! This is an incredibly rich dataset, and there are so many interesting things to discover. 
