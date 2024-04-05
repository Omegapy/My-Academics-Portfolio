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

------------------------------------------------------------ Program 1 Full moon
*/

#include <iostream>
#include <string>
#include <vector>

using namespace std;

// Global arrays
// Stores the month/day of full moons for 2022 utilized by num_days_full_moon()
int full_moon_dates_2022[][2] = {{1, 17}, {2,16}, {3,18}, {4, 16}, {5, 15}, {6, 14}, {7, 13}, {8, 11}, {9, 10}, {10, 9}, {11, 8}, {12, 7}};
// Stores the number of days in each for 2022, utilized by num_days_full_moon()
int num_days_in_months_2022[] = { 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 };

// ----------------------------------------------------------------- Functions declaration

// Accepts and validates the user input it it is an integer, 
// takes a string as an argument (question to be displayed), and returns the validated integer input,
int int_check_input(string question);

// Gets the system current time and returns the current month and day
vector<int> get_month_day();

// Accepts and validates the user's inputs 
// takes a vector as an argument(system current monthand day), and returns the validated today's date.
vector<int> input_month_day(vector<int> today);

// Computes the number days until the next full moon,
//takes a vector as an argument(validated monthand day inputs), and returns the number days until the next full moon.
int num_days_full_moon(vector<int> valided_today);

// ----------------------------------------------------------------- Program
int main() {

	// Local variable
	int num_of_days;

	// Local vectors
	vector<int> today_month_day, // Used to store get_month_day() results and it is past as an argument in input_month_day()
		        valided_month_day; // Used to store input_month_day() results and it is past as an argument in num_days_full_moon()
	
	// Banner
	cout << "\n                              *************\n                              * Full Moon *\n                              *************\n\n";
	cout << "     This program accepts the current date, and returns the number of days until the next full moon.\n\n";

	
	today_month_day = get_month_day();
	valided_month_day = input_month_day(today_month_day);
	num_of_days = num_days_full_moon(valided_month_day);

	if (num_of_days == -1) {
		cout << "\n      -- The last full moon for 2022 was Dec. 16th, and today is the " << valided_month_day[1] << " of December 2022. --\n\n";
	}
	else {
		cout << "\n     The next full moon will happend in " << num_of_days << " days.\n\n";
	}
	

	return 0;
	
}

int int_check_input(string question) { 

	/*      
	
	Accepts and validates the user input if it is an integer
	takes a string as an argument (question to be displayed), 
	and returns the validated integer input.

	*/

	// Local variables
	int user_input;
	char check_input_char;

	cout << "     " << question;

	do { // Validation loop, checks if the user input is an integer
		cin >> user_input;
		cin.get(check_input_char); // Gets the first non-digit character, if no non-digit character were found it returns an empty line, 
		// note that '.' in decimals inputs is a non-digit character.
		if (check_input_char != '\n') {
			cout << "\n      -- The entered input is not a valid input. It should be an integer. --\n     " << question;
			cin.clear(); // clears any error flag on cin
			cin.ignore(1000, '\n'); // ignore anything else on the same line as the non-number so that it does not cause another parse failure
		}
		else {
			break; // Input is an integer 
		}
	} while (true); // True if the input is not an integer

	return user_input; 
}

vector<int> get_month_day() {

	/*
	
	 Gets the system current time and returns the current month and day
	
	*/
	
	// Local vector
	vector<int> today_date;
	// Local variables
	struct tm today_time; // Time structure (second, hour, day and ect) from (time.h), C Time Library
	time_t time_now = time(0); // Get the system current number of seconds since 00:00, Jan 1 1970 UTC
	
	localtime_s(&today_time, &time_now); // Converts time_now to tm format, to today_time
	today_date.push_back(today_time.tm_mon + 1); // Current month
	today_date.push_back(today_time.tm_mday); // Current day

	return today_date;
}

vector<int> input_month_day(vector<int> today) {

	/*
	
	Accepts and validates the user's inputs
	takes a vector as an argument (system current month and day), 
	and returns the validated today's date.

	*/

	// Local variables
	int user_input_month, user_input_day;
	bool valid_day;

	// Local vector
	vector<int> validated_today;

	do { // Validates user's inputs are today's date

		do { // Validates user's month input
			user_input_month = int_check_input("Please enter the current month in numeric form: ");
			// Max 12 months in a year
			if (user_input_month <= 0 || user_input_month > 12) {
				cout << "\n      -- The entered input is not a valid month --\n";
			} else { break; } // month input is valid
		} while (true); // month input is not valid

		do { // Validates user's day input
			cout << endl;
			user_input_day = int_check_input("Please enter the current day of the month: ");
			// Max 31 days in a month Minimum 1
			(user_input_day <= 0 || user_input_month > 31) ? valid_day = false : 
				// 31 days months
				((user_input_month == 4 || user_input_month == 6 || user_input_month == 9 || user_input_month == 11) && user_input_day > 30) ? valid_day = false :
					// February 28 days 
					(user_input_month == 2 && user_input_day > 28) ? valid_day = false : // February 28 days 
						// else the day input is valid
						valid_day = true; 
			if (valid_day) { break; } // day input is valid
			cout << "\n      -- The entered input is not a valid day for entered month --";
		} while (true); // day input is not valid
		
		// Check if the inputs are the same as the system current month and day
		if (user_input_month != today[0] || user_input_day != today[1]) {
			cout << "\n      -- The entered input is not today's date, liar!  --\n";
		}
		else { // inputs are today's dates
			validated_today.push_back(user_input_month);
			validated_today.push_back(user_input_day);
			break;
		} 	

	} while (true); // inputs are not today's date

	return validated_today;
}

int num_days_full_moon(vector<int> valided_today) {

	/*
	
	Computes the number days until the next full moon,
	takes a vector as an argument (validated month and day inputs),
	and returns the number days until the next full moon.
	
	*/

	// Local variable
	int num_days_until_full_moon = 0;

	// Checks if the last full moon of the year is past
	if ((valided_today[0] == 12) && (valided_today[0] > 7)) {
		return -1;
	}

	// Finds the next fool moon
	for (int i = 0; i < 12; i++) {
		if (valided_today[0] == full_moon_dates_2022[i][0]) { // Finds inputted/current month in the array of full moon dates	
			if (full_moon_dates_2022[i][1] < valided_today[1]) { // If the full moon day is past for the inputed/current month
				// Computes the number days until the next moon, happening next month 
				num_days_until_full_moon = num_days_in_months_2022[valided_today[0] + 1] - valided_today[1] + full_moon_dates_2022[i+1][1];
				break;
			}
			else {
				// Computes the number days until the next full moon, happening this month
				num_days_until_full_moon = full_moon_dates_2022[i][1] - valided_today[1];
				break;
			}
		}	
	}
	
	return num_days_until_full_moon;
}