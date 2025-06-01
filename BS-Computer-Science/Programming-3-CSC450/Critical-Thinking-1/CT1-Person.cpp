
/*=========================================================================================================
    Program Name: Secure Person Management System
    Author: Alejandro (Alex) Ricciardi
    Date: 10/13/2024

    Requirement: C++23

    Program Description:
    This program is a small procedural C++ application that manages a vector of Person objects.
    It tests and implements secure coding practices to mitigate vulnerabilities such as:
    - Buffer overflows
    - Integer overflows
    - Incorrect type conversions
    - Null pointer dereferencing

    Note: Visual Studio 2022 IDE will give a warning when using strncpy, 
    and you'll need to add the line #define _CRT_SECURE_NO_WARNINGS to compile the program. 
    Another alternative is using std::string or strncpy_s for a safer implementation. 
    However, to showcase the vulnerability of buffer overflow when using a char array, 
    this program uses strncpy.
=========================================================================================================*/

#define _CRT_SECURE_NO_WARNINGS

/* ----------------------------------------------------------------------------------------------
      ------------------
     |    Libraries     |
      ------------------
   ---------------------------------------------------------------------------------------------- */

#include <iostream>
#include <string>
#include <climits>    // For UINT_MAX, Maximum size of an unsigned int
#include <stdexcept>  // For exceptions
#include <cstddef>    // For std::size_t, size type use of arrays and strings
#include <cstring>    // For strncpy, strlen
#include <vector>     // For std::vector

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
    char lastName[MAX_STRING_LENGTH + 1];
    char firstName[MAX_STRING_LENGTH + 1];
    char streetAddress[MAX_STRING_LENGTH + 1];
    char city[MAX_STRING_LENGTH + 1];
    char zipCode[MAX_STRING_LENGTH + 1];
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

  Returns true if the incrementation is successful, false if UINT_MAX is reached
  UINT_MAX, Maximum size of an unsigned int
-------------------------------------------------------------------------------------------- **/
static bool incrementNumOfPersons(unsigned& counter);

/** -------------------------------------------------------------------------------------------
  Creates a new Person with only lastName and firstName arguments inputted
  Uses safe string handling to prevent buffer overflows

  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
static bool createPerson(Person& person, const string& lastName, const string& firstName);

/** -------------------------------------------------------------------------------------------
  Creates a new Person with all arguments inputted
  Uses safe string handling to prevent buffer overflows

  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
static bool createPersonFull(Person& person, const string& lastName, const string& firstName,
    const string& streetAddress, const string& city,
    const string& zipCode);

/** -------------------------------------------------------------------------------------------
  Displays the contents of the persons vector
-------------------------------------------------------------------------------------------- **/
static void displayPersons(const vector<Person>& persons);

/** -------------------------------------------------------------------------------------------
  Displays a person's data at the given index in the persons vector
-------------------------------------------------------------------------------------------- **/
static void displayAPerson(const vector<Person>& persons, size_t index);

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
      
    // Variables used to test code vulnerability
    int negativeValue = -5;      // Used for unsigned int vulnerability
    string longString(100, 'A'); // Create a string with 100 'A's for string overflow
    Person* personPtr = nullptr; // Initialize pointer to null for null pointer vulnerability

    // Vector of persons to store person struct objects
    vector<Person> persons;

    /* ---------------------------------
      -------------
     |   Program   |
      ------------- */

    cout << banner << endl; // std::endl forces flushing of the buffer - good practice

    // ---------------------------------- Test 1: Buffer Overflow with Overly Long Strings

    cout << "-------------------------------------------------------------\n"
        << "Test 1: Buffer Overflow with Overly Long Strings\n"
        << "Creates a person with first and last names that are 100 characters long, filled with the letter 'A'.\n"
        << endl;
    // Not expected to fail due to safe string handling
    Person person1;
    if (!createPerson(person1, longString, longString)) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    persons.push_back(person1);
    displayPersons(persons);

    // ---------------------------------- Test 2: Integer Overflow when Creating Many Persons
    cout << "\n-------------------------------------------------------------\n"
        << "Test 2: Integer Overflow when Creating Too Many Persons\n"
        << "Simulate numOfPersons = UINT_MAX, Maximum size of an unsigned int\n"
        << "\nTrying to create a new person"
        << endl;

    numOfPersons = UINT_MAX;
    Person personFail
        ;
    if (!createPerson(personFail, "Doe", "John")) {
        // Expected to fail due to integer overflow security
        cout << "Failed to create person due to integer overflow." << endl;
    }
    // Reset numOfPersons for further tests
    numOfPersons = static_cast<unsigned>(persons.size());

    // ---------------------------------- Test 3: Incorrect Type Conversion
    cout << "\n-------------------------------------------------------------\n"
        << "Test 3: Incorrect Type Conversion" << endl;

    // new person
    Person person2;
    if (!createPerson(person2, "Conversion", "Alexandria")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    persons.push_back(person2);
    displayAPerson(persons, 1); // Index 1

    cout << "\nTrying to assign persons[1].personNum = " << negativeValue 
        <<", which is a negative value\n" << endl;

    // Security measure: Check if personNum is valid
    // Note that to comparator '<' comparates the value after the cast
    if (static_cast<int>(negativeValue) < 0) { 
        cerr << "--- Failed to assign new peraon number ---\n"
            << "\nIncorrect type conversion --- Negative value assigned to personNum.\n" 
            << "The value: " << negativeValue << " will cast as a person number: "
            << static_cast<unsigned>(negativeValue)
            << endl;
    }
    else {
        persons[1].personNum = static_cast<unsigned>(negativeValue);
        cout << "persons[1] number number is: " << persons[1].personNum << "\n"
            << endl;
    }

    displayAPerson(persons, 1);

    // ---------------------------------- Test 4: Null Pointer Dereferencing with Person Pointer
    cout << "\n-------------------------------------------------------------\n"
        << "Test 4: Testing Null Pointer before use - null pointer dereferencing\n"
        << "Checking if personPtr is null, and it is."
        << "But if it was not, displaying person first name."
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

    // new persons
    Person person3;
    if (!createPerson(person3, "More", "Bob")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    persons.push_back(person3);

    Person person4;
    if (!createPersonFull(person4, "Marquez", "Anita", "456 Ai Street", "Robot Town", "77442")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    persons.push_back(person4);

    Person person5;
    if (!createPersonFull(person5, "Wan", "Lu", "777 LLM Street", "AI Town", "77772")) {
        cout << "\n Error --- Failed to create person ---" << endl;
    }
    persons.push_back(person5);

    displayPersons(persons);

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

       Returns true if the incrementation is successful, false if UINT_MAX is reached
       UINT_MAX, Maximum size of an unsigned int
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
  Creates a new Person with only lastName and firstName arguments inputted
  Uses safe string handling to prevent buffer overflows

  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
bool static createPerson(Person& person, const string& lastNameInput, const string& firstNameInput) {
    
    // Increment the global numOfPersons counter
    if (!incrementNumOfPersons(numOfPersons)) {
        return false;
    }

    // lastNameInput to person.lastName 
    strncpy(person.lastName, lastNameInput.c_str(), MAX_STRING_LENGTH); // truncates if necessary
    // C and C++ do not automatically know strings length. Instead, 
    // at the end of a string is marked by the null character '\0'
    person.lastName[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    if (lastNameInput.length() > MAX_STRING_LENGTH) {
        cerr << "Warning --- Input string for lastName exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
    }

    // firstNameInput to person.firstName 
    strncpy(person.firstName, firstNameInput.c_str(), MAX_STRING_LENGTH); // truncates if necessary
    person.firstName[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    if (firstNameInput.length() > MAX_STRING_LENGTH) {
        cerr << "Warning --- Input string for firstName exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
    }

    // Initialize data with "nan" (Not Available)
    strncpy(person.streetAddress, "nan", MAX_STRING_LENGTH);
    person.streetAddress[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    strncpy(person.city, "nan", MAX_STRING_LENGTH);
    person.city[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    strncpy(person.zipCode, "nan", MAX_STRING_LENGTH);
    person.zipCode[MAX_STRING_LENGTH] = '\0'; // Ensure null termination

    // Assign a unique person number
    person.personNum = numOfPersons;
    cout << "\nA person with number id: " << person.personNum << " was created successfully!" << endl;
    return true;
}

// ----------------------------------------------------------------------------------------------

/** -------------------------------------------------------------------------------------------
  Creates a new Person with all arguments inputted
  Uses safe string handling to prevent buffer overflows

  Returns true if person created successfully, false otherwise
-------------------------------------------------------------------------------------------- **/
bool static createPersonFull(Person& person, const string& lastNameInput, const string& firstNameInput,
    const string& streetAddressInput, const string& cityInput,
    const string& zipCodeInput) {
    
    // Increment the global numOfPersons counter if numOfPersons is not reached
    if (!incrementNumOfPersons(numOfPersons)) {
        return false;
    }

    // lastNameInput to person.lastName 
    strncpy(person.lastName, lastNameInput.c_str(), MAX_STRING_LENGTH); // truncates if necessary
    // C and C++ do not automatically know strings length. Instead, 
    // at the end of a string is marked by the null character '\0'           
    person.lastName[MAX_STRING_LENGTH] = '\0'; 
    if (lastNameInput.length() > MAX_STRING_LENGTH) {
        cerr << "Warning --- Input string for lastName exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
    }

    // firstNameInput to person.firstName 
    strncpy(person.firstName, firstNameInput.c_str(), MAX_STRING_LENGTH); // truncates if necessary
    person.firstName[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    if (firstNameInput.length() > MAX_STRING_LENGTH) {
        cerr << "Warning --- Input string for firstName exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
    }

    // streetAddressInput to person.streetAddress 
    strncpy(person.streetAddress, streetAddressInput.c_str(), MAX_STRING_LENGTH); // truncates if necessary
    person.streetAddress[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    if (streetAddressInput.length() > MAX_STRING_LENGTH) {
        cerr << "Warning --- Input string for streetAddress exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
    }

    // cityInput to person.city 
    strncpy(person.city, cityInput.c_str(), MAX_STRING_LENGTH); // truncates if necessary
    person.city[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    if (cityInput.length() > MAX_STRING_LENGTH) {
        cerr << "Warning --- Input string for city exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
    }

    // zipCodeInput to person.zipCode 
    strncpy(person.zipCode, zipCodeInput.c_str(), MAX_STRING_LENGTH); // truncates if necessary
    person.zipCode[MAX_STRING_LENGTH] = '\0'; // Ensure null termination
    if (zipCodeInput.length() > MAX_STRING_LENGTH) {
        cerr << "Warning --- Input string for zipCode exceeded maximum length of "
            << MAX_STRING_LENGTH << " characters and has been truncated." << endl;
    }

    // Assign a unique person number
    person.personNum = numOfPersons;
    cout << "\nA person with number id: " << person.personNum << " was created successfully!" << endl;
    return true;
}

// ----------------------------------------------------------------------------------------------

/** -------------------------------------------------------------------------------------------
  Displays the contents of the persons vector
-------------------------------------------------------------------------------------------- **/
void static displayPersons(const vector<Person>& persons) {
    cout << "Persons List (Total persons created: " << numOfPersons << "):" << endl;
    for (size_t i = 0; i < persons.size(); ++i) {
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
  Displays a person's data at the given index in the persons vector
-------------------------------------------------------------------------------------------- **/
void static displayAPerson(const vector<Person>& persons, size_t index) {
    if (index < persons.size()) {
        cout << "Persons List (Total persons created: " << numOfPersons << "):" << endl;
        cout << "Person " << index + 1 << ": "
            << persons[index].personNum << " "
            << persons[index].firstName << " "
            << persons[index].lastName << ", "
            << persons[index].streetAddress << ", "
            << persons[index].city << ", "
            << persons[index].zipCode << endl;
    }
    else {
        cout << "Index out of range" << endl;
    }
}

