
My Python Data Visualization with the Library Matplotlib Practice Project From:

Codecademy Data Science course Python, Data Visualization with Matplotlib

Twitch Project
VISUALIZATION CUMULATIVE PROJECTS
(part-2)

(For “Twitch Part-1: Analyze Data with SQL” see README_SQLite.txt)

----------------------------------------------------------------------------------------

Project Requirements:

Python v2 or later:
https://www.python.org/


Matplotlib
https://matplotlib.org/

SQLite:
https://www.sqlite.org/index.html 

----------------------------------------------------------------------------------------

Overview:

Twitch Part-2: Visualize Data with Matplotlib

Welcome to Part-2 of the Twitch Project. In this part of the project, you will be taking your findings 
from the SQL queries and visualize them using Python and Matplotlib, in the forms of:

* Bar Graph: Featured Games
* Pie Chart: Stream Viewers’ Locations
* Line Graph: Time Series Analysis

The Twitch Science Team provided this practice dataset. You can download the .csv files (800,000 rows) from GitHub.
Note: This is data is scrubbed and is meant for practice use only.

----------------------------------------------------------------------------------------

Project map:

python code lines file
twitch_project\twitch.py

data files:
twitch_project\data\chat.csv
twitch_project\data\video_play.csv

SQL README file project part-1
twitch_project\README_SQLite.txt

SQL queries code lines project part-1
twitch_project\twitch_part1.sql

Project Presentation .pdf format				
twitch_project\twitch_presentation.pdf 

----------------------------------------------------------------------------------------

links:
PowerPoint Twitch Presentation
https://1drv.ms/p/s!AsKPX_vZuHCqhPB3vRZ0snTVAIMMyA?e=o5FT2M

----------------------------------------------------------------------------------------

Project:

--- Bar Graph: Featured Games

1.
Twitch’s home page has a Featured Games section where it lists the “Games people are watching now”.
In the previous part of the project, you used SQL to find the top 10 trending games (on January 1st, 2015) and their number of viewers.
It looked something like this:
https://s3.amazonaws.com/codecademy-content/projects/twitch/featured-sql.png

In the next few tasks, you are going to take this data and plot a bar graph using Matplotlib.

2.
The games and viewers are already loaded in the script.py file:
games = ["LoL", "Dota 2", "CS:GO", "DayZ", "HOS", "Isaac", "Shows", "Hearth", "WoT", "Agar.io"]
viewers =  [1070, 472, 302, 239, 210, 171, 170, 90, 86, 71]
Now, use the plt.bar() to plot a bar graph using range(len(games)) and viewers as arguments.
Then, use plt.show() to visualize it.

3.
Let’s make the graph more informative by doing the following:
Add a title
Add a legend
Add axis labels
Add ticks
Add tick labels (rotate if necessary)

4.
The visualization should look something like:
https://s3.amazonaws.com/codecademy-content/projects/twitch/bar.png

League of Legends really dominated the list on January 1st, 2015!.

--- Pie Chart: League of Legends Viewers' Whereabouts

5.
There are 1070 League of Legends viewers from this dataset. Where are they coming from?
When you performed the SQL query, you got this result:
https://s3.amazonaws.com/codecademy-content/projects/twitch/countries-sql.png

As well as other countries that accounted for another 279 stream viewers.
In the next few tasks, you are going to take this data and make a pie chart

6.
The labels and countries are already loaded into script.py:
labels = ["US", "DE", "CA", "N/A", "GB", "TR", "BR", "DK", "PL", "BE", "NL", "Others"]
countries = [447, 66, 64, 49, 45, 28, 25, 20, 19, 17, 17, 279]
Let’s add some colors!
Because there are 12 countries (including N/A and Others), let’s create an array called colors and add 12 color codes to it, like so:
colors = ['lightskyblue', 'gold', 'lightcoral', 'gainsboro', 'royalblue', 'lightpink', 'darkseagreen', 'sienna', 'khaki', 'gold', 'violet', 'yellowgreen']
Check out the Matplotlib color codes to find your inner Bob Ross.
Then, use plt.pie() to plot a pie chart.
Lastly, use plt.show() to visualize it.

7.
Optional: Let’s make it more visually appealing and more informative.
First, let’s “explode”, or break out, the 1st slice (United States)
Add the explode
Add shadows
Turn the pie 345 degrees
Add percentages
Configure the percentages’ placement

8.
The visualization should look something like:
https://s3.amazonaws.com/codecademy-content/projects/twitch/pie.png

--- Line Graph: Time Series Analysis

9.
We were able to find the number of US viewers at different hours of the day on January 1st, 2015:
https://s3.amazonaws.com/codecademy-content/projects/twitch/time.png

Let’s make this into a line graph.

10.
The hour and viewers_hour area already loaded into script.py:
hour = range(24)
viewers_hour = [30, 17, 34, 29, 19, 14, 3, 2, 4, 9, 5, 48, 62, 58, 40, 51, 69, 55, 76, 81, 102, 120, 71, 63]
Use plt.plot() to plot a line graph.
Then, add the title, the axis labels, legend, and ticks.

11.
There is some uncertainty in these numbers because some people leave their browsers open. Let’s account for a 15% error in the viewers_hour data.
First, create a list containing the upper bound of the viewers_hour and call it y_upper.
Then, create a list containing the lower bound of the viewers_hour and call it y_lower.
Lastly, use plt.fill_between() to shade the error, with an alpha of 0.2.

12. Your line graph should look something like:
https://s3.amazonaws.com/codecademy-content/projects/twitch/line.png

Look at the peak around 9 pm!

