
My SQL Practice Project From:

Codecademy Data Science course SQL intermediate level section
 
World Populations SQL Practice II

Overview:
This project is slightly different than others encounter on Codecademy. Instead of a step-by-step tutorial, 
this project contains a series of open-ended requirements which describe the project that needs to be built. 
There are many possible ways to correctly fulfill all of the requirements. 

In order to complete this project, you should have completed the Codecademy Learn SQL Manipulation, Queries, Aggregate Functions, and Multiple Tables lessons in the Codecademy Learn SQL course.

Project Goals:
A dataset of world population by country data from recent years. 
Write queries to retrieve interesting data and answer a set of specific questions.

Project map:
codecademy_sql\world_pop_2_sql\db.sqlite				SQLite database
codecademy_sql\world_pop_2_sql\population_ii_queries.sql		SQL queries code line file

Note:
Codecademy also stores my SQL queries code line file for this project on its GitHub repository 
https://gist.github.com/a44bda2e683054b1672a96a975ce3fd0

Project:
2.
In this project, you’ll answer questions using a database of world population by country.

There are two tables:

countries
Column		Type		Notes
id		INTEGER		Primary Key
name		TEXT	
continent	TEXT
	
population_years
Column		Type		Notes
id		INTEGER		Primary Key
population	NUMBER		(in millions)
year		NUMBER	
country_id	INTEGER		Foreign Key

When you finish this project, you should be able to answer each the questions that follow using a single SQL query.

3.
How many entries in the countries table are from Africa?

4.
What was the total population of the continent of Oceania in 2005?

5.
What is the average population of countries in South America in 2003?

6.
What country had the smallest population in 2007?

7.
What is the average population of Poland during the time period covered by this dataset?

8.
How many countries have the word “The” in their name?

9.
What was the total population of each continent in 2010?

