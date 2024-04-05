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

------------------------------------------------------------ Program 2 Get and Display Names
*/

#include <iostream>
#include <string>
#include <vector>

using namespace std;

// Global variable
string first_name;

// ----------------------------------------------------------------- Functions declaration

// Accepts and validates user first name input, takes the first name number as an argument,
// and returns the validated first name as a string data type
string input_last_name(int name_num);

// Stores the first names into a vector and displays the stored first names in reverse order of entry.
void vec_rev_first_name();

// Stores the first names into a character array and displays the stored first names in reverse order of entry.
void array_rev_first_name();

// ----------------------------------------------------------------- Program
int main() {
	
	// Banner
	cout << "\n                              *************************\n                              * Get and Display Names *\n                              *************************\n\n";
	cout << "     This program accepts 10 users' inputted first names, stores the name in a vector,\n     and displays the name in reverse order of entry,\n     then it repeats the process a second time using a character array instead of a vector.\n\n";
	
	vec_rev_first_name();
	cout << endl;
	array_rev_first_name();
	cout << endl;

	return 0;
}

// ----------------------------------------------------------------- Functions

string input_last_name(int name_num) {

	/*
	
	Accepts and validates user first name input, 
	takes the first name number as an argument
	returns the validated first name as a string data type.

	*/

	// Local variable 
	bool comma_in_name; // Used to validate first names with no commas in them

	do { // Accepts and validates user first name input
		comma_in_name = false;
		cout << "      Please enter first name number " << name_num << ": ";
		cin >> first_name;
		cout << endl;
		if (first_name.size() > 20) {
			cout << "      -- The entered name is too long, please enter a name with no more than 20 characters --\n";
		}
		else { 
			// Check if commas are part of the inputted name
			for (int i = 0; i < first_name.size(); i++) {
				if (first_name[i] == ',') {
					cout << "      -- Commas ',' are not accepted in first name --\n";
					comma_in_name = true;
					break;
				}
			}
			if ( !comma_in_name ) { break; } // Valid inputted first name	
		}
	} while (true); // Inputted first name is too long

	return first_name;
}


void vec_rev_first_name() {

	/*
	
	Stores the first names into a vector
	and displays the stored first names in reverse order of entry.
	
	*/

	// local variable
	string validated_first_name; // Used to store input_last_name() results

	// Local vector
	// Stores user inputed first names as strings
	vector<string> string_first_names;

	cout << "      First names to vector!\n";

	// Stores validated first name in vector
	for (int i = 0; i < 10; i++) {
		validated_first_name = input_last_name(i+1);
		string_first_names.push_back(validated_first_name);
	}

	cout << "      First names stored in vector displayed in reverse order of entry:\n      ";

	int j = 10; // reverse counter use to diplay first names
	// Displays the stored first name in reverse order of entry
	for (int i = 0; i < 10; i++) {
		j--;
		cout << string_first_names[j];
		if (j != 0) { cout << ", "; }
	}

	cout << "\n";
}

void array_rev_first_name() {

		/*

		Accepts and validates the user's first names inputs
		stores the first names into a character array,
		and displays the stored first names in reverse order of entry.

		*/

		// Local variables
		int char_array_index = 0; // Index for the array char_first_names
		string validated_first_name, // Used to store input_last_name() results
			name_to_display = "", // Store the characters forming the first name
			rev_name = ""; // It is the first name spelled in reverse

		// Local array
		// Stores user inputed first names as characters
		char char_first_names[210]; // Allocates 20 characters per name, commas ',' as separators, and '\0' null terminator

		cout << "\n      First names to Array!\n";

		// Accepts and validates the user's first names inputs
		for (int i = 0; i < 10; i++) {
			validated_first_name = input_last_name(i + 1);
			// Stores first name in chararter array
			for (int j = 0; j < validated_first_name.size(); j++) {
				char_first_names[char_array_index] = first_name[j];
				char_array_index++;
			}
			if (i != 9) { // Add a comma seperator
				char_first_names[char_array_index] = ',';
				char_array_index++;
			}
		}

		cout << "      First names stored in array displayed in reverse order of entry:\n      ";

		int k = 0; // Counter use to reverse reversed first names
		// Displays the stored first name in reverse order of entry
		while (char_array_index != 0) {
			char_array_index--; // Counts backwards
			// Finds the reversed name in char_first_names
			if ((char_first_names[char_array_index] == ',') || (char_array_index == 0)) {
				if (char_array_index == 0) { // Adds the last character  char_first_names to rev_name
					rev_name.push_back(char_first_names[0]);
				}
				k = rev_name.size(); // Counts backwards
				while (k != -1) { // Reverse reversed first names
					name_to_display.push_back(rev_name[k]);
					k--;
				}
				rev_name = "";
				cout << name_to_display;
				name_to_display = "";
				if (char_array_index != 0) { cout << ", "; }
			}
			else {
				rev_name.push_back(char_first_names[char_array_index]);
			}
		}
		cout << endl;
}