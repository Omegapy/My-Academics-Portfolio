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
# display_lib.py                                                          #
# is the category and question display code section,                      #
# the game console output library functions                               #
# for the Jeopardy and Double Jeopardy Rounds                             #
#                                                                         #
#-------------------------------------------------------------------------#
#
# -----------------------------------------
# ----------------- Libraries
# -----------------------------------------
#
import re # regex
# Miscellaneous operating system interfaces
import os # os.system('cls') to wipe the console display
# getch() for windows operating system
import msvcrt
#
# ---------------------------------------
# ---------------- General Functions
# ---------------------------------------
#
# -------------------- Wipe the console screen clear
#
def wipe_screen():
    # Checks if the operating system is MS, and clear the console display
    os.system('cls' if os.name == 'nt' else 'clear')
#
# -------------------- Display score Function
#
def score_display(score):
    print()
    print(' Your winnings are $' + str(score))
#
# -------------------- Leaving game Function
#
def quit_game():
    print()
    print(''' 
*************************************************    
Are you sure that you want to quite Jeopardy?
Press Y for yes and N for No
*************************************************''')
    q_choice = msvcrt.getch()
    if q_choice.lower() == b'y':
        exit()
    elif q_choice.lower() == b'n':
        return
    else:
        print(' Please Press Y for Yes and N for No!')
        quit_game()
#
# ---------------------------------------------
# ---------------- Displays selected question
# ---------------------------------------------
#
# Displays the selected question, checks the user answer
# and returns the new score
def question_selected_display(question_row, score, cheat_mode):
    # question_row is 1 row DataFrame
    # we need to reset the question_row index, we want the row index = 0
    question_row = question_row.reset_index(drop=True)
    # Displays question and category
    print('***********************************************************')
    print('\n From Category: ' + str(list(question_row.Category)[0]))
    print('\n For a value of: $' + str(int(list(question_row.Value)[0])))
    print('\n Clue:\n ' + str(list(question_row.Question)[0]))
    print()
    score_display(score)
    print()
    if cheat_mode:
        print('************************************************************')
        print(' cheat mode is enabled...\n The right response is:')
        print(' ' + str(list(question_row.Answer)[0]))
    print('************************************************************\n')
    print('''
*********************     
Type your response 
*********************''')
    user_answer = input()
    # Compares the user answer with the right answer
    user_answer = user_answer.lower()
    answer = list(question_row.Answer)[0].lower()
    if re.search(answer, user_answer):
        score += question_row.Value[0]
        print('\n******************************************************************************')
        print('\n Right response :)\n Your winnings are now: $' + str(score))
        print('\n******************************************************************************\n')
        print('''
*******************************
  Press a key to continue 
*******************************''')
        msvcrt.getch()
    else:
        score -= question_row.Value[0]
        print('\n******************************************************************************')
        print('\n Wrong response :(\n Your winnings are now: $' + str(score))
        print('\n The right response was: ' + question_row.Answer[0])
        print('\n******************************************************************************\n')
        print('''
********************************
 Press a key to continue
********************************''')
        msvcrt.getch()
        # Returns the new score
    return score
#
# ----------------------------------------------
# ---------------- Displays questions Values
# ----------------------------------------------
#
# Displays the questions for the selected category,
# for both the Jeopardy and Double Jeopardy rounds and checks questions if answered
def question_values_display(questions_df, choice, score):
    # Creating a data Storing the rows for the selected category
    questions = questions_df.loc[questions_df.Category == choice]
    questions = questions.sort_values(by=['Category', 'Value']).reset_index(drop=True)
    # From a pd.Series type to an object list type to be used in a for loop
    questions_list = list(questions.Question)
    # Displays question and category
    print(
        '********************************************************************************************************\n')
    print(' From Category: ' + choice)
    print()
    i = 0  # Choice number
    for q in questions_list:
        i += 1
        # Checks if the question has been not-answered
        if questions['not_answered'][i - 1]:
            print('                              Type -' + str(i) + '- : $' + str(int(questions.Value[i - 1])))
    print(
        '\n********************************************************************************************************')
    score_display(score)
    # Returns the DataFrame questions rows for the selected category
    return questions
#
# ---------------------------------------------
# ---------------- Displays categories
# --------------------------------------------
#
# Displays the categories for both the Jeopardy and Double Jeopardy rounds
# and checks all questions if answered
def display_categories(df_cat, df_list):
    if any(df_cat['questions_not_answered']):
        i = 0  # Tracks choice numbers
        # displaying Categories
        print(
            '********************************************************************************************************\n')
        for category in df_list:
            i += 1
            # Checks if all the questions in a category haven been not-answered
            if df_cat['questions_not_answered'][i - 1]:
                print('                             Type -' + str(i) + '- for category: ' + category)
        print(
            '\n********************************************************************************************************')
        # Returns True if any of the questions in the category are not answered
        return True
    # Returns False if all of the questions in the category are answered
    return False