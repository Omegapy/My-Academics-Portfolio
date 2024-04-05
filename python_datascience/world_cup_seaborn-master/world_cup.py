#-------------------------------------------------------------------------#
#                                                                         #
#             Codecademy Data Science course Python                       #
#             Data Visualization with the Matplotlib Library              #
#                       and The searborn Library                          #
#                                                                         #
#                             "World Cup!"                                #
#                                                                         #
#-------------------------------------------------------------------------#
#
# ----------------- 1. Libraries
#
# Matplotlib
from matplotlib import pyplot as plt
# Pandas
import pandas as pd
# Seaborn
import seaborn as sns
#
# ----------------- 3.
# Inspect the raw CSV files that you will be using in this project
# by selecting them in the file navigator.
#
df = pd.read_csv('WorldCupMatches.csv')
#
# ----------------- 4.
# Inspect the DataFrame using .head().
#
print(df.head(10))
#
# ----------------- 5.
# Create a new column in df named Total Goals,
# and set it equal to the sum of the columns Home Team Goals and Away Team Goals.
#
df['Total Goals'] = df['Home Team Goals'] + df['Away Team Goals']
print(df.head(10))
#
# ----------------- 6.
# You are going to create a bar chart visualizing
# how many goals were scored each year the World Cup was held between 1930-2014.
# Set the style of your plot to be whitegrid
#
sns.set_style("whitegrid")
sns.barplot(data=df, x='Year', y='Total Goals', ci=None, estimator=sum)
plt.show()
#
# ----------------- 7.
#
# To make the text in your visualization bigger and easier to read, set the context to be "poster".
# Note: I did not like "poster" looks like so i used (rc) to set my own parameters
#
sns.set_style("whitegrid")
sns.set_context( rc={'font.size': 10, 'xtick.labelsize': 6})
sns.barplot(data=df, x='Year', y='Total Goals', ci=None, estimator=sum)
plt.show()
#
# ----------------- 8.
# Create a figure and axes for your plot using the syntax:
# f, ax = plt.subplots()
# Inside of plt.subplots(), set the size of the figure to be 12 inches wide and 7 inches ta
#
f, ax = plt.subplots(figsize=(12, 7))
#
# ----------------- 9.
# Using the data in df and the syntax:
# ax = sns.barplot()
# visualize the columns Year and Total Goals as a bar chart.
# Year should be on the x-axis, and Total Goals should be on the y-axis.
#
ax = sns.barplot(data=df, x='Year', y='Total Goals', ci=None)
#
# ----------------- 11.
# Effective visualizations include a clear title.
# Give your bar chart a meaningful title using ax.set_title()
#
ax.set_title('Fifa World Cup, Goals')
#
# ----------------- 10.
# Render your bar chart so you can see it
#
plt.show()
#
# ----------------- 12.
# Load goals.csv into a DataFrame called df_goals,
# and take a quick look at the DataFrame using .head().
#
df_goals = pd.read_csv('goals.csv')
print(df_goals.head(10))
#
# ----------------- 13-14-15-16-17.
# experimenting with different contexts and font scales can help you decide on the best
# context and font scale for the particular visualization.
#
sns.set_style("darkgrid")
f, ax2 = plt.subplots(figsize=(12, 8))

ax2 = sns.boxplot(data=df_goals, x='year', y='goals')
ax2.set_xlabel('Year', fontsize=20)
ax2.set_ylabel('Goals', fontsize=20)
ax2.set_title('Fifa World Cup, Goals Distribution', fontsize=25)
ax2.set_xticklabels(df_goals.year, fontsize=10)
ax2.set_yticklabels(df_goals.goals, fontsize=15)
plt.show(ax2)

