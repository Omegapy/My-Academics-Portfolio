# -------------------------------------------
# Program Name: ITS320_CTA6_Option1
# Author: Alejandro (Alex) Ricciardi
# Date: 03/24/2024
# Program Objective: To perform arithmetic operations (addition, subtraction,
# multiplication, division, and modulus) on complex numbers input by the user.
#-------------------------------------------
# Pseudocode:
# 1. Display a banner for the program.
# 2. Prompt the user to enter the real and imaginary parts of two complex numbers.
#       a. Check is the number are valid floats
# 3. Creat a complex number class
#       a. create methods that perform arithmetic operations on complex number
#           - addition
#           - subtraction
#           - multiplication
#           - division
#           - modulus operations
#       b. create a method that the string representation of the complex number
# 4. Display the results of these operations.
#-------------------------------------------
# Program Inputs:
# - Two sets of real and imaginary parts of complex numbers entered by the user as a set of floats.
#-------------------------------------------
# Program Outputs:
# - The results of the operations on the input complex numbers:
# addition, subtraction, multiplication, division, and modulus operations.
#-------------------------------------------

#---- Imported Modules
import math

#---- Global Variables
#-- string literal
banner = '''
        *****************************************
        *     Imaginary Numbers Calculation     *
        *****************************************
'''

class Complex(object):
    '''
        A class representing a complex number.

        The Complex class allows the creation and manipulation of complex numbers.
        It provides methods for performing addition, subtraction, multiplication, division, and modulus
        on complex numbers.

        Attributes:
            real (float): The real part of the complex number.
            imaginary (float): The imaginary part of the complex number.
            operation_type (str): The type of operation performed on the complex number.

        Note this class overrides the default behavior of Python's built-in special methods, also known as magic methods
        or dunder (double underscore) classes:
         __add__, __sub__, __mul__,  __truediv__, and __str__
        Methods:
            __add__(no: object) -> object:
                Adds two complex numbers.
            __sub__(no: object) -> object:
                Subtracts two complex numbers.
            __mul__(no: object) -> object:
                Multiplies two complex numbers.
            __truediv__(no: object) -> object:
                Divides two complex numbers.
            mod() -> object:
                Calculates the modulus (magnitude) of the complex number.
            __str__() -> str:
                Returns the string representation of the complex number.
    '''

    # Static class variable
    __num_name = 'x'  # Class variable to keep track of the complex number name (x or y)

    def __init__(self, real, imaginary, operation_type=""):
        '''
            Initializes a complex number with the given real and imaginary parts.

            :param real: The real part of the complex number
            :param imaginary: The imaginary part of the complex number
            :param operation_type: The type of operation performed (default: "")
        '''
        self.real = real
        self.imaginary = imaginary
        self.operation_type = operation_type
        # Alternate between 'x' and 'y' for the number name
        if Complex.__num_name == 'y':
            Complex.__num_name = 'x'
        else:
            Complex.__num_name = 'y'

    def __add__(self, no: object) -> object:
        '''
            Adds two complex numbers.

            :param no: Complex class object, the complex number to add
            :return: Complex class object, the result of adding the two complex numbers, a complex number
        '''
        real = self.real + no.real
        imaginary = self.imaginary + no.imaginary
        operation_type = "   x+y"
        return Complex(real, imaginary, operation_type)

    def __sub__(self, no: object) -> object:
        '''
            Subtracts two complex numbers.

            :param no: Complex class object, the complex number to subtract
            :return: Complex class object, the result of subtracting the two complex numbers, , a complex number
        '''
        real = self.real - no.real
        imaginary = self.imaginary - no.imaginary
        operation_type = "   x-y"
        return Complex(real, imaginary, operation_type)

    def __mul__(self, no: object) -> object:
        '''
            Multiplies two complex numbers.

            :param no: Complex class object, a complex number, the complex number to multiply
            :return: Complex class object, the result of multiplying the two complex numbers, a complex number
        '''
        real = self.real * no.real - self.imaginary * no.imaginary
        imaginary = self.real * no.imaginary + self.imaginary * no.real
        operation_type = "   x*y"
        return Complex(real, imaginary, operation_type)

    def __truediv__(self, no: object) -> object:
        '''
            Divides two complex numbers.

            :param no: Complex class object, the complex number to divide by
            :return: Complex class object,the result of dividing the two complex numbers, a complex number
        '''
        denominator = no.real ** 2 + no.imaginary ** 2
        real = (self.real * no.real + self.imaginary * no.imaginary) / denominator
        imaginary = (self.imaginary * no.real - self.real * no.imaginary) / denominator
        operation_type = "   x/y"
        return Complex(real, imaginary, operation_type)

    def mod(self) -> object:
        '''
            Calculates the modulus (magnitude) of the complex number.

            :param None:
            :return: Complex class object, the modulus of the complex number, a complex number
        '''
        real = math.sqrt(self.real ** 2 + self.imaginary ** 2)
        operation_type = f"mod({Complex.__num_name})"
        return Complex(real, 0, operation_type)

    def __str__(self) -> str:
        '''
            Returns the string representation of the complex number.

            :return: The string representation of the complex number
        '''
        # return f"{self.real:.2f}{self.imaginary:.2f}i"
        if self.imaginary == 0:
            result = f"{self.operation_type} = {self.real:.2f}+0.00i"
        elif self.real == 0:
            if self.imaginary >= 0:
                result = f"{self.operation_type} = 0.00+{self.imaginary:.2f}i"
            else:
                result = f"{self.operation_type} = 0.00-{abs(self.imaginary):.2f}i"
        elif self.imaginary > 0:
            result = f"{self.operation_type} = {self.real: .2f}+{self.imaginary:.2f}i"
        else:
            result = f"{self.operation_type} = {self.real: .2f}-{abs(self.imaginary):.2f}i"
        return result

# Main function
def main() -> None:
    '''
        The main function of the program.
        It prompts the user to enter two complex numbers and performs various operations on them.
        The results of the operations are then printed to the console.

        :param None:
        :return: None
    '''

    print(banner)

    # Prompts the user to enter two complex numbers until two valid complex numbers are enter
    while True:
        # Checks if the two numbers are valid complex numbers
        try:
            # Get the first complex number from user input
            C = map(float, input('''
Please enter the first complex number (x).
Enter the real and imaginary parts separate by a space with no i: ''').split())
            # Get the second complex number from user input
            D = map(float, input('''
Please enter the second complex number(y).
Enter the real and imaginary parts separate by a space with no i: ''').split())

            # Create Complex number object
            x = Complex(*C)
            y = Complex(*D)
        except ValueError:
            print("\n-- Invalid entry, please try again --")
        except TypeError:
            print("\n-- Invalid entry, please try again --")
        else:
            break

    # Print the results of the complex number operations
    print('\n     '.join(map(str, ["\nResults:", x + y, x - y, x * y, x / y, x.mod(), y.mod()])))

# Execute the program
if __name__ == '__main__': main()
