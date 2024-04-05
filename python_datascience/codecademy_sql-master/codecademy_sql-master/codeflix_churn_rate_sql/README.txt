
My SQL Practice Project From:

Codecademy Data Science course SQL Analyze real Data with SQL section
User Churn Rate

----------------------------------------------------------------------------------------

Overview:

Codeflix, a streaming video startup, is interested in measuring their user churn rate. 
In this project, you’ll be helping them answer these questions about their churn:

1. Get familiar with the company.

	* How many months has the company been operating? 
	  Which months do you have enough information to calculate a churn rate?
	* What segments of users exist?

2. What is the overall churn trend since the company started?

3. Compare the churn rates between user segments.

	* Which segment of users should the company focus on expanding?

Four months into launching Codeflix.
The marketing department is particularly interested in how the churn compares between two segments of users. 
They provide you with a dataset containing subscription data for users 
who were acquired through two distinct channels.

The dataset provided to you contains one SQL table, subscriptions. Within the table, there are 4 columns:

	* id - the subscription id
	* subscription_start - the start date of the subscription
	* subscription_end - the end date of the subscription
	* segment - this identifies which segment the subscription owner belongs to

Codeflix requires a minimum subscription length of 31 days, 
so a user can never start and end their subscription in the same month.


----------------------------------------------------------------------------------------

Project map:

codecademy_sql\codeflix_churn_rate_sql\codeflix_churn_rate_project.sql 		SQL queries code lines
codeflix_churn_rate_project_presentation.pdf					Project Presentation .pdf format

Link:
PowerPoint Codeflix User Churn Rate Project Presentation
https://onedrive.live.com/edit.aspx?resid=AA70B8D9FB5F8FC2!54057&ithint=file%2cpptx&authkey=!AMVFwiQopo31zCU   


----------------------------------------------------------------------------------------

Project:

	Get familiar with the data
1.
Take a look at the first 100 rows of data in the subscriptions table. How many different segments do you see?

2.
Determine the range of months of data provided. Which months will you be able to calculate churn for?


	Calculate churn rate for each segment

3.
You’ll be calculating the churn rate for both segments (87 and 30) over the first 3 months of 2017 
(you can’t calculate it for December, since there are no subscription_end values yet). 
To get started, create a temporary table of months.

4.
Create a temporary table, cross_join, from subscriptions and your months. Be sure to SELECT every column.

5.
Create a temporary table, status, from the cross_join table you created. This table should contain:

	* id selected from cross_join
	* month as an alias of first_day
	* is_active_87 created using a CASE WHEN to find any users 
	  from segment 87 who existed prior to the beginning of the month. 
	  This is 1 if true and 0 otherwise.
	* is_active_30 created using a CASE WHEN to find any users 
          from segment 30 who existed prior to the beginning of the month. 
          This is 1 if true and 0 otherwise.

6.
Add an is_canceled_87 and an is_canceled_30 column to the status temporary table. 
This should be 1 if the subscription is canceled during the month and 0 otherwise.

7.
Create a status_aggregate temporary table that is a SUM of the active and canceled subscriptions for each segment, 
for each month.

The resulting columns should be:

	* sum_active_87
	* sum_active_30
	* sum_canceled_87
	* sum_canceled_30

8.
Calculate the churn rates for the two segments over the three month period. Which segment has a lower churn rate?


	Bonus

9.
How would you modify this code to support a large number of segments?
