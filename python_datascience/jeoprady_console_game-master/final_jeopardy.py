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
# final_jeopardy.py                                                       #
# is the code section running the Final Jeopardy Round                    #
#                                                                         #
#-------------------------------------------------------------------------#
#
# -----------------------------------------
# ----------------- Libraries
# -----------------------------------------
#
import re # regex
import msvcrt # getch()
#
# -----------------------------------------
# ----------------- Imports game files
# -----------------------------------------
#
# Input errors handling functions
import input_error as ie
# Display function file
import display_lib as dl
#
# ---------------------------------------
# ---------------- General Functions
# ---------------------------------------
#
# ------------ Final wager input and errors check
#
def wager_amount(score):
    wager = input(' ')
    # Checks if the User is entering a no-integer
    while ie.check_num_error(wager):
        print('\n-------------------------------- Error')
        print(' Wrong entry')
        print('-------------------------------- Error')
        print('\n*************************\n Enter a whole number amount\n')
        #
        wager = input(' ')
    # Checks if an invalid numeric key was pressed by user
    if int(wager) > score:
        print('\n-------------------------------- Error')
        print(' Wrong entry')
        print('-------------------------------- Error')
        print('\n*************************\n The amount is greater than yor winning')
        print(' Please enter an amount same as or lesser than your winning \n')
        # calls back
        wager = wager_amount(score)
    # Returns
    return int(wager)
#
# -----------------------------------------------------
#
# --------- Main Final Jeopardy round function
#
# -----------------------------------------------------
#
def final_jeopardy_round(final_jeopardy, score, cheat_mode):
    # Wipe console display
    dl.wipe_screen()
    # Final Jeopardy Banner
    print()
    print('''
                                                                                *********************************************************************************
                                                                                **                                                                             ** 
                                                                                **                         Congratulations you reached                         **
                                                                                **                           Final Jeopardy Round-3                            ** 
                                                                                **                                                                             ** 
                                                                                *********************************************************************************
                ''')
    # Displays question and category
    print('\n***********************************************************')
    print('\n From Category: ' + str(list(final_jeopardy.Category)[0]))
    print('\n Clue:')
    print(' ' + str(list(final_jeopardy.Question)[0]))
    print()
    dl.score_display(score)
    print('\n************************************************************\n')
    if cheat_mode:
        print('\n************************************************************')
        print(' cheat mode is enabled...\n The right response is:')
        print(' ' + str(list(final_jeopardy.Answer)[0]))
    print('************************************************************\n')
    print('''
*******************     
Enter your wager
*******************''')
    # Returns the user input wager amount and check for errors
    wager = wager_amount(score)
    print('''
*********************     
Type your response 
*********************''')
    user_answer = input(' ')
    # Compares the user answer with the right answer
    user_answer = user_answer.lower()
    answer = list(final_jeopardy.Answer)[0].lower()
    if re.search(answer, user_answer):
        score += wager
        print('\n******************************************************************************\n')
        print(' Right response :)\n Your winnings are now: $' + str(score))
        print('\n******************************************************************************')
        print('''
*******************************
Press any key to continue 
*******************************''')
        msvcrt.getch()
    else:
        score -= wager
        print('\n******************************************************************************\n')
        print(' Wrong response :(\n Your winnings are now: $' + str(score))
        print('\n The right answer was: ' + list(final_jeopardy.Answer)[0])
        print('\n******************************************************************************')
        print('''
*******************************
Press any key to continue
*******************************''')
        msvcrt.getch()
    #-------- Redirect to the jeopardy category display
    # Wipe console display
    dl.wipe_screen()
    print('''
                                                                                *********************************************************************************
                                                                                **                                                                             ** 
                                                                                **                     Congratulations you reached                             **
                                                                                **                        The end of the Game                                  ** 
                                                                                **                                                                             ** 
                                                                                *********************************************************************************''')
    print('\n******************************************************************************\n')
    print('                    Your Total winnings are : \n\n                      $' + str(score) + '\n')
    print('\n******************************************************************************\n')
    # End Game
    # Jeopardy.py end_game(score, 'Final Jeopardy!')
