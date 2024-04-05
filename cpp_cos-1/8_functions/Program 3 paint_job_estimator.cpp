/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 10 / 04 / 2022
Functions

Complete the following programs; take screen captures of your output, package them with your .cpp source files and submit in a zipped folder.

1. Celsius Temperature Table

	The formula to convert a temperature from Fahrenheit to Celsius is:

	C = (F - 32) * 5/9   < With F being the Fahrenheit temp and C being the Celsius temp.>

	Write a function called Celsius that accepts the Fahrenheit temperature as an argument.
	The function should return the temperature after it has been converted to Celsius.
	Demonstrate the function by putting it in a loop that displays first the Fahrenheit temperature and
	then the Celsius equivalent temperature every 6 degrees between 32 degrees Fahrenheit and 92 degrees Fahrenheit.
	Use proper headings and spacing to make the output easy to read.

2.  Winning Sales Division

	Write a program that determines which of a company's eight divisions (Northeast, Southeast,
	NorthCentral, SouthCentral, NorthPlains, SouthPlains, Northwest, Southwest) had the greatest sales for a quarter.
	The program should include the following two functions, both of which will be called by main.

	double getSales( )  is passed the name of a division; it will ask the user for a division's quarterly sales figure, validate that input, then return it.
	This function should be called once for each division.

	void findHighest( )  is passed all eight sales totals.  It will determine which is the largest and print the name of the corresponding sales division and sales figure.

	INPUT VALIDATION:  Do not accept values lower than $0.01 for the sales figure.

3. Paint Job Estimator

	A painting contractor has determined that for every 115 square feet of wall space, 1 gallon of paint and 6 hours of labor will be required.
	The company charges $54.00 per hour for labor.  Write a modular program that allows the user to enter the number of rooms to be painted,
	the price of paint per gallon, and then the square footage of each room.  The program should then display the following information properly spaced and labelled:

		The number of gallons of paint required.
		The total hours of labor needed. (This is a union job, so assume they'll be taking breaks and not working more than 10 hours per day. Divide up into working days if necessary.)
		The total cost of the paint.
		The labor charges.
		The total cost of the paint job.

	INPUT VALIDATION: Do not accept a value lower than 1 for the number of rooms; all rooms must have at least 85 square feet of wall space to be painted.
	The average cost of the paint is $32.50 per gallon, do not accept values lower 75% of that price or greater than 1.25 times that price.

Functions Rubric Grading:

	Program 1 Celsius Temperature Table: CPP File
		15 pts
		Program runs and performs the requirements without errors.
		8 pts
		Program runs with minor errors or fails to perform as intended
		0 pts
		Program fails to run
		Program 1: Screen Capture
			5 pts
			Full Marks
			0 pts
			No Marks
		Total: 20 pts

	Program 2 Winning Sales Division: CPP File
		15 pts
		Program runs and performs the requirements without errors.
		8 pts
		Program runs with minor errors or fails to perform as intended
		0 pts
		Program fails to run
		Program 2: Screen Capture
			5 pts
			Full Marks
			0 pts
			No Marks
		Total: 20 pts

	Program 3 Paint Job Estimator: CPP File
		15 pts
		Program runs and performs the requirements without errors.
		8 pts
		Program runs with minor errors or fails to perform as intended
		0 pts
		Program fails to run
		Program 3: Screen Capture
			5 pts
			Full Marks
			0 pts
			No Marks
		Total: 20 pts

	Total possible points: 60

------------------------------------------------------------ Program 3 Paint Job Estimator
*/

#include <iostream>
#include <string>
#include <iomanip> // std::setprecision

using namespace std;

// Global variables
int total_gallons_paint, total_labor_hours;
double total_walls_square_feet, total_paint_cost, total_labor_cost, total_paint_job_cost;
bool valided_zero = false; // The user acknowledged that the room will be not painted

// ----------------------------------------------------------------- Functions declaration
// Checks if input is a number
double num_check_input(string question);

// Checks if input is an integer
int int_check_input(string question);

// Gets input from user, the number of rooms and the walls square feet for each room, 
// computes and returns the total of walls square feet
double get_walls_square_feet();

// User Validation if inputed room walls square feet is less than 85, return square foot to be painted 
// Returns square feet = 0 if user validated inputed of the room walls square feet is less than 85
double room_walls_less_85(double square_feet, int i);

// Computes and returns the upward rounded number of gallons needed for the job 
int num_gallons_pain(double total_square_feet);

// Gets input from user, the price of the paint,
// computes and returns the the cost of the paint
double get_paint_cost(int gallons_paint);

// Computes and returns the number of labor hours needed for the job
int num_labor_hours(double total_square_feet);

// Computes and returns the labor cost
double labor_charge(int labor_hours);


// ------------------------------------------------------------------ Program
int main() {

	// Banner
	cout << "\n                 ***********************\n                 * Paint Job Estimator *\n                 ***********************\n\n";
	cout << "     This program allows the user to enter the number of rooms to be painted,\n     the price of paint per gallon, and the square footage of each room.\n     Then the program will display an invoise.\n\n";

	total_walls_square_feet = get_walls_square_feet();
	total_gallons_paint = num_gallons_pain(total_walls_square_feet);
	total_paint_cost = get_paint_cost(total_gallons_paint);
	total_labor_hours = num_labor_hours(total_walls_square_feet);
	total_labor_cost = labor_charge(total_labor_hours);
	total_paint_job_cost = total_paint_cost + total_labor_cost;

	cout << setprecision(2) << fixed; // Display the double variables precision to two decimals 

	cout << "\n\n      ******** Invoice ********\n"
		<< "\n      The number of gallons of paint required: " << total_gallons_paint
		<< "\n      The total hours of labor needed:         " << total_labor_hours
		<< "\n      The total cost of the paint:             $" << total_paint_cost
		<< "\n      The labor charges:                       $" << total_labor_cost
		<< "\n      The total cost of the pain job:          $" << total_paint_job_cost
		<< "\n\n";

	return 0;
}

// ---------------------------------------------------------------- Functions

double num_check_input(string question) { // --- Checks if input is a number
	
	// Local variables
	double user_input;
	char check_input_char = '\n';

	cout << "     " << question;

	do {
		cin >> user_input;
		cin.get(check_input_char); // Gets the first non-digit character, if no non-digit character were found it returns an empty line, 
		if (check_input_char != '\n' && check_input_char != '.') {
			cout << "\n      -- The entered input is not a valid input. It should be a number. --\n     " << question;
			cin.clear(); // clears any error flag on cin
			cin.ignore(1000, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
		}
		else {
			break;
		}
	} while (true);

	return user_input;
}


int int_check_input(string question) { // --- Checks for user valid integer input
	
	// Local variables
	int user_input;
	char check_input_char;

	cout << "     " << question;

	do {
		cin >> user_input;
		cin.get(check_input_char); // Gets the first non-digit character, if no non-digit character were found it returns an empty line, 
		// note that '.' in decimals inputs is a non-digit character.
		if (check_input_char != '\n') {
			cout << "\n      -- The entered input is not a valid input. It should be an integer. --\n     " << question;
			cin.clear(); // clears any error flag on cin
			cin.ignore(1000, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
		}
		else {
			break;
		}
	} while (true);

	return user_input;
}

double room_walls_less_85(double square_feet, int i) { // --- User Validation if inputed room walls square feet is less than 85, return square foot to be painted 
													   // --- Returns square feet = 0 if user validated inputed of the room walls square feet is less than 85
// local varible 
	string yes_or_no;

	cout << "\n       -- A room with a walls square feet less than 85 will not be painted --\n";
	cout << "       Enter 'yes' if you want to renter a difference value for the room walls square feet\n";
	cout << "       or enter 'no', by enetering 'no' you acknowledge that room will be not painted: ";
	do {
		cin >> yes_or_no;
		cout << endl;
		if (yes_or_no == "yes") {
			square_feet = num_check_input("Please enter the total walls square feet for room number " + to_string(i) + ": ");
			break;
		}
		else if (yes_or_no == "no") {
			square_feet = 0;
			valided_zero = true; // The user acknowledged that the room will be not painted
			break;
		}
		cout << "       -- Invalid input entered, please enter 'yes' or 'no': ";
	} while (true);

	return square_feet;
}

double get_walls_square_feet() { // --- Gets input from user, the number of rooms and the walls square feet for each room, 
								// --- computes and returns the total of walls square feet
	// Local variables
	int num_of_rooms = 0 ;
	double room_walls_square_feet = 0, total = 0;
	string question;

	do {
		num_of_rooms = int_check_input("Please enter the number of rooms that need to be painted: ");
		if (num_of_rooms < 1) {
			cout << "\n       -- The entered input is not valid, the number of room can be less than 1 --\n";
		} else { break; }
	} while (true);
	cout << endl;
	for (int i = 1; i < num_of_rooms + 1; i++) {
		valided_zero = false; // Reset the user acknowledgment that the room will be not painted
		room_walls_square_feet = num_check_input("Please enter the total walls square feet for room number " + to_string(i) + ": ");
		while (room_walls_square_feet < 85 && !valided_zero) {
			room_walls_square_feet = room_walls_less_85(room_walls_square_feet, i);
		}
		total = total + room_walls_square_feet;
	}

	return total;
}

int num_gallons_pain(double total_square_feet) { // ---  Computes and returns the upward rounded number of gallons need for the job 
	// Local variables
	double feet_square_per_gallon = 115;
	return ceil(total_square_feet / feet_square_per_gallon); 
}

double get_paint_cost(int gallons_paint) { // --- Gets input from user, the price of the paint
									       // --- computes and returns the cost of the paint for the job
	// Local variables
	double avg_paint_price = 32.50, inputed_paint_price = 0, feet_square_per_gallon = 115;

	cout << endl;
	do {
		inputed_paint_price = num_check_input("Please enter the paint's price per gallon: ");
		if (inputed_paint_price < avg_paint_price * 0.75) {
			cout << "\n     -- The entered paint's price is too cheap choose a different paint! --\n";
		}
		else if (inputed_paint_price > avg_paint_price * 1.25) {
			cout << "\n     -- The entered paint's price entered is too expensive choose a different paint! --\n";
		}
		else { break; }
	} while (true);

	return gallons_paint * inputed_paint_price; 

}

int num_labor_hours(double total_square_feet) { // --- Computes and returns the number of labor hours needed for the job
	
	// Local variables
	int full_10_hours_days;
	double square_feet_per_hour = 115, total_hours, remaining_hours;

	total_hours = total_square_feet / square_feet_per_hour;

	// Note that the workers take a 15mn break evrery 4 hours in a day and do not work more than 10 hours
	if (total_hours < 10) { // less than one 10 hour day
		// The workers got 15mn break
		remaining_hours = total_hours;
	}
	else {
		// Computes 10 hours work days and breaks
		full_10_hours_days = floor(total_hours / 10);
		remaining_hours = total_hours - (full_10_hours_days * 10);
		total_hours = total_hours + (full_10_hours_days / 2.0); // adds to total an 1/2 hour payed break per day
	}
	// Checks if workers got break from the remaining hours 
	if (remaining_hours >= 8) { // less then 10 hours worked but equal or more than 8 hours worked, 1/2 hour payed break added to total
		total_hours = total_hours + 0.5; 
	}
	else if (remaining_hours >= 4) { // less then 8 hours worked but equal or more than 4 hours worked, 15mn payed break added to total
		total_hours = total_hours + 0.25;

	}

	return ceil(total_hours); // Most businesses round upward the hours needed to perform a task
}

double labor_charge(int labor_hours) { // --- Computes and returns the labor cost
	// Local variables
	double cost_per_hour = 54.00;
	return labor_hours * cost_per_hour;
}
