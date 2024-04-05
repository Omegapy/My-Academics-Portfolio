/*
COSC 1030 – Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 09 / 06 / 2022
Box Office

Assignment :
Loan Calculator Program
The monthly payment on a loan may be calculated with the following formula:
Payment = ((Rate * (1 + Rate) ^ N) / (((1 + Rate) ^ N) - 1)) * L
Rate is the monthly interest rate, which is the annual interest rate divided by 12. N is the number of payments, 
and L is the amount of the loan. Write a program that asks for these values 
and displays a report similar to the following example:

Loan Amount:                    $ 10000.00
Monthly Interest Rate:          1%
Number of Payments:             36
Monthly Payment:                $ 332.14
Interest Paid:                  $ 1957.15
Total Amount Paid:              $ 11957.15

DO NOT use the same numbers I did!
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
#include <cmath>

using namespace std;

// Variables
	// Input variables
double loan_amount;
int number_of_payments;
double annual_interest_rate;
	// Calculations ouput variables
double monthly_interest_rate;
double monthly_payment;
double interest_paid;
double total_amount_paid;

int main() {
	
	// User inputs
	cout << "\n       *******************\n       * Loan Calculator *\n       *******************\n\n\n";
	cout << "\n   Enter the Loan Amount: ";
	cin >> loan_amount;
	cout << "\n   Enter the The Annual Interest Rate in % form: ";
	cin >> annual_interest_rate;
	cout << "\n   Enter the Number of Payments: ";
	cin >> number_of_payments; 

	// Calculations
	monthly_interest_rate = (annual_interest_rate / 12) / 100;
	
	monthly_payment = 
		(
			(monthly_interest_rate * pow(1 + monthly_interest_rate, number_of_payments)) 
			/ (pow(1 + monthly_interest_rate, number_of_payments) - 1)
		) 
		* loan_amount;
	
	total_amount_paid = monthly_payment * number_of_payments;
	interest_paid = total_amount_paid - loan_amount;

	// Display results
	cout << setprecision(2) << fixed; // Display the double variables precision to two decimals 
	cout << endl
		 << "\n   Loan Amount:             $ " << loan_amount
		 << "\n   Monthly Interest Rate:   " << monthly_interest_rate * 100 << "%"
		 << "\n   Number of Payments:      " << number_of_payments
		 << "\n   Monthly Payment:         $ " << monthly_payment
		 << "\n   Interest Paid:           $ " << interest_paid
		 << "\n   Total Amount Paid:       $ " << total_amount_paid
		 << endl;

	return 0;
}