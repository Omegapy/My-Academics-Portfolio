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

------------------------------------------------------------ Program 4 Driver's License Exam
*/

#include <iostream>
#include <string>
#include <vector>


using namespace std;

// Global arrays
// Stores the exam's anwsers key
char anwser_key[] = { 'B', 'D', 'A', 'A', 'C', 'A', 'B', 'A', 'C', 'D', 'B', 'C', 'D', 'A', 'D', 'C', 'C', 'B', 'D', 'A' },
	 student_anwsers[20]; // Stores the the student's exam anwsers


// ----------------------------------------------------------------- Functions declaration

// Accepts and validates the user input if it is a character, takes a string as an argument(question to be displayed),
// and returns the validated character input.
char char_check_input(string question);

// Rolls 2 dices 1000 times and stores results.


// Computes the number of combination roolled and displays results


// ----------------------------------------------------------------- Program
int main() {

	// Locoal variable
	int points = 0;

	// Local vector
	vector<int> correct_questions_anwsers;

	// Banner
	cout << "\n                              *************************\n                              * Driver's License Exam *\n                              *************************\n\n";
	cout << "     This program grades the written section of the drive's license exam.\n\n";
	cout << "\n    -- Driver exam questions --\n";

	// Asks 20 questions
	for (int i = 0; i < 20; i++) {
		cout << "\n     Question number-" << i+1 << endl;
		do {
			// Accpts and valitades the input id it is a character
			student_anwsers[i] = char_check_input("Please enter your anwser: ");
			// Checks if the input is valid
			if ((student_anwsers[i] == 'A') || (student_anwsers[i] == 'B') || (student_anwsers[i] == 'C') || (student_anwsers[i] == 'D')) { break; }
			// The input was not valid
			cout << "\n      -- The entered input is not a valid input. It should be a letter (A, B, C or D). Remember to cap your letters --\n";
		} while (true);
	}
	
	// Computes points and correct questions
	for (int i = 0; i < 20; i++) {
		if (student_anwsers[i] == anwser_key[i]) { 
			points++; 
			correct_questions_anwsers.push_back(i);
		}
	}

	//--- Display results
	cout << "\n    -- Results --\n\n"
		<< "    The following questions were anwsered correctly: ";
	// Displays the list of question anwsered correctly
	for (int i = 0; i < correct_questions_anwsers.size(); i++) {
		if ((i % 3) == 0) { cout << endl; }
		cout << "    question-" << correct_questions_anwsers[i] +1;
	}
	
	cout << "\n\n     You got a total of " << points << " points.";
	if (points < 15) {
		cout << "\n     You did not passed the exam. :(";
	}
	else {
		cout << "\n     Congratulation! You passed the exam";
	}

	cout << "\n\n";

	return 0;
}

// ----------------------------------------------------------------- Functions

char char_check_input(string question) {

	/*

	Accepts and validates if the user input if it is a character
	takes a string as an argument (question to be displayed),
	and returns the validated character input.

	*/

	// Local variables
	char char_user_input; // Retunr validated character input
	string user_input;

	cout << "     " << question;

	do { // Validation loop, checks if the user input is an character
		cin >> user_input;
		if (user_input.size() > 1) {
			cout << "\n      -- The entered input is not a valid input. It should be a chraracter. --\n     " << question;
			user_input = '\n';
		}
		else {
			break; // Input is a character 
		}
	} while (true); // True if the input is not a character

	char_user_input = user_input[0];

	return char_user_input;
}