/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 11 / 15 / 2022


																			Car Class

Write a class named Car that has the following member variables:

yearModel: An int to hold the model year.
type: A string to hold the type of car (sports car, SUV, van, sedan, etc).
make: A string to hold the make of the car. (Jeep Wrangler, Ford Mustang, etc.)
speed: an int to hold the current speed of the car.

In addition, the class should have the following constructor and other member functions:

Constructor:
The constructor should accept the car's model year and make as parameters.
These values should be assigned to the object's yearModel and make member variables.
The constructor should also assign 0 to the speed member variable.

Accessors:
Appropriate accessor functions to get the values stored in an object's yearModel, type, make and speed member variables.

accelerate:
the accelerate function should add 5 to the speed member variable each time the function is called.

brake:
The brake function should subtract 5 from the speed member variable each time the function is called.

Demonstrate the class in a program that creates a Car object, and then calls the accelerate function five times.

After each call to the accelerate function, get the current speed of the car and display it.
Then, call the break function five times. After each call to the break function, get and display the current speed of the car.

Validation check: Do not have the car going at a negative speed at any time.

*** Please read  ***
This programm will only run on Window OS

*/

#include <iostream>
#include <string>
#include <cmath>
#include <vector>
// Console Input & Output Header file, Window OS only
#include <conio.h> // getch()
// Console Window size header file, Window OS only
#define _WIN32_WINNT 0x0500
#include<windows.h> // MoveWindow()

using namespace std;

//*** Global vector
vector<vector<string>> cars_inventory = {
	{"2017","Sports", "Chevrolet Camaro ZL1"},
	{"2018","Sedan", "Ford Fusion"},
	{"2020","Sports SUV", "Jeep Wrangler"},
	{"2021", "SUV", "Toyota Sequoia"},
	{"2022", "Minivan", "Chrysler Pacifica"}
};

//******************************************************************** Class

class Car {
	
	/*
		Stores car data, returns car data, and change speed variable using methods.
		Takes the arguments:
			model_year, type, make.
		Private variables:
			model_year,type, make, and speed.
		Public methods:
			get_car_data() Accessor Function, returns car data vector
			accelerate() Mutator Function for speed, add 5 to speed
			brake() Mutator Fuction for speed, subtract 5 to speed
	*/

	//--- Private Variables
	int  speed;
	string type, make, model_year;


	public:

		//--- Public Methods

		vector<string> get_car_data() { 
			
			/*
				Accessor function.
				Stores car data in vector,
				and returns car data vector.
			*/

			// local vector
			vector<string> car_data = { model_year, type, make, to_string(speed) };
			
			return car_data = { model_year, type, make, to_string(speed) };
			
		}

		void accelerate() {
			/*
				Mutator Function.
				Add 5 to speed.
			*/
			speed += 5;
		}

		void brake() {
			/*
			    Mutator Function.
				Substract 5 to speed
			*/
			speed -= 5;
		}

		//-- Construtor
		Car(string model_year, string type, string make) {
			this->model_year = model_year;
			this->type = type;
			this->make = make;
			this->speed = 0;
		}
};


//******************************************************************** Functions declaration

/*
	Clears the console screen.
*/
void clear();

/*
	Waits for a key to be pressed.
*/
void press_key();

/*
		Sets size of the Console's window
		and position the console in desktop screen utilizing the variable position_console
		Takes the console with width, lenght and position as arguments.
		position_console values:
		"center", "left_center", "right_center",
		"top_left", "top_center", "top_right",
		"bottom_left", "bottom_center", "bottom_right".
*/
void console_size(int screen_width, int screen_lenght, string position_console);

/*********************************************************************
*					            Program                              *
 *********************************************************************/

int main() {

	//-- Variable
	char ch; // utilize by _getch() 
	int user_choice; // user menu choice

	//-- Vector 
	vector<string> car_data; // Stores the car data from the Car class

	// Sets screen size
	console_size(300, 500, "center");

	// Displays menu and the user choice results
	do {
		
		//-- Banner
		cout << "\n                          ************\n                          *   Cars   *\n                          ************\n\n";
		
		//-- menu list
		cout << " Please choose from the following menu:\n";
		for (int i = 0; i < cars_inventory.size(); i++) {
			cout << "  Press " << i + 1 << " - To drive ";
			for (int j = 0; j < cars_inventory[i].size(); j++) {
				cout << " " << cars_inventory[i][j];
			}
			cout << "\n";
		}
		cout << "  Press 0 - To exit -\n\n";
		// Waits for user to press a key
		ch = _getch();
		
		//-- Processes user choice
		// Exit program
		if (ch == '0') { return 0; };
		// Converts the user choice from a char to an int, to index cars_inventory array
		user_choice = (ch - '0') - 1;
		// Checks for invalid input
		if ((user_choice < 0) || (user_choice > cars_inventory.size())) {
			cout << " ----- Invalid input, please enter a valid input ------\n"
			     << "    To continue"; 
			press_key();
			clear();
		} 
		else {
			// Initializes a Cars type object
			Car car(cars_inventory[user_choice][0], cars_inventory[user_choice][1], cars_inventory[user_choice][2]);
			
			//-- Displays utilizing Car class Accessor
			car_data = car.get_car_data();
			cout << "  Your choice:\n\n"
				 << "   " << car_data[0] << " " << car_data[1]  << " " << car_data[2] 
				 << "\n   and your speed is " << car_data[3] << "\n\n";
			
			// Accelerate, using Car class speed Mutator +5 speed 
			for (int i = 0; i < 5; i++)
			{
				cout << "\n   To accelerate";
				press_key();
				car.accelerate(); // Sepeed +5
				cout << "\n   Your speed is now: " << car.get_car_data()[3];
			}
			cout << "\n";
			// Brake, using Car class speed Mutator -5 speed 
			for (int i = 0; i < 5; i++)
			{
				cout << "\n   To Brake";
				press_key();
				car.brake(); // Sepeed +5
				cout << "\n   Your speed is now: " << car.get_car_data()[3];
			}

			cout << "\n\n   To continue";
			press_key();
			clear();
		}
	} while (true);
}

//******************************************************************** Functions 

void clear() {

	/*

	Clears the console screen

	*/

	for (int i = 0; i < 25; i++) {
		cout << "\n";
	}
	cout << endl; // will flush the output buffer and insert a new line.
}

void press_key() {

	/*
	
		 Waits for a key to be pressed.

	 */

	 // -- Local variables
	 // Press key to continue variable
	char ch;

	cout << " press any key ";
	ch = _getch();

}


void console_size(int console_width, int console_lenght, string position_console) {

	/*
	
		Sets size of the Console's window 
		and position the console in desktop screen utilizing the variable position_console
		Takes the console with width, lenght and position as arguments.

		position_console values: 
		"center", "left_center", "right_center",
		"top_left", "top_center", "top_right",
		"bottom_left", "bottom_center", "bottom_right".

	
	*/

	//-- Local variables
	int console_position_left = 0,
		console_position_top = 0;

	// Creats a structure type rectangle coordinates, upper-left and lower-right corners
	RECT desktop;
	// Gets the desktop screen data 
	HWND my_desktop = GetDesktopWindow();
	// Stores the size of monitor screen to the variable desktop
	GetWindowRect(my_desktop, &desktop);
	/*
		The top left corner of the monitor has the coordinates (0, 0)
		and the bottom right corner has the coordinates (desktop.right, desktop.bottom).
		Note that the desktop.right = monitor lenght
		and the desktop.bottom = monitor width.
	*/
	// Checks if the wanted console lenght is bigger than the monitor screen lenght, 'desktop.right'
	if (desktop.right < console_lenght) { console_lenght = floor(desktop.right); }
	// Checks if the wanted console width is bigger than the monitor screen width, 'desktop.bottom'
	if (desktop.bottom < console_width) { console_width = floor(desktop.bottom); }
	
	// Checks if the wanted console's width or lenght are NOT the same as the width or lenght of the desktop screen
	// if true initializes the console's coordinates to the wanted console position
	// else console_position_left = 0, console_position_top = 0.
	if (console_lenght != desktop.right || console_width != desktop.bottom) {
		// Checks the wanted position and computes the related coordinates	
		if (position_console == "center") {
			console_position_left = round((desktop.right - console_lenght) / 2);
			console_position_top = round((desktop.bottom - console_width) / 2);
		}
		else if (position_console == "left_center") {
			console_position_left = 10;
			console_position_top = round((desktop.bottom - console_width) / 2);
		}
		else if (position_console == "right_center") {
			console_position_left = round((desktop.right - console_lenght) - 10);
			console_position_top = round((desktop.bottom - console_width) / 2);
		}
		else if (position_console == "top_left") {
			console_position_left = 10;
			console_position_top = 10;
		}
		else if (position_console == "top_center") {
			console_position_left = round((desktop.right - console_lenght) / 2);
			console_position_top = 10;
		}
		else if (position_console == "top_right") {
			console_position_left = round((desktop.right - console_lenght) - 10);
			console_position_top = 10;
		}
		else if (position_console == "bottom_left") {
			console_position_left = 10;
			console_position_top = round((desktop.bottom - console_width) - 40);
		}
		else if (position_console == "bottom_center") {
			console_position_left = round((desktop.right - console_lenght) / 2);
			console_position_top = round((desktop.bottom - console_width) - 40);
		}
		else if (position_console == "bottom_right") {
			console_position_left = round((desktop.right - console_lenght) - 10);
			console_position_top = round((desktop.bottom - console_width) - 40);
		}
	}
		
	// Gets the existing console screen data
	HWND my_console = GetConsoleWindow();
	// Initializes the console to the wanted size and its position to the center of the screen monitor 
	MoveWindow(my_console, console_position_left, console_position_top, console_lenght, console_width, TRUE);
}
