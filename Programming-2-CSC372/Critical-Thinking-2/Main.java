/*
    Program Name: Bank Account
    Author: Alejandro (Alex) Ricciardi
    Date: 06/16/2024
    
    Program Description: 
    The program manages bank accounts with basic functionalities 
    such as deposit and withdrawal.
    It includes a BankAccount class and a CheckingAccount class that extends the BankAccount 
    with additional features like interest rates and overdraft fees.
*/

/*-------------------
 |     Packages     |
 --------------------*/
package bankAccount;

/**
 * The Main class tests the functionalities of the BankAccount and
 * CheckingAccount classes, including all constructors, getters, setters, and
 * methods. This class ensures that each method and constructor works as
 * expected.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 06/16/2024
 */
public class Main {

	/**
	 * The main method tests the functionality of the BankAccount and
	 * CheckingAccount classes. It creates instances using various constructors,
	 * sets values using setters, and retrieves values using getters. It also tests
	 * deposit and withdrawal methods, including cash and checks overdrafts in the
	 * BankAccount class and CheckingAccount class.
	 * 
	 * 
	 * 
	 * @param args Command line arguments
	 */
	public static void main(String[] args) {
		String banner = """

				        ************************
				        *     Bank Account     *
				        ************************
				""";

		System.out.println(banner);

		System.out.println("            ******* Testing Functionality ********");

		// ------------------------------ BankAccount's constructors, setters, and
		// getters

		System.out.println("\n**********************************************************");
		System.out.println("\n******* Creating Bank Accounts");

		// Default Constructor BankAccount
		System.out.println("\n*** Default Constructor - bankAccount1 BankAccount object");
		BankAccount bankAccount1 = new BankAccount();
		bankAccount1.accountSummary();
		System.out.println("\n--- setting values in bankAccount1");
		bankAccount1.setFirstName("John");
		bankAccount1.setLastName("Doe");
		bankAccount1.setAccountID(12563478);
		System.out.println(bankAccount1);
		System.out.println("\n--- deposite $500 and cash withdrawal $100 in bankAccount1");
		bankAccount1.deposit(500.0);
		bankAccount1.withdrawalCash(100.0);
		bankAccount1.accountSummary();

		// Constructor-2 BankAccount
		System.out.println("\n      ****************");
		System.out.println("\n*** constructor-2 with first name and last name - bankAccount2 BankAccount object");
		BankAccount bankAccount2 = new BankAccount("Jane", "Smith");
		bankAccount2.accountSummary();

		// Constructor-3 BankAccount
		System.out.println("\n      ****************");
		System.out.println(
				"\n*** constructor-3 with first name, last name, and balance -  bankAccount3 BankAccount object");
		BankAccount bankAccount3 = new BankAccount("Alice", "Johnson", 2000.0);
		bankAccount3.accountSummary();
		System.out.println("\n--- checking getters with bankAccount3");
		System.out.println("Getting first name: " + bankAccount3.getFirstName());
		System.out.println("Getting last name: " + bankAccount3.getLastName());
		System.out.printf("Getting account ID: %08d\n", bankAccount3.getAccountID());
		System.out.printf("Getting Balance: $%.2f\n", bankAccount3.getBalance());

		// ------------------------------ CheckingAccount's constructors, setters, and
		// getters

		System.out.println("\n**********************************************************");
		System.out.println("\n******* Creating Checking Accounts");

		// Default Constructor CheckingAccount
		System.out.println("\n*** Default Constructor - checkingAccount1 CheckingAccount object");
		CheckingAccount checkingAccount1 = new CheckingAccount();
		checkingAccount1.displayAccount();
		System.out.println("\n--- setting values in checkingAccount1");
		checkingAccount1.setFirstName("Tom");
		checkingAccount1.setLastName("Hart");
		checkingAccount1.setAccountID(78901234);
		checkingAccount1.setInterestRate(1.5);
		checkingAccount1.displayAccount();
		System.out.println("\n--- deposite $500 and cash check withdrawal $100 in checkingAccount1");
		checkingAccount1.deposit(500.0);
		checkingAccount1.processWithdrawal(100.0);
		checkingAccount1.accountSummary();

		// Constructor-1 CheckingAccount
		System.out.println("\n      ****************");
		System.out.println(
				"\n*** constructor-1 with first name and last name but no balance or interest rate - checkingAccount2 CheckingAccount object");
		CheckingAccount checkingAccount2 = new CheckingAccount("Janet", "Lock");
		checkingAccount2.displayAccount();

		// Constructor-2 CheckingAccount
		System.out.println("\n      ****************");
		System.out.println(
				"\n*** constructor-2 with first name, last name, and interest rate but no balance - checkingAccount3 CheckingAccount object");
		CheckingAccount checkingAccount3 = new CheckingAccount("Greg", "Martin", 1.5);
		checkingAccount3.displayAccount();

		// Constructor-3 CheckingAccount
		System.out.println("\n      ****************");
		System.out.println(
				"\n*** constructor-3 with first name, last name, balance, and interest rate - checkingAccount4 CheckingAccount object");
		CheckingAccount checkingAccount4 = new CheckingAccount("Claire", "Douglass", 1000.00, 1.5);
		System.out.println("\n--- checking getters with checkingAccount4");
		System.out.println("Getting first name: " + checkingAccount4.getFirstName());
		System.out.println("Getting last name: " + checkingAccount4.getLastName());
		System.out.printf("Getting account ID: %08d\n", checkingAccount4.getAccountID());
		System.out.printf("Getting Balance: $%.2f\n", checkingAccount4.getBalance());
		System.out.printf("Getting Interest Rate: %.2f\n", checkingAccount4.getInterestRate());

		// Constructor-4 CheckingAccount utilized a bank account ID to attache a
		// checking account to an existing bank account - no interest rate
		System.out.println("\n      ****************");
		System.out.println(
				"\n*** constructor-4 with account ID but no interest rate- checkingAccount5 CheckingAccount object");
		bankAccount2.accountSummary(); // existing bank account before attaching checking account
		CheckingAccount checkingAccount5 = new CheckingAccount(2);
		checkingAccount5.displayAccount();

		// Constructor-4 CheckingAccount utilized a bank account ID to attache a
		// checking account to an existing bank account - no interest rate
		System.out.println("\n      ****************");
		System.out.println(
				"\n*** constructor-5 with account ID and interest rate- checkingAccount6 CheckingAccount object");
		bankAccount3.accountSummary(); // existing bank account before attaching checking account
		System.out.println();
		CheckingAccount checkingAccount6 = new CheckingAccount(3, 1.5);
		checkingAccount6.displayAccount();

		// ------------------------------ Checking Cash and checking Overdraft
		// functionalities

		System.out.println("\n**********************************************************");
		System.out.println("\n******* Checking Cash and checking Overdraft functionalities.");

		// Cash Overdraft
		System.out.println("\n      ****************");
		System.out.println("\n*** Cash Overdraft functionalities using bankAccount3, withdrawal balance + $1");
		bankAccount3.accountSummary();
		System.out.println();
		try {
			bankAccount3.withdrawalCash(bankAccount3.getBalance() + 1.0); // Cash Overdraft
		} catch (IllegalArgumentException e) {
			System.out.println(e.getMessage());
		}
		System.out.println("\n      ****************");
		// Check Overdraft
		System.out.println("\n*** Check Overdraft functionalities using checkingAccount4, withdrawal balance + $20.");
		checkingAccount4.displayAccount();
		System.out.println();
		checkingAccount4.processWithdrawal(checkingAccount4.getBalance() + 20.0); // Cash Overdraft
		checkingAccount4.displayAccount();
	}
}
