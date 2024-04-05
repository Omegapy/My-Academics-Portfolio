/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 11 / 15 / 2022


1. Date Class

Design a class called Date.  The class should store a date as three (3) integers: month, day, and year.  
There should be member functions to print (display) the date in the following formats:

11/01/16
November 1, 2016
1 November, 2016

Demonstrate this class by writing a complete program implementing it.

HINT: 
You will need a way to convert the integer for the month into the month name. Think arrays or vectors.

Input Validation: 
Do not accept values for the day greater than 31 or less than 1.  
Do not accept values for the month greater than 12 or less than 1.


*/

#include <iostream>
#include <string>

using namespace std;

//******************************************************************** Class

class Date {

	/*
		Stores date and returns date in different format.
		Public variables: 
			month, day and year integers.
		Public methods:
			date_num_format() returns date format " 01/01/2000 "
			date_str_format_1() returns date format " January 1, 2000 "
			date_str_format_2() returns date format " 1 January, 2000 "
	*/

	// Private Array
	string month_str[12] = { "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"};
	
	public:
		
		//--- Public Variables
		int month, day, year;
		
		//--- Public Methods

		string date_num_format() { 
			/*
				Returns date in format " 01/01/2000 "
			*/
			if ((month < 10) && (day < 10)) { // Adds '0' in the front of 1 digit month and day
				return '0' + to_string(month) + "/" + '0' + to_string(day) + "/" + to_string(year);
			}
			else if (month < 10) { // Adds '0' in the front of 1 digit month 
				return '0' + to_string(month) + "/" + to_string(day) + "/" + to_string(year);
			}
			else if (day < 10) { // Adds '0' in the front of 1 digit day 
				return '0' + to_string(month) + "/" + to_string(day) + "/" + to_string(year);
			}
			return to_string(month) + "/" + to_string(day) + "/" + to_string(year); // No '0'
		}

		string date_str_format_1() { // 
			/*
				Returns date in format " January 1, 2000 "
			*/
			return month_str[month-1] + " " + to_string(day) + ", " + to_string(year);
		}
		string date_str_format_2() { 
			/*
				Returns date in format " 1 January, 2000 "
			*/
			return  to_string(day) + " " + month_str[month - 1] + ", " + to_string(year);
		}
};

//******************************************************************** Functions declaration

/* 
	Acceptsand validates the user input it it is an integer,
	takes a string as an argument (question to be displayed), and returns the validated integer input. 
*/ 
int int_check_input(string question); // Utilize by get_month() and get_day()

/*
	Accepts and validates the user's month input,
	and returns the validated month input.
*/
int get_month();

/*
	Accepts and validates the user's day input,
	and returns the validated day input.
*/
int get_day(Date &date);


/*********************************************************************
*					            Program                              *
 *********************************************************************/

int main() {

	// Initializes a Date type object
	Date date;

	//-- Banner
	cout << "\n                              \033[1m*************\n                              *   Dates   *\n                              *************\033[m\n\n";
	cout << "     This program displays user inputed date in sifferent format.\n\n";

	date.month = get_month();
	date.day = get_day(date);
	date.year = int_check_input("Please enter the year: ");

	cout << "\n     First format:  " << date.date_num_format() << "\n" 
		 << "     Second format: " << date.date_str_format_1() << "\n" 
		 << "     Third format:  " << date.date_str_format_2() << "\n\n";
	return 0;
}

//******************************************************************** Functions 

int int_check_input(string question) {

	/*
		Accepts and validates the user input if it is an integer
		takes a string as an argument (question to be displayed),
		and returns the validated integer input.
	*/

	// Local variables
	int user_input;
	char check_input_char;

	cout << "     " << question;

	do { // Validation loop, checks if the user input is an integer
		cin >> user_input;
		cin.get(check_input_char); // Gets the first non-digit character, if no non-digit character were found it returns an empty line, 
		// note that '.' in decimals inputs is a non-digit character.
		if (check_input_char != '\n') {
			cout << "      -- The entered input is not a valid input. It should be an integer. --\n     " << question;
			cin.clear(); // clears any error flag on cin
			cin.ignore(1000, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
		}
		else {
			break; // Input is an integer 
		}
	} while (true); // True if the input is not an integer

	return user_input;
}


int get_month() {

	/*
		Accepts and validates the user'S month input,
		and returns the validated month input.
	*/

	//--- Local variable
	int user_input_month;

	do { // Validates user's month input
		user_input_month = int_check_input("Please enter month in numeric form: ");
		// Max 12 months in a year
		if (user_input_month <= 0 || user_input_month > 12) {
			cout << "      -- The entered input is not a valid month --\n";
		}
		else { break; } // month input is valid
	} while (true); // month input is not valid

	return user_input_month;
}


int get_day(Date &date) {

	/*
		Accepts and validates the user's day input,
		and returns the validated day input.
	*/

	//--- local variable
	int user_input_day;
	bool valid_day;

	do { // validates user's day input
		user_input_day = int_check_input("Please enter day: ");
		// max 31 days in a month minimum 1
		((user_input_day <= 0) || (user_input_day > 31)) ? valid_day = false :
			// 31 days months
			(((date.month == 4) || (date.month == 6) || (date.month == 9) || (date.month == 11)) && (user_input_day > 30)) ? valid_day = false :
			// february 28 days 
			((date.month == 2) && (user_input_day > 28)) ? valid_day = false : // february 28 days 
			// else the day input is valid
			valid_day = true;
		if (valid_day) { break; } // day input is valid
		cout << "      -- the entered input is not a valid day for entered month --\n";
	} while (true); // day input is not valid

	return user_input_day;
}