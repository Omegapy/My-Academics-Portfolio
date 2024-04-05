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

--------------------------------------------------- Program 1 
*/

#include <iostream>
using namespace std;

// Variables
int num_of_heads = 0,
	num_rolls_2 = 0, num_rolls_3 = 0, num_rolls_4 = 0, num_rolls_5 = 0, num_rolls_6 = 0,
	num_rolls_7 = 0, num_rolls_8 = 0, num_rolls_9 = 0, num_rolls_10 = 0, num_rolls_11 = 0, num_rolls_12 = 0;

int main() {

	srand(time(NULL)); // set random seed number = system clock time

	// Banner
	cout << "\n                 *************************\n                 * Flip and Roll Program *\n                 *************************\n\n";

	// --- Flip the Coin
	cout << "\n   ------- Flip the Coin -------\n";
	for (int i = 0; i < 50; i++) {
		num_of_heads = num_of_heads + (rand() % 2);
	}
	cout << "\n      The number of heads fliped is : " << num_of_heads
		<< "\n      The number of tails fliped is : " << (50 - num_of_heads);

	// --- Rolls the Dices
	cout << "\n\n   ------- Roll the Dices -------\n";
	for (int i = 0; i < 50; i++) {
		switch (rand() % 6 + 1 + rand() % 6 + 1) {
		case 2:
			num_rolls_2++;
			break;
		case 3:
			num_rolls_3++;
			break;
		case 4:
			num_rolls_4++;
			break;
		case 5:
			num_rolls_5++;
			break;
		case 6:
			num_rolls_6++;
			break;
		case 7:
			num_rolls_7++;
			break;
		case 8:
			num_rolls_8++;
			break;
		case 9:
			num_rolls_9++;
			break;
		case 10:
			num_rolls_10++;
			break;
		case 11:
			num_rolls_11++;
			break;
		case 12:
			num_rolls_12++;
			break;
		default: // an error occured with the output of (rand() % 6 + 1 + rand() % 6 + 1)
			// resets variables and the for loop
			i = -1, num_rolls_2 = 0, num_rolls_3 = 0, num_rolls_4 = 0, num_rolls_5 = 0, num_rolls_6 = 0,
				num_rolls_7 = 0, num_rolls_8 = 0, num_rolls_9 = 0, num_rolls_10 = 0, num_rolls_11 = 0, num_rolls_12 = 0;
			break;
		}
	}
	cout << "\n      The combination number 2 rolled : " << num_rolls_2 << "   The combination number 3 rolled : " << num_rolls_3 << "   The combination number 4 rolled : " << num_rolls_4
		<< "\n      The combination number 5 rolled : " << num_rolls_5 << "   The combination number 6 rolled : " << num_rolls_6 << "   The combination number 7 rolled : " << num_rolls_7
		<< "\n      The combination number 8 rolled : " << num_rolls_8 << "   The combination number 9 rolled : " << num_rolls_9 << "   The combination number 10 rolled : " << num_rolls_10
		<< "\n      The combination number 11 rolled : " << num_rolls_11 << "   The combination number 12 rolled : " << num_rolls_12 << "\n\n   ------------------------\n";

	return 0;
}