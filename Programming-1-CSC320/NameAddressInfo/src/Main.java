/*
	Program Name: Name and Address Information
	Author: Alejandro (Alex) Ricciardi
	Date: 04/14/2024
	
	Program Description: 
	A simple java application that will print a fictional person information on individual lines.
 		First name
 		Last name
 		Street address
 		City
 		Zip code
*/

/**
 * The Main class used to run the program.
 * It creates a Person object and displays the person's information.
 * 
 * @author Alejandro Ricciardi
 */
public class Main {
	/**
     * The main method, creates a Person object and displays the person's information..
     * 
     * @param args The command line arguments (not used in this application).
     */
	public static void main(String[] args) {
		
		// Initializes a Customer object with a customer information
		Person person = new Person("Greg", "Blackwatters", "345 Ai Street", "Robottown", "87011");
		
		// Displaying the customer's information
		person.displayInformation();
	}

}
