/*=========================================================================================================
    Program Name: Integer Pointers
    Author: Alejandro (Alex) Ricciardi
    Date: 10/27/2024

    Requirement: C++23

    Program Description:
    The program is a small procedural C++ program that prompts a user to enter three integer values,
    validates the input values as integers and stores the values using raw pointers.

    Note:
    - The standard integer is typically 4 bytes, it is platform dependent.
    - The Program accepts whitespaces to be entered before and/or after the integer value.
    - The program follows the following SEI CERT C/C++ Coding Standard:
        - EXP34-C. Do not dereference null pointers
        - EXP53-CPP. Do not read uninitialized memory
        - ERR50-CPP. Do not abruptly terminate the program
        - ERR51-CPP. Handle all exceptions
        - ERR56-CPP. Guarantee exception safety
        - ERR57-CPP. Do not leak resources when handling exceptions
        - MEM50-CPP. Do not access freed memory
        - MEM51-CPP. Properly deallocate dynamically allocated resources
        - MEM57-CPP. Avoid using default operator new for over-aligned types
        - INT50-CPP. Do not cast to an out-of-range enumeration value
        - STR50-CPP. Guarantee that storage for strings has sufficient space
          for character data and the null terminator

=========================================================================================================*/

/* ----------------------------------------------------------------------------------------------
      ------------------
     |    Libraries     |
      ------------------
------------------------------------------------------------------------------------------------- */
#include <iostream>
#include <limits>       // For INT_MAX and INT_MIN 
#include <string>       
#include <stdexcept>    // For exception handling 
#include <new>          // For std::nothrow, preventes exceptions on memory allocation failure

using namespace std;

/* ----------------------------------------------------------------------------------------------
     -------------------------
    |    Global Variables     |
     -------------------------
------------------------------------------------------------------------------------------------- */
// Banner - multi Line String
const string banner = R"(
               **********************
               *  Integer Pointers  *
               **********************
)";

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ----------------------------
     |    Function Declaration    |
      ----------------------------
-------------------------------------------------------------------------------------------------- */
// ========================================================================================================

/**
 * Prompts the user to enter an integer and validates the input
 * It will prompt the user until a valid integer is entered
 *
 * Note:
 * The standard integer is typically 4 bytes, it is platform dependent
 * The Program accepts spaces before and after the integer value
 *
 * Handles Rules:
 * - ERR50-CPP. Do not abruptly terminate the program
 * - ERR51-CPP. Handle all exceptions
 * - INT50-CPP. Do not cast to an out-of-range enumeration value
 * - STR50-CPP. Guarantee that storage for strings has sufficient space
 *   for character data and the null terminator
 *
 * @param prompt The message to user
 * @return validated integer
 */
int getValidatedInput(const string& prompt) noexcept(false);  

/**
 * Displays the value pointed to by ptr.
 * checks if the pointer is not null, if it is, it displays an error,
 * othervise it display the value pointed (Rule: EXP53-CPP)
 *
 * @param name The name of the pointer for display purposes.
 * @param ptr The pointer to an integer
 */
void displayPointer(const char* name, int* ptr);
 

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ---------------------
     |    Main Function    |
      ---------------------

     The main function runs the program.
     Asks the user to enter three integers, validates inputs, and displays inputs.

-------------------------------------------------------------------------------------------------- */
// ========================================================================================================
int main() {
    int num1, num2, num3;  // Stores the validated integers

    cout << banner << endl;

    cout << "Enter three integer values!\n\n";

    // Try-catch block handle all exceptions (ERR51-CPP, ERR50-CPP)
    try {
        // Accepts user inputs and validates them (Rules: STR50-CPP, INT50-CPP)
        num1 = getValidatedInput("Enter integer 1: ");
        num2 = getValidatedInput("Enter integer 2: ");
        num3 = getValidatedInput("Enter integer 3: ");


        // Exception-safe dynamic memory allocation (Rule: ERR57-CPP and MEM50-CPP)
        int* ptr1 = new(nothrow) int; // Allocates memory without throwing an exception (Rule: MEM50-CPP)
        int* ptr2 = new(nothrow) int;
        int* ptr3 = new(nothrow) int;

        // Memory allocation check (Rule: MEM51-CPP, ERR50-CPP)
        if (!ptr1 || !ptr2 || !ptr3) {
            cerr << "\n--- ERROR: Memory allocation failed. Exiting program.\n"; // Error message 
            // Clean-up allocated memory before exiting (Rule: MEM51-CPP)
            delete ptr1;
            delete ptr2;
            delete ptr3;
            return 1;  // Exit the program with an error code
        }

        // Stores the validated integers in dynamically allocated memory (Rule: EXP34-C: Avoid dangling references)
        // Note that the address-of operator (&) is not needed
        // The memory address was allocated using 'new(nothrow) int' at the pointer initialization step
        *ptr1 = num1;
        *ptr2 = num2;
        *ptr3 = num3;

        // Displays variable values
        cout << "\nValues stored in variables:\n\n";
        cout << "num1 = " << num1 << "\n"
            << "num2 = " << num2 << "\n"
            << "num3 = " << num3 << "\n" << endl;

        // Displays the values pointed by ptr1, ptr2, and ptr3 
        // checks for null pointer (Rule: EXP53-CPP)
        displayPointer("ptr1", ptr1);
        displayPointer("ptr2", ptr2);
        displayPointer("ptr3", ptr3);

        // Deallocate memory properly preventing memory leaks (Rule: MEM51-CPP)
        delete ptr1;
        delete ptr2;
        delete ptr3;
    }
    // catch all unhandled all exceptions 
    // (Rule: ERR51-CPP. Handle all exceptions, ERR50-CPP. Do not abruptly terminate the program)
    catch (const exception& e) {
        // Catch any standard exceptions thrown in the try block
        cerr << "\n--- ERROR: Exception caught: " << e.what() << endl;
        return 1;  // Exit the program with an error code
    }
    catch (...) {
        // Catch any non-standard exceptions
        cerr << "\n--- ERROR: Unknown exception caught. Exiting program.\n";
        return 1;  // Exit the program with an error code
    }

    return 0;  // Successful program termination
}

// ----------------------------------------------------------------------------------------------

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ----------------------------
     |    Function Definitions    |
      ----------------------------
------------------------------------------------------------------------------------------------- */
// ========================================================================================================

/**
 * Prompts the user to enter an integer and validates the input
 * It will prompt the user until a valid integer is entered
 *
 * Note:
 * The standard integer is typically 4 bytes, it is platform dependent
 * The Program accepts whitespaces before and after the integer value
 *
 * Handles Rules:
 * - ERR50-CPP. Do not abruptly terminate the program
 * - ERR51-CPP. Handle all exceptions
 * - INT50-CPP. Do not cast to an out-of-range enumeration value
 * - STR50-CPP. Guarantee that storage for strings has sufficient space
 *   for character data and the null terminator
 *
 * @param prompt The message to user
 * @return validated integer
 */
int getValidatedInput(const string& prompt) noexcept(false) { 
    while (true) {
        string input;

        cout << prompt;

        // Gets the entire line of input and stores it in a string object  
        // Using std::string is safer for string manipulation (STR50-CPP)
        getline(cin, input);

        //----- Whitespaces Handling ------

        // Remove leading and trailing whitespaces from the input
        size_t start = input.find_first_not_of(" \t\n\r");
        size_t end = input.find_last_not_of(" \t\n\r");

        // Check if the input only contains whitespaces 
        // The following will be true if after removing all the whitespaces 
        // and if the input contain only whitespace
        // 'string::npos' no position meaning that start has no position after parsing
        if (start == string::npos) {
            cerr << "--- Invalid input: Please enter an integer value.\n";
            // skips the rest of the current while loop iteration
            continue; // Prompt the user again 
        }

        // Trim the input to remove leading and trailing whitespaces
        input = input.substr(start, end - start + 1);

        //---- Check if the input is an integer -----

        // Try-catch block to handle all exceptions (ERR51-CPP, ERR50-CPP)
        try {
            // Holds the position where parsing stopped
            size_t pos;
            // Convert the inputted string to a long integer using stol (Rule: INT50-CPP)
            // used to check if the string entered is an integer
            long temp = stol(input, &pos);

            // Check if all the string was converted to a long temp (Rule: INT50-CPP)
            if (pos != input.size()) { // If true invalid characters were entered
                // There are remaining characters after the parsed number
                // Non-integer characters detected
                throw invalid_argument("--- Invalid input: Non-integer characters detected.");
            }

            // Check if long int parsed from the string is within the range of an int
            if (temp > INT_MAX || temp < INT_MIN) { // Prevents integer overflow/underflow (Rule: INT50-CPP)
                throw out_of_range("--- Invalid input: Input is out of integer range.");
            }
            return static_cast<int>(temp); // Return the validated integer
        }
        catch (const invalid_argument& e) {
            // Handle invalid input (non-integer characters or floating-point numbers)
            if (input.find('.') != string::npos) {
                cerr << "--- Invalid input: Floating-point numbers not allowed. Please enter an integer.\n";
            }
            else {
                cerr << "--- Invalid input: Non-integer, non-digit characters not allowed. Please enter a valid integer.\n";
            }
        }
        catch (const out_of_range& e) {
            // Handle input numbers that are out of the allowable int range
            cerr << "--- Invalid input: Number out of range. Please enter an integer between "
                << INT_MIN << " and " << INT_MAX << ".\n";
        }
        catch (...) {
            // Catch any other exceptions and provide a generic error message
            cerr << "--- Invalid input: Please enter a valid integer.\n";
        }
    }
}

// ----------------------------------------------------------------------------------------------

/**
 * Displays the value pointed to by ptr.
 * checks if the pointer is not null, if it is, it displays an error,
 * othervise it display the value pointed (Rule: EXP53-CPP)
 *
 * @param name The name of the pointer for display purposes.
 * @param ptr The pointer to an integer
 */
void displayPointer(const char* name, int* ptr) { 
    if (ptr == nullptr) {  // Check if the pointer is null (Rule: EXP53-CPP)
        cerr << name << "\n--- ERROR: null pointer!\n";
    }
    else { // Dereference the pointer and display its value
        cout << "*" << name << " = " << *ptr << endl;
    }
}

// ----------------------------------------------------------------------------------------------
