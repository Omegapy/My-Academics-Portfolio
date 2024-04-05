
My Python Data Visualization with the Library Matplotlib a Practice Project From: Codecademy Data Science course Python, Data Visualization with Matplotlib

"Twitch" project  
Part 1: Analyze Data with SQL 

----------------------------------------------------------------------------------------

Project Requirements:

SQLite:
https://www.sqlite.org/index.html 

Python v2 or later:
https://www.python.org/

Matplotlib:
https://matplotlib.org/


----------------------------------------------------------------------------------------

Overview:


Twitch is the world’s leading video platform and community for gamers, with 15+ million unique daily visitors. Using data to understand its users and products is one of the chief responsibilities of the Twitch Science Team.
In this project, you will be working with two training tables that contain Twitch users’ stream (video) viewing data and chat room usage data.

Stream viewing data:
	* stream table
Chat usage data:
	* chat table
The Twitch Science Team provided this practice dataset. You can download the .csv files (800,000 rows) from GitHub.

(For “Twitch Part-2: Python, Data Visualization with Matplotlib see README.txt)

----------------------------------------------------------------------------------------

Project map:

SQL queries code lines project part-1
twitch_project\twitch_part1.sql

python README file project part-2
twitch_project\README.txt

python code lines file (part-2)
twitch_project\twitch.py

data files
twitch_project\data\chat.csv (chat table)
twitch_project\data\video_play.csv (stream table)

Project Presentation .pdf format				
twitch_project\twitch_presentation.pdf 

----------------------------------------------------------------------------------------

links:
PowerPoint Twitch Presentation
https://1drv.ms/p/s!AsKPX_vZuHCqhPB3vRZ0snTVAIMMyA?e=o5FT2M

----------------------------------------------------------------------------------------
Project:

Getting Started

1.
Start by getting a feel for the stream table and the chat table:
Select all columns from the first 20 rows.

2.
What are the unique games in the stream table?

3.
What are the unique channels in the stream table?

Aggregate Functions:


4.
What are the most popular games in the stream table?
Create a list of games and their number of viewers using GROUP BY.

5.
These are some big numbers from the game League of Legends (also known as LoL).
Where are these LoL stream viewers located?
Create a list of countries and their number of LoL viewers using WHERE and GROUP BY.

6.
he player column contains the source the user is using to view the stream (site, iphone, android, etc).
Create a list of players and their number of streamers.

7.
Create a new column named genre for each of the games.
Group the games into their genres: Multiplayer Online Battle Arena (MOBA), First Person Shooter (FPS), Survival, and Other.
Using CASE, your logic should be:

If League of Legends ? MOBA
If Dota 2 ? MOBA
If Heroes of the Strom ? MOBA
If Counter-Strike: Global Offensive ? FPS
If DayZ ? Survival
If Survival Evolved ? Survival
Else ? Other
Use GROUP BY and ORDER BY to showcase only the unique game titles.

How does view count change in the course of a day?

8.
Before we get started, let’s run this query and take a look at the time column from the stream table:

SELECT time
FROM stream
LIMIT 10;

The data type of the time column is DATETIME. It is for storing a date/time value in the database.
Notice that the values are formatted like:
2015-01-01 18:33:52
So the format is:
YYYY-MM-DD HH:MM:SS

9.
SQLite comes with a strftime() function - a very powerful function that allows you to return a formatted date.
It takes two arguments:
strftime(format, column)
Let’s test this function out:

SELECT time,
   strftime('%S', time)
FROM stream
GROUP BY 1
LIMIT 20;

10.
Okay, now we understand how strftime() works. Let’s write a query that returns three columns:
The hours of the time column
The view count for each hour
Lastly, filter the result with only the users in your country using a WHERE clause.

11.
The stream table and the chat table share a column: device_id.
Let’s join the two tables on that column

