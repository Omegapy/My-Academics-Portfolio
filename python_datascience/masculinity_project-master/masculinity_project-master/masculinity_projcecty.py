'''
###################################################################################
#                                                                                 #
#                                  Masculinity Survey                             #
#                                                                                 #
###################################################################################


My Codecademy Masculinity Survey Project From The Data Scientist Path Foundations of Machine Learning: Unsupervised Learning.

+ Project Goal
Find patterns in the way men view masculinity by utilizing the KMeans algorithm on a FiveThirtyEight masculinity survey data.


+ Overview
In this project, I investigated the way people think about masculinity by applying the KMeans algorithm to data from FiveThirtyEight.
https://fivethirtyeight.com/features/what-do-men-think-it-means-to-be-a-man/
FiveThirtyEight is a popular website known for their use of statistical analysis in many of their stories.

FiveThirtyEight and WNYC studios used 'masculinity-survey.pdf' to get their male readers' thoughts on masculinity.
FiveThirtyEight's article What Do Men Think It Means To Be A Man? contains their major takeaways.


+ Project Requirements
    Be familiar with:
        - Python3
        - Machine Learning: Unsupervised Learning

    The Python Libraries:
        - Pandas
        - NumPy
        - Matplotlib
        - Sklearn

+ Links
Blog Masculinity Survey
Project GitHub

'''
#
####################################################################################  Libraries
#
# Data manipulation tool
import pandas as pd
# Disable pandas copy warnings https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)
# Scientific computing, array
import numpy as np
# Data visualization
from matplotlib import pyplot as plt
# Theme to use with matplotlib
from jupyterthemes import jtplot
jtplot.style(theme='chesterish')
# Text I/O (https://docs.python.org/3/library/io.html)
# Utilize in converting the pandas.DataFrame.info() (NoneType) data output into a pandas.DataFrame type data.
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
# Regex
import re
# K-Means Clustering model
from sklearn.cluster import KMeans
#
#---- My Local python files
#
import column_types as ct
import feature_combinations as fc
#
####################################################################################  Investigate the Data
#
########################################################### Questions
#
# From the information found in 'masculinity-survey.pdf', I created a survey questions Series .
# The python file 'survey_questions.py' creates the Series.
survey_questions = pd.read_csv('data/survey_questions.csv', index_col = 0, squeeze = True)
print(survey_questions.to_frame())
#
###########################################################  The responses data
#
# Loading data
survey = pd.read_csv("masculinity.csv").drop(columns=['Unnamed: 0'])
print(survey)
############################ Numbers of columns and rows
# Survey Info
output = StringIO()
# Write info to a string buffer
survey.info(buf=output, verbose=True, null_counts=True)
# Stores the info into a pandas.Series
survey_info =  pd.Series(data=output.getvalue().split('\n'))
# Saves survey info
survey_info.to_csv('data/survey_info.csv')
print('\n')
print(survey_info.head(20))
# The 'survey' data frame has 98 columns and 1188 surveys, the column are questions' responses and survey responders collected information.
# The 'Dtypes' is showing mostly object data types, using 'column_types()' function to find out what kind of data type the objects are.
# Survey Info
output = StringIO()
# Write info to a string buffer
survey.info(buf=output, verbose=True, null_counts=True)
# Stores the info into a pandas.Series
survey_info =  pd.Series(data=output.getvalue().split('\n'))
# Saves survey info
survey_info.to_csv('data/survey_info.csv')
print(survey_info.head(20))
# The 'survey' data frame has 98 columns and 1188 surveys, the column are questions' responses and survey responders collected information.
# The 'Dtypes' is showing mostly object data types, using 'column_types()' function to find out what kind of data type the objects are.
survey_column_types = ct.column_types(survey)
survey_column_types.to_csv('data/survey_column_types.csv')
pd.set_option('display.max_rows', 200)
print('\n')
print(survey_column_types)
# - Checking for duplicated columns¶
# 'race2' and 'racethn4'
# 'educ3' and 'educ4'
# race2 and racethn4
print('\n')
print(survey['race2'].value_counts())
print('\n')
print(survey['racethn4'].value_counts())
# The columns 'race2' and 'racethn4' are not duplicated columns.
# The column 'race2' classifies survey responders as 'White' or 'Non_white'.
# The column 'racethn4' classifies survey responders as 'Black', 'White', 'Hispanic', 'Other' and 1 'W'.
# educ3 and educ4
for i in range(10):
    if survey['educ3'][i] != survey['educ4'][i]:
        print(survey['educ3'][i])
        print(survey['educ4'][i])
# 3 The some of the values `'College or more'` from the column `'educ3'` have been replace by
# the value `'Post graduate degree'` in the column `'educ4'`.
# Even if the columns `'educ3'` and `'educ4'` are not exact duplicate of each other,
# I decided to drop the column `'educ3'` from the `'survey'` DataFrame, and rename the the column `'educ4'`, `'education'`.
survey = survey.drop(['educ3'], axis=1).rename(columns={'educ4':'education'})
print('\n')
print(survey.columns)
############################ Number of people who said that they often ask a friend for professional advice
q0007_0001_count = survey["q0007_0001"].value_counts().to_frame()
print('\n')
print(q0007_0001_count)
print('\n')
print(q0007_0001_count.loc['Often'].to_frame())
############################ The questions 34 through 36 are not described in the masculinity-survey.pdf.
# I investigated the questions' responses data to find out the questions' topics
for question in ['q0034', 'q0035', 'q0036']:
    print(f'\nQuestion: {question}')
    print(survey[question].value_counts())
# From the questions' responses data I deducted:
# The question-34 topic is about the survey responder income.
# The question-35 topic is about the survey responder time zone.
# The question-36 topic is about device used by the responder to take the survey.
#
####################################################################################  Mapping the Data
#
# In order to use the KMeans algorithm with this data, I needed to first figure out how to turn
# the responses data into numerical data.
# For this exercise, I chose to use the responses data from 'question 7', the question is a matrix of multiple choice sub-questions.
# The sub-questions 7 and 1 through 4 are traditionally seen as feminine activities and
# the questions 5, 6, 8 and 9 are traditionally seen as masculine activities.
# The matrix sub-questions responses can be utilize by the K-Means algorithm to find out if 2 clusters based on
# those responses represent traditionally feminine and traditionally masculine people.
#
# I could cluster the data using the phrases 'Often' or 'Rarely', but I needed to turn the phrases into numbers,
# I decided to map the data in the following way:
#
# "Often" -> 4
# "Sometimes" -> 3
# "Rarely" -> 2
# "Never, but open to it" -> 1
# "Never, and not open to it" -> 0.
#
# Note that it's important that these responses are somewhat linear. 'Often' is at one end of the spectrum with 'Never,
# and not open to it' at the other. The other values fall in sequence between the two.
# I could perform a similar mapping for the 'education' responses , but there isn't an obvious linear progression in the 'racethn4' responses.
#
########################################################### The map_responses() function
#
def map_responses(responses_list, responses_ref):
    '''
    The function maps a given question sub-question responses data to numerical data.
    Takes the arguments:
        - responses_list, a list data type
        - question_ref, a string data type
    Finds sub-questions names
        - Maps sub-questions responses data to a numeric data
        - Returns a mapped responses DataFrame
    '''
    # Finds question sub-questions responses reference
    pattern = re.compile(responses_ref)
    q_col_name = [col_name for col_name in survey.columns if pattern.match(col_name)]
    # Maps sub-questions' responses to numeric data
    # Stores results into a DataFrame
    map_responses = pd.DataFrame()
    for col in q_col_name:
        map_responses[col] = survey[col].map({responses_list[i]: i for i in range(len(responses_list))})

    return map_responses
#
########################################################### Mapping question 7 response
#
# List of responses
q0007_responses_list = ['Never, and not open to it', 'Never, but open to it', 'Rarely', 'Sometimes', 'Often']
# Maps question 7 sub-question responses
q0007_responses = map_responses(q0007_responses_list, 'q0007')
q0007_responses.to_csv('data/q0007_responses.csv')
# Value count question 7 sub-question 1
q0007_0001_responses_count = q0007_responses['q0007_0001'].value_counts().to_frame().sort_index().reset_index().rename(columns={'index':'response_num'})
# map_q0007_0001['sub_questions'] = sub_q0007_list
q0007_0001_responses_count['responses'] = q0007_responses_list
q0007_0001_responses_count = q0007_0001_responses_count[['responses', 'q0007_0001']]
# Sets the output display precision in terms of decimal places, 0.
pd.set_option('precision', 0)
print('\n')
print(q0007_0001_responses_count)
#
#################################################################################### Plotting Question 7 Data
#
#
########################################################### Question 7 sub-questions
#
q0007_list = ['Ask a friend for professional advice',
              'Ask a friend for personal advice',
              'Express physical affection to male friends, like hugging, rubbing shoulders',
              'Cry',
              'Get in a physical fight with another person',
              'Have sexual relations with women, including anything from kissing to sex',
              'Have sexual relations with men, including anything from kissing to sex',
              'Watch sports of any kind',
              'Work out',
              'See a therapist',
              'Feel lonely or isolated']
#
########################################################### The plot_features() function
#
def plot_features(questions_list, responses, responses_list, question_name):
    '''
    The function scatters plots a given question sub-question responses into a grid of 2d graphs.
    - Takes the arguments:
        - questions_list, a list data type
        - responses, a DataFrame data type
        - responses_list, a list data type
        - question_name, a string data type<br><br>
    - plots grid of scatters plots
    - Saves grid
    '''
    # nCr combination to combine the mapped responses
    comb_responses = list(fc.f_combinations(responses.columns, 2))
    comb_questions_list = list(fc.f_combinations(questions_list, 2))
    # Numbers of 2 responses combinations
    num_comb = len(comb_responses)
    # Plot index counter used when displaying scatter plot matrix
    k = 1
    # Rows counter, number of rows needed for a 4 columns plotting grid
    if num_comb % 4 == 0:
        rows = num_comb / 4
    else:
        rows = (num_comb + 4 - (num_comb % 4)) / 4
    # Initializes figure
    grid = plt.figure(figsize=(22, 5* rows))
    plt.subplots_adjust(wspace=0.2, hspace=4 / rows)
    # Grid
    for i in range(num_comb):
        # Combination responses
        responses_1 = comb_responses[i][0]
        responses_2 = comb_responses[i][1]
        # Combination sub-question
        sub_q_1 = comb_questions_list[i][0]
        sub_q_2 = comb_questions_list[i][1]
        # Plot grid location
        plt.subplot(int(rows), 4, k)
        # Scatters plot
        plt.scatter(
            responses[responses_1],
            responses[responses_2],
            alpha=0.05,
            s=100,
            color='y'
        )
        # Ticks
        plt.xticks(np.arange(0, len(responses_list), step=1))
        plt.yticks(np.arange(0, len(responses_list), step=1))
        # Labels
        plt.xlabel(responses_1)
        plt.ylabel(responses_2)
        # Increment Plot index counter
        k += 1
        # Grid title, question
        if i == 2:
            plt.text(
                -0.5,
                len(responses_list) + 1,
                question_name,
                fontsize=34,
                horizontalalignment='center',
                verticalalignment='center',
                bbox=dict(
                    facecolor='#323a47',
                    edgecolor='None'
                )
            )
        # Questions legend
        if i == 0:
            questions = responses.columns
            legend = ''.join(str(e) for e in [f'{questions[i]} : {questions_list[i]}\n' for i in range(len(questions))])
            plt.text(
                0,
                len(responses_list) + 0.7,
                legend,
                fontsize=14,
                color='w',
                horizontalalignment='left',
                verticalalignment='center',
                bbox=dict(facecolor='#323a47', edgecolor='None')
            )
        # responses legend
        if i == 3:
            legend = ''.join(str(e) for e in [f'{i} : {responses_list[i]}\n' for i in range(len(responses_list))])
            plt.text(
                0,
                len(responses_list) + 0.7,
                legend,
                fontsize=14,
                horizontalalignment='left',
                verticalalignment='center',
                bbox=dict(facecolor='#323a47', edgecolor='None')
            )

    plt.savefig(f'graph/{question_name}.png')
    plt.show()
#
########################################################### Plotting question 7
#
plot_features(q0007_list, q0007_responses, q0007_responses_list, 'Question 7')
#
####################################################################################  K-Means Model
#
#
########################################################### Training model with selected question 7 sub-question response
#
# Isolates selected sub-questions and drops NaN values columns
# Finds question 7 sub-questions names
pattern = re.compile('q0007')
q0007_id = [col_name for col_name in survey.columns if pattern.match(col_name)]
q0007_responses = q0007_responses.dropna(subset = q0007_id)
# Initializes K-Means model
classifier = KMeans(n_clusters = 2, random_state=1)
# Training/Classifying selected sub-question responses
classifier.fit(q0007_responses[q0007_id])
############################  Centroids
# Stores centroids coordinates
centroids_q0007 = pd.DataFrame(classifier.cluster_centers_)
# Display
pd.set_option('precision', 8)
print('\n')
print(centroids_q0007)
 # Note: The inputted data has 11 features and 2 clusters, 'cluster_centers' returns 2 centroids in 11-dimensions
# (1 dimension per sub-question). Each list corresponds to the coordinates of the centroids in R^11.
# Renames columns
centroids_q0007 = centroids_q0007.rename(columns={i:f'R^{i+1}' for i in range(len(centroids_q0007.columns))})
# Adds a cluster number column
centroids_q0007['clusters'] = [1, 2]
# Rearranges columns
col_list = ['clusters']+[ centroids_q0007.columns[i] for i in range(len(centroids_q0007.columns)-1)]
centroids_q0007 = centroids_q0007[col_list]
# Saves and display DataFrame
centroids_q0007.to_csv('data/centroids_q0007.csv')
print(centroids_q0007)
#
#################################################################################### Separating by clusters
#
############### Labels
print('\n')
print(classifier.labels_)
#
########################################################### Adding model classifications results to the q0007_responses DataFrame
#
q0007_responses['clusters'] = classifier.labels_
print('\n')
print(q0007_responses)
#
########################################################### Separating question 7 responses data by clusters
#
# Cluster 1
q0007_responses_to_cluster_1 = q0007_responses.loc[q0007_responses['clusters'] == 0].drop('clusters', axis=1)
# Cluster 2
q0007_responses_to_cluster_2 = q0007_responses.loc[q0007_responses['clusters'] == 1].drop('clusters', axis=1)
# Samples
print('\nQuestion 7 Cluster-1:')
print(q0007_responses_to_cluster_1)
print(f'\nValues of cluster_1 DataFrame loc[2]:\n\n{q0007_responses_to_cluster_1.loc[2]}')
print(f'\nIndex values of question 7 cluster-1 DataFrame at index 0 to 9:\n{[q0007_responses_to_cluster_1.index[i] for i in range(10)]}')
#
########################################################### Plotting Question 7 Clusters
#
################################## The plot_clusters() fuction
def plot_clusters(cluster_1, cluster_2, questions_id, questions_list, responses_list, question_name):
    '''
    The function scatters plots a given question sub-question classified answer clusters into a grid of 2d graphs.
    - Takes the arguments:
        - cluster_1, a DataFrame data type
        - cluster_2, a DataFrame data type
        - question_id, a list data type
        - questions_list,  a list data type
        - responses_list, a list data type
        - question_name, a string data type<br><br>
    - plots a 1 row 2 column scatters plots grid
    - Saves grid
    '''
    clusters = [cluster_1, cluster_2]
    # Shorten question reference number
    q_id = [f'Q{i}' for i in range(1, len(questions_id) + 1)]

    plt.figure(figsize=(14, 14))
    # Grid
    for i in range(2):
        # Plots clusters
        # Note, the Grid has 2 rows, the first row accommodates the responses and questions legends
        # the seconds countains the plots, removing the first row will no the display by it will affect the legends when saving the figure
        plt.subplot(2, 2, i + 3)
        for j in clusters[i].index:
            plt.scatter(
                q_id,
                clusters[i].loc[j].values,
                alpha=0.05,
                s=100,
                color='y'
            )
            plt.yticks(np.arange(0, 5, step=1))
            plt.title(f'Cluster-{i + 1}')
            plt.xlabel('Questions')
            plt.ylabel('responses')
        # Title and questions legend
        if i + 3 == 3:
            legend = ''.join(str(e) for e in [f'{q_id[i]} : {questions_list[i]}\n' for i in range(len(q_id))])
            # Questions legend
            plt.text(
                -0.5,
                len(responses_list) + 0.8,
                legend,
                fontsize=12,
                color='w',
                horizontalalignment='left',
                verticalalignment='center',
                bbox=dict(facecolor='#323a47', edgecolor='None')
            )
            # Title
            plt.text(
                len(q_id) + 1,
                len(responses_list) - 0.2,
                question_name,
                fontsize=22,
                horizontalalignment='center',
                verticalalignment='center',
                bbox=dict(facecolor='#323a47', edgecolor='None')
            )
        # responses legend
        if i + 3 == 4:
            legend = ''.join(str(e) for e in [f'{i} : {responses_list[i]}\n' for i in range(len(responses_list))])
            plt.text(
                len(q_id) / 2,
                len(responses_list) + 0.7,
                legend,
                fontsize=12,
                horizontalalignment='left',
                verticalalignment='center',
                bbox=dict(facecolor='#323a47', edgecolor='None')
            )

    plt.savefig(f'graph/clusters_{question_name}.png')
    plt.show()
# Plotting question 7 clusters
plot_clusters(q0007_responses_to_cluster_1, q0007_responses_to_cluster_2, q0007_id, q0007_list, q0007_responses_list, 'Question 7 Clusters')
#
########################################################### Separating the survey data by Clusters
#
#
################################## Modifying the survey_questions
print(f'"kids" feature response from the 100th survey: {survey["kids"][100]}\n')
print(f'- "q025_0001" response from the 100th survey: {survey["q0025_0001"][100]}\n')
print(f'- "q025_0002" response from the 100th survey: {survey["q0025_0002"][100]}\n')
print(f'- "q025_0003" response from the 100th survey: {survey["q0025_0003"][100]}\n')
# Adding features to survey_questions
# Lists
missing_features_id = ['race2', 'racethn4', 'education', 'age3', 'kids', 'orientation', 'weight']
missing_features_description = ['Race', 'Race', 'Level of Education', 'Age', 'Children', 'Sexual Orientation', 'Weight']
# Creates a missing feature Series
missing_features = pd.Series(missing_features_description, index=missing_features_id)
# Adds
survey_questions = survey_questions.append(missing_features).rename('Survey Questions')
print('\n')
print(survey_questions.to_frame())
#
################################## Creating survey_questions DataFrame
# Transforms the 'survey_questions' Series into a DataFrame with an 'q_id' column
survey_questions_df = survey_questions.reset_index().rename(columns={'index':'q_id'})
survey_questions_df.to_csv('data/survey_questions_df.csv')
print('\n')
print(survey_questions_df)
#
################################## Creatingg Clusters DataFrame
# Empty cluster DataFrames
cluster_1_df = pd.DataFrame()
cluster_2_df = pd.DataFrame()
# Separates Dataframe 'survey' by clusters
for q_id in survey_questions_df['q_id']:
    # Finds the question id corresponding responses ids in the survey DataFrame
    pattern = re.compile(q_id)
    responses_id = [col_name for col_name in survey.columns if pattern.match(col_name)]
    for r_id in responses_id:
        cluster_1_df[r_id] = [survey[r_id][i] for i in q0007_responses_to_cluster_1.index]
        cluster_2_df[r_id] = [survey[r_id][i] for i in q0007_responses_to_cluster_2.index]

cluster_1_df.to_csv('data/cluster_1_df.csv')
cluster_2_df.to_csv('data/cluster_2_df.csv')
print('\n')
print(cluster_1_df)
#
#################################################################################### Investigate the Cluster Members
#
#
########################################################### The investigate_member() function
#
################################## The argument member
# The function takes the argument member, it is the a question id number, from the survey_question['q_id'] Series.
def investigate_member(member, cluster_1=cluster_1_df, cluster_2=cluster_2_df, survey=survey):
    '''
    The function, investigate_member(), returns a question percentages of responses, per selectable responses, and by cluster.
    Takes the arguments:
        - member, a string data type
        - cluster_1, a DataFrame data type defaulted to cluster_1_df
        - cluster_2, a DataFrame data type defaulted to cluster_2_df
        - survey, a DataFrame data type defaulted to survey
    Computes the member question percentages of responses, per selectable responses, and by cluster
    Returns a DataFrame of the percentages of responses, per selectable responses, and by cluster

    '''
    # Finds the member corresponding responses reference in the survey DataFrame
    pattern = re.compile(member)
    responses_id = [col_name for col_name in survey.columns if pattern.match(col_name)]
    # Empty ivestagation DataFrame
    investigation = pd.DataFrame()
    # Response 'weight'
    if member == 'weight':
        investigation['cluster_1'] = [cluster_1['weight'].mean()]
        investigation['cluster_2'] = [cluster_2['weight'].mean()]
    # Responses
    else:
        # Calculates the question percentages of responses, per responses part, and by cluster
        for r_id in responses_id:
            # Empty response part DataFrame
            inv = pd.DataFrame()
            # Calculates saves percentages
            inv['cluster_1'] = cluster_1[r_id].value_counts()/len(cluster_1_df[r_id])
            inv['cluster_2'] = cluster_2[r_id].value_counts()/len(cluster_2_df[r_id])
            # Creates a new index list and keeps the old index list
            inv = inv.reset_index()
            # Removed the response part not selected percentages
            inv = inv[inv['index'] != 'Not selected']
            # Add the response part percentages to the main DataFrame
            investigation = pd.concat([investigation, inv], axis=0).reset_index(drop=True)
    # Renames the column index to the question sentence and creates a new index list
    question = survey_questions_df['Survey Questions'][survey_questions_df['q_id'] == member].values[0]
    investigation = investigation.rename(columns={'index':question}).reset_index()
    # Renames the column index to 'member'
    investigation = investigation.rename(columns={'index':member})
    return investigation
#
########################################################### Responses investigation results
#
print('\n')
print(investigate_member('q0004'))
print('\n')
print(investigate_member('q0010'))
print('\n')
print(investigate_member('q0011'))
#
########################################################### Answering the demographic question
#
# In the survey_questions_df, the demographic features are found from the indexes 29, q0024, to 44, weight.
print('\n')
print(survey_questions_df[29:])
# Some of the demographic features are closely related like q0025, Do you have any children?, and kid, Children.
# For this exercise, I decided to remove some of related features.
demographic_survey_questions = survey_questions_df[29:].drop([31, 39, 40, 42])
print('\n')
print(demographic_survey_questions)
#
############################## Demographic features correlation with the traditional ideas of masculinity, Cluster-2
#
# Creates an empty cluster-2  demographic analysis DataFrame
analysis_demographic_c2 = pd.DataFrame(columns=['id', 'reponses', 'cluster_1', 'cluster_2'])
# Finds demographic survey questions responses
for q_id in demographic_survey_questions['q_id']:
    # Calculates percentages, features investigation results
    an_demographic = investigate_member(q_id)
    # Compares features investigation and saves results
    for i in range(len(an_demographic)):
        # Compares features investigation results results
        if an_demographic['cluster_1'][i] < an_demographic['cluster_2'][i]:
            # Finds the responses 'id' and store the values to used as a columns name
            values = [an_demographic.columns[0]] + an_demographic.loc[i][1:].values.tolist()
            # Stores comparison results
            analysis_demographic_c2 = analysis_demographic_c2.append(dict(zip(analysis_demographic_c2.columns, values)),
                                                                     ignore_index=True)
    # Calculates the difference between the cluster-2 higher than cluster-1 features investigation results
    analysis_demographic_c2['Diff'] = analysis_demographic_c2['cluster_2'] - analysis_demographic_c2['cluster_1']
# Sorts by Difference values
analysis_demographic_c2 = analysis_demographic_c2.sort_values(by=['Diff'], ascending=False)

analysis_demographic_c2.to_csv('data/analysis_demographic_c2.csv')
print('\n')
print(analysis_demographic_c2.head(10))
 #The demographic features having the strongest correlations with the ideas of *traditional* masculinity are:
# straight men over 65 years old that use windows desktops or/and laptops as personal computers, and have children over 18 years old.
#
############################## Demographic features correlation with the non-traditional ideas of masculinity, Cluster-1
#
# Creates an empty cluster-1 demographic analysis DataFrame
analysis_demographic_c1 = pd.DataFrame(columns=['id', 'reponses', 'cluster_1', 'cluster_2'])
# Finds demographic survey questions responses
for q_id in demographic_survey_questions['q_id']:
    # Calculates percentages, features investigation results
    an_demographic = investigate_member(q_id)
    # Compares features investigation and saves results
    for i in range(len(an_demographic)):
        # Compares features investigation results results
        if an_demographic['cluster_1'][i] > an_demographic['cluster_2'][i]:
            # Finds the responses 'id' and store the values to used as a columns name
            values = [an_demographic.columns[0]] + an_demographic.loc[i][1:].values.tolist()
            # Stores comparison results
            analysis_demographic_c1 = analysis_demographic_c1.append(dict(zip(analysis_demographic_c1.columns, values)),
                                                                     ignore_index=True)
     # Calculates the difference between the cluster-1 higher than cluster-2 features investigation results
    analysis_demographic_c1['Diff'] = analysis_demographic_c1['cluster_1'] - analysis_demographic_c1['cluster_2']
# Sorts by Difference values
analysis_demographic_c1 = analysis_demographic_c1.sort_values(by=['Diff'], ascending=False)

analysis_demographic_c1.to_csv('data/analysis_demographic_c1.csv')
print('\n')
print(analysis_demographic_c1.head(10))
# The demographic features having the strongest correlations with the ideas of non-traditional masculinity are:
# Gay or bisexual post graduate degree men between 35-64 years old that use iOS phones or/and tablets.
#
#################################################################################### All the features investigation results
#
# The following code cell outputs all the features investigation results, if you are interested to take a look at i
for q_id in survey_questions_df['q_id']:
    investigation = investigate_member(q_id)
    # Saves
    question_id = investigation.columns[0]
    investigation.to_csv(f'data/inv_{question_id}.csv')
    # Displays
    print('\n')
    print(investigation)