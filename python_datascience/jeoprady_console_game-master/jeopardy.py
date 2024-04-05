#-------------------------------------------------------------------------#
#                                                                         #
#             Codecademy Data Science course Python                       #
#             Data Analysis with the Pandas Library                       #
#                      "This Is Jeopardy!"                                #
#                                                                         #
#                       THE CONSOLE GAME                                  #
#                                                                         #
#-------------------------------------------------------------------------#
#                                                                         #
# jeopardy.py                                                             #
# is the game main code section                                           #
#                                                                         #
#-------------------------------------------------------------------------#
#
# -----------------------------------------
# ----------------- Libraries
# -----------------------------------------
#
import pandas as pd
import numpy as np
# getch() for windows operating system
import msvcrt
#
# -----------------------------------------
# ----------------- Imports game files
# -----------------------------------------
#
# Input errors handling functions
import input_error as ie
# Display functions
import display_lib as dl
# Final Jeopardy! Round functions
import final_jeopardy as fj
#
# ---------------------------------------
# ---------------- General Functions
# ---------------------------------------
#
# ------------------ End Game Functions
# End the game or replay
def end_game(score, round):
    if round != 'Final Jeopardy!':
        print('----------------------------------------------------------------------------\n')
        print('     Your winnings are $' + str(score) + '\n')
        print('     You have no winnings, you can not proceed to the next round... :(\n \n      \
        You reached the Round: ' + round)
    print('''
---------------------------------------------------------------------------

Do you want to play again?

----------------------------------------------------------------------------

Press Y for yes and N for No

----------------------------------------------------------------------------
                    ''')
    key = msvcrt.getch()
    if key.lower() == b'y':
        this_is_jeopardy()
    elif key.lower() == b'n':
        exit()
    else:
        print('--------------------- error\n wrong key.........')
        # Calls back
        end_game(score, round)
#
# -----------------------------------------------------
#
# ------------------- Tidying data section
#
# -----------------------------------------------------
#
# ----------------------Importing jeopardy data files
#
jeopardy = pd.read_csv("data/jeopardy.csv")
#
# -------------------------------------------------- Tidying the data
#
# Renaming the mis-formatted columns names
jeopardy = jeopardy.rename(columns=lambda column_name: column_name[1:] if column_name != 'Show Number' else column_name)
# Re-formatting rows with a NaN Answer value
jeopardy = jeopardy.fillna(value={'Answer' : 'Null'})
# Reformatting the column (Value) by removing ($) and (,) turning the data value into integers
jeopardy.Value = jeopardy['Value'].replace('[\$,]', '', regex=True)
# Replacing the (None) values with (0)
jeopardy.Value = jeopardy['Value'].replace('None', '0')
# Value column from string type to an integer type
jeopardy.Value = pd.to_numeric(jeopardy.Value)
# Removing Hyperlinks
jeopardy.Question = jeopardy['Question'].replace('(\(?<.*>\.?\)?)', '', regex=True)
# Removing spaces
jeopardy.Question = jeopardy['Question'].replace(r'^\s*$', np.nan, regex=True)
# Removing [video clue]
jeopardy.Question = jeopardy['Question'].replace(r'[\[video clue\]]', np.nan, regex=True)
#
# -----------------------------------------------------
#
# ------------------- Main Game function
#
# -----------------------------------------------------
#
def this_is_jeopardy():
    #
    # --------------------------
    # ----------- Variables
    # --------------------------
    #
    # ---- Settings variable
    #
    num_cat_jeopardy = 2
    num_question_jeopardy = 2
    num_cat_double_jeopardy = 2
    num_question_double_jeopardy = 2
    #
    # Winnings tracker
    score = 0
    #
    # -------------------------------------------
    # ----------- Game building data functions
    # ------------------------------------------
    #
    # ---- Lambda functions
    #
    # The lambda function is selecting data by a given category
    jeopardy_category = lambda x: x == category
    # The lambda function Not-selecting data by a given category
    not_jeopardy_category = lambda x: x != category
    #
    # ---- selecting rows from the game built DataFrame and check if they are duplicated
    #
    def sample_dupl(df, num):
        series_d = df.sample(n=num) # pd.Series
        # Checks for duplicates
        series_duplicates = series_d.duplicated()
        if series_duplicates.any():
            sample_dupl(df, num)
        return series_d
    #
    # -------------------------------------------
    # ----------- Settings option
    # ------------------------------------------
    #
    # ---- User settings input, input errors check and returns integer 0<>4
    #
    def num_settings():
        num = msvcrt.getch()
        print('\n You entered: ' + num.decode('utf-8'))
        print()
        # Checks if a no-numeric key was pressed by user
        while ie.check_num_error(num):
            print('\n-------------------------------- Error')
            print(' Wrong entry\n')
            print('-------------------------------- Error')
            print('\n*************************\n Please a number between 1 and 4')
            num = msvcrt.getch()
            print(' You entered: ' + num.decode('utf-8'))
            print()
        # From byte type to integer type
        num = int(num)
        # Checks if an invalid numeric key was pressed by user
        if num == 0 or num > 4:
            print('\n-------------------------------- Error')
            print(' Wrong entry\n')
            print('-------------------------------- Error')
            print('\n*************************\n Please enter a number between 1 and 4')
            # Calls Back
            num = num_settings()
        # Returns the number as integer 0<>4
        return num
    #
    # ------------------ Main setting option function
    # The user can change the numbers of categories and questions per category
    def settings_option():
        # Stores user numbers choices
        num_list = [2, 2, 2, 2, 2]
        print('''
******************************************************************* 
* Enter the number of categories for the Jeopardy! Round, up to 4 *
*******************************************************************''')
        num_list[0] = num_settings()
        #
        print('''
*****************************************************************************
* Enter the number of clues per categories for the Jeopardy! Round, up to 4 *
*****************************************************************************''')
        num_list[1] = num_settings()
        #
        print('''
**************************************************************************
* Enter the number of categories for the Double Jeopardy! Round, up to 4 *
**************************************************************************''')
        num_list[2] = num_settings()
        #
        print('''
************************************************************************************
* Enter the number of clues per categories for the Double Jeopardy! Round, up to 4 *
************************************************************************************''')
        num_list[3] = num_settings()
        #
        print('''                                                 
***************************
* Press a key to continue *
***************************''')
        msvcrt.getch()
        # Returns the numbers list
        return num_list
    #
    # ----------------------------
    # ----------- Cheat mode
    # ---------------------------
    #
    def cheat_mode_on():
        # Cheat mode tracker
        cheat_mode = False
        print(''' 
                                                                                                **************************************************************
                                                                                                
                                                                                                    Do you want enable cheat mode?
 
                                                                                                    In cheat mode,
                                                                                                    the answers to the clues will be displayed on the screen
 
                                                                                                **************************************************************

                                                                                                         Press Y for yes and N for No

                                                                                                **************************************************************''')
        key = msvcrt.getch()
        if key.lower() == b'y':
            cheat_mode = True
            return cheat_mode
        elif key.lower() == b'n':
            return cheat_mode
        # User enter an invalid input
        else:
            print('--------------------- error\n wrong key.........')
            # calls back
            cheat_mode_on()
    #
    # ------------------------------------
    # ----------- Description option
    # ------------------------------------
    #
    # ---- Displays the game play description
    #
    def game_play_description():
        print()
        print('''
                                                                    ******************************************************************************************************************
                                                                    **                                                                                                              **
                                                                    **   "This is Jeopardy"                                                                                         **                                                          
                                                                    **                                                                                                              **    
                                                                    **     The game play consists of a clue quiz comprising of 3 rounds.                                            **
                                                                    **                                                                                                              **
                                                                    **     The clues in the quiz are presented as "answers",                                                        **
                                                                    **     and responses must be phrased in the form of a question.                                                 **
                                                                    **                                                                                                              **
                                                                    **                                                                                                              **
                                                                    ******************************************************************************************************************

                                                                    ******************************************************************************************************************
                                                                    **                                                                                                              **
                                                                    **      Round-1 Jeopardy!                                                                                       **
                                                                    **                                                                                                              **
                                                                    **                2 Categories                                                                                  **
                                                                    **                2 Clues per Category                                                                          **
                                                                    **                                                                                                              **
                                                                    **                Note:                                                                                         **
                                                                    **                 To move to round-2, all the clues in all the categories have to be answered                  **
                                                                    **                 and your winnings can not be $0 or less.                                                      **
                                                                    **                                                                                                              **
                                                                    **                 The number of categories and clues per category,                                             **
                                                                    **                 can be changed by entering the game settings option.                                         **
                                                                    **                                                                                                              **
                                                                    ******************************************************************************************************************                                                           
                ''')
        print('''
                                                                    *******************************
                                                                     Press a key to continue
                                                                    *******************************''')
        msvcrt.getch()
        print('''
                                                                    ******************************************************************************************************************
                                                                    **                                                                                                              **
                                                                    **      Round-2 Double Jeopardy!                                                                                **
                                                                    **                                                                                                              **
                                                                    **                The clues values are double                                                                   **
                                                                    **                                                                                                              **
                                                                    **                2 Categories                                                                                  **
                                                                    **                2 Clues per Category                                                                          **
                                                                    **                                                                                                              **
                                                                    **                Note:                                                                                         **
                                                                    **                 To move to round-3, all the clues in all the categories have to be answered                  **
                                                                    **                 and your winnings can not be $0 or less                                                      **
                                                                    **                                                                                                              **
                                                                    **                 The number of categories and clues per category,                                             **
                                                                    **                 can be changed by entering the game settings option.                                         **
                                                                    **                                                                                                              **
                                                                    **                                                                                                              **
                                                                    ******************************************************************************************************************                                                           
                    ''')
        print('''
                                                                    *******************************
                                                                     Press a key to continue
                                                                    *******************************''')
        msvcrt.getch()
        print('''
                                                                    ******************************************************************************************************************
                                                                    **                                                                                                              **
                                                                    **      Round-3 Final Jeopardy!                                                                                 **
                                                                    **                                                                                                              **
                                                                    **                Has a single Clue                                                                             **
                                                                    **                                                                                                              **
                                                                    **                In this round you need to make a wager.                                                       **
                                                                    **                The wager amount can be equal to your winnings amount or less, but not equal to 0,            **
                                                                    **                and it has to be a whole number.                                                              **
                                                                    **                                                                                                              **
                                                                    ******************************************************************************************************************                                                           
                        ''')
        print('''
                                                                    *******************************
                                                                        Press a key to continue
                                                                    *******************************''')
        msvcrt.getch()
        # Wipe console display
        dl.wipe_screen()
    #
    # ------------------------------------------------------
    #
    # ------------------ Main Game DataFrame
    #
    # ------------------------------------------------------
    #
    # ---- Tidying the data to meet the game needs
    #
    # Selecting only the needed columns
    df_jeopardy_game = jeopardy.loc[:, ['Category', 'Value', 'Question', 'Answer']]
    # Reformatting Question values made of only spaces with the value NaN
    df_jeopardy_game.Question = df_jeopardy_game.Question.replace(r'^\s*$', np.nan, regex=True)
    # Reformatting Question values of [video clue] with the value NaN
    df_jeopardy_game.Question = df_jeopardy_game.Question.replace(r'[\[video clue\]]', np.nan, regex=True)
    # Removing parenthesis from the Answer column values
    df_jeopardy_game.Answer = df_jeopardy_game.Answer.replace(r'\(|\)', '', regex=True)
    # Removing rows with the category VWLLSS FRT
    df_jeopardy_game = df_jeopardy_game.loc[jeopardy.Category != 'VWLLSS FRT']
    # Removing rows with the category VWLLSS FLWRS
    df_jeopardy_game = df_jeopardy_game.loc[jeopardy.Category != 'VWLLSS FLWRS']
    # Removing rows with the category VWLLSS VGTBLS
    df_jeopardy_game = df_jeopardy_game.loc[jeopardy.Category != 'VWLLSS VGTBLS']
    # Removing rows with the category VWLLSS CNTRS
    df_jeopardy_game = df_jeopardy_game.loc[jeopardy.Category != 'VWLLSS CNTRS']
    # Removing empty questions with a values NaN
    df_jeopardy_game = df_jeopardy_game.loc[df_jeopardy_game.Question.notna()].reset_index(drop=True)
    #
    # ---- Removing categories with less than 4 questions
    #
    # Creating a category DataFrame with the number of unique questions per category
    category_q_count = df_jeopardy_game.Category.value_counts()
    category_q_count = category_q_count.reset_index() # pd.DataFrame type
    # Renaming columns, index named column can create issues
    category_q_count = category_q_count.rename(columns = {"index" : "category", "Category" : "num_of_questions"})
    # Categories with 3 or less of questions
    category_3q_count = category_q_count.loc[category_q_count.num_of_questions <= 3, 'category'] # pd.Series type
    # From a pd.Series type to an object list type
    category_3q_count = list(category_3q_count)
    # Removing categories with 3 or less questions
    for category in category_3q_count:
        df_jeopardy_game = df_jeopardy_game.loc[df_jeopardy_game.Category.apply(not_jeopardy_category)]
    #
    # ------------------------------------------------------
    #
    # ------------------- Game play Functions
    #
    # ------------------------------------------------------
    #
    # -------------------------------------------------
    # ----------- Selected question display mode
    # For the Jeopardy! and Double Jeopardy! rounds
    # -------------------------------------------------
    #
    def question_selected_display_mode(question_choice, round_cat, round_cat_list, questions_round, round, score, cheat_mode):
        # Wipe console display
        dl.wipe_screen()
        # Question selected banner
        print('\n                                                                                                         **********************************************')
        print('                                                                                                             You are in the ' + round + ' round')
        print('                                                                                                         **********************************************')
        print('''
                                                                                  *********************************************************************************
                                                                                  **                                                                             ** 
                                                                                  **                            ----- CLUE -----                                 **
                                                                                  **                                                                             ** 
                                                                                  *********************************************************************************''')
        print()
        # Displays the selected question, checks the user answer
        # and returns the new score
        score = dl.question_selected_display(question_choice, score, cheat_mode)
        # Redirect to round mode
        round_mode(round_cat, round_cat_list, questions_round, round, score, cheat_mode)
        #
        # -------------------------------------------------
        # ----------- User question value select mode
        # For the Jeopardy! and Double Jeopardy! rounds
        # -------------------------------------------------
        #
    def question_value_select_mode(questions, round_cat, round_cat_list, questions_round, round, score, cheat_mode):
        # User selects question
        print()
        print('''
*************************
Choose a clue value!
Or press Q to quit.
*************************''')
        # User input
        value_choice = msvcrt.getch()  # getch returns a byte data type
        # b'q', the b stands for byte
        if value_choice.lower() == b'q':
            # Quite?
            dl.quit_game()
            # user replied no to leave the game
            print('\n*************************\n\n Please choose a clues value')
            value_choice = msvcrt.getch()
            # Checks for user invalid key inputs
        value_choice = ie.check_error_question(value_choice, questions)
        # Sets question as answered
        questions.loc[[value_choice - 1], 'not_answered'] = False
        questions_round.loc[questions_round['Question'] == questions.Question[value_choice - 1], \
                         'not_answered'] = False
        # Checks if all the questions in the category have been answered
        if any(questions['not_answered']) == False:
            # Sets all question in category to answered
            round_cat.loc[round_cat['Category'] == questions.Category[value_choice - 1], \
                            'questions_not_answered'] = False
        # Returns the row of the selected question
        question_choice = questions.loc[[value_choice - 1]]
        # Redirects to the question display mode
        question_selected_display_mode(question_choice, round_cat, round_cat_list, questions_round, round, score, cheat_mode)
        #
        # -------------------------------------------------
        # ----------- Questions values display mode
        # For the Jeopardy! and Double Jeopardy! rounds
        # -------------------------------------------------
        #
    def questions_values_display_mode(cat_selection, round_cat, round_cat_list, questions_round, round, score, cheat_mode):
        # Wipe console display
        dl.wipe_screen()
        # Questions values display banner
        print('\n                                                                                                         **********************************************')
        print('                                                                                                              You are in the ' + round + ' round')
        print('                                                                                                         **********************************************')
        if round == 'Jeopardy!':
            print('''
                                                                            *********************************************************************************
                                                                            **                                                                             ** 
                                                                            **                        ----- CHOOSE A CLUE VALUE -----                      **
                                                                            **                                                                             ** 
                                                                            *********************************************************************************''')
        else:
            print('''
                                                                           *********************************************************************************
                                                                           **                                                                             ** 
                                                                           **                        ----- CHOOSE A CLUE VALUE -----                      **
                                                                           **  The clue values are Doubled                                                ** 
                                                                           *********************************************************************************''')
        print()
        # Displays the questions for the selected category checks if the question was already answered
        # and returns the questions DataFrame of the selected category
        questions = dl.question_values_display(questions_round, cat_selection, score)
        # Redirects to the user questions selection mode
        question_value_select_mode(questions, round_cat, round_cat_list, questions_round, round, score, cheat_mode)
        #
        # -------------------------------------------------
        # ----------- User category select mode
        # For the Jeopardy! and Double Jeopardy! rounds
        # -------------------------------------------------
        #
    def cat_select_mode(round_cat, round_cat_list, questions_round, round, score, cheat_mode):
        # User selects Category
        print()
        print('''
*************************
 Choose a category!
 Or press Q to quit.
*************************''')
        # User input
        category_choice = msvcrt.getch()  # getch returns a byte data type
        # b'q', the b stands for byte
        if category_choice.lower() == b'q':
            # Quite?
            dl.quit_game()
            # user replied no to leave the game
            print('\n*************************\n\n Please choose a category')
            category_choice = msvcrt.getch()
        # Checks for user invalid key inputs
        category_choice = ie.check_error_cat(round_cat, category_choice, round_cat_list)
        # Returns the selected category
        cat_selection = (round_cat.Category[category_choice - 1])
        # Redirects to the question values menu for selected category
        questions_values_display_mode(cat_selection , round_cat, round_cat_list, questions_round, round, score, cheat_mode)
        #
        # -------------------------------------------------
        # ----------- Rounds Start and End mode
        # It also display categories
        # For the Jeopardy! and Double Jeopardy! rounds
        # -------------------------------------------------
        #
    def round_mode(round_cat, round_cat_list, questions_round, round, score, cheat_mode):
        # Wipe console display
        dl.wipe_screen()
        # Category display banner
        print('\n                                                                                                         **********************************************')
        print('                                                                                                             You are in the ' + round + ' round')
        print('                                                                                                         **********************************************')
        print('''
                                                                                *********************************************************************************
                                                                                **                                                                             ** 
                                                                                **                         ----- CHOOSE A CATEGORY -----                       **
                                                                                **                                                                             ** 
                                                                                *********************************************************************************''')
        print('\n')
        # Displays the categories,
        # and return True if all the questions in all the categories haven been not-answered
        if dl.display_categories(round_cat, round_cat_list):
            dl.score_display(score)
            # Redirects to the user category selection function
            cat_select_mode(round_cat, round_cat_list, questions_round, round, score, cheat_mode)
        #
        print('''
                                                                                            ******************************************************************

                                                                                                All the clues in all the categories have been answered.
  
                                                                                            ******************************************************************

                                                                                                                Press any key to continue

                                                                                            ******************************************************************''')
        msvcrt.getch()
        # Checks score if to proceed to the next round
        if score < 1:
            end_game(score, round)
        # Next double Jeopardy Round
        elif round == 'Jeopardy!':
            round_mode(double_jeopardy_cat, double_jeopardy_cat_list, questions_double_jeopardy, 'Double Jeopardy!', score, cheat_mode)
        else:
            # Next Final Jeopardy Round
            fj.final_jeopardy_round(final_jeopardy, score, cheat_mode)
            # Game ends
            end_game(score, 'Final Jeopardy!')
    #
    # ------------------------------------------------------
    #
    # ------------------- Game initialization
    #
    # ------------------------------------------------------
    #
    # ------------------------------------
    # -----------Welcome banner
    # ------------------------------------
    #
    # Wipe console display
    dl.wipe_screen()
    #
    print('''
                                                                ********************************************************************************************************************
                                                                ********************************************************************************************************************
                                                                ***                                                                                                              ***
                                                                ***                                         WELCOME TO THIS IS JEOPARDY!                                         ***
                                                                ***                                                                                                              ***
                                                                ********************************************************************************************************************
                                                                ********************************************************************************************************************
                
                                                                                             *********************************************************
        
                                                                                                    Press D for the game play description 
                                                                                                    or any other key to continue
 
                                                                                             *********************************************************''')
    #
    # ----------------------------------------
    # ----------- Enter Description option?
    # ----------------------------------------
    #
    # Checks for user choice and redirects if need it
    desp = msvcrt.getch()
    if desp.lower() == b'd': game_play_description()
    #
    # ----------------------------------------
    # ----------- Enter Cheat mode?
    # ----------------------------------------
    cheat_mode = cheat_mode_on()
    #
    # ----------------------------------------
    # ----------- Enter Setting mode?
    # ----------------------------------------
    #
    print(''' 
                                                                                                ********************************************************* 

                                                                                                    Do you want enter settings option?
 
                                                                                                    In the settings mode,
                                                                                                    you can change 
                                                                                                    the number of categories and clues per category
 
                                                                                                *********************************************************

                                                                                                    Press Y for yes or any another key to continue

                                                                                                *********************************************************''')
    key = msvcrt.getch()
    #
    if key.lower() == b'y':
        num_list = settings_option()
        num_cat_jeopardy = num_list[0]
        num_question_jeopardy = num_list[1]
        num_cat_double_jeopardy = num_list[2]
        num_question_double_jeopardy = num_list[3]
    #
    # -------------------------------------------
    #
    # -----------Game data initialization
    #
    # -------------------------------------------
    #
    # ----------------------------------------
    # ----------- Categories initialization
    # ----------------------------------------
    #
    # ------ Final Jeopardy! Round-3
    #
    # Randomly selecting a category/question
    final_jeopardy = df_jeopardy_game.sample(n=1).reset_index(drop=True)  # pd.Series Type
    final_jeopardy.cat = str(list(final_jeopardy.Category))
    #
    # ------ Double Jeopardy! Round-2
    #
    # Creating a jeopardy_game DataFrame without the category from round-3
    double_jeopardy_game = df_jeopardy_game.loc[df_jeopardy_game.Category != final_jeopardy.cat]
    # Sorting the Double Jeopardy round DataFrame by Category and value columns
    double_jeopardy_game = double_jeopardy_game.sort_values(by=['Category', 'Value']).reset_index(drop=True)
    # Randomly selecting categories and check for duplicates
    double_jeopardy_cat = sample_dupl(double_jeopardy_game.Category, num_cat_double_jeopardy)  # pd.Series Type
    # From a pd.Series type to an object list type to be used in a for loop
    double_jeopardy_cat_list = list(double_jeopardy_cat)  # list type
    # double_jeopardy_cat to pd.DataFrame type
    # (note: using reset_index(drop=True) will keep double_jeopardy_cat as a pd.Series)
    double_jeopardy_cat = double_jeopardy_cat.reset_index()
    # Adding a Boolean column to track if all the question in a category have been answered
    double_jeopardy_cat['questions_not_answered'] = True
    #
    # ------ Jeopardy! Round-1
    #
    # Creating a jeopardy_game DataFrame without the categories from round-3 and 4
    jeopardy_game = pd.DataFrame()
    for category in double_jeopardy_cat_list:
        jeopardy_game = double_jeopardy_game.loc[double_jeopardy_game.Category.apply(not_jeopardy_category)]
    # Sorting the Jeopardy round DataFrame by Category and value columns
    jeopardy_game = jeopardy_game.sort_values(by=['Category', 'Value']).reset_index(drop=True)
    # Randomly selects categories and checks for duplicated
    jeopardy_cat = sample_dupl(jeopardy_game.Category, num_cat_jeopardy)  # pd.Series Type
    # From a pd.Series type to an object list type to be used in a for loop
    jeopardy_cat_list = list(jeopardy_cat)  # list type
    # jeopardy_cat to pd.DataFrame type
    # (note: using reset_index(drop=True) will keep jeopardy_cat as a pd.Series)
    jeopardy_cat = jeopardy_cat.reset_index()  # pd.DataFrame type
    # Adding a Boolean column to track if all the question in a category have been answered
    jeopardy_cat['questions_not_answered'] = True
    #
    # ---------------------------------------------------------
    # ----------- Questions for each category initialization
    # ---------------------------------------------------------
    #
    # ------ Double Jeopardy! Round-2
    #
    # Creates a jeopardy_game DataFrame containing
    # all the randomly selected Double Jeopardy rows questions
    questions_double_jeopardy = pd.DataFrame()
    for category in double_jeopardy_cat_list:
        # DataFrame storing all the rows for the randomly selected categories
        double_jeopardy_cat_rows = double_jeopardy_game.loc[double_jeopardy_game.Category.apply(jeopardy_category)]  # pd.DataFrame type
        # Randomly selects rows (question) for each randomly selected categories and checks for duplicated
        double_jeopardy_rows = sample_dupl(double_jeopardy_cat_rows, num_question_double_jeopardy)  # pd.Series Type
        # DataFrame storing the randomly selected rows (question) for each randomly selected categories
        questions_double_jeopardy = questions_double_jeopardy.append(double_jeopardy_rows, ignore_index=True)
    # Adding the not-answered column and set to true
    questions_double_jeopardy['not_answered'] = True
    # In the Double Jeopardy round the question values are Doubled
    questions_double_jeopardy.Value = questions_double_jeopardy.Value.apply(lambda x: x * 2)
    # Sorting the Double Jeopardy round DataFrame by Category and value columns
    questions_double_jeopardy = questions_double_jeopardy.sort_values(by=['Category', 'Value']).reset_index(
        drop=True)
    #
    # ------ Jeopardy! Round-1
    #
    # Creates a jeopardy_game DataFrame containing
    # all the randomly selected jeopardy rows questions
    questions_jeopardy = pd.DataFrame()
    questions_jeopardy.name = 'questions_jeopardy'
    for category in jeopardy_cat_list:
        # DataFrame storing all the rows for the randomly selected categories
        jeopardy_cat_rows = jeopardy_game.loc[jeopardy_game.Category.apply(jeopardy_category)]
        # Randomly selects rows (question) for each randomly selected categories and checks for duplicated
        jeopardy_rows = sample_dupl(jeopardy_cat_rows, num_question_jeopardy)  # pd.Series Type
        # DataFrame storing the randomly selected rows (question) for each randomly selected categories
        questions_jeopardy = questions_jeopardy.append(jeopardy_rows, ignore_index=True)
    # Adding the Not-answered column and set to true
    questions_jeopardy['not_answered'] = True
    # Sorting the Double Jeopardy round DataFrame by Category and value columns
    questions_jeopardy = questions_jeopardy.sort_values(by=['Category', 'Value']).reset_index(drop=True)
    #
    # -----------------------------
    # ----------- Rounds launch
    # -----------------------------
    #
    # ---- Jeopardy round
    round_mode(jeopardy_cat, jeopardy_cat_list, questions_jeopardy, 'Jeopardy!', score, cheat_mode)
#
# ------------------------------------------------------
#                   Launch the game
# ------------------------------------------------------
#
this_is_jeopardy()

