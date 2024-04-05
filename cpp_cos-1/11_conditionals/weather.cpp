/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 09 / 13 / 2022
Conditional Statements

This is a two part assignment: Part 1 consists of creating a flowchart diagram; part 2 will be writing a program to match that diagram.

Part 1:  Create a flowchart using the tools in the Useful Resources module of how you should dress based on the following weather conditions:
- Temperature over 80 degrees Fahrenheit (temp>80);
- Temperature over 50 degrees Fahrenheit (temp<80 && temp>50);
- Temperature below 32 degrees Fahrenheit (temp<32);
- Raining (note that if the temperature is below 32 degrees Fahrenheit and it is raining then we consider that to be snowing).
The check for rain can be a simple yes or no ('y' or 'n').

Part 2: Based on your flowchart, create a C++ program that follows the same process. You will need to use conditional statements for this program.
When the program is complete, run the program 2 times with different criteria, take screen captures of BOTH sets of results!
(You should be asking the user for the temperature and whether or not it is raining.)

Package your screen captures, flowchart and .cpp file into a zipped folder and turn that in.

Grading:

Part 1: UML/Flowchart
the follows the proper logic for attire selection
10 pts Full Marks
0 pts No Marks

Part 2: Program .cpp file
This criterion is linked to a Learning Outcome
7 pts
Program runs and performs the requirements without errors.
3 pts
Program runs but does not perform to the requirements or has errors.
0 pts No Marks

Two screen captures of the running program
This criterion is linked to a Learning OutcomeTwo screen captures of the running program
3 pts
Student submitted a screen shots of program output that is readable
0 pts No Marks

Total Points: 20
*/


#include <iostream>

using namespace std;

// Variables
int temp;
string precipitation;
string chance_of_precipitation;
string feels;
char check_input_char;

int main() {

	// Banner
	cout << "\n                 *****************************************\n                 * Weather Condition in Cheyenne Wyoming *\n                 *****************************************\n\n";
	// User inpute temperature
	cout << "\n\n    Please enter the temperature in degrees Fahrenheit: ";

	// User input temp and Checks for valid integer input
	while (true) {
		cin >> temp;
		cin.get(check_input_char); // Gets the first non-digit character, if no non-digit character were found it returns an empty line, 
								   // note that '.' in decimals inputs is a non-digit character.
		if (check_input_char != '\n') {
			cout << "\n    The entered input is not a valid input.\n    Please enter the temperature in degrees Fahrenheit, as a whole number: ";
			cin.clear(); // clears any error flag on cin
			cin.ignore(1000, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
		}
		else { 
			break; 
		}
	}

	// Assigns values to the varaibles feels and precipitation
	(temp <= 32) ? precipitation = "snow" : precipitation = "rain";
	// Note that I added an extra temperature bracket, not required by the assignment, it makes sense with my program to have it.
	(temp > 80) ? feels = "hot" : 
		(temp <= 80 && temp > 50) ? feels = "warm" : 
			(temp <= 50 && temp > 32) ? feels = "chilly" : feels = "cold"; // temp =< 32
				
	// User input chance_of_precipitation and Checks for valid yes or no input
	cout << endl;
	while (true) {
		cout << "    Please enter 'y' if it is "
			 << precipitation
			 << "ing or 'n' if it is not "
			 << precipitation
			 << "ing: ";
		cin >> chance_of_precipitation;
		cout << endl;
		// Checks chance_of_precipitation input
		if (chance_of_precipitation == "y") {
			cout << "    Today in Cheyenne Wyoming is a "
				 << feels
				 << " "
				 << precipitation
				 << "y day.\n";
			if (precipitation == "snow") {
				cout << "    You should dress warm and put snow boots on!\n";
			}
			else if ((precipitation == "rain") && (feels == "chilly")) {
				cout << "    You should dress warm and put rain boots on!\n";
			}
			else {
				cout << "    You should wear a t-shirt and shorts with rain boots!\n";
			}
			break;	
		} 
		else if (chance_of_precipitation == "n") {
			cout << "\n    Today in Cheyenne Wyoming is a "
				 << feels
				 << " day with no "
				 << precipitation
				 << ".\n";
			if ((feels == "chilly") || (feels == "cold")) {
				cout << "    You should dress warm!\n";
			}
			else {
				cout << "    You should wear a t-shirt and shorts!\n";
			}
			break;

		}
		// Else invalid input entered
		cout << "    The entered input is not a valid input.\n";
		cin.clear(); // clears the error flag on cin
		cin.ignore(256, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
	}

	return 0;
}