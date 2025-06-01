# -------------------------------------------
# Program Name: ITS320_CTA2_Option2
# Author: Alejandro (Alex) Ricciardi
# Date: 02/25/2024
# Program Objective: Store user inputted data in a dictionary and print out the contents of the dictionary.
#-------------------------------------------
# Pseudocode:
# 1. Print the banner Car Brand
# 2. Prompt the user for car details:
#    - brand
#    - model
#    - year
#    - starting odometer
#    - ending odometer
#    - miles per gallon
# 3. Validate each input:
#    - year must be an integer between 1886 and the current year. 1886 is when the first car was made.
#    - starting odometer reading and miles per gallon must be a non-negative integer
#    - ending odometer reading must be greater than or equal to the starting odometer reading
#      (starting odometer reading must not be greater than or not equal to the ending odometer reading)
# 4. Store the validated inputs in a dictionary
# 5. Print the car details stored in the dictionary
# -------------------------------------------
# Program Inputs:
# - brand (string)
# - model (string)
# - year (4 digit integer between 1886 and the current year)
# - starting odometer reading (non-negative integer)
# - ending odometer reading (non-negative integer, greater than or equal to starting odometer)
# - miles per gallon (non-negative integer)
# -------------------------------------------
# Program Outputs:
# - brand (string)
# - model (string)
# - year (int)
# - starting odometer (int)
# - ending odometer (int)
# - miles per gallon (int)
# -------------------------------------------

#---- Global Variables
#-- string literal
banner = '''
        *********************
        *     Car Brand     *
        *********************
'''

#---- Functions

def is_valid_year(user_input: str) -> bool:
    '''
        Checks if the input is a valid 4 digit year between 1886 and the current year.
        :param user_input: The year to check inputted as a string
        :return: True if the year is valid, False if it is not valid
    '''
    current_year = 2024  # Assume the current year is 2024 for this example
    # Checks if the user inputted value is an integer between 1886 and the current year
    # isdigit() checks is the string is made of digits, the character '-' is not a digit,
    # ex: ('-3')isdigit() will return False, ('3').isdigit() will return True, and ('3.0').isdigit() will return False
    if user_input.isdigit():
        year = int(user_input)
        if 1886 <= year <= current_year:
            return True
        else:
            return False
    else:
        return False

def input_year() -> int:
    '''
        Prompts the user to enter a car year, until a valid year is entered.
        :return: The valid car year as an integer
    '''
    #
    user_input = input("Enter the car year: ")
    # Checks if the user inputted value is a valid year
    while not is_valid_year(user_input):
        user_input = input("The enter car year is invalid, please try again: ")
    return int(user_input)

def input_starting_odometer() -> int:
    '''
        Prompts the user for a starting odometer reading value
        until a valid starting odometer reading value is entered.
        :return: The starting odometer reading as an integer.
    '''
    user_input = input("Enter the starting odometer as a whole number: ")
    # Checks if the user inputted value is a non-negative integer
    # isdigit() checks is the string is made of digits, the character '-' is not a digit,
    # ex: ('-3')isdigit() will return False, ('3').isdigit() will return True, and ('3.0').isdigit() will return False
    while not user_input.isdigit():
        user_input = input("The entered starting odometer is invalid, please try again: ")
    return int(user_input)

def input_ending_odometer(starting_odometer: int) -> int:
    '''
        Prompts the user for an ending odometer reading value
        until a valid ending odometer reading value is entered.
        :param starting_odometer: The ending odometer reading value.
        :return: The ending odometer reading as an integer.
    '''
    user_input = input("Enter the ending odometer as a whole number: ")
    # Checks if the user inputted value is an integer greater or equal to the starting_odometer
    # isdigit() checks is the string is made of digits, the character '-' is not a digit
    # ex: ('-3')isdigit() will return False, ('3').isdigit() will return True, and ('3.0').isdigit() will return False
    while (not user_input.isdigit()
           or not (int(user_input) >= starting_odometer)): # the ending odometer can be equal to the starting odometer
        user_input = input("The entered ending odometer is invalid, please try again: ")
    return int(user_input)

def input_miles_per_gallon() -> int:
    '''
        Prompts the user for the miles per gallon,
        checks if it is a valid non-negative integer.
        :return: The miles per gallon as an integer
    '''
    user_input = input("Enter the miles_per_gallon as a whole number: ")
    # Checks if the user inputted value is a non-negative integer, the miles_per_gallon can be equal to 0 if the car is electric
    # isdigit() checks is the string is made of digits, the character '-' is not a digit,
    # ex: ('-3')isdigit() will return False, ('3').isdigit() will return True, and ('3.0').isdigit() will return False
    while not user_input.isdigit():
        user_input = input("The entered miles per gallon is invalid, please try again: ")
    return int(user_input)

def input_car() -> dict:
    '''
        Gathers car information from the user,
        brand, model, year, odometer readings, and MPG.
        Checks and validates and collects odometer readings and MPG.
        :return: A dictionary containing the car's details
    '''
    brand = input("Enter the car brand: ")
    model = input("Enter the car model: ")
    year = input_year()
    starting_odometer = input_starting_odometer()
    ending_odometer = input_ending_odometer(starting_odometer)
    miles_per_gallon = input_miles_per_gallon()

    car = {
        "brand": brand,
        "model": model,
        "year": year,
        "starting_odometer": starting_odometer,
        "ending_odometer": ending_odometer,
        "miles_per_gallon": miles_per_gallon,
    }
    return car

#---- Main Program
def main() -> None:

    print(banner)

    car_details = input_car()

    # Printing the car details
    print("\nCar Details:")
    for key, value in car_details.items():
        # The condense if-else expression in the print function,
        # checks if value is a string data type, if not it casts it into an integer data type
        # This is done to comply with the Golden Rule of Expressions
        print(f"{key.title()}: {value if isinstance(value, str) else str(value)}")

if __name__ == "__main__": main()
