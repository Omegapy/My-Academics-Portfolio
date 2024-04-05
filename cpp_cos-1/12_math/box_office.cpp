/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student: Alejandro (Alex) Ricciardi
Due date : 09 / 06 / 2022
Box Office

Assignment : 
Box Office
A movie theater only keeps a percentage of the revenue earned from ticket sales, the rest of the money goes to the movie distributor.
Write a program that calculates the theater's gross (overall amount earned) and net (amount after the distributor's cut) box office profit for one night.  
The program should ask for the name of the movie and how many adult tickets and child tickets were sold.  
Adult tickets cost $12.00 each; seniors and children tickets cost $9.00 each. Students and Military with valid ID are $10.00 each.  
The theater keeps 20% of the ticket sales, the remainder goes to the distributor.  
Have the program display the information in the same format as the example below:

Movie Name:							" Movie Name "
Adult Tickets Sold:					##
Senior/Child Tickets Sold:			##
Student/Military Tickets Sold:		##
Gross Box Office Profit:			$ ###.##
Net Box Office Profit:              $ ###.##
Amount Paid to Distributor:			$ ###.##

When finished, take a screen capture of your output and submit both the screen capture and your .cpp file.

Problem: Running .cpp file
10 pts Program runs and performs the requirements without errors.
5 pts Program runs but does not perform to the requirements or has errors.
0 pts No Marks
Problem: Screenshot
5 pts Student submitted a screenshot of program output that is readable(see file pic)
0 pts No Marks.
*/


#include <iostream>
#include <string>
#include <iomanip> // std::setprecision

using namespace std;

// Variables
string movie_name;
	// Ticket prices
double ticket_adult_price = 12.00;
double ticket_senior_child_price = 9.00;
double ticket_student_military_price = 10.00;
	// Tickets sold
int sold_tickets_adult;
int sold_tickets_senior_child;
int sold_tickets_student_military;
	// Profits
double gross;
double net_profit;
double distributor_cut;
double theater_perc = 20.00;

int main() {

	cout << "\n       *********************************\n       * Movie Tickets Sold Calculator *\n       *********************************\n\n\n";
	
	// User inputs
	cout << "   Enter the movie's name: ";
	getline(cin, movie_name);
	cout << "\n   Enter the number of Adult Ticket Sold: ";
	cin >> sold_tickets_adult;
	cout << "\n   Enter the number of Senior/Child Tickets Sold: ";
	cin >> sold_tickets_senior_child;
	cout << "\n   Enter the number of Student/Military Tickets Sold: ";
	cin >> sold_tickets_student_military;

	// Calculations
	gross = sold_tickets_adult * ticket_adult_price + 
		    sold_tickets_senior_child * ticket_senior_child_price + 
		    sold_tickets_student_military * ticket_student_military_price;
	net_profit = gross * theater_perc / 100;
	distributor_cut = gross - net_profit;

	// Display results
	cout << setprecision(2) << fixed; // Display the double variables precision to two decimals 
	cout << "\n   Movie Name:                       " << movie_name
		 << "\n   Adult Tickets Sold:               " << sold_tickets_adult
		 << "\n   Senior/Child Tickets Sold:        " << sold_tickets_senior_child
		 << "\n   Student/Military Tickets Sold:    " << sold_tickets_student_military
		 << "\n   Gross Box Office Profit:          $ " << gross
		 << "\n   Net Box Office Profit:            $ " << net_profit
		 << "\n   Amount Paid to Distributor:       $ " << distributor_cut
		 << endl;

	return 0;
}