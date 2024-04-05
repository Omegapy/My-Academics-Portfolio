'''
###################################################################################
#                                  Tweet Location                                   #
#               Twitter Classification Cumulative Project Part-2                  #
###################################################################################

My Codecademy Challenging Part-2 Project From The Data Scientist Path Foundations of Machine Learning:
Supervised Learning Course, Advance Classification Models Section.

Overview
In this project, Twitter Classification Cumulative Project,
I use real tweets to find patterns in the way people use social media. There are two parts to this project:

Part-1:  Viral Tweets, Predict Viral Tweets, using a K-Nearest Neighbors classifier model.
Part-2: Classifying Tweet - Tweet Location (this section).

+ Project Goal
Using Naive Bayes Classifier Models, classify any tweet (or sentence) and predict
whether that sentence came from New York, London, or Paris.

+ Project Requirements

    Be familiar with:
        -Python3
        -Machine Learning: Supervised Learning
        -The Python Libraries:
            Pandas
            NumPy
            SKlearn

'''
#
####################################################################################  Libraries
#
# Data manipulation tool
import pandas as pd
# Scientific computing, array
import numpy as np
# Data splitter
from sklearn.model_selection import train_test_split
# Convert a collection of text documents to a matrix of token counts
from sklearn.feature_extraction.text import CountVectorizer
# Naive Bayes Classifier
from sklearn.naive_bayes import MultinomialNB
# Model evaluation
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix
#
#################################################################################### Investigate the Data
#
# ----------- Importing the data
new_york_tweets = pd.read_json("data_json/new_york.json", lines=True)
london_tweets = pd.read_json("data_json/london.json", lines=True)
paris_tweets = pd.read_json("data_json/paris.json", lines=True)
#########################  The columns, or features, of a tweet
features_type = new_york_tweets[new_york_tweets.columns].dtypes.to_frame().rename(columns={0:'dtype'})
print(f'--------- Tweets\' Features Dtype\n\n{features_type}')
# --------------- Some of the features are objects, for example "user", let's explore and find out what kind of object those features are.
features_type['type'] = [type(new_york_tweets.loc[0][col]).__name__ for col in new_york_tweets.columns]
print(f'\n--------- Tweets\' Features Dtype\n\n{features_type}')
# I used the new_york_tweets index O row to output the objects' data type,
# some of features object values of the row are equal to NaN outputting a NoneType data type,
# let's find out those objects' actual data type by using different row values not equal to NaN.
for feature in features_type.index:
    if features_type.loc[feature]['type'] == 'NoneType':
        for i in range(len(new_york_tweets)):
            if new_york_tweets.loc[i][feature] != None:
                features_type.loc[feature]['type'] = type(new_york_tweets.loc[i][feature]).__name__
                break
features_type.to_csv('data/features_type.csv')
print(f'\n--------- Tweets\' Features Dtype\n\n{features_type}')
#-------------------------------- The "text" features has useful data to predict a tweet location.
print(f'\nText of 12th tweet: {new_york_tweets.loc[12]["text"]}')
######################### new_york_tweets, london_tweets and paris_tweets number of tweets:
print(f'Number of tweets from New York: {len(new_york_tweets)}')
print(f'Number of tweets from London: {len(london_tweets)}')
print(f'Number of tweets from Paris: {len(paris_tweets)}')
#
#################################################################################### Naive Bayes Classifier
#
################ Defining data and labels
# Isolating the `text` features data from each DataFrame
new_york_text = new_york_tweets["text"].tolist()
london_text = london_tweets["text"].tolist()
paris_text = paris_tweets["text"].tolist()
# Combined text data
all_tweets_text = new_york_text + london_text + paris_text
# Labels
labels = [0] * len(new_york_text) + [1] * len(london_text) + [2] * len(paris_text)
################  Creating training and test sets
train_data, test_data, train_labels, test_labels = train_test_split(all_tweets_text, labels, test_size = 0.2, random_state = 1)
# Set Samples
print(f'\n--------- Tweets\' Labels Test Sample\n\n{pd.DataFrame({"test_labels":test_labels}).head(10)}')
print(f'\n--------- Tweets\' Data Test Sample\n\n{pd.DataFrame({"test_data":test_data}).head(10)}')
#
################  Making the Count Vectors
# Initializes the counter vector
counter = CountVectorizer()
# learns a vocabulary dictionary: raw text corpus → processed text → tokenized text → corpus vocabulary → text representation
counter.fit(train_data)
# Vector, transforms the learned vocabulary dictionary to a document-term matrix
train_counts = counter.transform(train_data)
test_counts = counter.transform(test_data)
# Count Vector Sample
print(f'\nTrain data 3rd tweet:\n{train_data[3]}\n')
print('Count Vector:\n')
print(train_counts[3])
#
################  Train and Test the Naive Bayes Classifier
# Initializes Naive Bayes model
classifier = MultinomialNB()
# Trains model
classifier.fit(train_counts, train_labels)
# Predicts the tweets test data locations
predictions = classifier.predict(test_counts)
# Prediction Sample
print(f'\n--------- Predictions\' Sample\n\n{pd.DataFrame({"Predictions":predictions}).head(10)}')
#
#################################################################################### Evaluating The Model
#
################ Accuracy
accuracy = accuracy_score(test_labels, predictions)
# Saves and displays the accuracy score
accuracy = pd.DataFrame({'Accuracy':[accuracy]})
accuracy.to_csv('accuracy.csv')
print(f'\n--------- Accuracy\n\n{accuracy}')
#
################ Precision
# List of locations
locations = ['New York', 'London', 'Paris', 'Combined Locations']
# The argument "average=None" returns each class precision score
precisions = precision_score(test_labels, predictions, average=None)
# The argument "average='weighted'" returns the weighted averaged precision score of the three classes
precision_avg = precision_score(test_labels, predictions, average='weighted')
# Combined precision scores results
precisions = np.append(precisions, [precision_avg], axis=0)
precision_scores = pd.DataFrame({'Locations':locations, 'Precision Scores':precisions})
# Saves precision scores results
precision_scores.to_csv('data/precision_scores.csv')
# Displays
print(f'\n--------- Precisions\n\n{precision_scores}')
#
################ Precision
# The argument "average=None" returns each class recall score
recalls = recall_score(test_labels, predictions, average=None)
# The argument "average='weighted'" returns the weighted averaged recall score of the three classes
recall_avg = recall_score(test_labels, predictions, average='weighted')
# Combined recall scores results
recalls = np.append(recalls, [recall_avg], axis=0)
recall_scores = pd.DataFrame({'Locations':locations, 'Recall Scores':recalls})
# Saves precision scores results
recall_scores.to_csv('data/recall_scores.csv')
# Displays
print(f'\n--------- Recall\n\n{recall_scores}')
#
################ Confusion Matrix
cf_matrix = confusion_matrix(test_labels, predictions)
raw_cf_matrix = pd.DataFrame(columns=[''])
for result in cf_matrix:
    raw_cf_matrix = raw_cf_matrix.append({'':result}, ignore_index=True)
# Saves raw matrix
raw_cf_matrix.to_csv('data/raw_cf_matrix.csv')
print(f'\n--------- Raw Confusion Matrix\n\n{raw_cf_matrix}')
# ----------------- Descriptive Confusion Matrix DataFrame
new_york_matrix_labels = ['True Positives:', 'False Positive - Was London:', 'False Positive - Was Paris:']
london_matrix_labels = ['True Positives:', 'False Positive - Was New York:', 'False Positive - Was Paris:']
paris_matrix_labels = ['True Positives:', 'False Positive - Was New York:', 'False Positive - Was London:']

desp_cf_matix = pd.DataFrame({'New York':new_york_matrix_labels, ' ':cf_matrix[0],
                            'London':london_matrix_labels, '  ':cf_matrix[1],
                            'Paris':paris_matrix_labels, '   ':cf_matrix[2]})
# Saves description matrix
desp_cf_matix.to_csv('data/desp_cf_matix.csv')
print(f'\n--------- Description Confusion Matrix\n\n{desp_cf_matix}')
#
#################################################################################### Test Your Own Tweet
#
tweet = input(f'\nEnter your tweet:\n')
# Vectorizes the tweet
tweet_counts = counter.transform([tweet])
# Predicts
location = classifier.predict(tweet_counts)
if location == 0:
    print(f'\nBase on your tweet, you are probably from: {locations[0]}')
elif location == 1:
     print(f'\nBase on your tweet, you are probably from: {locations[1]}')
else:
     print(f'\nBase on your tweet, you are probably from: {locations[2]}')