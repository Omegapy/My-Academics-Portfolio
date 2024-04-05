/*

													President of the United States Information Dump

Using the link below to an external site. website, record information on past U.S. 
Presidents into a set of arrays (you may also use vectors, but they are more difficult to sort).
https://www.whitehouse.gov/about-the-white-house/presidents/

- potus_Last_Name (string): The President's last name. <- This is what you will sort by.
- potus_First_Name (string): The President's first name. <- Do NOT sort by this. 
  DO remember to include this when displaying the names. 
  If a middle initial is needed it should go here. (George H. W. Bush vs. George W. Bush)
- potus_Terms (int): The number of terms the President served.
- potus_FirstYear (int): The year the President started serving his term in office.  <- Note that this is NOT the same as the year the President was elected. 
  President Biden was elected in 2020, but his term started in 2021. (<- Most recent example.)

All of this information should be hard coded, there should be no user input up to this point.

You will need to have options for the user to do the following:

Display the list of Presidents, in order, first to most recent, in groups of 10.  i.e. Display Washington through Tyler, 
pause for user to hit a key, then display Polk through Garfield, etc. Yes, you need to list Cleveland twice.
Sort the list of names in Alphabetical order and display it in groups of 10 Presidents at a time. Again, 
display 1 through 10, wait for key press, then 11 through 20, etc. (i.e. Quincy-Adams should be sorted as a 'Q' not as an 'A'.)
Show only Presidents who served 1 term.
Show only Presidents who served 2 or more terms. (Yes, we had one 4 term President. (Yes, you should know that by now if you are from the U.S.))
Show a list of the Presidents and the year they started serving their term. Again, you need to show Cleveland twice.
You need to use functions for each of these options. At least one function for each one. That's five different functions just for the displays, 
plus those you'll need for the sorting and the searching.

Display a menu of the options that the user can choose from. Have the program clear the screen and return to the menu after each option is done.

      --Don't forget an option to exit the program.

Note: 
There should be no input from the user other than their menu choices. All the Presidential data should be hard coded.

Hint: 
You can clear the screen by simply printing endl 30-50 times. Use a loop.
Input Validation: 
Do not accept options not included in the menu. (A, B, C or 1, 2, 3 etc.)
Screen Capture: 
Screen capture should show the first 20 presidents from the default display.

Note: 
Make sure the information you are displaying is accurate. 
Yes, there are Presidents I am not that fond of either, but that is no excuse for getting the information wrong.

Warning: 
The instructor just so happens to have his undergrad degree in U.S. History and will notice wild inaccuracies.

 Sorting and Searching Rubric (1) Grading:
		potUS_info: .CPP File
			60 pts
			Program runs without errors or corrections.
			45 pts
			Program runs, but has minor errors or needs corrections to run.
			25 pts
			Program needs major revisions/error correction before it will run.
			0 pts
			No Marks
		potUS_info: Comments
			20 pts
			Proper levels of commenting.
			Functions are given at least simple descriptions, purposes/uses of loops and conditionals are given at least simple descriptions.
			15 pts
			Acceptable levels of comments in most areas.
			10pts
			Minor commenting done; or only bare details provided.
			0 pts
			No Marks
		potUS_info: Screen Capture
			10 pts
			Full Marks
			0 pts
			No Marks
Total possible points: 90


*** Please read  ***

This programm will only run on Window OS
It is important to note that:
Not all the Presidents served full terms.
Also, the US has/had 46 presidents but only 45 individuals served as Presidents
this is due to President Grover Cleveland who served 2 nonconsecutive terms, i.e., he is the 22sd and 24th President

Ter completion types:
- Full Term - the President completed a full term.
- Unfinished Term - the President did not complete a full term (passed away, assassinated, resigned).
- Partial Term - the President was the vice president and became the President after the elected President did not finish his term.

I utilized some of the information from the following website 
https://historyinpieces.com/research/presidential-inauguration-dates

*/

#include <iostream>
#include <string>
#include <vector>
// Console Input & Output.Header file, Window OS only
#include <conio.h> // getch()

using namespace std;

// -- Global Array

// US presidents first last and number of electected terms
string presidents_data[46][10] = { // Utilized build_presidents_table()
	//          |                     |               |                             |                        |
	// number   |        Names        | Num. of terms |       Terms starting date   |  nonconsecutive term   | // Checks if the term(s) is/are nonconsecutive
	//          |                     |               | f=full, u=unfinished        | t=true, f=false        |
	// index=0  | first and last      |               | term, p=partial term        |                        |
	// index=1  | index=2  index=3    |    index=4    |    index=5  to index=8      |           index=9      |
	{"1","\n",  "George","Washington",      "2",        "04/30/1789/f","03/04/1793/f","\n","\n",  "f"        },
	{"2","\n",  "John","Adams",             "1",        "03/04/1797/f","\n","\n","\n",            "f"        },
	{"3","\n",  "Thomas","Jefferson",       "2",        "03/04/1801/f","03/04/1805/f","\n","\n",  "f"        },
	{"4","\n",  "James","Madison",          "2",        "03/04/1809/f","03/04/1813/f","\n","\n",  "f"        },
	{"5","\n",  "James","Monroe",           "2",        "03/04/1817/f","03/04/1821/f","\n","\n",  "f"        },
	{"6","\n",  "John","Quincy Adams",      "1",        "03/04/1825/f","\n","\n","\n",            "f"        },
	{"7","\n",  "Andrew","Jackson",         "2",        "03/04/1829/f","03/04/1833/f","\n","\n",  "f"        },
	{"8","\n",  "Martin","Van Buren",       "1",        "03/04/1837/f","\n","\n","\n",            "f"        },
	{"9","\n",  "William","Henry Harrison", "1",        "03/04/1841/u","\n","\n","\n",            "f"        },
	{"10","\n", "John","Tyler",             "1",        "04/06/1841/p","\n","\n","\n",            "f"        },
	{"11","\n", "James K.","Polk",          "1",        "03/04/1845/f","\n","\n","\n",            "f"        },
	{"12","\n", "Zachary","Taylor",         "1",        "03/04/1849/u","\n","\n","\n",            "f"        },
	{"13","\n", "Millard ","Fillmore",      "1",        "07/10/1850/p","\n","\n","\n",            "f"        },
	{"14","\n", "Franklin","Pierce",        "1",        "03/04/1853/f","\n","\n","\n",            "f"        },
	{"15","\n", "James","Buchanan",         "1",        "03/04/1857/f","\n","\n","\n",            "f"        },
	{"16","\n", "Abraham","Lincoln",        "2",        "03/04/1861/f","03/04/1865/u","\n","\n",  "f"        },
	{"17","\n", "Andrew","Johnson",         "1",        "04/15/1865/p","\n","\n","\n",            "f"        },
	{"18","\n", "Ulysses S.","Grant",       "2",        "03/04/1869/f","03/04/1873/f","\n","\n",  "f"        },
	{"19","\n", "Rutherford B.","Hayes",    "1",        "03/04/1877/f","\n","\n","\n",            "f"        },
	{"20","\n", "James A.","Garfield",      "1",        "03/04/1881/u","\n","\n","\n",            "f"        },
	{"21","\n", "Chester A.","Arthur",      "1",        "09/20/1881/p","\n","\n","\n",            "f"        },
	{"22","24", "Grover","Cleveland",       "2",        "03/04/1885/f","03/04/1893/f","\n","\n",  "f"        },
	{"23","\n", "Benjamin","Harrison",      "1",        "03/04/1889/f","\n","\n","\n",            "f"        },
	{"24","22", "Grover","Cleveland",       "2",        "03/04/1885/f","03/04/1893/f","\n","\n",  "t"        }, // nonconsecutive term
	{"25","\n", "William","McKinley",       "2",        "03/04/1897/f","03/04/1901/u","\n","\n",  "f"        },
	{"26","\n", "Theodore","Roosevelt",     "2",        "09/14/1901/p","03/04/1905/f","\n","\n",  "f"        },
	{"27","\n", "William H.","Taft",        "1",        "03/04/1909/f","\n","\n","\n",            "f"        },
	{"28","\n", "Woodrow","Wilson",         "2",        "03/04/1913/f","03/04/1917/f","\n","\n",  "f"        },
	{"29","\n", "Warren G.","Harding",      "1",        "03/04/1921/u","\n","\n","\n",            "f"        },
	{"30","\n", "Calvin","Coolidge",        "2",        "08/03/1923/p","03/04/1925/f","\n","\n",  "f"        },
	{"31","\n", "Herbert C.","Hoover",      "1",        "03/04/1929/f","\n","\n","\n",            "f"        },
	{"32","\n", "Franklin D.","Roosevelt",  "4",        "03/04/1933/f","01/20/1937/f",
	                                                    "01/20/1941/f","01/20/1945/u",            "f"        },
	{"33","\n", "Harry S.","Truman",        "2",        "04/12/1945/p","01/20/1949/f","\n","\n",  "f"        },
	{"34","\n", "Dwight D.","Eisenhower",   "2",        "01/20/1953/f","01/21/1957/f","\n","\n",  "f"        },
	{"35","\n", "John F.","Kennedy",        "1",        "01/20/1961/u","\n","\n","\n",            "f"        },
	{"36","\n", "Lyndon B.","Johnson",      "2",        "11/22/1963/p","01/20/1965/f","\n","\n",  "f"        },
	{"37","\n", "Richard M.","Nixon",       "2",        "01/20/1969/f","01/20/1973/u","","",      "f"        },
	{"38","\n", "Gerald R.","Ford",         "1",        "08/09/1974/p","\n","\n","\n",            "f"        },
	{"39","\n", "James Earl","Carter",      "1",        "01/20/1977/f","\n","\n","\n",            "f"        },
	{"40","\n", "Ronald","Reagan",          "2",        "01/20/1981/f","01/21/1985/f","\n","\n",  "f"        },
	{"41","\n", "George H. W.","Bush",      "1",        "01/20/1989/f","\n","\n","\n",            "f"        },
	{"42","\n", "William J.","Clinton",     "2",        "01/20/1993/f","01/20/1997/f","\n","\n",  "f"        },
	{"43","\n", "George W.","Bush",         "2",        "01/20/2001/f","01/20/2005/f","\n","\n",  "f"        },
	{"44","\n", "Barack H.","Obama",        "2",        "01/20/2009/f","01/21/2013/f","\n","\n",  "f"        },
	{"45","\n", "Donald J.","Trump",        "1",        "01/20/2017/f","\n","\n","\n",            "f"        },
	// Joseph R. Biden is the current President of the US, presuming that he will fully complete his term
	{"46","\n", "Joseph R.","Biden",        "1",        "01/20/2021/f","\n","\n","\n",            "f"        }
};

// -- Global Structure

/* 
	Data structure to stores the a President data.

	Utilize by:
	build_presidents_table(), build_presidents_table(), 
	sort_last_names(), display_results(), find_one_term_presidents(), 
	find_multiple_terms_presidents(), find_unfinished_term_presidents(), 
	and find_partial_term_presidents().

*/
struct presidents {
	vector<int> numbers;
	string first_name;
	string last_name;
	int num_terms = NULL;
	vector<string> terms_start_date,
		           terms_completion;
	bool nonconsecutive = false; // note set to false, changed to true for President(s) with nonconsecutive terms, aka President Grover Cleveland
};

// ----------------------------------------------------------------- Functions declaration

/* 
	Clears the console screen.
	Utilize by press_key_to_continue()
*/
void clear(); 

/* 
	Waits for a key to be pressed, and clear the screen.
	utilize by display_results()
*/
void press_key_to_continue();

/* 
	Builds a table storing the presidents info,
	and returns a vector of objects containing the presidents data.
*/
vector<presidents> build_presidents_table();

/* 
	Displays the sort or search table results,
	takes the  sort or search  president table to be displayed, the name of the table,
	and boolean to display or not nonconsecutive term president data.
*/
void display_results(vector<presidents> table, string table_name, bool display_nonconsecutive);

/* 
	Utilized Bubble sort to sort the presidents info by last names in Alphabetical order,
	takes the presidents table to be sorted,
	and returns the sorted table.
*/
vector<presidents> sort_presidents_last_names(vector<presidents> table);

/* 
	Finds one term presidents, takes a presidents table,
	and returns a table of one term presidents.
 */
vector<presidents> find_one_term_presidents(vector<presidents> table);

/* 
	Finds multiple term presidents, takes a presidents table,
	and returns a table of several terms presidents.
*/
vector<presidents> find_multiple_term_presidents(vector<presidents> table);

/*
	Finds unfinished term presidents, takes a presidents table,
	and returns a table of unfinished terms presidents.
*/ 
vector<presidents> find_unfinished_term_presidents(vector<presidents> table);

/* 
	Finds partial term presidents, takes a presidents table,
	and returns a table of partial terms presidents.
*/
vector<presidents> find_partial_term_presidents(vector<presidents> table);

// ------------------------------------------------------------------ Program
int main() {

	//-- Variable
	char ch; // utilize by _getch() and the menu switch

	// -- Vectors
	// Utilize to stores and displays presidents data
	vector<presidents> us_presidents, sorted_presidents_names, 
					one_term_presidents, multiple_term_presidents, 
					unfinished_term_presidents, partial_term_presidents;
	
	// Builds a presidents data table from the global array presidents_data
	us_presidents = build_presidents_table();
	
	// Builds presidents data tables, utilize by display_results()
	sorted_presidents_names = sort_presidents_last_names(us_presidents); // Sorts by last names
	one_term_presidents = find_one_term_presidents(us_presidents); // Finds one term presidents
	// Note that following code will store chronologically the President search category results
	// Replacing 'us_presidents' with 'sorted_presidents_names' will store by last name the President search category results
	multiple_term_presidents = find_multiple_term_presidents(us_presidents);// Finds multiple term presidents
	unfinished_term_presidents = find_unfinished_term_presidents(us_presidents); // Finds unfinished term presidents
	partial_term_presidents = find_partial_term_presidents(us_presidents); // Finds partial term presidents

	//----- Menu
	do {
		//-- Banner
		cout << "\n                              **********************\n                              *   U.S Presidents   *\n                              **********************\n\n";
		// menu list
		cout
			<< " Please choose from folling the menu:\n"
			<< "  Press 1 - To view the list of Presidents, from the first President to the most recent -\n"
			<< "  Press 2 - To view the list of Presidents in last names Alphabetical order -\n"
			<< "  Press 3 - To view the list of one term Presidents -\n"
			<< "  Press 4 - To view the list of multiple term Presidents -\n"
			<< "  Press 5 - To view the list of Presidents that did not finish their term - \n"
			<< "  Press 6 - To view the list of Presidents with partial term - \n"
			<< "  Press 0 - To exit -\n\n"
			<< "  Note: Term Completions\n"
			<< "  - Full - the President completed a full term\n"
			<< "  - Unfinished - the President did not complete a full term (passed away, assassinated, resigned)\n"
			<< "  - Partial - the President was the vice president\n  and became the President after the elected President did not finish his term\n\n";
		
		// Waits for user to press a key
		ch = _getch();

		// Exit program
		if (ch == '0'){ break; }

		// Checks user inputed key, and displays the user menu choice
		switch (ch) {
			case '1' : 
				// Note that display_nonconsecutive (term) is set to true, it will display President Grover Cleveland twice
				display_results(us_presidents, "From The First President To The Most Recent", true); // chronologically
				break;
			case '2':
				display_results(sorted_presidents_names, "Presidents In Last Names Alphabetical  Order", false); // by last names
				break;
			case '3':
				display_results(one_term_presidents, "One Term Presidents", false); // one term
				break;
			case '4':
				display_results(multiple_term_presidents, "Multiple Term Presidents", false); // multiple terms
				break;
			case '5':
				display_results(unfinished_term_presidents, "Unfinished Term Presidents", false); // unfinished terms
				break;
			case '6':
				display_results(partial_term_presidents, "Partial Term Presidents", false); // partial terms
				break;
			default :
				cout << " ----- Invalid input, please enter a valid input ------\n";
				press_key_to_continue();
		}	
	} while (true);

	return 0;
}

// ----------------------------------------------------------------- Functions

void clear() {

	/*
	
	Clears the console screen
	
	*/

	for (int i = 0; i < 50; i++) {
		cout << "\n";
	}
	cout << endl; // will flush the output buffer and insert a new line.
}

void press_key_to_continue() {
	
	/*
	 
		 Waits for a key to be pressed,
		 and clear the screen,
		 utilize by display_results().

	 */
	
	// -- Local variables
	// Press key to continue variable
	char ch;

	cout << "\n  -- Press any key to continue -- ";
	ch = _getch();
	clear();

}

vector<presidents> build_presidents_table() {

	/*
	
		Builds a table storing the presidents data,
		and returns a vector of objects containing the presidents data.

	*/

	//-- Local vector
	// Stores the presidents data
	vector<presidents> presidents_table;

	// Itinerates trough the presidents_data array
	for (int  i=0; i < 46 ; i++) { 
		
		// Intializes the president info to be stores as a presidents data structure
		presidents president;

		// Stores the president number
		president.numbers.push_back(stoi(presidents_data[i][0]));
		// Check if the president served 2 nonconsecutive terms, if yes it will add a second president number to the president numbers
		if (presidents_data[i][1] != "\n") { president.numbers.push_back(stoi(presidents_data[i][1])); }
		
		// Stores the president first, last name, and number of term served
		president.first_name = presidents_data[i][2];
		president.last_name = presidents_data[i][3];
		president.num_terms = stoi(presidents_data[i][4]);
		
		// Stores the terms served starting dates
		for (int j=5; j<5+president.num_terms; j++) {
			// Term dates
			president.terms_start_date.push_back(presidents_data[i][j].substr(0,10));
			// Term completion type f, p or u
			president.terms_completion.push_back(presidents_data[i][j].substr(11));
		}

		// Checks if president nonconsecutive tearm data is true (t), if it is true changes nonconsecutive from false to true in president data structure
		if (presidents_data[i][9] == "t") { president.nonconsecutive = true; }

		// Stores the president data into the presidents_table stucture array
		presidents_table.push_back(president);

	}
	
	return presidents_table;
}

void display_results(vector<presidents> table, string table_name, bool display_nonconsecutive) {

	/*
	
		Displays the sort or search table results,
		takes the  sort or search president table to be displayed, the name of the table,
		and boolean to display or not nonconsecutive term president data
	
	*/
	
	// -- Local variables
	// Keeps track of spaces to display to the right of president numbers
	// and to the left of the president names.
	string spaces;

	//-- Banner
	clear();
	cout << "  ---- " << table_name << " ----\n"
		<< "  ----------------------------------------------------------------------------------------------------\n"
		<< "  | Number |      President Name     | Number of Terms |     Term Start dates     |  Term Completion |\n"
		<< "  ----------------------------------------------------------------------------------------------------\n";

	// Itinerates trough the presidents_data array
	for (int i = 0; i < table.size(); i++) {

		// Checks if display_nonconsecutive and table[i].nonconsecutive are both true, 
		// if they are the president data will be displayed
		// the president data will be also displayed if table[i].nonconsecutive is false
		if ((display_nonconsecutive  && table[i].nonconsecutive) || !table[i].nonconsecutive ) {

			// Diplays President number
			if (table[i].numbers.size() > 1) { // Checks if the president served nonconsecutive terms, aka president Grover Cleveland,
				// this will only display in this matter if the table was sorted by president last names
				cout << "  | ";
				for (int j = 0; j < table[i].numbers.size(); j++) {
					if (j != table[i].numbers.size() - 1) {
						cout << table[i].numbers[j] << ", ";
					}
					else {
						cout << table[i].numbers[j] << " ";
					}
				}
				cout << "|";
			}
			else if (table[i].numbers[0] < 10) { // assignes number of space to diplays right of the president numbers
				spaces = "    ";
				cout << "  |" << spaces << table[i].numbers[0] << "   |";
			}
			else {
				spaces = "   ";
				cout << "  |" << spaces << table[i].numbers[0] << "   |";
			}
			// Display President name
			spaces = "";
			// Computes the numbers of spaces need to align the president names
			for (int j = 0; j < 23 - table[i].first_name.size() - table[i].last_name.size(); j++) {
				spaces += " ";
			}
			// Diplays first and last names
			cout << " " << table[i].first_name << " " << table[i].last_name << spaces << "|"
				// Diplay the number of terms	
				<< "        " << table[i].num_terms << "        |";
			// Itinerates through the president terms dates
			for (int j = 0; j < table[i].num_terms; j++) {
				// Displays terms dates
				cout << "        " << table[i].terms_start_date[j] << "        |";
				// Displays completion type
				if (table[i].terms_completion[j] == "f") {
					cout << "       Full       |";
				}
				else if (table[i].terms_completion[j] == "p") {
					cout << "      Partial     |";
				}
				else {
					cout << "    Unfinished    |";
				}
				// If terms is not the last one add a row to the display table
				if (j != table[i].num_terms - 1) {
					cout << "\n  |        |                         |                 |";
				}
			}
			// Presidents row separation
			cout << "\n  ----------------------------------------------------------------------------------------------------\n";
			// After every 10 presidents displayed ask user to press a key to continue
			if ((i != 1) && ((i + 1) % 10 == 0)) {
				press_key_to_continue();
				// Banner
				cout << "  ---- " << table_name << " ----\n"
					<< "  ----------------------------------------------------------------------------------------------------\n"
					<< "  | Number |      President Name     | Number of Terms |     Term Start dates     |  Term Completion |\n"
					<< "  ----------------------------------------------------------------------------------------------------\n";
			}
		}
	}
	press_key_to_continue();
}

//------------------------------------------------------------------------------- Functions

vector<presidents> sort_presidents_last_names(vector<presidents> table) {

	/*
	
		Utilized Bubble sort to sort the presidents info by last names in Alphabetical order,
		takes the presidents table to be sorted,
		and returns the sorted table.
	
	*/
	
	//-- Local variables
	bool swap;
	//--- structur
	presidents temp; // store temporary a president data
	// Buuble sort, sort presidents info by last names in Alphabetical order 
	do { 
		swap = false;
		for (int i = 0; i < table.size() - 1; i++) { // Itinerates through the president info
			// if presidents have the same last name but sort by first name, aka Presidents Bushes
			if (table[i].last_name == table[i+1].last_name) {
				// if the presidents have the same last name and first name, aka president Grover Cleveland
				if (table[i].first_name == table[i+1].first_name) {
					// Compares president last names and, if needed, swaps presidents data
					if (table[i].last_name > table[i+1].last_name) {
						temp = table[i];
						table[i] = table[i+1];
						table[i+1] = temp;
						swap = true;
					}
				}
				// Compares president first names and, if needed, swaps presidents data
				else if (table[i].first_name > table[i + 1].first_name) {
					temp = table[i];
					table[i] = table[i + 1];
					table[i + 1] = temp;
					swap = true;
				}
			}
			// Compares president last names and, if needed, swaps presidents data
			else if (table[i].last_name > table[i + 1].last_name) {
				temp = table[i];
				table[i] = table[i + 1];
				table[i + 1] = temp;
				swap = true;
			}
		}
	} while (swap);

	return table;
}



vector<presidents> find_one_term_presidents(vector<presidents> table) {
	
	/*
	
		Finds one terms presidents,
		takes a presidents table,
		and returns a table of one terms presidents.

	*/

	//-- Local vector
	// Stores one term presidents data
	vector<presidents> one_term_table;

	for (int i=0; i < table.size(); i++) { // Itinerates through the president terms dates
		if (table[i].num_terms == 1) { // Finds one term presidents
			one_term_table.push_back(table[i]);
		}
	}

	return one_term_table;
}

vector<presidents> find_multiple_term_presidents(vector<presidents> table) {

	/*

		Finds multiple term presidents,
		takes a presidents table,
		and returns a table of several terms presidents.

	*/

	//-- Local vector
	// Stores multiple term presidents data
	vector<presidents> several_terms_table;

	for (int i = 0; i < table.size(); i++) { // Itinerates through the president terms dates
		if (table[i].num_terms > 1) { // Finds multiple term presidents
			several_terms_table.push_back(table[i]);
		}
	}

	return several_terms_table;
}

vector<presidents> find_unfinished_term_presidents(vector<presidents> table) {
	
	/*

		Finds unfinished term presidents,
		takes a presidents table,
		and returns a table of unfinished terms presidents.noun

	*/

	//-- Local vector
    // Stores unfinished term presidents data
	vector<presidents> unfinished_term_table;

	for (int i = 0; i < table.size(); i++) { // Itinerates through the president data
		for (int j = 0; j < table[i].num_terms; j++) { // Itinerates trough the president terms completion types 
			if (table[i].terms_completion[j] == "u") { // Finds terms presidents terms completion type 'u'
				unfinished_term_table.push_back(table[i]);
			}
		}
	}

	return unfinished_term_table;
}

vector<presidents> find_partial_term_presidents(vector<presidents> table) {

	/*

		Finds partial term presidents,
		takes a presidents table,
		and returns a table of partial terms presidents.

	*/

	//-- Local vector
	// Stores partial terms presidents data
	vector<presidents> partial_term_table;

	for (int i = 0; i < table.size(); i++) { // Itinerates through the president data
		for (int j = 0; j < table[i].num_terms; j++) { // Itinerates trough the president 
			if (table[i].terms_completion[j] == "p") { // Finds terms presidents terms completion type 'p'
				partial_term_table.push_back(table[i]);
			}
		}
	}

	return partial_term_table;
}
