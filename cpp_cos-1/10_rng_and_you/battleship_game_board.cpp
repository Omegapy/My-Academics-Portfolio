/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 09 / 20 / 2022
RNG and You

Using the random number generation that was covered in class, create the following programs:

Program 1:
- Flip a coin 50 times and get the number of heads flipped and the number of tails flipped.
- Roll two 6-sided dice 50 times and record the number of times each combination of numbers (2-12) is rolled.
- Display these to the screen with proper labels and spacing.

Program 2:
- A Battleship game board is 10 x 10.
- The PT Boat holds 2 pegs,
- the submarine and Frigate hold 3,
- the Battleship 4
- and the Aircraft carrier 5.
Based on this information, use random numbers to figure out the average number of turns it will take to sink all five ships over 5 games of Battleship.

Place your screen captures and .cpp files in a folder, zip that folder and submit it.

Hints:

	1. This isn't as complicated as it looks, so don't try to make it more complicated than it is.

	2. Get a random number between 0 & 1 (see sample program). Track the number of 0's and number of 1's. Do that 50 times.
	   Use a switch statement for the dice. (See week 3's menu template for an example of a switch statement.)

	3. 10 * 10 == 100.  2+3+3+4+5 == 17.  Get a random number between 1-100 (0-99, don't forget the computer starts at 0!)
	   And if that number is between 1 and 17 (0-16) you hit a ship. Each time you get a new random number is 1 turn.
	   Record number of turns. Repeat until you get 17 hits. Repeat that process 5 times.  Take the average.
	   Yes, it will be a long program. Copy/Paste is your friend (make sure the code works before you copy/paste).

	4. Have a good weekend.

Grading:

Program 1: CPP File
	20 pts
	Program runs and performs the requirements without errors.
	10 pts
	Program has minor errors or does not perform to requirements
	0 pts
	Program has serious errors or fails to run
Program 1: Screen Capture
	10 pts
	Full Marks
	0 pts
	No Marks

Program 2: CPP File
	20 pts
	Program runs and performs the requirements without errors.
	10 pts
	Program has minor errors or does not perform to requirements
	0 pts
	Program has serious errors or fails to run
Program 2: Screen Capture
	10 pts
	Full Marks
	0 pts
	No Marks

Total possible points: 60

------------------------------------------------------------- Program 2
*/

#include <iostream>
using namespace std;

// Variables
int hits = 0,
	turns = 0,
	n;

int main() {
	
	srand(time(NULL)); // set random seed number = system clock time

	// Baner
	cout << "\n                 *********************************\n                 * Battleship Game Board program *\n                 *********************************\n\n";

	// ------ The 5 games
	for (int i = 1; i < 6; i++) { // 5 games
		// Counts hits and turns, every 17 hits loop ends, 
		// hits is not reset to O at the beginning of a new game, insteat it is compared to (17 * i), with i being the game number.
		while (hits < 17 * i) { 
			if (rand() % 100 + 1 <= 17) { hits++; } //  rng number is between 1 and 17 is a hit
			turns++; 
		}  
	}
	cout << "\n    The average number of turns to sink all five ships over 5 games of Battleship is: " << turns << " / 5 = " << (turns / 5.) << endl;
	
	return 0;
}