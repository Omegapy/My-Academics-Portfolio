
My SQL Practice Project From:

Codecademy Data Science course SQL Analyze real Data with SQL section 
Usage Funnels with Warby Parker

----------------------------------------------------------------------------------------

Overview:

Warby Parker is a transformative lifestyle brand with a lofty objective: to offer designer eyewear at a revolutionary price while leading the way for socially conscious businesses. 
Founded in 2010 and named after two characters in an early Jack Kerouac journal, Warby Parker believes in creative thinking, smart design, and doing good in the world. 
For every pair of eyeglasses and sunglasses sold, a pair is distributed to someone in need.

In this project, you will analyze different Warby Parker’s marketing funnels in order to calculate conversion rates. Here are the funnels and the tables that you are given:

Quiz Funnel:
survey

Home Try-On Funnel:
quiz
home_try_on
purchase

This project was a collaboration with Warby Parker’s Data Science team (thank you!) and uses fictional data.

----------------------------------------------------------------------------------------

Project map:

codecademy_sql\warby_parker_sql_project\survey.csv			Data Table
codecademy_sql\warby_parker_sql_project\quiz.csv			Data Table
codecademy_sql\warby_parker_sql_project\home_try_on.csv			Data Table
codecademy_sql\warby_parker_sql_project\purchase.csv			Data Table

codecademy_sql\warby_parker_sql_project\ warby_parker_data_query.sql  			SQL queries code lines
codecademy_sql\warby_parker_sql_project\warby_parker_project_presentation.pdf		Project Presentation .pdf format
codecademy_sql\warby_parker_sql_project\questions_completion_rate.xlsx  		Excel spreadsheet Ref. Question #3

----------------------------------------------------------------------------------------

Link:

https://onedrive.live.com/edit.aspx?resid=AA70B8D9FB5F8FC2!54047&ithint=file%2cpptx&authkey=!AKiBm9JB2NQ7cno        PowerPoint Warby Parker Project Presentation 
https://github.com/Codecademy/datasets/tree/master/warby-parker  						    Codecademy GitHub Warby Parker	
			
----------------------------------------------------------------------------------------

Project:

	1.
	To help users find their perfect frame, Warby Parker has a Style Quiz that has the following questions:
		1. “What are you looking for?”
		2. “What’s your fit?”
		3. “Which shapes do you like?”
		4. “Which colors do you like?”
		5. “When was your last eye exam?”
	The users’ responses are stored in a table called survey.
	Select all columns from the first 10 rows. What columns does the table have?

	2.
	Users will “give up” at different points in the survey. Let’s analyze how many users move from Question 1 to Question 2, etc.
	Create a quiz funnel using the GROUP BY command.
	What is the number of responses for each question?

	3.
	Using a spreadsheet program like Excel or Google Sheets, calculate the percentage of users who answer each question:
	Which question(s) of the quiz have a lower completion rates?
	What do you think is the reason?

	4.
	Warby Parker’s purchase funnel is:
	Take the Style Quiz -> Home Try-On -> Purchase the Perfect Pair of Glasses
	During the Home Try-On stage, we will be conducting an A/B Test:
	 50% of the users will get 3 pairs to try on
	 50% of the users will get 5 pairs to try on
	Let’s find out whether or not users who get more pairs to try on at home will be more likely to make a purchase.
	The data will be distributed across three tables:
		* quiz
		* home_try_on
		* purchase
	Examine the first five rows of each table
	What are the column names?

	5.
	We’d like to create a new table with the following layout:

	user_id		is_home_try_on		number_of_pairs		is_purchase       f49d4197dc	     True		     3			   False
       5373a1a04	     False		    NULL                   False
        440117a              True		     5			   True

	Each row will represent a single user from the browse table:
	* If the user has any entries in home_try_on, then is_home_try_on will be ‘True’.
	* number_of_pairs comes from home_try_on table
	* If the user has any entries in is_purchase, then is_purchase will be ‘True’.
	Use a LEFT JOIN to combine the three tables, starting with the top of the funnel (quiz) and ending with the bottom of the funnel (purchase).
	Select only the first 10 rows from this table (otherwise, the query will run really slowly).

	6.
	Once we have the data in this format, we can analyze it in several ways:
	* We can calculate overall conversion rates by aggregating across all rows.
	* We can compare conversion from quiz?home_try_on and home_try_on?purchase.
	* We can calculate the difference in purchase rates between customers who had 3 number_of_pairs with ones who had 5.
	* And more!

	We can also use the original tables to calculate things like:
	* The most common results of the style quiz.
	* The most common types of purchase made.
	* And more!

	What are some actionable insights for Warby Parker?
