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

------------------------------------------------------------ Program 1 Celsius Temperature Table
*/

#include <iostream>
#include <string>

using namespace std;

// -- Function declaration
double Celsius(double temp);

// -- Program
int main() {

	// Banner
	cout << "\n                 *****************************\n                 * Celsius Temperature Table *\n                 *****************************\n\n";
	cout << "     This program coverts and displays a table of Fahrenheit temperatures into Celsius temperatures.\n\n";
	
	for (int i = 32; i < 93; i = i + 6) {
		cout << "\n     Fahrenheit: " << i << "     Celsius: " << round(Celsius(i));
	}
	
	cout << "\n\n ";

	return 0;
}

// -- Function 
double Celsius(double temp) {

	return (temp - 32) * 5/9;

}
