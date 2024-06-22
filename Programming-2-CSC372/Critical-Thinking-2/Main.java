/*
    Program Name: Bank Account GUI
    Author: Alejandro (Alex) Ricciardi
    Date: 06/23/2024
    
    Program Description: 
    Bank Account GUI is a simple banking manager system that utilizes the swing library, a graphical user interface (GUI) library. 
    The program allows users to manage basic bank accounts and checking accounts with various functionalities 
    such as creating accounts, attaching checking accounts, 
    depositing and withdrawing funds, and viewing account balances.
*/

/*-------------------
 |     Packages     |
 --------------------*/
package bankAccountGUI;

/**
 *
 * The Main class initializes and runs the Bank Account GUI application. It
 * populates the system with some fake checking accounts and launches the GUI.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 06/23/2024
 */
public class Main {

	/**
	 * 
	 * It populates the system with some fake checking accounts and launches the
	 * GUI.
	 * 
	 * @param args Command line arguments
	 */
	public static void main(String[] args) {
		String banner = """

				        ***************************
				        *     Bank Account GUI    *
				        ***************************
				""";

		System.out.println(banner);

		/*----------------------------------------------
		 |     Populates With Fake Checking Accounts   |
		 ----------------------------------------------*/
		System.out.println("\n**********************************************************");
		System.out.println("\n******* Creating Fake Checking Accounts");
		// Create 5 checking accounts with fake data
		@SuppressWarnings("unused")
		CheckingAccount account1 = new CheckingAccount("John", "Doe", 1000.0, 0.01);
		@SuppressWarnings("unused")
		CheckingAccount account2 = new CheckingAccount("Jane", "Smith", 1500.0, 0.01);
		@SuppressWarnings("unused")
		CheckingAccount account3 = new CheckingAccount("Alice", "Johnson", 2000.0, 0.01);
		@SuppressWarnings("unused")
		CheckingAccount account4 = new CheckingAccount("Bob", "Brown", 2500.0, 0.01);
		@SuppressWarnings("unused")
		CheckingAccount account5 = new CheckingAccount("Charlie", "Davis", 3000.0, 0.01);

		// Display the account details
		for (BankAccount account : BankAccount.accountsList) {
			((CheckingAccount) account).displayAccount();
		}

		/*--------------
		 |     GUI     |
		 --------------*/
		new FrameBankAccount();

	}
}
