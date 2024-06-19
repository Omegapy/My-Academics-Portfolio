/*
    Program Name: Bank Account GUI
    Author: Alejandro (Alex) Ricciardi
    Date: 06/23/2024
    
    Program Description: 
    
*/

/*-------------------
 |     Packages     |
 --------------------*/
package bankAccountGUI;

/**
 *
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 06/23/2024
 */
public class Main {

	/**
	 * 
	 * 
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
		CheckingAccount account1 = new CheckingAccount("John", "Doe", 1000.0, 0.01);
		CheckingAccount account2 = new CheckingAccount("Jane", "Smith", 1500.0, 0.01);
		CheckingAccount account3 = new CheckingAccount("Alice", "Johnson", 2000.0, 0.01);
		CheckingAccount account4 = new CheckingAccount("Bob", "Brown", 2500.0, 0.01);
		CheckingAccount account5 = new CheckingAccount("Charlie", "Davis", 3000.0, 0.01);

		// Display the account details
		for (BankAccount account : BankAccount.accountsList) {
			((CheckingAccount) account).displayAccount();
		}

		new FrameBankAccount();

	}
}
