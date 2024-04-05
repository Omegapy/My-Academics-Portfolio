
My SQL Practice Project From:

Codecademy Data Science course SQL Analyze real Data with SQL section
Attribution Queries

----------------------------------------------------------------------------------------

Overview:

CoolTShirts, an innovative apparel shop, is running a bunch of marketing campaigns. 
In this project, you’ll be helping them answer these questions about their campaigns:

1. Get familiar with the company.
How many campaigns and sources does CoolTShirts use and how are they related? 
Be sure to explain the difference between utm_campaign and utm_source.
What pages are on their website?

2. What is the user journey?

How many first touches is each campaign responsible for?
How many last touches is each campaign responsible for?
How many visitors make a purchase?
How many last touches on the purchase page is each campaign responsible for?
What is the typical user journey?

3. Optimize the campaign budget.

CoolTShirts can re-invest in 5 campaigns. Which should they pick and why?

CoolTShirts sells shirts of all kinds, as long as they are T-shaped and cool. Recently, 
CTS started a few marketing campaigns to increase website visits and purchases. 

Using touch attribution, they’d like to map their customers’ journey: 
from initial visit to purchase. They can use that information to optimize their marketing campaigns.

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

	Get familiar with CoolTShirts

1.
How many campaigns and sources does CoolTShirts use? Which source is used for each campaign?

Use three queries:

* one for the number of distinct campaigns,
* one for the number of distinct sources,
* one to find how they are related.

2.
What pages are on the CoolTShirts website?

Find the distinct values of the page_name column.

What is the user journey?

3.
How many first touches is each campaign responsible for?

You’ll need to use the first-touch query from the lesson (also provided in the hint below). Group by campaign and count the number of first touches for each.

4.
How many last touches is each campaign responsible for?

Starting with the last-touch query from the lesson, group by campaign and count the number of last touches for each.

5.
How many visitors make a purchase?

Count the distinct users who visited the page named 4 - purchase.

6.
How many last touches on the purchase page is each campaign responsible for?

This query will look similar to your last-touch query, but with an additional WHERE clause.

7.
CoolTShirts can re-invest in 5 campaigns. Given your findings in the project, which should they pick and why?
