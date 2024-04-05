# -------------------------------------------
# Program Name: ITS320_CTA5_Option2
# Author: Alejandro (Alex) Ricciardi
# Date: 03/17/2024
# Program Objective: Concatenate the first two given strings and reverse order the third given string.
#-------------------------------------------
# Pseudocode:
# 1. Display a banner.
# 2. Prompt the user to enter three strings.
#   a. For each user input, checks if a string was entered, if not prompts the user to reenter a string.
#   b. Store the three string in a list
# 3. Call the process_strings function
#   NOTE: this function breaks the Golden Rule of Modularization, but it is compliant with the assignment instructions.
#          Assignment Instructions:
#                 Write a Python function that will work on three strings.
#                 The function will return a concatenation of the first two strings
#                 and will print the third string in reverse order. The function is to be called from the main program.
#                 In the main program, prompt the user for the three strings and pass these values to the function.
#   a. Call the concatenated_strings function
#       Concatenate the first two strings.
#       Return concatenated string
#   b. Call the concatenated_strings function
#       Reverse the third string.
#       Return reversed string
#   c. Print the concatenated string
#   d. Return concatenated string from the return concatenated_strings function
# 6. Print the reversed third string.
# 7. Print the concatenated string.
#-------------------------------------------
# Program Inputs:
# - Three strings entered by the user.
#-------------------------------------------
# Program Outputs:
# - reversed_string, the reversed third string.
# - concatenated_str, the concatenated string of the first two strings.
#-------------------------------------------

#---- Global Variables

#-- string literal
banner = '''
        *********************************************************
        *     Concatenate and Third String in Reverse Order     *
        *********************************************************
'''

#---- Functions
def concatenated_strings(str_1: str, str_2: str) -> str:
    '''
        Concatenates two strings.

        :param str_1: str, first string to be concatenated
        :param str_2: str, second string to be concatenated
        :return: The concatenated string of str_1 and str_2.
    '''

    return str_1 + str_2

def reverse_string(string_to_reverse: str) -> str:
    '''
        Concatenates two strings.

        :param string_to_reverse: str, string to be concatenated
        :return: The reversed string.
    '''
    return string_to_reverse[::-1]

def process_strings(str_lst: list) -> str:
    '''
         Concatenates the first two strings in a list of strings and reverses the third string in the list.
         NOTE: this function breaks the Golden Rule of Modularization, but it is compliant with the assignment instructions

         Assignment Instructions:
                Write a Python function that will work on three strings.
                The function will return a concatenation of the first two strings
                and will print the third string in reverse order. The function is to be called from the main program.
                In the main program, prompt the user for the three strings and pass these values to the function.

        :param str_lst: list of three strings
        :return: The concatenated string of str_lst[0] and str_lst[1].
     '''

    # Call the process strings functions
    concatenated_str = concatenated_strings(str_lst[0], str_lst[1])
    reversed_str = reverse_string(str_lst[2])

    print("\nReversed third string:", reversed_str)

    return concatenated_str

#--- Main Program
def main() -> None:
    '''
        The main function that prompts the user for three strings,
        calls the process_strings function, and prints the concatenated string.

        :param None:
        :return: None
    '''

    print(banner)

    # Prompt the user for three strings
    str_lst = []
    for i in range(1, 4):
        input_str = input(f"Enter the string number ({i}): ")
        # Checks if a string was entered, if not prompts the user to reenter a string
        while input_str == '':
            input_str = input(f"No string was entered, please enter the string number ({i}): ")
        str_lst.append(input_str)

    # Call the process strings function
    concatenated_str = process_strings(str_lst)

    print("Concatenated first two strings:", concatenated_str)

#--- Execute the program
if __name__ == "__main__": main()