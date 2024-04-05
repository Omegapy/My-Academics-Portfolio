'''

                                                U.S.A. Presidential Vocabulary

A Codecademy practice project from the Data Scientist Path Natural Languages Processing (NLP) Course, Word Embeddings Section.

Overview:

Whenever a United States of America president is elected or re-elected,
an inauguration ceremony takes place to mark the beginning of the president’s term.
During the ceremony, the president gives an inaugural address to the nation, dictating the tone
and focus of the next four years of leadership.

In this project you will have the chance to analyze the inaugural addresses of the presidents of the United States of America,
as collected by the Natural Language Toolkit, using word embeddings.

By training sets of word embeddings on subsets of inaugural address versus the collection of presidents as a whole,
we can learn about the different ways in which the presidents use language to convey their agenda.

Project Goal:
Analyze USA presidential inaugural speeches using NLP word embeddings models.

Project Requirements
Be familiar with:
    Python3
    NLP (Natural Languages Processing)

    The Python Libraries:
        re
        Pandas
        Json
        Collections
        NLKT
        Sklearn
        gensim

Link:
My Project Blog Presentation:
https://www.alex-ricciardi.com/post/u-s-a-presidential-vocabulary

Project Jupiter Notebook Code presentation:
https://github.com/ARiccGitHub/us_presidential_vocabulary/blob/master/us_presidential_vocabulary.ipynb

Project GitHub:
https://github.com/ARiccGitHub/us_presidential_vocabulary

'''


#-------------------------------------------------------------------------------------------------- Libraries:

# Regex
import re
# Operating system dependent functionality
import os
# JSON encoder and decoder
import json
# Data manipulation tool
import pandas as pd
# Natural language processing
import nltk
# Tokenization into sentences
from nltk.tokenize import PunktSentenceTokenizer
# Stop words and lexical database of English
from nltk.corpus import stopwords, wordnet
# lemmatization class
from nltk.stem import WordNetLemmatizer
# Counter Dictionary class - https://docs.python.org/3/library/collections.html#collections.Counter -
from collections import Counter
# word2vec model library
import gensim

#-------------------------------------------------------------------------------------------------- Variable

# The option to use the function input_word()
input_option = False

#-------------------------------------------------------------------------------------------------- Funtions

def save_list(file_name, list_to_save):
    '''
    Takes the arguments:
        file_name, string data type
        list_to_save, list data type
    Saves list_to_save into file_name.txt as json objects
    '''
    with open(f'data/{file_name}.txt', 'w') as file:
        file.write(json.dumps(list_to_save))

def load_list(list_name):
    '''
    Takes the arguments:
        list_name, string data type
    Load list_name.txt
    Returns the list_name.txt as a list
    '''
    with open(f'data/{file_name}.txt', 'r') as file:
        return json.loads(file.read())

def input_word(input_subject, word_list):
    '''
    The input function is optional, a personal preference,
    I created the function to easily input different variable values without having to change the code.
    The option to use the function is by default turn on

    The function takes the arguments:
        input_subject, string data type
        word_list, list data integer type
    Outputs on screen the input_subject
    Take a user input, inputted_word
    Compares inputted_word with items in the word_list
    Returns inputted_word.lower()
    '''
    # Inputs a president name
    inputted_word = input(f'\nEnter a {input_subject}: ')

    while inputted_word.lower() not in word_list:
        print(f'\n{inputted_word} is not in the {input_subject} list')
        inputted_word = input(f'\nPlease reenter a {input_subject}: ')
    print()

    return inputted_word.lower()

def get_part_of_speech(word):
    '''
    Takes the arguments:
        word, string data type.
    Matches word with synonyms
    Tags word and count tags.
    Returns The most common tag, the tag with the highest count, ex: n for Noun, string data type.
    '''
    # Synonyms matching
    probable_part_of_speech = wordnet.synsets(word)
    # Initializing Counter class object
    pos_counts = Counter()
    # Taging and counting tags
    pos_counts["n"] = len([item for item in probable_part_of_speech if item.pos() == "n"])  # Noun
    pos_counts["v"] = len([item for item in probable_part_of_speech if item.pos() == "v"])  # Verb
    pos_counts["a"] = len([item for item in probable_part_of_speech if item.pos() == "a"])  # Adjectif
    pos_counts["r"] = len([item for item in probable_part_of_speech if item.pos() == "r"])  # Adverb
    # The most common tag, the tag with the highest count, ex: n for Noun
    most_likely_part_of_speech = pos_counts.most_common(1)[0][0]

    return most_likely_part_of_speech


#----------------------------------------------------------------------------------------------- Preprocessing the Data

#-----------------------------Converting files into a corpus
# Project directory path
path = os.getcwd()
# Sorts and save files name from the corpus_data folder
file_names = sorted([file for file in os.listdir(f"{path}/corpus_data")])
# Creates a speeches list from files
speeches = []
for name in file_names:
    with open(f'corpus_data/{name}', 'r+') as file:
        speeches.append(file.read())
# Sample from the speeches corpus:
# 1793-Washington's speech
print(speeches[1])

#------------------------------------------------------------------------------------ Converting files into a corpus
# The 'us' word:
# The word 'us' is a commonly used word in presidential inauguration addresses.
# The result of preprocessing the word 'us' through lemmatizing with the part-of-speech tagging method
# nlt.corpus.reader.wordnet.synsets() function and in conjunction with stopwords removal and
# the nltk.stem.WordNetLemmatizer().lemmatize() method, is that the word 'us' becomes 'u'.
# This happens because the lemmatize(word, get_part_of_speech(word)) method removes the character 's'
# at the end of words tagged as nouns. The word 'us', which is not part of the stopwords list, is tagged
# as a noun causing the lemmatization result of 'us' to be 'u'.
print(f"Is the word 'us' a stopword?\n{'us' in set(stopwords.words('english'))}")
print('\nDoes the get_part_of_speech() function tags the word "us" as a noun?')
if get_part_of_speech('us') == 'n':
    print('yes\n')
else:
    print('No\n')
# The lemmatize(word, get_part_of_speech(word)) method removes the character 's' at the of words tags as noun,
# and the word 'us' is tagged as a noun causing the lemmatization result of 'us' to be 'u'
normalizer_us = WordNetLemmatizer()
print(f"Result of the lemmatization of the word 'us':\n{normalizer_us.lemmatize('us', get_part_of_speech('us'))}\n")

#------------------------------------------------------------------------------------ Preprocessing
# Stop words
stop_words = set(stopwords.words('english'))
# Initializes the lemmatizer
normalizer = WordNetLemmatizer()
# Creates an empty list of processed speeches
preprocessed_speeches = []
# ---------------------- Preprocessing loop
for speech in speeches:
    # ------------------ Tokenizing
    # Initializes sentence tokenizer
    sentence_tokenizer = PunktSentenceTokenizer()
    # Tokenizes speech into sentences
    sentence_tokenized_speech = sentence_tokenizer.tokenize(speech)
    # ------------------ Normalizing loop
    # Creates an empty sentences list
    word_sentences = []
    for sentence in sentence_tokenized_speech:
        # ----------- Removes noise from sentence and tokenizes the sentence into words
        word_tokenized_sentence = [re.sub('[^a-zA-Z0-9]+', '', word.lower()) \
                                   for word in sentence.replace(",", "").replace("-", " ").replace(":", "").split()]
        # ---------------- Removes stopwords from sentences
        sentence_no_stopwords = [word for word in word_tokenized_sentence if word not in stop_words]
        # ---------------- Before lemmatizing, adds a 's' to the word 'us'
        word_sentence_us = ['uss' if word == 'us' else word for word in sentence_no_stopwords]
        # ---------------- Lemmatizes
        word_sentence = [normalizer.lemmatize(word, get_part_of_speech(word)) \
                         for word in word_sentence_us if not re.match(r'\d+', word)]
        # Stores preprocessed word
        word_sentences.append(word_sentence)
        # Stores sentence tokenized into words
    preprocessed_speeches.append(word_sentences)
# Saves preprocessed corpus
save_list('preprocessed_speeches', preprocessed_speeches)
# Displays words from the second speech first sentences
print(f'Sample from the preprocessed_speeches list, preprocessed corpus:\n{preprocessed_speeches[1][0]}\n')
#------------------------------------------------------------- Presidents speeches dictionary
# Creates a list of the speech's names relative to the presidents' names and year of the speech
year_president_speech_names = [name.lower().replace('.txt', '').replace('1989-bush', '1989-bush senior') for name in file_names]
# Creates a dictionary of the presidents preprocessed speeches
presidents_speeches = dict(zip(year_president_speech_names, preprocessed_speeches))
#------------------------------------------------------------- Presidents preprocessed speeches DataFrame:
df_presidents_speeches = pd.DataFrame({'Preprocessed Speech' : preprocessed_speeches}, index = year_president_speech_names)
df_presidents_speeches.to_csv('data/processed_presidents_speeches.csv')
print('Presidents preprocessed speeches DataFrame:')
print(df_presidents_speeches.head())
# Displays words in each sentences from the 1793-Washington's speech
print(f"\nSample from the df_presidents_speeches DataFrame:\n{df_presidents_speeches.loc['1793-washington'][0]}\n")
# Displays words in the first sentence from the 1793-Washington's speech
print(f"Displays words in the first sentence from the 1793-Washington's speech\n{df_presidents_speeches.loc['1793-washington'][0][0]}\n")
#------------------------------------------------------------- All words and speeches
# Creates an empty list of all the sentences in processed_speeches
all_sentences = [sentence for speech in preprocessed_speeches for sentence in speech]
# Saves all_sentences
save_list('all_sentences', all_sentences)
print(f"Sample from the all_sentences list:\n{all_sentences[23]}\n")
# Words in all sentences list:
all_words = [word for sentence in all_sentences for word in sentence]
# Saves all_words
save_list('all_words', all_words)

#-------------------------------------------------------------------------------------------------- Word Embeddings

#------------------------------------------------------------------------------------ All Presidents
#------------------------------------------------------------- Most frequently used terms:
most_freq_words = Counter(all_words).most_common()
# Saves most_freq_words
save_list('most_freq_words', most_freq_words)
# 10 first most frequently used words
print(f'Most frequently used terms:\n{most_freq_words[:10]}\n')
# 3 most frequently used words with count
print(f'3 most frequently used words with count:\n{most_freq_words[:3]}\n')
print(f'3 most frequently used words:\n{[word[0] for word in most_freq_words[:3]]}\n')
#------------------------------------------------------------- Word2Vec, word embeddings model
word_embeddings = gensim.models.Word2Vec(all_sentences,
                                         size=96, window=5, min_count=1, workers=2, sg=1)
# Removing duplicated words in all_words
vocabulary_of_terms = list(set(all_words))
# Saves vocabulary_of_terms
save_list('vocabulary_of_terms', vocabulary_of_terms)
# A sample of a word vector representation generate by the word_embedding model
vec_word = 'us'
# Word vector representation
print(f'{vec_word} vector representation:\n{word_embeddings.wv[vec_word]}\n')
#------------------------------------------------------------- Similar terms sample:
# Optional input function
if input_option:
    similar_to_word = input_word('similar word', vocabulary_of_terms)
else:
    similar_to_word = 'government'
# Calculate the cosine distance between word vectors outputting the 20 most similar words to the inputted word
similar_word_dist_vec = word_embeddings.wv.most_similar(similar_to_word, topn=20)
# Saves vocabulary_of_terms
save_list('vocabulary_of_terms', vocabulary_of_terms)
# List of similar words and their vectors cosine distance relative to the inputted word
print(f'Similar terms to {similar_to_word} with distance vectors:\n{similar_word_dist_vec}\n')
# List of the similar words no distance vector
print(f'Similar terms to {similar_to_word}:\n{[word[0] for word in similar_word_dist_vec]}\n')

#------------------------------------------------------------------------------------ One President
#------------------------------------------------------------- President's names list
president_names = list(dict.fromkeys([re.sub(r'^....-', '', name) for name in year_president_speech_names]))
# Saves president_names
save_list('president_names', president_names)
print(f'President names:\n{president_names}')
#------------------------------------------------------------- Preprocessing one president's data
# Optional input function
if input_option:
    president_name = input_word('president name', president_names)
else:
    president_name = 'bush'
# Speeches list
one_president_speeches = [presidents_speeches[name] for name in year_president_speech_names if president_name in name]
# Sentences list
one_president_sentences = [sentence for speech in one_president_speeches for sentence in speech]
# Words list
one_president_all_words = [word for sentence in one_president_sentences for word in sentence]
one_president_most_freq_words = Counter(one_president_all_words).most_common()
#------------------------------------------------------------- Most freq. terms
# 10 most frequently used words
print(president_name)
print(f'\n10 most frequently used terms:\n{president_name}\n{one_president_most_freq_words[:10]}')
print(f'\n3 most frequently used terms:\n{president_name}\n{one_president_most_freq_words[:3]}')
print(f'\n3 most frequently used terms no cosine dist:\n{president_name}\n{[word[0] for word in one_president_most_freq_words[0:3]]}')
#------------------------------------------------------------- The one president word embeddings model
one_president_word_embeddings = gensim.models.Word2Vec(one_president_sentences,
                                                       size=96, window=5, min_count=1, workers=2, sg=1)
# The one president vocabulary of terms:
# Removing duplicated words in one_president_all_words
one_president_vocabulary_of_terms = list(set(one_president_all_words))
#------------------------------------------------------------- Similar terms sample:
# Optional input function
if input_option:
    one_president_similar_to_word = input_word('similar word', one_president_vocabulary_of_terms)
else:
    one_president_similar_to_word = 'government'
# Calculate the cosine distance between word vectors outputting the 20 most similar words to the inputted word
one_president_similar_word_dist = one_president_word_embeddings.wv.most_similar(one_president_similar_to_word, topn=20)
# List of similar words and their vectors cosine distance relative to the inputted word
print(f'\nTerms similar: {president_name}\'s {one_president_similar_to_word}\n{one_president_similar_word_dist}')
print(f'\nTerms similar to no cosine dist. \n{president_name}\'s {one_president_similar_to_word} {[word[0] for word in one_president_similar_word_dist]}')
#------------------------------------------------------------- Presidents vocabularies DataFrame
#------------ Creates a president vocabularies DataFrame
df_presidents_vocabularies = pd.DataFrame(index=president_names)
# Speeches list
all_presidents_speeches = [[presidents_speeches[name] for name in year_president_speech_names if president in name] \
                           for president in president_names]
# Sentences list
all_presidents_sentences = [[sentence for speech in speeches for sentence in speech] \
                            for speeches in all_presidents_speeches]
# Words list
all_presidents_all_words = [[word for sentence in sentences for word in sentence] \
                            for sentences in all_presidents_sentences]
# Each president most three recurrent words
df_presidents_vocabularies['Three Most Recurrent Terms'] = [[word[0] for word in Counter(words).most_common()[:3]] \
                                                            for words in all_presidents_all_words]
# Each president most 10 recurrent words
df_presidents_vocabularies['Ten Most Recurrent Terms'] = [[word[0] for word in Counter(words).most_common()[:15]] \
                                                      for words in all_presidents_all_words]
# Each president vocabulary of terms
df_presidents_vocabularies['Terms List'] = [list(set(one_president_all_words)) \
                                       for presidents_all_words in all_presidents_all_words]
# Saves DataFrame
df_presidents_vocabularies.to_csv('data/presidents_vocabularies.csv')
print('\nPresident Vocabularies:')
print(df_presidents_vocabularies)

#------------------------------------------------------------------------------------ Selection of Presidents
#------------------------------------------------------------- Preprocessing the data:
# All words list
first_5_presidents_all_words = [word for words in all_presidents_all_words[:5] for word in words]
last_5_presidents_all_words = [word for words in all_presidents_all_words[len(all_presidents_all_words)-6:-1] \
                                                                                                       for word in words]
# Sentences list
first_5_presidents_sentences = [sentence for sentences in all_presidents_sentences[:5] for sentence in sentences]
last_5_presidents_sentences = [sentence for sentences in all_presidents_sentences[len(all_presidents_sentences)-6:-1] \
                                                                                                for sentence in sentences]
# Vocabulary of terms:
first_5_presidents_vocabulary = list(set(first_5_presidents_all_words))
last_5_presidents_vocabulary = list(set(last_5_presidents_all_words))
#------------------------------------------------------------- Most frequently used terms:
# First five presidents
first_5_presidents_most_freq_words = Counter(first_5_presidents_all_words).most_common()
# 10 first most frequently used words
print('\nFirst Five Presidents 10 most used terms:')
print(first_5_presidents_most_freq_words[:10])
# Last five presidents
last_5_presidents_most_freq_words = Counter(last_5_presidents_all_words).most_common()
# 10 first most frequently used words
print('\nLast Five Presidents 10 most used terms:')
print(last_5_presidents_most_freq_words[:10])
# 3 first most frequently used words
print('\nFirst Five Presidents 3 most used terms with count:')
print(first_5_presidents_most_freq_words[:3])
# 3 most frequently used words
print('\nLast Five Presidents 3 most used terms with count:')
print(last_5_presidents_most_freq_words[:3])
# 3 most frequently used words
print('\nFirst Five Presidents 3 most used terms:')
print([word[0] for word in first_5_presidents_most_freq_words[:3]])
print('\nLast Five Presidents 3 most used terms:')
print([word[0] for word in last_5_presidents_most_freq_words[:3]])
#-------------------------------------------------------------Word embeddings:
first_5_presidents_word_embeddings = gensim.models.Word2Vec(first_5_presidents_sentences,
                                                            size=96, window=5, min_count=1, workers=2, sg=1)
last_5_presidents_word_embeddings = gensim.models.Word2Vec(last_5_presidents_sentences,
                                                           size=96, window=5, min_count=1, workers=2, sg=1)
#---------- Similar words:
# Optional input function
if input_option:
    first_last_pre_voc = list(set(first_5_presidents_vocabulary + last_5_presidents_vocabulary))
    first_last_pre_similar_to_word = input_word('First and last four presidents word', first_last_pre_voc)
else:
    first_last_pre_similar_to_word = 'government'
# Calculate the cosine distance between word vectors outputting the 20 most similar words to the inputted word
first_5_pre_similar_word_dist = first_5_presidents_word_embeddings.wv.most_similar(first_last_pre_similar_to_word, topn=20)
last_5_pre_similar_word_dist = last_5_presidents_word_embeddings.wv.most_similar(first_last_pre_similar_to_word, topn=20)
# List of similar words and their vectors cosine distance relative to the inputted word
print(f'\nFirst five presidents terms similar to with cosine dist. {first_last_pre_similar_to_word}')
print(first_5_pre_similar_word_dist)
print(f'\nLast five presidents terms similar to with cosine dist. {first_last_pre_similar_to_word}')
print(last_5_pre_similar_word_dist)
print(f'\nFirst five presidents terms similar to {first_last_pre_similar_to_word}')
print([word[0] for word in first_5_pre_similar_word_dist])
print(f'\nLast five presidents terms similar to {first_last_pre_similar_to_word}')
print([word[0] for word in last_5_pre_similar_word_dist])