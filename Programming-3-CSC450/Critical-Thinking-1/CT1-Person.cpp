
/*=========================================================================================================
    Program Name: Secure Person Management System
    Author: Alejandro (Alex) Ricciardi
    Date: 10/13/2024

    Requirement: C++23

    Program Description:
    This program is a small procedural C++ application that manages an array of Person objects. 
    It tests and implements secure coding practices to mitigate vulnerabilities such as:
    - Buffer overflows
    - Integer overflows
    - Incorrect type conversions
    - Null pointer dereferencing
=========================================================================================================*/

/* ----------------------------------------------------------------------------------------------
      ------------------
     |    Libraries     |
      ------------------
   ---------------------------------------------------------------------------------------------- */

#include <iostream>
#include <string>
#include <climits>   // For UINT_MAX, Maxumum size of an unsigned int
#include <stdexcept>  // For exceptions
#include <cstddef>   // For std::size_t, size type use of arrays and strings

// Use the standard namespace to simplify code syntax
using namespace std;

/* ----------------------------------------------------------------------------------------------
      -------------------------
     |    Global Variables     |
      -------------------------
-------------------------------------------------------------------------------------------------- */

// Maximum allowed length for string inputs to enhance security
const size_t MAX_STRING_LENGTH = 75;

// Global variable to keep track of the number of persons
unsigned numOfPersons = 0;

// Structure to hold person information
struct Person {
    string lastName;
    string firstName;
    string streetAddress;
    string city;
    string zipCode;
    unsigned personNum = 0; // Unique ID for each person
};

// Banner - multi Line String
const string banner = R"(
               ***********************************
               * Secure Person Management System *
               ***********************************

)";

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ----------------------------
     |    Function Declaration    |
      ----------------------------
-------------------------------------------------------------------------------------------------- */
// ========================================================================================================

/** -------------------------------------------------------------------------------------------
  Increments numOfPersons and check for integer overflow  
  
  Returns true if the incrementation is successfull, false if UINT_MAX is reached
  UINT_MAX, Maxumum size of an unsigned int
-------------------------------------------------------------------------------------------- **/
static bool incrementNumOfPersons(unsigned& counter);

/** -------------------------------------------------------------------------------------------
  Limits string length to MAX_STRING_LENGTH characters 
  Truncates the string if it exceeds the maximum length and issues a warning
  Used by createPerson() and createPersonFull() functions 
  
  Returns verified string
-------------------------------------------------------------------------------------------- **/
static string limitStringLength(const string& input);

/** -------------------------------------------------------------------------------------------
  struck Person construtor-1
  Create a new Person with whth only lastName and firstName arguments inputted
  Uses limitStringLength() to verify string lenght
  
  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
static bool createPerson(Person& person, const string& lastName, const string& firstName);

/** -------------------------------------------------------------------------------------------
  struck Person construtor-2
  Create a new Person with all arguments inputted
  Uses limitStringLength() to verify string lenght
  
  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
static bool createPersonFull(Person& person, const string& lastName, const string& firstName,
    const string& streetAddress, const string& city,
    const string& zipCode);

/** -------------------------------------------------------------------------------------------
  Displays the contents of the persons array
  "size_t iterate" is used to iterate the array
-------------------------------------------------------------------------------------------- **/
static void displayPersons(const Person persons[], size_t iterate);

/** -------------------------------------------------------------------------------------------
  Displays a person data
  "size_t index" is the index of the person object in the persons array
-------------------------------------------------------------------------------------------- **/
static void displayAPerson(const Person persons[], size_t index);

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ---------------------
     |    Main Function    |
      ---------------------

     tests secure coding practices such as:
     - Buffer overflows
     - Integer overflows
     - Incorrect type conversions
     - Null pointer dereferencing
-------------------------------------------------------------------------------------------------- */
// ========================================================================================================
int main() {

    /* ---------------------------------
      ---------------
     |   Variables   |
      --------------- */
    
    // ----- Variables used to test code vulnerability
    int negativeValue = -5;      // use for unsigned int vulnerability
    string longString(100, 'A'); // Create a string with 100 'A's use for string overflow
    Person* personPtr = nullptr; // Initialize pointer to null use for null pointer vulnerability
    void* voidPerson1Ptr; // Generic type pointer use for void pointer vulnerability

    //---- Create an array of persons (size 5)
    Person persons[5];

    /* ---------------------------------
      -------------
     |   Program   |
      ------------- */

    cout << banner << endl; // std::endl forces flushing of the buffer - good pratice


    // ---------------------------------- Test 1: Buffer Overflow with Overly Long Strings

    cout << "-------------------------------------------------------------\n"
        << "Test 1: Buffer Overflow with Overly Long Strings\n" 
        << "Creates a person with first and last names that are 100 characters long, filled with the letter 'A'.\n"
        << endl; 
    // not expected fail due tolimitStringLength() truncating functionality
    if (!createPerson(persons[0], longString, longString)) { 
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    displayPersons(persons, 1);

    // ---------------------------------- Test 2: Integer Overflow when Creating Many Persons
    cout << "\n-------------------------------------------------------------\n"
        << "Test 2: Integer Overflow when Creating Too Many Persons\n"
        << "Simulate numOfPersons = UINT_MAX, Maxumum size of an unsigned int\n" 
        << "\nTrying to create a new person"
        << endl;

    numOfPersons = UINT_MAX;
    if (!createPerson(persons[1], "Doe", "John")) {
        // Expected to fail due to integer overflow securety
        cout << "Failed to create person due to integer overflow." << endl;
    }
    // Reset numOfPersons for further tests
    numOfPersons = 1;

    // ---------------------------------- Test 3: Incorrect Type Conversion
    cout << "\n-------------------------------------------------------------\n" 
        << "Test 3: Incorrect Type Conversion" << endl;
    
    // Creating a new person
    if (!createPerson(persons[1], "Conversion", "Alexandria")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    displayAPerson(persons, 1);

    cout << "\nTring to assign persons[1].personNum = -5, which is a negative value"
        << endl;
    
    // Incorrectly assign negative value to unsigned personNum
    persons[2].personNum = static_cast<unsigned>(negativeValue); // negativeValue = -5
    // Security measure: Check if personNum is valid
    if (static_cast<int>(persons[2].personNum) < 0) {
        cerr << "\nIncorrect type conversion --- Negative value assigned to unsigned personNum." << endl;
    }
    else {
        cout << "Person number is: " << persons[2].personNum << endl;
    }

    // ---------------------------------- Test 4: Null Pointer Dereferencing with Person Pointer
    cout << "\n-------------------------------------------------------------\n" 
        << "Test 4: Testing Null Pointer before use - null pointer dereferencing\n" 
        << "Checking if personPtr is null, and it is."
        << endl;
    
    // Attempt to access member of null pointer
    if (personPtr == nullptr) {
        cerr << "\nPerson pointer is null! Cannot use!." << endl;
    }
    else {
        cout << "\nPerson first name: " << personPtr->firstName << endl;
    }

    // ---------------------------------- Additional test: Properly adding and displaying persons
    cout << "\n-------------------------------------------------------------\n"
        << "\nAdditional Test: Adding and Displaying Persons" << endl;
    
    // Creating a new person
    if (!createPerson(persons[2], "More", "Bob")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    if (!createPersonFull(persons[3], "Marquez", "Anita", "456 Ai Street", "Robot Town", "77442")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    if (!createPersonFull(persons[4], "Wan", "Lu", "777 LLM Street", "AI Town", "77772")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }

    displayPersons(persons, 5);

    return 0;
} 


// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ----------------------------
     |    Function Definition     |
      ---------------------------
   ---------------------------------------------------------------------------------------------- */
// ========================================================================================================

/** -------------------------------------------------------------------------------------------
    Increments numOfPersons and check for integer overflow

    Returns true if the incrementation is successfull, false if UINT_MAX is reached
    UINT_MAX, Maxumum size of an unsigned int
-------------------------------------------------------------------------------------------- **/
bool static incrementNumOfPersons(unsigned& counter) {
    // Check if counter has reached the maximum value for unsigned int
    if (counter == UINT_MAX) {
        // Security measure: Prevent integer overflow by checking maximum value
        cerr << "\nError --- Maximum number of persons reached!" << endl;
        return false;
    }
    // Increment the counter safely
    ++counter;
    return true;
}

// ----------------------------------------------------------------------------------------------

/** -------------------------------------------------------------------------------------------
  Limits string length to MAX_STRING_LENGTH characters
  Truncates the string if it exceeds the maximum length and issues a warning
  Used by createPerson() and createPersonFull() functions

  Returns verified string
-------------------------------------------------------------------------------------------- **/
// Function to limit string length to MAX_STRING_LENGTH characters
string static limitStringLength(const string& input) {
    if (input.length() > MAX_STRING_LENGTH) {
        // Security measure: Prevent buffer overflows by limiting string length
        // Truncate the string and issue a warning
        cerr << "Warning --- Input string exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
        return input.substr(0, MAX_STRING_LENGTH);
    }
    return input;
}

// ----------------------------------------------------------------------------------------------

/** -------------------------------------------------------------------------------------------
  struck Person construtor-1
  Create a new Person with whth only lastName and firstName arguments inputted
  Uses limitStringLength() to verify string lenght

  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
bool static createPerson(Person& person, const string& lastNameInput, const string& firstNameInput) {
    // Safely increment the global numOfPersons counter
    if (!incrementNumOfPersons(numOfPersons)) {
        return false;
    }
    // Limit the length of input strings to prevent buffer overflows
    person.lastName = limitStringLength(lastNameInput);
    person.firstName = limitStringLength(firstNameInput);
    // Initialize address fields with "nan" (Not Available)
    // "nan" is implemented to so the variables are not null
    person.streetAddress = "nan"; 
    person.city = "nan";
    person.zipCode = "nan";
    // Assign a unique person number
    person.personNum = numOfPersons;
    cout << "\nA person with number id: " << person.personNum << " was created successfully!" << endl;
    return true;
}

// ----------------------------------------------------------------------------------------------

/** -------------------------------------------------------------------------------------------
  struck Person construtor-2
  Create a new Person with all arguments inputted
  Uses limitStringLength() to verify string lenght

  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
bool static createPersonFull(Person& person, const string& lastNameInput, const string& firstNameInput,
    const string& streetAddressInput, const string& cityInput,
    const string& zipCodeInput) {
    // Safely increment the global numOfPersons counter
    if (!incrementNumOfPersons(numOfPersons)) {
        return false;
    }
    // Limit the length of input strings to prevent buffer overflows
    person.lastName = limitStringLength(lastNameInput);
    person.firstName = limitStringLength(firstNameInput);
    person.streetAddress = limitStringLength(streetAddressInput);
    person.city = limitStringLength(cityInput);
    person.zipCode = limitStringLength(zipCodeInput);
    // Assign a unique person number
    person.personNum = numOfPersons;
    cout << "\nA person with number id: " << person.personNum << " was created successfully!" << endl;
    return true;
}

// ----------------------------------------------------------------------------------------------

/** -------------------------------------------------------------------------------------------
  Displays the contents of the persons array
  "size_t iterate" is used to iterate the array
-------------------------------------------------------------------------------------------- **/
void static displayPersons(const Person persons[], size_t size) {
    cout << "Persons List (Total persons created: " << numOfPersons << "):" << endl;
    for (size_t i = 0; i < size; ++i) {
        cout << "Person " << i + 1 << ": "
            << persons[i].personNum << " "
            << persons[i].firstName << " "
            << persons[i].lastName << ", "
            << persons[i].streetAddress << ", "
            << persons[i].city << ", "
            << persons[i].zipCode << endl;
    }
}

// ----------------------------------------------------------------------------------------------

/** -------------------------------------------------------------------------------------------
  Displays a person data
  "size_t index" is the index of the person object in the persons array
-------------------------------------------------------------------------------------------- **/
void static displayAPerson(const Person persons[], size_t index) {
    cout << "Persons List (Total persons created: " << numOfPersons << "):" << endl;
    cout << "Person " << index + 1 << ": "
        << persons[index].personNum << " "
        << persons[index].firstName << " "
        << persons[index].lastName << ", "
        << persons[index].streetAddress << ", "
        << persons[index].city << ", "
        << persons[index].zipCode << endl;
   
}
