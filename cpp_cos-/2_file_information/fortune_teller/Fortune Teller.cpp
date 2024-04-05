
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*-------------------------------*****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		       Fortune Teller            *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 12 / 06 / 2022


											 File Information

You need to submit the entire project FOLDER for both assignments!

1. Fortune Teller

Using the "FORTUNES.txt" file in the modules tab, 
create a program that reads the fortunes from the text file into either a vector or an array (strings or characters).  
Display a prompt for the user to enter the number of their birth month (1 == January, 2 == February, etc.), and then generate a random fortune, 
as being the current fortune for people born in the named month.

Example:
Enter the number of your birth month: 8
Fortune for people born in August: "If it looks back at you from the plate, don't eat it."

INPUT VALIDATION:
Make sure that the program can find the file and read the contents prior to importing the information.
Do not accept numbers less than 1 or greater than 12 for the birth month.


2. Driver's License Exam Re-visit

Using the file "correctanswers.txt" populate the correct answers array for the drivers license exam program.  
Create a text file with the student answers, one letter per line (see the correct answers file for an example).  
Import the student answers from your text file into the program.  After the student answers have been imported, 
the program should compare the student answers to the correct answers and display a message indicating whether the student passed or failed the exam.  
(At least 15 correct answers are required to pass the exam.) Additionally, the total number of correctly answered questions,
and a list showing the question numbers of the questions the student got wrong should all be written to a new text file.

Turn in your .cpp file, student answers file, and final report text file as your submission; you do NOT need to turn in a screen capture.

NOTE:
You do not need an output text file for the first program. You do not need a screen capture for the second program.
When working with output files, some times you need to create the file yourself before the IDE can find it.  
Also the text files need to be in the same folder as your project. 
If you forget to include the correctanswer.txt or FORTUNES.txt files I have copies of those, 
but if you don't submit your student answer text file your program will not work.


********************************************************************* Praogram-1: Fortune Teller


*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*-------------------------------*****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		          Headers                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include <iostream>
#include <string>
#include <vector>
#include <fstream>

using namespace std;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *	        Function Declaration         *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*
	Accepts and validates the user input if it is an integer.
	takes a string as an argument (question to be displayed), and returns the validated integer input.
*/
int int_check_input(string question); // Utilized by get_month()

/*
	Accepts and validates the user's month input,
	and returns the validated month input.
*/
int get_month(string question);

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		          Program                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main() {

	//--- variables
	string fortune;
	int month;

	//--- Vector
	vector<string>fortunes;

	// Opens the file and assigns to it the variable name fortunes_file
	ifstream fortunes_file("FORTUNES.txt"); 

	try { // Error handler
		if (fortunes_file.is_open()) { // Check if the file opened successfully
			while (getline(fortunes_file, fortune)) { // Stores fortune into a vector
				fortunes.push_back(fortune);
			}
		}
		else { // Throw an exception if the file does not open successely
			throw "The FORTUNES.txt file failed to open."; 
		}
	}
	catch (const char *e) { // Catch the exception if it occurs

		cout << "    -- Error --\n    The FORTUNES.txt file failed to open!\n\n";
		exit(-1); // exits program

	}

	fortunes_file.close();

	// utilize by the class ship, its private function position_ship() and std::rnd() funtion
	srand(time(NULL)); // set random seed number = system clock time

	//-- Banner
	cout << "\n                              ********************\n                              *  Fortune Teller  *\n                              ********************\n\n";
	cout << "   Tell us the number of your birth month, and will tell you a fortune.\n\n";


		
	month = get_month("Please enter the number of your birth month: ");
		
	cout << "\n  Your fortune:\n  "
		<< fortunes[rand() % fortunes.size()] << "\n\n";
	

	return 0;

}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		         Functions               *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

int int_check_input(string question) { // Utilized by get_month()
	/*
		Accepts and validates the user input if it is an integer  
		takes a string as an argument (question to be displayed),
		and returns the validated integer input.
	*/

	// -- Local variables
	int user_input;
	char check_input_char;

	cout << "   " << question;

	do { // Validation loop, checks if the user input is an integer
		cin >> user_input;
		cin.get(check_input_char); // Gets the first non-digit character, if no non-digit character were found it returns an empty line, 
		// note that '.' in decimals inputs is a non-digit character.
		if (check_input_char != '\n') { // If the character check is not empty an error message is displayed
			cout << "\n   -- The entered input is not a valid input. The input should be an integer. --\n   " << question;
			cin.clear(); // clears any error flag on cin
			cin.ignore(1000, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
		}
		else {
			break; // Input is an integer
		}
	} while (true); // True if the input is an integer 

	return user_input;
}

int get_month(string question) {
	/*
		Accepts and validates the user's month input,
		and returns the validated month input.
	*/

	//--- Local variable
	int user_input_month;

	do { // Validates user's month input
		user_input_month = int_check_input(question);
		// Max 12 months in a year
		if (user_input_month <= 0 || user_input_month > 12) {
			cout << "\n   -- The entered input is not a valid month --\n";
		}
		else { break; } // month input is valid
	} while (true); // month input is not valid

	return user_input_month;
}