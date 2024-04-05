# -------------------------------------------
# Program Name: ITS320_CTA4_Option2
# Author: Alejandro (Alex) Ricciardi
# Date: 03/10/2024
# Program Objective: Calculate grades statistics (Average, Maximum, Minimum) from of a set of user inputted grades
#-------------------------------------------
# Pseudocode:
# 1. Initialize program banner
# 2. Create - initialize a global dictionary to store average, maximum, and minimum grades statistics.
# 3. Define a function to check if a string can be converted to a float.
# 4. Define a function to prompt the user to enter five valid grades.
#       a. validate each user inputted to ensure it is a float between 0 and 100 included
#       b. return a list of float grades
# 5. Define a function to calculate and store the average, maximum, and minimum of the grades.
# 6. Define a function to display the calculated grade statistics.
# 7. In the main function, allow input grades, calculate and display statistics,
#    and then offer the user to exit program or enter another set of grades.
# -------------------------------------------
# Program Inputs:
# Five grades inputted (str) by the user
# -------------------------------------------
# Program Outputs:
# - banner (str)
# - average (float)
# - maximum (float)
# - minimum  (float)
# -------------------------------------------

#---- Global Variables

#-- string literal
banner = '''
        ****************************
        *     Grade Statistics     *
        ****************************
'''

#--- Dictionary
grades_statistics = {
    "average": float,
    "maximum": float,
    "minimum": float,
}

#---- Functions

def is_input_float(user_input: str) -> bool:
    '''
        Checks if user_input can be converted to a float.
        :param: user_input: string to be checked
        :return: True if user_input can be converted to a float, False otherwise.
    '''
    try:
        float(user_input)  # attempts to convert the user_input string to a float
        return True
    except ValueError:
        return False

def input_grade() -> list:
    '''
        Prompts the user to enter five grades, ensuring each is a valid float between 0 and 100 included.
        :param: None
        :return: A list of the valid float grades inputted by the user.
    '''
    # Local variable
    grades = []  # store valid grades
    for i in range(1, 6):
        user_input = input(f"Please enter grade number ({i}): ")
        # Note: A boolean short-circuit occurs if 'not is_input_float(user_input)' returns True.
        # As a result,'float(user_input)' in '0 <= float(user_input) <= 100'
        # will not be executed preventing an exception from occurring if user_input is not a decimal number
        while not is_input_float(user_input) or not (0 <= float(user_input) <= 100):
            user_input = input(f"--- The enter grade number ({i}) is invalid! Please try again: ")
        grades.append(float(user_input))

    return grades

def calculate_stats(grades: list[float])-> None:
    '''
        Calculates and stores the average, maximum, and minimum of the grades in the global grade_statistics dictionary.
        :param: List of float grades
        :return: None
    '''
    grades_statistics["average"] = sum(grades) / len(grades)
    grades_statistics["maximum"] = max(grades)
    grades_statistics["minimum"] = min(grades)

def display_stats() -> None:
    '''
        Displays the calculated grades statistics.
        :param: None
        :return: None
    '''
    print("\n--- Grades Statistics ---")
    for key, value in grades_statistics.items():
        print(f"{key.title()}: {value: .2f}")

#--- Main Program
def main() -> None:
    '''
        Main function runs the program loop,
        allows user input of grades,
        calculates and display statistics until user decides to exit.
        :param: None
        :return: None
    '''

    print(banner)

    # Loop until user exits
    while True:

        grades = input_grade()
        calculate_stats(grades)
        display_stats()

        is_more_grades = ('y' or "yes") in input("\n--- Do you need to enter another set of grades: ").lower()
        print()
        if not is_more_grades: break  # if true exits program



#--- Execute the program
if __name__ == "__main__": main()

