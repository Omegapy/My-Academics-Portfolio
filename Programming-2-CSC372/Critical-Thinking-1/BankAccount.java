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
package bankAccount; // Program Folder

/*---------------------------
 |    Imported modules      |
 ---------------------------*/
import java.util.ArrayList;

/**
 * The BankAccount class represents a basic bank account with fields for first
 * name, account ID, and balance. It provides methods to deposit and withdraw
 * funds and does not allow cash overdrafts in comparison its extended
 * CheckingAccount class allows with an overdraft fee the checks overdraft.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 06/16/2024
 */
public class BankAccount {
	private static Integer numAccounts = 0;
	protected static ArrayList<BankAccount> accountsList = new ArrayList<BankAccount>();

	protected String firstName;
	protected String lastName;
	protected int accountID; // Used int primitive type instead of Integer class type as required by
								// assignment
	protected double balance; // Used double primitive type instead of Double class type as required by
								// assignment

	/*---------------------
	 |     Constructors    |
	 ----------------------*/
	/**
	 * Default constructor. Initializes a bank account with default values. The
	 * account ID is auto-incremented.
	 */
	public BankAccount() {
		assignAccountID();
		this.firstName = "Unknown";
		this.lastName = "Unknown";
		this.balance = 0.0;
		BankAccount.accountsList.add(this); // adds the newly created BankAccount object (ref) to the accountList
		System.out.println("The BankAccount object was created successfully!"); // success message
	}

	// ---------------------------------------------------------------------------------------------------------
	/**
	 * Constructor-1 with account ID. This constructor is utilized by the
	 * AccountCheck class to attache a checking account to an existing bank account
	 * 
	 * @param accountID The account ID for an existing bank account.
	 */
	protected BankAccount(Integer accountID) {
		this.accountID = accountID;
		this.firstName = "Unknown";
		this.lastName = "Unknown";
		this.balance = 0.0;
		BankAccount.accountsList.add(this); // adds the newly created BankAccount object (ref) to the accountsList
		System.out.println("The BankAccount object was created successfully!"); // success message
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Constructor-2 with first name, last name.
	 * 
	 * @param firstName The first name.
	 * @param lastName  The last name.
	 * @throws IllegalArgumentException if the first or last name is empty or
	 *                                  invalid.
	 */
	public BankAccount(String firstName, String lastName) throws IllegalArgumentException {
		try {
			if (firstName.isEmpty()) {
				throw new IllegalArgumentException("The value of the firstName can not be empty.");
			} else if (lastName.isEmpty()) {
				throw new IllegalArgumentException("The value of the lastName can not be empty");
			} else {
				assignAccountID();
				this.firstName = firstName;
				this.lastName = lastName;
				this.balance = 0.0;
				BankAccount.accountsList.add(this); // adds the newly created BankAccount object (ref) to the
													// accountsList
				System.out.println("The BankAccount object was created successfully!"); // success message
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(
					"The BankAccount object was not created successfully.\n" + e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Constructor-3 with first name, last name, and balance.
	 * 
	 * @param firstName The first name.
	 * @param lastName  The last name.
	 * @param balance   The initial balance.
	 * @throws IllegalArgumentException if the first or last name is empty, or the
	 *                                  balance is invalid.
	 */
	public BankAccount(String firstName, String lastName, Double balance) throws IllegalArgumentException {
		try {
			if (firstName.isEmpty()) {
				throw new IllegalArgumentException("The value of the firstName can not be empty.");
			} else if (lastName.isEmpty()) {
				throw new IllegalArgumentException("The value of the lastName can not be empty");
			} else if (balance < 0) {
				throw new IllegalArgumentException("When creating an Bank Account the balance can not be negative.");
			} else {
				assignAccountID();
				this.firstName = firstName;
				this.lastName = lastName;
				this.balance = balance;
				BankAccount.accountsList.add(this); // adds the newly created BankAccount object (ref) to the
													// accountsList
				System.out.println("The BankAccount object was created successfully!"); // success message
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(
					"The BankAccount object was not created successfully.\n" + e.getMessage()); // failure message
		}
	}

	// ==============================================================================================
	/*----------------
	 |    Getters    |
	 ----------------*/

	/**
	 * Gets the first name of the account.
	 * 
	 * @return The first name.
	 */
	public String getFirstName() {
		return firstName;
	}

	/**
	 * Gets the last name of the account.
	 * 
	 * @return The last name.
	 */
	public String getLastName() {
		return lastName;
	}

	/**
	 * Gets the account ID.
	 * 
	 * @return The account ID.
	 */
	public int getAccountID() {
		return accountID;
	}

	/**
	 * Gets the balance of the account.
	 * 
	 * @return The account balance.
	 */
	public double getBalance() {
		return balance;
	}

	// ==============================================================================================
	/*-----------------
	 |     Setters    |
	 -----------------*/

	/**
	 * Sets the first name of the account.
	 * 
	 * @param firstName The first name to set.
	 * @throws IllegalArgumentException if the first name is empty or invalid.
	 */
	public void setFirstName(String firstName) throws IllegalArgumentException {
		try {
			if (firstName.isEmpty()) {
				throw new IllegalArgumentException("Invalid First Name, the value of the first Name can not be empty.");
			} else {
				this.firstName = firstName;
				System.out.println("The First Name was set successfully!"); // success message
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Sets the last name of the account.
	 * 
	 * @param lastName The last name to set.
	 * @throws IllegalArgumentException if the last name is empty or invalid.
	 */
	public void setLastName(String lastName) throws IllegalArgumentException {
		try {
			if (firstName.isEmpty()) {
				throw new IllegalArgumentException("Invalid Last Name, the value of the Last Name can not be empty.");
			} else {
				this.lastName = lastName;
				System.out.println("The Last Name was set successfully!"); // success message
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Sets the account ID.
	 * 
	 * @param accountID The account ID to set.
	 * @throws IllegalArgumentException if the account ID is invalid or already in
	 *                                  use.
	 */
	public void setAccountID(Integer accountID) throws IllegalArgumentException {
		Boolean isAccountID = false;
		for (BankAccount account : BankAccount.accountsList) {
			if (account.getAccountID() == accountID) {
				isAccountID = true;
				break;
			}
		}
		try {
			if (accountID > 99999999 || accountID < 1) {
				throw new IllegalArgumentException(
						"Invalid Accound ID, the Account ID needs to be a 8 digits positive nonzero integer.");
			} else if (isAccountID) {
				throw new IllegalArgumentException(
						"Invalid Accound ID, this Account ID needs is use by another account.");
			} else {
				this.accountID = accountID;
				System.out.println("The Accound ID was set successfully!"); // success message
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ==============================================================================================
	/*-----------------
	 |     Methods    |
	 -----------------*/

	/**
	 * Sets the account ID. It Look for a not used account ID and assigned it to the
	 * BankAccount object. This prevents duplicating the account IDs created with
	 * the setAccountID() method
	 * 
	 * @param accountID The account ID to set.
	 */
	private void assignAccountID() {
		Boolean isAccountIDUsed = false;
		do { // Increments numAccounts until account ID is not used
			this.accountID = ++BankAccount.numAccounts;
			if (!BankAccount.accountsList.isEmpty()) {
				for (BankAccount account : BankAccount.accountsList) { // searches for account ID match
					if (account.getAccountID() == this.accountID) {
						isAccountIDUsed = true;
						break; // exits for-loop
					}
				} // End for-loop
			} else {
				isAccountIDUsed = false;
			}
		} while (isAccountIDUsed);
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Deposits a specified amount into the account.
	 * 
	 * @param amount The amount to deposit.
	 * @throws IllegalArgumentException if the deposit amount is invalid.
	 */
	public void deposit(double amount) {
		try {
			if (amount > 0) {
				balance += amount;
				System.out.println("The Deposite was added successfully!"); // success message
			} else {
				throw new IllegalArgumentException("The deposit amount must be positive.");
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Withdraws a specified amount from the account.
	 * 
	 * @param amount The amount to withdraw.
	 * @throws IllegalArgumentException if the withdrawal amount is invalid.
	 */
	public void withdrawalCash(Double amount) {
		try {
			if (amount > 0 && amount <= balance) {
				balance -= amount;
				System.out.println("The Cash Withdrawal was successful!"); // success message
			} else {
				throw new IllegalArgumentException("Insufficient balance or invalid amount.");
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Provides a string representation of the bank account details.
	 * 
	 * @return A string containing the account summary.
	 */
	@Override
	public String toString() {
		String strAccountID = String.format("%08d", accountID);
		String strBalance = String.format("%.2f", balance);
		return "First Name: " + firstName + "\n" + "Last Name: " + lastName + "\n" + "Account ID: " + strAccountID
				+ "\n" + "Balance: $" + strBalance;
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Displays the bank account summary.
	 * 
	 */
	public void accountSummary() {
		System.out.println("\n---- Bank Account Summary ----");
		System.out.println(this);
	}

	// ---------------------------------------------------------------------------------------------------------
}
