/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 09 / 26 / 2022
RNG and You

Complete the following programs; when finished take a screen capture of the output from your running program and package it with your .cpp file. Submit a zipped folder with your work.

1. Hotel Occupancy

Write a program that calculates the occupancy rate for a hotel; the program should start by asking the user for the number of floors in the hotel.  
A for loop should then iterate once for each floor.  In each iteration, the loop should ask the user for the number of rooms on the floor and how many of them are occupied.  
After all the iterations, the program should display how many rooms the hotel has, how many of them are occupied, how many are unoccupied, and the percentage of rooms that are occupied. 
The percentage may be calculated by dividing the number of occupied rooms by the total number of rooms.

NOTE: It is traditional that no hotel have a 13th floor!  The loop should skip the entire 13th iteration.

INPUT VALIDATION:  Do not accept values less than 13 for the number of floors.  Do not accept a number less than 10 or greater than 24 for the number of rooms per floor.


2.  Random Number Guessing Game

Write a program that generates a random number between 1 and 100 and asks the user to guess what the number is.  
If the user's guess is higher than the random number, the program should display "Too high, try again."  
If the user's guess is lower than the random number the program should display "Too low, try again."  
The program should use a do-while loop that repeats until the user guesses the number correctly.  
The program should also employ a while loop that keeps track of the number of guesses made by the user and, 
once the user guesses the number correctly, displays the number of guesses the user made.

Loops Rubric Grading:

Program 1: CPP File
	20 pts
	Program runs with no errors.
	15 pts
	Input Validation does not catch input errors properly.
	10 pts
	Program has minor errors or requires minor fixes to run correctly.
	0 pts
	Program has serious errors or fails to run
Program 1: Screen Capture
	10 pts
	Full Marks
	0 pts
	No Marks

Program 2: CPP File
	20 pts
	Program runs with no errors.
	15 pts
	Input Validation does not catch input errors properly.
	10 pts
	Program has minor errors or requires minor fixes to run correctly.
	0 pts
	Program has serious errors or fails to run
Program 2: Screen Capture
	10 pts
	Full Marks
	0 pts
	No Marks

Total possible points: 60

------------------------------------------------------------ Program 1
*/

#include <iostream>
#include <string>
#include <iomanip> // std::setprecision

using namespace std;

// -- Variables
int num_of_floors, num_of_rooms, num_of_rooms_occupied, total_rooms = 0, total_rooms_occupied = 0;
string question_room, question_room_occupied;

// -- Functions
// Checks for user valid integer input
int int_check_input( string question ) {

	// Local variables
	int user_input;
	char check_input_char;

	cout << "     " << question;

	while (true) {
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
	}
	return user_input;
}
// Displays error messages if less than 13 floors is entered
void error_floors() {
	cout << "\n     -- Your entered an invalid number of floors. --\n     Note that the hotel can not have less than 13th floors.\n\n";
}
// Displays error messages if less than 10 or more than 24 rooms is entered
void error_rooms() {
	cout << "\n     -- Your entered an invalid number of rooms. --\n     Note that the floors can not have less than 10 or more than 24 rooms.\n\n";
}
// Displays error messages if number of occupided room are entered is greater than the number of rooms in the floor
void error_rooms_occupied() {
	cout << "\n     -- Your entered an invalid number of rooms occupied. --\n     Note that number of occupided rooms can not be less then 0 or greater than the number of rooms in the floor.\n\n";
}

// -- Program
int main() {

	// Banner
	cout << "\n                 *******************\n                 * Hotel Occupancy *\n                 *******************\n\n";
	cout << "     This program calculates the occupancy rate for a hotel.\n     Note that the hotel can not have less than 13 floors,\n     and traditional hotels do not have a 13th floor!\n\n";
	
	// Checks for floors input errors
	while (true) {
		num_of_floors = int_check_input("Please enter the number of floors in the hotel: ");
		if (num_of_floors < 13) { error_floors(); } else { break; } 
	}

	cout << "\n      -- Rooms -- Note that the floors can not have less than 10 or more than 24 rooms.\n";

	for (int i = 0; i < num_of_floors; i++) {

		if (i == 12) { i++; } // Skips the 13th floor

		cout << endl;
		question_room = "Please enter the number of rooms in floor number " + to_string(i + 1) + ": ";
		question_room_occupied = "Please enter the number of rooms in floor number " + to_string(i + 1) + " that are occupied: ";
		
		// Checks for rooms input errors
		while (true) {
			num_of_rooms = int_check_input(question_room);
			if (num_of_rooms < 10 || num_of_rooms > 24) { error_rooms(); }
			else { break; }
		}

		total_rooms = total_rooms + num_of_rooms;

		// Checks for rooms occupied input errors
		while (true) {
			num_of_rooms_occupied = int_check_input(question_room_occupied);
			if (num_of_rooms_occupied < 0 || num_of_rooms_occupied > num_of_rooms) { error_rooms_occupied(); } else { break; }
		}

		total_rooms_occupied = total_rooms_occupied + num_of_rooms_occupied;

	}

	cout << setprecision(2) << fixed; // Display the double variables precision to two decimals 

	cout << "\n   -- Totals --\n      The number of rooms in the hotel is: " << total_rooms
		<< "\n      The number of occupied rooms in the hotel is: " << total_rooms_occupied
		<< "\n      The number of unoccupied rooms in the hotel is: " << total_rooms - total_rooms_occupied
		<< "\n      The percentage of occupied rooms in the hotel is: " << (total_rooms_occupied * 1. / total_rooms) * 100 << "%\n\n";
}