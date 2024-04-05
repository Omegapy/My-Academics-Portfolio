#-------------------------------------------------------------------------#
#                                                                         #
#             Codecademy Data Science course Python                       #
#                    Data Analysis with Pandas                            #
#                   "This Is Jeopardy!" Tasks                           #
#                                                                         #
#--------------------------------------------------------------------------

#------------------------------------------#
#               Libraries                  #
#------------------------------------------#
import re # regex
import pandas as pd


# display on the console
pd.set_option('display.width', 400)
pd.options.display.max_colwidth = 120 # Allows to fully read most jeopardy.Question columns values
pd.set_option('display.max_columns', 20)
pd.set_option('display.max_rows', 50)

# ---------------------------------------------------------------------------#
# 2. We’ve provided a csv file containing data about the game show Jeopardy! #
# in a file named jeopardy.csv.                                              #
# Load the data into a DataFrame and investigate its contents.               #
# ---------------------------------------------------------------------------#

# The print() functions make the console outputs easier to read
print()
print('----------------------------------------------------------------------------------------------------------------')
print("                                             ------ Task.2 -------")
print('----------------------------------------------------------------------------------------------------------------')
print()
print('------------------------------------ Table ---------------------------------------------------------------------')
print()
# Importing jeopardy data files
jeopardy = pd.read_csv("data/jeopardy.csv")
# Inspecting the first 5 row of the DataFrame jeopardy
print(jeopardy.head())
print()
print('------------------------------------ Data Type -----------------------------------------------------------------')
print()
# Finding what is wrong with the columns names
print(jeopardy.dtypes)
print()
print('------------------------------------ Data type Formatted Columns Names -----------------------------------------')
print()
# Renaming the misformatted columns names
jeopardy = jeopardy.rename(columns=lambda column_name: column_name[1:] if column_name != 'Show Number' else column_name)
print(jeopardy.dtypes)
print()
print('------------------------------------ Table Info ----------------------------------------------------------------')
print()
# Finding more (info) from the database jeopardy
print(jeopardy.info())
print()
print('------------------------------------ NaN Answers meat to be the Null answer ------------------------------------')
print()
# Rows with a NaN Answer value
print(jeopardy[jeopardy.Answer.isna()])
print()
print('------------------------------------ Reformatted NaN rows ')
print()
# Reformmatting rows with a NaN Answer value
jeopardy = jeopardy.fillna(value={'Answer' : 'Null'})
# Checking the Reformmatting rows with a NaN Answer value
print(jeopardy.loc[[143297]])
print()
print('------------------------------------ Value Column --------------------------------------------------------------')
print()
# Inspecting the (value) column
print(pd.Series(jeopardy['Value'].unique()))
print()
print('------------------------------------ Reformatted Value Column values ------------------------------------------')
print()
# Reformatting the column (Value) by removing ($) and (,) turning the data value into integers
jeopardy.Value = jeopardy['Value'].replace('[\$,]', '', regex=True)
# Checking the reformatting the column (Value) results
print(pd.Series(jeopardy['Value'].unique()))
print()
print('------------------------------------ Reformatted Value Column values (none) -----------------------------------')
print()
# Replacing the (None) values with (0),
# the None values were inputted when players placed wagers during a Tiebreaker a Final Jeopardy round
jeopardy.Value = jeopardy['Value'].replace('None', '0')
print(jeopardy.Value.loc[[55]])
print()
print()
print('------------------------------------ Converted Value Column data type to int64 ---------------------------------')
print()
jeopardy.Value = pd.to_numeric(jeopardy.Value)
print(jeopardy.Value.dtypes)
print()
print('------------------------------------ Air Date Column -----------------------------------------------------------')
print()
# Inspecting the (value) column
print(jeopardy['Air Date'].head())
print()
print('------------------------------------ Reformatted Air Date data type  ------------------------------------------')
print()
print()
jeopardy['Air Date'] = pd.to_datetime(jeopardy['Air Date'])
print(jeopardy['Air Date'].head())
print()
print('------------------------------------ Numbers of categories -----------------------------------------------------')
print()
print(len(jeopardy['Category'].unique()))
print()
print('------------------------------------ Numbers of questions ------------------------------------------------------')
print()
print(len(jeopardy['Question'].unique()))
print()
print('------------------------------------ Reformatted question column with <a > values -----------------------------')
print()
print(jeopardy.loc[[51115]])
# Removing Hyperlinks
jeopardy.Question = jeopardy['Question'].replace('(\(?<.*>\.?\)?)', '', regex=True)
print()
print(jeopardy.loc[[51115]])
print()
print('------------------------------------ list of Rounds   ----------------------------------------------------------')
print()
print(jeopardy['Round'].unique())

#------------------------------------------------------------#
# 3. Write a function that filters the dataset for questions #
# that contains all of the words in a list of words.         #
#------------------------------------------------------------#
print()
print('----------------------------------------------------------------------------------------------------------------')
print("                                             ------ Task.3 -------")
print('----------------------------------------------------------------------------------------------------------------')
print()
# Function that filters the data set for questions containing all the words in a list
def filter_questions_data(df, words):
    # Function that filters the word list for a question
    def filter_word_list(question, words):
        words_in_question = True # Boolean to check if all the words are in the question
        question = question.lower()
        for word in words: # loops through the word list
            if (word.lower() in question) == False: # Check if the word is in the question
                words_in_question = False
        return words_in_question
    # The lambda function filters the dataset using the filter_word_list function
    filter_datset = lambda x: filter_word_list(x, words)
    # df.loc returns the dataframe rows where the questions are located
    return df.loc[df['Question'].apply(filter_datset)]

filter_questions_df = filter_questions_data(jeopardy, ["kinG", "England"])
print(filter_questions_df)
print()
print(filter_questions_df.Question.loc[[86353]])
print()
print(filter_questions_df.Question.loc[[129106]])

#-------------------------------------------------------------------#
# 4. Test your original function with a few different sets of words #
# to try to find some ways your function breaks.                    #
#-------------------------------------------------------------------#
print()
print('----------------------------------------------------------------------------------------------------------------')
print("                                             ------ Task.4 -------")
print('----------------------------------------------------------------------------------------------------------------')
print()
# Function that filters the dataset for questions containing all the words in a list
def regex_filter_questions_data(df, words):
    # Function that filters the word list for a question
    def filter_word_list(question, words):
        words_in_question = True # Boolean to check if all the words are in the question
        question = question.lower()
        for word in words: # loops through the word list
            word = word.lower()
            word = re.compile(r'(\A|\s|\'|\"|\( re.IGNORECASE)' + word + r"([,]|\.|\'|\"|\)|s|\s|\Z|\W, re.IGNORECASE)")
            if re.search(word, question) == None: # Check if the word is in the question
                words_in_question = False # Set the boolean to False if word is not in question
        return words_in_question
    # The lambda function filters the dataset using the filter_word_list function
    filter_datset = lambda question: filter_word_list(question, words)
    # df.loc returns the dataframe rows where the questions are located
    return df[df['Question'].apply(filter_datset)]

print(regex_filter_questions_data(jeopardy, ["king", "England"]))
print()
print('---------------------------- Checking if the Function check for the words and not the strings -------------------')
print()
print(filter_questions_df.Question.loc[[86353]]) # Has the word england and taking
regex_filter_questions_df = regex_filter_questions_data(jeopardy, ["King", "England"])
print(filter_questions_df.Question.loc[[86353]].isin(regex_filter_questions_df['Question'])) # output false
print()
print('---------------------------- Checking function with length = 1 word list ---------------------------------------')
print()
print(regex_filter_questions_data(jeopardy, ["weed"]))
print()
print('---------------------------- Checking function with length = 3 words list --------------------------------------')
print()
print(regex_filter_questions_data(jeopardy, ["weed", "CrEw", "great"]))


#-------------------------------------------------------------#
# 5. Convert the " Value" column to floats. If you’d like to, #
# you can create a new column with the float values.          #
#-------------------------------------------------------------#
print()
print('----------------------------------------------------------------------------------------------------------------')
print("                                             ------ Task.5 -------")
print('----------------------------------------------------------------------------------------------------------------')
print()
jeopardy.Value = pd.to_numeric(jeopardy.Value, downcast='float')
print()
print('--------- Value column data type---------------------')
print()
print(jeopardy.Value.dtypes)
print()
print('------------------------------------ average value of questions that contain the word "King" -------------------')
print()
filter_questions_king = regex_filter_questions_data(jeopardy, ["King"])
print(filter_questions_king.Value.mean())

#-------------------------------------------------------------------#
# 6. Write a function that returns the count of the unique answers  #
# to all of the questions in a dataset.                             #
#-------------------------------------------------------------------#
print()
print('----------------------------------------------------------------------------------------------------------------')
print("                                             ------ Task.6 -------")
print('----------------------------------------------------------------------------------------------------------------')
print()
def get_answers(word_list):
    df = regex_filter_questions_data(jeopardy, word_list)
    return df.Answer.value_counts()
#
print(get_answers(['King']))

#-------------------------------------------------------------------#
# 7. Explore from here!                                             #
#-------------------------------------------------------------------#
print()
print('----------------------------------------------------------------------------------------------------------------')
print("                                             ------ Task.7 -------")
print('----------------------------------------------------------------------------------------------------------------')
print()
print('------------------------------------ How many questions from the 90s -------------------------------------------')
print()
# How many questions from the 90s use the word "Computer" compared to questions from the 2000s?
filter_questions_pc = regex_filter_questions_data(jeopardy, ["Computer"])

# Number of questions per decade
# 1990s
pc_1990_questions = filter_questions_pc.\
    loc[(filter_questions_pc['Air Date'] >= '01-01-1990') & (filter_questions_pc['Air Date'] <= '12-31-1999')]

num_pc_1990_unique_questions = len(pc_1990_questions.Question.unique())
# 2000s
pc_2000_questions = filter_questions_pc.\
  loc[(filter_questions_pc['Air Date'] >= '01-01-2000') & (filter_questions_pc['Air Date'] <= '12-31-2009')]

num_pc_2000_unique_questions = len(pc_2000_questions.Question.unique())
# Data Frame storing the number of question with the word (computer) in it
num_pc_questions = pd.DataFrame(
    { 'Decade': ['1990s', '2000s'],
      'Numbers of Question':[num_pc_1990_unique_questions, num_pc_2000_unique_questions]
     })

print(num_pc_questions)

print()
print('------------------------------------ Is there a connection between the Round and the Category ------------------')
print()
# Creating a Data Frame with Round and Category
round_category_value = jeopardy.groupby(['Round', 'Category']).Value.mean().reset_index()
# Category as rows and Round as columns number of questions per Round/Category as values
round_category = round_category_value.pivot(
    index='Category',
    columns='Round',
    values='Value'
).reset_index()
# Reordering the columns
round_category = round_category[['Category', 'Tiebreaker', 'Final Jeopardy!', 'Double Jeopardy!', 'Jeopardy!']]
# Output
print(round_category)
print()
# removing the the DatFrame name (Round)
round_category.columns.name = ""
# Looking if a Category is used is all 4 rounds
print()
print(round_category.loc[(round_category['Final Jeopardy!'].notna()) & \
                         (round_category['Double Jeopardy!']).notna() & \
                         (round_category['Jeopardy!']).notna() & \
                         (round_category['Tiebreaker']).notna()])