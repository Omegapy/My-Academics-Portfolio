
#-------------------------------------------------------------------------#
#                                                                         #
#                   Codecademy Data Science course Python                 #
#             Data Visualization with the Matplotlib Library              #
#                            Part-2                                       #
#                                                                         #
#                            "Twitch"                                     #
#                                                                         #
#-------------------------------------------------------------------------#

# Import Matplolib
from matplotlib import pyplot as plt

# Project Data
# Bar Graph: Featured Games
games = ["LoL", "Dota 2", "CS:GO", "DayZ", "HOS", "Isaac", "Shows", "Hearth", "WoT", "Agar.io"]
viewers =  [1070, 472, 302, 239, 210, 171, 170, 90, 86, 71]

# Pie Chart: League of Legends Viewers' Whereabouts
labels = ["US", "DE", "CA", "N/A", "GB", "TR", "BR", "DK", "PL", "BE", "NL", "Others"]
countries = [447, 66, 64, 49, 45, 28, 25, 20, 19, 17, 17, 279]

# Line Graph: Time Series Analysis
hour = range(24)
viewers_hour = [30, 17, 34, 29, 19, 14, 3, 2, 4, 9, 5, 48, 62, 58, 40, 51, 69, 55, 76, 81, 102, 120, 71, 63]

#--------------------------------------
#-------- Bar Graph: Featured Games
#--------------------------------------

# Config figure size, Personal preference, not a project requirement
plt.figure(figsize=(8,6))
# 2. Use the plt.bar() to plot a bar graph
plt.bar(range(len(games)), viewers)
# ouput
plt.show()
# Clear the current figure
plt.clf()

# 3. Add a title, legend, axis labels, ticks, ticks label
plt.bar(range(len(games)), viewers, color='#8A2BE2')
# Graph title
plt.title('Features Games Viewers', fontsize=16)
# Legend
plt.legend(["Twitch"])
# axis Label
plt.xlabel('Games', fontsize=12)
plt.ylabel('Viewers', fontsize=12)
# axis object
ax = plt.subplot()
# x ticks axis object
ax.set_xticks(range(len(games)))
ax.set_xticklabels(games, rotation=30)
# Graph background color
ax.set_facecolor('lightgray')
# Draws grid lines behind other graph elements
ax.set_axisbelow(True)
# Draw a grid
plt.grid(axis='y', color='w', linestyle='solid')
# ouput
plt.show()
# Close figure
plt.close()


#--------------------------------------------------------------
#--------- Pie Chart: League of Legends Viewers' Whereabouts
#--------------------------------------------------------------
# Config figure size, Personal preference, not a project requirement
plt.figure(figsize=(5,5))

# 5. 6. use plt.pie() to plot a pie chart

# Color countries list
colors = ['lightskyblue', 'gold', 'lightcoral', 'gainsboro', 'royalblue', 'lightpink', 'darkseagreen', 'sienna', 'khaki', 'gold', 'violet', 'yellowgreen']
# Makes pie plot
plt.pie(countries, colors=colors)
# ouput
plt.show()
# Clear the current figure
plt.clf()

# 7. Let's make it more visually appealing and more informative.

# Explode list 
explode = (0.07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
# Makes visually appealing pie plot 
plt.pie(countries, explode=explode, colors=colors, shadow=True, startangle=345, autopct='%1.0f%%', pctdistance=1.1, textprops={'fontsize': 7.4})
# Title
plt.title("League of Legends Viewers' Whereabouts", fontsize=16)
# Legend
plt.legend(labels, bbox_to_anchor=(1.1, 0.5), prop={'size': 11}, loc="right")
# ouput
plt.show()
# Close figure
plt.close()

#--------------------------------------------
#---------  Line Graph: Time Series Analysis
#--------------------------------------------
# Config figure size, Personal preference, not a project requirement
plt.figure(figsize=(8,6))
# 10. Use plt.plot() to plot a line graph

# Title
plt.title("Time Series")
# axis labels
plt.xlabel("Hour")
plt.ylabel("Viewers")
# Makes line plot
plt.plot(hour, viewers_hour, linewidth=2)
# Legend
plt.legend(['Jan, 1st 2015'])
# Adding x Ticks
ax = plt.subplot()
ax.set_xticks(hour)
# ouput
plt.show()
# Clear the current figure
plt.clf()

# 11. Let's account for a 15% error in the viewers_hour\

# Title
plt.title("Time Series", fontsize=16)
# axis labels
plt.xlabel("Hour", fontsize=12)
plt.ylabel("Viewers", fontsize=12)
# Makes line plot
plt.plot(hour, viewers_hour, linewidth=2)
# Legend
plt.legend(['Jan, 1st 2015'], loc='upper left')
# %15 error range upper and lower
y_upper = [i + (i*0.15) for i in viewers_hour]
y_lower = [i - (i*0.15) for i in viewers_hour]
# shade 15% error
plt.fill_between(hour, y_lower, y_upper, alpha=0.2)

ax = plt.subplot()
# Graph background color
ax.set_facecolor('#F5F5DC')
# x ticks
ax.set_xticks(hour)
# Draw a grid 
ax.grid(color='w', linestyle='solid')
# ouput
plt.show()
# Close figure
plt.close()
