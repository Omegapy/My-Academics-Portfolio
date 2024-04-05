/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro(Alex) Ricciardi
Due date : 09 / 26 / 2022
RNG and You

Complete the following programs; when finished take a screen capture of the output from your running programand package it with your.cpp file.Submit a zipped folder with your work.

1. Hotel Occupancy

Write a program that calculates the occupancy rate for a hotel; the program should start by asking the user for the number of floors in the hotel.
A for loop should then iterate once for each floor.In each iteration, the loop should ask the user for the number of rooms on the floorand how many of them are occupied.
After all the iterations, the program should display how many rooms the hotel has, how many of them are occupied, how many are unoccupied, and the percentage of rooms that are occupied.
The percentage may be calculated by dividing the number of occupied rooms by the total number of rooms.

NOTE: It is traditional that no hotel have a 13th floor!The loop should skip the entire 13th iteration.

INPUT VALIDATION : Do not accept values less than 13 for the number of floors.Do not accept a number less than 10 or greater than 24 for the number of rooms per floor.


2.  Random Number Guessing Game

Write a program that generates a random number between 1 and 100 and asks the user to guess what the number is.
If the user's guess is higher than the random number, the program should display "Too high, try again."  
If the user's guess is lower than the random number the program should display "Too low, try again."  
The program should use a do - while loop that repeats until the user guesses the number correctly.
The program should also employ a while loop that keeps track of the number of guesses made by the user and,
once the user guesses the number correctly, displays the number of guesses the user made.

Loops Rubric Grading :

Program 1 : CPP File
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

Total possible points : 60

------------------------------------------------------------ Program 2
*/

#include <iostream>
#include <string>

using namespace std;

// -- Variables
int guesses = 0, rgn_num, user_guessed_num;

// -- Function
// Checks for user valid integer input
int int_check_input(string question) {

	// Local variables
	int user_input;
	char check_input_char;

	cout << "     " << question;

	do {
		cin >> user_input;
		cin.get(check_input_char); // Gets the first non-digit character, if no non-digit character were found it returns an empty line, 
		// note that '.' in decimals inputs is a non-digit character.
		if (check_input_char != '\n') {
			cout << "\n     -- The entered input is not a valid input. It should be an integer. --\n     " << question;
			cin.clear(); // clears any error flag on cin
			cin.ignore(1000, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
		}
		else {
			break;
		} 
	} while (true);

	return user_input;
}

// Program
int main() {

	srand(time(NULL)); // set random seed number = system clock time

	// Baner
	cout << "\n                 *******************************\n                 * Random Number Guessing Game *\n                 *******************************\n\n";

	cout << "     In this game you need to guess a random generated integer between 1 and 100.\n\n";

	rgn_num = rand() % 100 + 1; // generated integer
	
	do {
		while (true) {
			user_guessed_num = int_check_input("Enter your guess for the random generated number: ");

			if (user_guessed_num < 1 || user_guessed_num > 100) { 
				cout << "\n     -- The entered input is not a valid input. --\n     The guessed number should be an integer between 1 and 100.\n";
			} 
			else { 
				guesses++;
				break; 
			}	
		}	
		if (user_guessed_num > rgn_num) {
			cout << "\n     -- Too high, try again. --\n";
		}
		else if (user_guessed_num < rgn_num) {
			cout << "\n     -- Too low, try again. --\n";
		}
	} while (user_guessed_num != rgn_num);

	cout << "\n      The random generated number was: " << rgn_num
		 << "\n      It took you " << guesses << " guesses to get it right!\n\n";
	
	return 0;
}