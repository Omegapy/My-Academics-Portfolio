/*=========================================================================================================
    Program Name: Two String Input Concatenated  
    Author: Alejandro (Alex) Ricciardi
    Date: 10/20/2024

    Requirement: C++23

    Program Description:
    The program takes two strings inputted by the user, concatenates them, 
    and prints the resulting concatenated string. 
    The input strings and their concatenation are safely handled using C++'s std::string class, 
    which automatically manages memory, preventing buffer overflows.
    The program also uses std::getline for string inputs, ensuring strings with spaces are fully captured. 
    The program repeats the process three times, accepting two string inputs and concatenating them 
    to test if varying string lengths are handled securely.
    
=========================================================================================================*/

/* ----------------------------------------------------------------------------------------------
      ------------------
     |    Libraries     |
      ------------------
------------------------------------------------------------------------------------------------- */
#include <iostream>
#include <string>

using namespace std;

/* ----------------------------------------------------------------------------------------------
     -------------------------
    |    Global Variables     |
     -------------------------
------------------------------------------------------------------------------------------------- */
// Banner - multi Line String
const string banner = R"(
               ***********************************
               *  Two String Input Concatenated  *
               ***********************************
)";

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ---------------------
     |    Main Function    |
      ---------------------

     The main function runs the program. 
     It loops three times, asking the user for two string inputs each
     time, then concatenating them and printing the result. 
     The program uses std::string and std::getline to ensure safe string capturing and handling, 
     preventing buffer overflows and memory leaks.

-------------------------------------------------------------------------------------------------- */
// ========================================================================================================
int main() {

    cout << banner << endl;

    // Loop three times to handle varying string lengths
    for (int i = 0; i < 3; ++i) {
        // Use std::string for safer string manipulation (STR50-CPP)
        string firstString;
        string secondString;

        cout << "Enter the first string: ";
        // Use std::getline to read entire lines, preventing buffer overflow (STR50-CPP)
        getline(std::cin, firstString);

        cout << "Enter the second string: ";
        getline(std::cin, secondString);

        // Concatenate strings using + operator
        // Safe concatenation with std::string (compliant with STR50-CPP and STR51-CPP)
        string concatenatedString = firstString + secondString;

        // Output the concatenated string
        cout << "Concatenated String: " << concatenatedString << std::endl << std::endl;
    }

    return 0;
}
