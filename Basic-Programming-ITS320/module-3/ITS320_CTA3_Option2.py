# -------------------------------------------
# Program Name: ITS320_CTA3_Option2
# Author: Alejandro (Alex) Ricciardi
# Date: 03/03/2024
# Program Objective: Calculate the weekly average tax withholding for a customer.
#-------------------------------------------
# Pseudocode:
# 1. Create a dictionary to store the  weekly income brackets (as keys) and related tax rates (as values).
# 2. Display program banner.
# 3. Prompt the user to enter weekly income.
#       a. Validate the input to ensure it is a positive whole number or a positive two decimal number (currency)
# 5. Calculate the tax based the brackets weekly income and related tax rates dictionary values.
#       a. Handle errors.
# 7. Display the weekly income, tax rate, and the average tax withholding to the user.
# -------------------------------------------
# Program Inputs:
# - weekly_income (str) entered by the user
# -------------------------------------------
# Program Outputs:
# - banner (str)
# - weekly_income (float)
# - tax_rate (percentage as float)
# - tax 'withholding amount' (float)
# -------------------------------------------

#---- Global Variables
#-- string literal
banner = '''
        ******************************************
        *     Weekly Average Tax Withholding     *
        ******************************************
'''

tax_calculation_error_message = '''

    ***** A calculation error occurred *****
    please try again
    
'''

#-- Dictionary
# This dictionary stores the weekly income brackets as keys and related tax rates as values
# this is done to align the assignment description of the given data
# that is the tax rate percentages values are used to performer calculations and the weekly income brackets are used as categories
tax_brackets = {
    (0.00, 499.99): 0.10,             # Weekly income bracket less than $500: tax rate 10%
    (500.00, 1499.99): 0.15,          # Weekly income bracket equal to $500 less to $1500: tax rate 15%
    (1500.00, 2499.99): 0.20,         # Weekly income bracket equal to $1500 less to $2499: tax rate 20%
    (2500.00, float('inf')): 0.30,    # Weekly income bracket greater than/equal to $2500: tax rate 30%
    # In Python 3.5 float('inf') represents positive infinity - https://docs.python.org/3/library/math.html
}

#---- Functions

def is_input_float(user_input: str) -> bool:
    '''
        Checks if user_input can be converted to a float.
        :param user_input: string to be checked
        :return: True if user_input can be converted to a float, False otherwise.
    '''
    try:
        float(user_input)  # attempts to convert the user_input string to a float
        return True
    except ValueError:
        return False

def is_input_two_decimal_num(user_input: str) -> bool:
    '''
        Checks if the user_input is a two decimal number, currency
        :param user_input:
        :return: True if user_input is a two decimal float, False otherwise.
    '''
    user_input_decimal_digits = user_input.split('.')[-1]
    if is_input_float(user_input) and len(user_input_decimal_digits) == 2:
        return True
    else:
        return False

def is_input_valid_income(user_input: str) -> bool:
    '''
        Checks if user_input is a valid income
        :param user_input:
        :return: True if user_input is a valid income, False otherwise.
    '''

    if user_input.isdigit():  # Checks if the user_input is positive all number
        return True
    elif is_input_two_decimal_num(user_input) and float(user_input) >= 0:  # Checks if the user_input is a positive num
        return True
    else:
        return False

def input_weekly_income() -> float:
    '''
        Prompts the user to enter weekly income
        Handles the validation of the user entered income
        :return: The validated weekly income as a float.
    '''
    user_input = input("Please enter weekly income: ")
    while not is_input_valid_income(user_input):
        user_input = input("\n--- The enter weekly income is invalid!\nEnter the income as a positive two decimal number. Please try again: ")
    return float(user_input)

def tax_calculation(weekly_income: float) -> (float, float):
    '''
        Calculates the tax based on the given weekly income using the tax brackets dictionary.
        Handles any potential errors
        :param weekly_income: The weekly income as a float.
        :return: A tuple containing the tax rate and the calculated tax.
                 Returns None, None if no tax bracket is matched with the given weekly income. (An error occurred)
    '''
    for bracket in tax_brackets:
        if bracket[0] <= weekly_income <= bracket[1]:
            tax_rate = tax_brackets[bracket]
            break
    # The below else belongs to the for loop, not the if statement.
    # The else statement is use in conjunction with a loop statement when a break statement is utilized to exit the loop.
    # This translates to "if break do this .... else do this ..."
    else:
        # Here an error occur and no value was assign to tax_rate the function returns None, None
        return None, None

    tax = weekly_income * tax_rate

    return tax_rate, tax

#--- Main Program
def main() -> None:
    '''
        Main function executes the Weekly Average Tax Withholding calculation program.
    '''

    #--- Variables
    user_exit = ''

    print(banner)

    while user_exit.lower() != 'x':

        weekly_income = input_weekly_income()

        tax_rate, tax = tax_calculation(weekly_income)

        # Checks if an error occurred
        while tax_rate == None or tax == None:
            print(tax_calculation_error_message)
            tax_rate, tax = tax_calculation(weekly_income)

        #--- Display results
        # Note that type(f"Weekly Income: ${weekly_income:,.2f}") >>> class str,
        # f"Weekly Income: f"${weekly_income:,.2f}" is a f-string (Formatted String Literals). See https://docs.python.org/3/tutorial/inputoutput.html for more info.
        # This complies with the Golden Rule of Expressions in prints expressions
        print(f"\nWeekly Income: ${weekly_income:,.2f}")
        print(f"Tax Rate: {tax_rate * 100:,.2f}%")
        print(f"Weekly Average Tax Withholding: ${tax:,.2f}")

        user_exit = input("\n--- Enter x to exit or press enter to enter another income: ")
        print()

# Execute the program
if __name__ == "__main__": main()