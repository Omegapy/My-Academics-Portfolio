/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 10 / 11 / 2022
Functions

1. Full Moons
	Using the data provided below, create a program that stores the dates of the full moons for the rest of 2022 in a integer array.
	Have the user enter the current date (i.e. 02 27) and return the number of days until the next full moon. Full moon information can be found at THIS Links to an external site.
	"https://www.calendar-12.com/moon_phases/2022".
		If the user enters a date that is past the full moon for the current month the program should move to the next month.
		If the user enters a date after December 18th the program should return an error message.
	INPUT VALIDATION:
		Do not accept numbers above 31 as the day for the date in March, May, July, August,
		October or December and do not accept a number above 30 for April, June, September or November.
		Do not accept a number below 10 or above 12 for the month.
	Hint:
		You don't have to use the date entered by the user!
		(You do still need the user to enter the date though.)
		If you #include <ctime> you can get the current date from the system clock!
		Search for ctime and getdate() for c++.

2. Get and Display Names
	Ask the user for a first name and store it in a vector of strings. Do this 10 times.
	After the final name, print the names to the screen in reverse order of entry.
	Then do this with a second set of 10 names using a character array. The amount of space allocated for each name should be at least 15 characters.
	(REMEMBER: The final place in an array holds the null terminator; this is not counted as a character!)

3. Revisiting: RNG and You
	Flip a coin 500 times and store the information in a vector.
	Using a for loop, get the number of heads flipped and subtract this from the total size of the vector using size().
	Roll two 6-sided dice 1000 times and record the number of times each combination of numbers (2-12) is rolled.
	Display these to the screen with proper labels and spacing.
	(Yes, you can just modify your existing code rather than writing it all from scratch. Make sure you get your numbers correct though.)

4. Driver's License Exam
	The local Driver's License Office has asked you to write a program that grades the written section of the drive's license exam.
	The exam has 20 multiple choice questions; the correct answers are below:
		1. B   2. D   3. A   4. A   5. C   6. A   7. B   8. A   9. C   10. D
		11. B   12. C   13. D   14. A  15. D   16. C  17. C   18. B   19. D   20. A
	Your program should store the correct answers (show above) in an array.
	It should ask the user to enter the student's answers for each of the 20 questions and store the answers in a second array.
	After the student answers have been entered, the program should display a message indicating whether the student passed or failed the exam.
	(At least 15 correct answers are required to pass the exam.)  The program should then display the total number of correctly answered questions,
	and a list showing the question numbers of the questions the student got wrong.
	Input Validation:
		Only accept the letters 'A', 'B', 'C' and 'D' as answers.

Note that there is now a criteria in the grading for your comments in the program.
You need to start commenting about what things do, where variables are being used (especially if you are passing them to functions)
and your loops/conditionals. Switch statements are conditionals. Purposes of functions. I won't be jumping on you hard over this (yet).
But I will be leaving comments in the rubric for your submissions, so make sure you check that. (If you want a sample, look at the paintJobEstimator_Sample file in module 6.)
Larger programs with longer and more complex loops or conditionals would need more detailed comments around those items,
and comments for functions as well. Functions should have at least a minimal comment detailing what the purpose of the function is.

Functions Rubric Grading:

	Program 1, 2 , 3 and 4 : CPP File
			10 pts
			Program runs and performs the requirements without errors.
			4 pts
			Program runs with minor errors or fails to perform as intended
			0 pts
			Program fails to run
		Program 1: Comments
			5 pts
			Proper comments on variables, functions and loops; comments detail whys, whats, and hows.
			3 pts
			Minor commenting done; or only bare details provided.
			0 pts
			No comments.
		Program 1: Screen Capture
			5 pts
			Full Marks
			0 pts
			No Marks
		Total: 20 pts
	Program 2 Get and Display Names: CPP File
			10 pts
			Program runs and performs the requirements without errors.
			4 pts
			Program runs with minor errors or fails to perform as intended
			0 pts
			Program fails to run
		Program 2: Comments
			5 pts
			Proper comments on variables, functions and loops; comments detail whys, whats, and hows.
			3 pts
			Minor commenting done; or only bare details provided.
			0 pts
			No comments.
		Program 2: Screen Capture
			5 pts
			Full Marks
			0 pts
			No Marks
		Total: 20 pts

Total possible points: 80

------------------------------------------------------------ Program 3 Revisiting: RNG and You
*/

#include <iostream>
#include <string>
#include <vector>

using namespace std;

// Global vector
// Stores rolls results; utlized by role_dices() and display_com_rolls()
vector<vector<int>>rolls;

// ----------------------------------------------------------------- Functions declaration

//	Flips a coins 500 times and displays how many times head and tail were respectively flipped.
void flip_a_coin();

// Rolls 2 dices 1000 times and stores results.
void roll_dices();

// Computes the number of combination roolled and displays results
void display_com_rolls();

// ----------------------------------------------------------------- Program
int main() {

	// Banner
	cout << "\n                              ***************************\n                              * Revisiting: RNG and You *\n                              ***************************\n\n";
	cout << "     This program flips a coin 500 times and reports how many times head and tail were respectively flipped.\n     Then rolls two 6 dices 1000 times and reports the number of times the combination (2-12) was rolled.\n\n";

	cout << "\n     ------- Flip the Coin -------\n\n";
	flip_a_coin();

	cout << "\n\n     ------- Roll the Dices -------\n";
	roll_dices();
	display_com_rolls();

	cout << "\n\n"; 

	return 0;
}

// ----------------------------------------------------------------- Functions

void flip_a_coin() {

	/*
	
	Flips a coins 500 times 
	and displays how many times head and tail were respectively flipped.
	
	*/

	// Local variable
	int num_heads = 0;
	
	// Local vector
	// Stores flips results
	vector<int> flips;

	
	srand(time(NULL)); // set random seed number = system clock time

	// Flips the coin
	for (int i = 0; i < 500; i++) {
		 flips.push_back(rand() % 2); // Generate random numbers, with a range of 2, 0 or 1
	}
	// Counts thw number of heads flipped
	for (int i = 0; i < flips.size(); i++) {
		num_heads = num_heads + flips[i];
	}
	
	cout << "     The number of head flipped is  " << num_heads
		<< "\n     The number of tails flipped is " << flips.size() - num_heads;
}

void roll_dices() {

	/*

	Rolls 2 dices 1000 times and stores results.

	*/

	// Local vector
	// Stores rolls dices rolls
	vector<int> dice_1; vector<int> dice_2;


	srand(time(NULL)); // set random seed number = system clock time

	// Roll the dices
	for (int i = 0; i < 1000; i++) {
		// Generate random numbers, with a range 1 to 6
		dice_1.push_back(rand() % 6 + 1); // dice 1
		dice_2.push_back(rand() % 6 + 1); // dice 2
	}

	rolls.push_back(dice_1);
	rolls.push_back(dice_2);
}

void display_com_rolls() {

	/*
	
	Computes the number of combination roolled and displays results.
	
	*/

	// Local array
	// Stores the number of combinations (2-12) rolled
	int combinations[11][2] = { {2, 0}, {3, 0}, {4, 0}, {5, 0}, {6, 0}, {7, 0}, {8, 0}, {9, 0}, {10, 0}, {11, 0}, {12, 0} };

	// Computes the number of combinatios 
	for (int i = 0; i < 1000; i++) {
		switch (rolls[0][i] + rolls[1][i]) {
		case 2:
			combinations[0][1] = combinations[0][1] + 1;
			break;
		case 3:
			combinations[1][1] = combinations[1][1] + 1;
			break;			
		case 4:				
			combinations[2][1] = combinations[2][1] + 1;
			break;			
		case 5:				
			combinations[3][1] = combinations[3][1] + 1;
			break;			
		case 6:				
			combinations[4][1] = combinations[4][1] + 1;
			break;			
		case 7:				
			combinations[5][1] = combinations[5][1] + 1;
			break;			
		case 8:				
			combinations[6][1] = combinations[6][1] + 1;
			break;			
		case 9:				
			combinations[7][1] = combinations[7][1] + 1;
			break;
		case 10:			
			combinations[8][1] = combinations[8][1] + 1;
			break;			
		case 11:			
			combinations[9][1] = combinations[9][1] + 1;
			break;
		case 12:
			combinations[10][1] = combinations[10][1] + 1;
			break;
		}
	}
	// Display the results
	for (int i = 0; i < 11; i++) {
		cout << "\n     The combination " << combinations[i][0] << " rolled " << combinations[i][1] << " times.";
	} 
}
