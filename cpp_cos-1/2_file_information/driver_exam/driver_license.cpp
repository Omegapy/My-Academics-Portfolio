
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*-------------------------------*****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *	   Driver's License Exam Re-visit    *                                 |
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


********************************************************************* Program-2: Driver's License Exam Re-visit

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
#include <cctype> // toupper()

using namespace std;

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *	        Function Declaration         *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////


/*
	It is a better an alternative than Window getch()
	if the user needs to see/correct her/his input before pressing enter.
	Accepts and validates if the user input if it is a character
	takes a string as an argument (question to be displayed),
	and returns the validated character input.
*/
char char_check_input(string question);

/*
	Asks the questions and returns the anwsers.
*/
vector<char> exam();

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		          Program                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

int main() {


	//--- variables
	char correct_anwser;
	int points = 0;
	string name;

	//--- Vector
	vector<char>correct_answers, student_anwsers;
	vector<int> student_correct_answers, student_wrong_answers;

	// Opens the file and assigns to it the variable name correct_answers_file
	ifstream correct_answers_file("correctanswers.txt");
	
	try { // Error handler
		if (correct_answers_file.is_open()) { // Checks if the file opened successfully
			while (correct_answers_file >> correct_anwser) { // Stores correct_anwser into a vector
				correct_answers.push_back(correct_anwser);
			}
		}
		else {

			throw "The correctanswers.txt file failed to open.";
		}
	}
	catch (const char *e) { // Catch the exception if it occurs

		cout << "    -- Error --\n    The correctanswers.txt file failed to open!\n\n";
		exit(-1); // exits program

	}

	correct_answers_file.close();

	// Banner
	cout << "\n                              *************************\n                              * Driver's License Exam *\n                              *************************\n\n";
	cout << "     This program grades the written section of the drive's license exam.\n\n";

	cout << "\n    Please enter your name: ";
	getline(cin, name);

	cout << "\n\n    -- Driver exam questions --\n";

	//Asks the questions and returns the anwsers.
	student_anwsers = exam();

	// Computes points and correct questions
	for (int i = 0; i < 20; i++) {
		if (student_anwsers[i] == correct_answers[i]) {
			points++;
			student_correct_answers.push_back(i+1);
		}
		else {
			student_wrong_answers.push_back(i+1);
		}
	}

	//--- Display results
	cout << "\n    -- Results --\n\n"
		<< "    The following questions were anwsered correctly: ";
	// Displays the list of question anwsered correctly
	for (int i = 0; i < student_correct_answers.size(); i++) {
		if ((i % 3) == 0) { cout << endl; }
		cout << "    question-" << student_correct_answers[i];
	}

	cout << "\n\n     You got a total of " << points << " points.";
	if (points < 15) {
		cout << "\n     You did not passed the exam. :(";
	}
	else {
		cout << "\n     Congratulation! You passed the exam";
	}

	cout << "\n\n";

	//------ Save results
	
	// Declares an object file and creates a file
	ofstream student_exam_file(name + "_exam.txt");

	if (student_exam_file.is_open()) { // Checks if the file opened successfully
		
		student_exam_file << name << "\n";
		student_exam_file << "correct questions" << "\n";

		for (int question : student_correct_answers) { // Saves into file
			student_exam_file << question << "\n";
		}

		student_exam_file << "incorrect questions" << "\n";

		for (int question : student_wrong_answers) { // Saves into file
			student_exam_file << question << "\n";
		}

	}
	else {
		cout << "    -- Error --\n    The created file failed to open!";
		return -2; // exits program
	}

	student_exam_file.close();
    return 0;
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		         Functions               *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////

char char_check_input(string question) {
	/*
		It is a better an alternative than Window getch()
		if the user needs to see/correct her/his input before pressing enter.
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

vector<char> exam() {
	/*
		Asks the questions and returns the anwsers.
	*/

	//-- Local variable
	char student_anwser;

	//-- Local vector
	vector<char> student_anwsers;

	// Asks 20 questions
	for (int i = 0; i < 20; i++) {
		cout << "\n     Question number-" << i + 1 << endl;
		do {
			// Accepts and validates the char. input 
			student_anwser = toupper(char_check_input("Please enter your anwser: "));
			// Checks if the input is valid letter
			if (student_anwser >= 'A' && student_anwser <= 'D') { 
				student_anwsers.push_back(student_anwser);
				break; 
			}
			// The input was not valid
			cout << "\n      -- The entered input is not a valid input. It should be a letter (A, B, C or D). Remember to cap your letters --\n";
		} while (true);
	}

	return student_anwsers;
}
