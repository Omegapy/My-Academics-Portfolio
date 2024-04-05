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

------------------------------------------------------------ Program 2 Winning Sales Division
*/

#include <iostream>
#include <string>

using namespace std;

// Global arrays
string divisions_name[8] = { "Northeast", "Southeast", "NorthCentral", "SouthCentral", "NorthPlains", "SouthPlains", "Northwest", "Southwest" };
double sales_figures[8] = {};

// -- Functions declaration
// Checks if input is a number
double num_check_input(string question);
// Asks the user for a division's quarterly sales figure
double getSales(string div_name);
// Find the highest quarterly sales figure
void findHighest(double divisions_figures[]);

// ----------------------------------------------------------------- Program
int main() {

	// Banner
	cout << "\n                 **************************\n                 * Winning Sales Division *\n                 **************************\n\n";
	cout << "     This program determines which of a company's eight divisions has the greatest sales for a quarter.\n\n";
	
	for (int i = 0; i < size(divisions_name); i++) { 
		sales_figures[i] = getSales(divisions_name[i]); 
		
	}

	findHighest(sales_figures);

	return 0;
}

// --------------------------------------------------------------- Functions
// Checks if input is a number
double num_check_input(string question) {

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
// Asks the user for a division's quarterly sales figure
double getSales(string div_name) {

	// Local variable
	double input_sales_figure;

	do {
		input_sales_figure = num_check_input("Please enter " + div_name + " devision quarterly sales figure: ");
		cout << endl;
		if (input_sales_figure < 0.01) {
			cout << "      -- The entered input is not valid, the devision quarterly sales figure's value can not be lower than $0.01. --\n";
		}
		else { 
			break; }
	} while (true);

	return input_sales_figure;
}

// Find the highest quarterly sales figure
void findHighest(double divisions_figures[]) { 
	
	// Local variable
	double highest_sales = 0;
	string div_name;
	bool two_highest_sales = false;

	for (int i = 0; i < size(divisions_name); i++) {
		if (highest_sales < divisions_figures[i]) {
			highest_sales = divisions_figures[i];
			div_name = divisions_name[i];
			two_highest_sales = false;
		}
		// Checks if 2 divisions have the largest sales figure
		else if (highest_sales == divisions_figures[i]) {
			div_name = div_name + " and " + divisions_name[i];
			two_highest_sales = true;
		}
	}
	
	if (two_highest_sales) {
		cout << "\n    Two divisions have the Largest quarterly sales figure and they are " << div_name << " with a $" << highest_sales << " quarterly sales figure.\n\n";
	
	}
	else {
		cout << "\n    The division with the Largest quarterly sales figure is " << div_name << " with a $" << highest_sales << " quarterly sales figure.\n\n";
	}

}
