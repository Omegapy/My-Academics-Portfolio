
My Python Data Visualization with the Library Matplotlib Practice Project From:

Codecademy Data Science course Python, Data Visualization with Seaborn Matplotlib and Jupyter Notebook

Visualizing Kiva Data with Seaborn
Seaborn Project Cumulative

----------------------------------------------------------------------------------------

Project Requirements:

Python v2 or later:
https://www.python.org/


Matplotlib
https://matplotlib.org/

Seaborn:
https://seaborn.pydata.org/

Jupyter notebook:
https://jupyter.org/

----------------------------------------------------------------------------------------

Overview:

In this project, we will be visualizing and looking for insights in a dataset from Kaggle (https://www.kaggle.com/fkosmowski/kivadhsv1), 
that contains information about loans awarded by the non-profit Kiva (https://www.kiva.org/).

Using Seaborn, we will explore the average loan amount by country using aggregated bar charts, 
and visualize the distribution of loan amount by project type and gender using box plots and violin plots.

You will be completing this project on your computer, similar to the other off-platform projects that we’ve done during this path.

WORKING ON YOUR COMPUTER
Learn about Jupyter Notebooks, a cool way of combining Python code with explanations or instruction in a web terminal.

----------------------------------------------------------------------------------------

Project map:

Python Jupiter code lines file
kiva_project.ipynb

data files
kiva_data.csv

----------------------------------------------------------------------------------------

Project:

1.
Import Necessary Python Modules

2.
Load kiva_data.csv into a DataFrame called df. Then, quickly inspect the DataFrame using .head().
Use pd.read_csv().

3.
Examine The Data.

Each entry (row) in the dataset represents a loan that Kiva awarded to a particular project. The loan_amount column shows the amount (in U.S. dollars) awarded to the project. The activity column has the category type that the project falls under. The country column is the country where the project is located. The gender column represents the gender of the primary person who applied for the loan.

Print the first 25 rows of df using .head()

4.
Bar Charts

Create a bar plot using Seaborn to visualize the average size of Kiva loans given to projects, by country.

We've set up the figure you'll use to plot your bar plot on. The f variable gives us access to the figure and ax gives us access to the axes.

Use sns.barplot() with the following arguments:

data set to df
x set to country
y set to loan_amount

Adding $ units¶
Format the ticks on the y-axis begin with a $ (units of USD).

5.
Learn More By Using hue In Your Visualization.

You can visualize even more data on one bar plot by visualizing the loan amount by country, and "nesting" by gender. Add the hue parameter to your sns.barplot() and set it so that the visualization includes the nested category of gender.

On average, do female or male recipients receive larger loans from Kiva?
Which country has the least disparity in loan amounts awarded by gender?
Based on the data, what kind of recommendations can you make to Kiva about the loans they give?
What actions could be taken to implement the recommendations you've made?

6.
Styling

Set a different color palette using sns.set_palette(). You can use any of the Color Brewer qualitative color palettes:

Set1
Set2
Set3
Pastel1
Pastel2
Dark2
Accent
You can read more about qualitative color palettes in the Seaborn documentation.

Set the plot background style using sns.set_style(). You can experiment with:

whitegrid
darkgrid
white
dark
Set the title using ax.set_title("").


7.
Box Plots With Kiva Data

So far you have visualized the average size of loans by country using bar charts; now you are going to make a box plot to compare the distribution of loans by country.

We have set up a figure for you to plot on. Use sns.boxplot() to compare the distribution of loan amounts by country for the Kiva dataset.

sns.boxplot() can be passed the same parameters as sns.barplot().

Optional: You may set a new color palette if you would like to continue using sns.set_palette().

8.
Box Plot by Activity

Instead of visualizing the loan amount by country, use sns.boxplot() to plot the loan amount by activity.

Optional: Set a different plot style and color palette to best visualize this data.

Reflection Questions¶
What does this visualization reveal that previous ones did not?

9.
Violin Plots

You can use nearly identical syntax (as you have used for box plots) to create violin plots. Take this line of code from above:

sns.boxplot(data=df, x="activity", y="loan_amount")
To visualize the distribution of the exact same data as a violin plot you could pass the same parameters to sns.violinplot() instead of sns.boxplot().

*  Change the code in the cell below so that the data is plotted as a violin plot instead of a barplot.

*  Create a violin plot that visualizes the distribution of loan amount by country.¶

*  Previously, you created a violin plot and plotted the data by activity. This time, create a violin plot that plots the data by country.


10.
Split Violin Plots

Use the hue and split parameters with sns.violinplot() to visualize the distribution of loan amount by country, split by gender.

