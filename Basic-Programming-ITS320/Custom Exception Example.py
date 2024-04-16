##-------------------------------------------
# Program Name: Custom Exception Example
# Author: Alejandro (Alex) Ricciardi
# Date: 03/26/2024
# Program Objective: Demonstrate the usage of custom exceptions and exception handling in Python.
#-------------------------------------------
# Pseudocode:
# 1. Define a base CustomException class that extends the built-in Exception class.
# 2. Define specific exception classes (DatabaseError and NetworkError) that inherit from CustomException.
# 3. Create a process_data function that simulates different scenarios based on the input data.
# 4. Use a try-except block to handle the exceptions raised in the process_data function.
# 5. Enrich the caught exceptions with additional notes using the add_note method.
# 6. Re-raise the exceptions to propagate them to the calling code.
# 7. Use a try-except block in the main function to catch and handle the specific exceptions.
#-------------------------------------------
# Program Inputs:
# - data: A string representing the input data for the process_data function.
#-------------------------------------------
# Program Outputs:
# - Custom exception messages and status codes when exceptions occur.
# - Success message when data is processed successfully.
# - Cleanup message when the finally block is executed.
#-------------------------------------------

#---- Global Variables
#-- string literal
banner = '''
*****************************
*  Custom Exception Example *
*****************************
'''

#--- Classes
class CustomException(Exception):
    '''
        A base class for custom exceptions.
        Child class of Exception class

        Attributes:
            message (str): The error message.
            status_code (int): The status code associated with the exception.
    '''
    def __init__(self, message, status_code=None) -> object:
        '''
            Initializes a new instance of the CustomException class.

            :param object: message, the error message.
            :param: object error, status_code, the status code associated with the exception (default: None).
        '''
        super().__init__(message)
        self.status_code = status_code

    def __str__(self) -> str:
        '''
            Returns a string representation of the CustomException.

            :param None:
            :return: The string representation of the exception.
        '''
        return f"CustomException: {self.args[0]}, Status Code: {self.status_code}"

class DatabaseError(CustomException):
    '''
        A custom exception class for database-related errors.
        Subclass of the CustomException class
    '''
    pass

class NetworkError(CustomException):
    '''
        A custom exception class for network-related errors.
        Subclass of the CustomException class
    '''
    pass

#--- Global Functions
def process_data(data) -> str:
    '''
        Simulates different scenarios based on the input data and raises exceptions accordingly.

        :param object: A string representing the input data.
        :return: string, the processed data (in uppercase) if no exception occurs.
    '''
    try:
        # Simulating a database operation
        if data == "database_error":
            raise DatabaseError("Database connection failed", status_code=500)

        # Simulating a network operation
        if data == "network_error":
            raise NetworkError("Network connection timed out", status_code=408)

        # Simulating a successful operation
        result = data.upper()
    except CustomException as e:
        e.add_note("An error occurred while processing the data")
        raise
    else:
        print("Data processed successfully")
    finally:
        print("Cleaning up resources")

    return result

#--- Main Program
def main() -> None:
    '''
        The main function that demonstrates the usage of custom exception class.

        :param None:
        :return: None
    '''
    try:
        process_data("hello")  # Successful operation
        process_data("database_error")  # Raises DatabaseError
        process_data("network_error")  # Raises NetworkError
    except (DatabaseError, NetworkError) as e:
        print(str(e))

#--- Execute the program
if __name__ == "__main__": main()