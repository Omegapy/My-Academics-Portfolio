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
# input_error.py                                                          #
# is the input error handling code section                           #
#                                                                         #
#-------------------------------------------------------------------------#

#
# -----------------------------------------
# ----------------- Libraries
# -----------------------------------------
# getch() for windows operating system
import msvcrt
#
# -----------------------------------------------------
#
# --------- Exceptions error handling function
#
# -----------------------------------------------------
#
# Checks if the User entered a no-numeric key or no-integer input
def check_num_error(key):
    try:
        key = int(key)
    except ValueError:
        return True
    # User entered a no-integer input
    return False


# -----------------------------------------------------
#
# --------- Question and Category Error handling
#
# -----------------------------------------------------
#
# ---------------------------------------
# ---------------- Error Messages
# ---------------------------------------
#
# ---- Question selection error message
#
def question_error_message():
    print('\n-------------------------------- Error')
    print(' Wrong entry\n')
    print('-------------------------------- Error')
    print('\n*************************\n Please choose a clues')
#
# ---- Category selection error message
#
def category_error_message():
    print('\n-------------------------------- Error')
    print(' Wrong entry\n')
    print('-------------------------------- Error')
    print('\n*************************\n Please choose a category')
#
# ----------------------------------------------
# ---------------- Input question error
# ----------------------------------------------
# Question value choice
def check_error_question(question_choice, questions):
    # Checks if a no-numeric key was pressed by user
    while check_num_error(question_choice):
        question_error_message()
        question_choice = msvcrt.getch()
    # From byte type to integer type
    question_choice = int(question_choice)
    # Checks if an invalid numeric key was pressed by user
    if question_choice == 0 or question_choice > len(questions):
        category_error_message()
        question_choice = msvcrt.getch()
        # Calls Back
        question_choice = check_error_question(question_choice, questions)
        # Checks if the select category questions have been already answered
    if questions['not_answered'][question_choice - 1] == False:
        print('--------------------------------------------------- Error')
        print('   The clue value -' + str(question_choice) + '- ' + \
              questions.Question[question_choice - 1])
        print('    has been already answered...')
        print('--------------------------------------------------- Error')
        print('   Please choose another clue value')
        print('---------------------------------------------------')
        question_choice = msvcrt.getch()  # getch returns a byte data type
        # Call back
        question_choice = check_error_question(question_choice, questions)
    # Returns question_choice as integer 0<>4
    return question_choice
#
# ----------------------------------------------
# ---------------- Input category error
# ----------------------------------------------
#
def check_error_cat(category_df, category_choice, round_cat_list):
    # Checks if a no-numeric key was pressed by user
    while check_num_error(category_choice):
        category_error_message()
        category_choice = msvcrt.getch()
    # From byte type to integer type
    category_choice = int(category_choice)
    # Checks if an invalid numeric key was pressed by user
    if category_choice == 0 or category_choice > len(round_cat_list):
        category_error_message()
        category_choice = msvcrt.getch()
        # Calls Back
        category_choice = check_error_cat(category_df, category_choice, round_cat_list)
        # Checks if the select category questions have been already answered
    if category_df['questions_not_answered'][category_choice - 1] == False:
        print('--------------------------------------------------- Error')
        print('   All the clues in ')
        print('   The category -' + str(category_choice) + '- ' + \
              category_df.Category[category_choice - 1])
        print('   have been answered...')
        print('--------------------------------------------------- Error')
        print('   Please choose another category')
        print('---------------------------------------------------')
        category_choice = msvcrt.getch()  # getch returns a byte data type
        # Calls back
        category_choice = check_error_cat(category_df, category_choice, round_cat_list)
    # Returns category_choice as integer 0<>4
    return category_choice
