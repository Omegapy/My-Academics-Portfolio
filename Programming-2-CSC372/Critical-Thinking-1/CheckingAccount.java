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

/**
 * The CheckingAccount class represents a checking account that is a child of
 * the BankAccount class. It includes an interest rate and allows for overdraft
 * withdrawals but it applies an overdraft fee.
 *
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 06/16/2024
 */
public class CheckingAccount extends BankAccount {
	private Double interestRate;
	private static final double OVERDRAFT_FEE = 30.0;

	/*----------------------
	 |     Constructors    |
	 ----------------------*/

	/**
	 * Default constructor. Initializes a checking account.
	 */
	public CheckingAccount() {
		super();
		this.interestRate = -1.0;
		// adds the newly created BankAccount-CheckingAccount object (ref) to the
		// accountsList
		BankAccount.accountsList.add(this);
		System.out.println("The BankAccount-CheckingAccount object was created successfully!"); // success message
	}

	/**
	 * Constructor-1 with first name and last name but no interest rate. This
	 * constructor creates a new BankAccount object and sets the interest rate to
	 * -1.0.
	 * 
	 * @param firstName The first name of the account holder.
	 * @param lastName  The last name of the account holder.
	 * @throws IllegalArgumentException if the first or last name is empty or
	 *                                  invalid.
	 */
	public CheckingAccount(String firstName, String lastName) throws IllegalArgumentException {
		super(firstName, lastName);
		this.interestRate = -1.0; // this constructor does not set the interest rate.
		// adds the newly created BankAccount-CheckingAccount object (ref) to the
		// accountsList
		BankAccount.accountsList.add(this);
		System.out.println("The BankAccount-CheckingAccount object was created successfully!"); // success message
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Constructor-2 with first name, last name, interest rate, but no balance. This
	 * constructor creates a new BankAccount object.
	 * 
	 * @param firstName    The first name of the account holder.
	 * @param lastName     The last name of the account holder.
	 * @param balance      The initial balance of the account.
	 * @param interestRate The interest rate for the checking account.
	 * @throws IllegalArgumentException if the first or last name is empty, or if
	 *                                  the balance or interest rate is invalid.
	 */
	public CheckingAccount(String firstName, String lastName, Double interestRate) throws IllegalArgumentException {
		super(firstName, lastName);
		try {
			this.interestRate = interestRate;
			// adds the newly created BankAccount-CheckingAccount object (ref) to the
			// accountsList
			BankAccount.accountsList.add(this);
			System.out.println("The BankAccount-CheckingAccount object was created successfully!"); // success message
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Constructor-3 with first name, last name, balance, and interest rate. This
	 * constructor creates a new BankAccount object.
	 * 
	 * @param firstName    The first name of the account holder.
	 * @param lastName     The last name of the account holder.
	 * @param balance      The initial balance of the account.
	 * @param interestRate The interest rate for the checking account.
	 * @throws IllegalArgumentException if the first or last name is empty, or if
	 *                                  the balance or interest rate is invalid.
	 */
	public CheckingAccount(String firstName, String lastName, Double balance, Double interestRate)
			throws IllegalArgumentException {
		super(firstName, lastName, balance);
		try {
			this.interestRate = interestRate;
			// adds the newly created BankAccount-CheckingAccount object (ref) to the
			// accountsList
			BankAccount.accountsList.add(this);
			System.out.println("The BankAccount-CheckingAccount object was created successfully!"); // success message
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Constructor-4 with account ID but no interest rate. This constructor utilized
	 * a bank account ID to attache a checking account to an existing bank account
	 * and sets the interest rate to -1.0.
	 * 
	 * @param accountID The account ID.
	 * @throws IllegalArgumentException if the account ID is invalid.
	 */
	public CheckingAccount(Integer accountID) throws IllegalArgumentException {
		super(accountID);
		try {
			for (BankAccount account : BankAccount.accountsList) {
				if (account.getAccountID() == accountID) {
					this.interestRate = -1.0; // this constructor does not set the interest rate.
					this.firstName = account.firstName;
					this.lastName = account.lastName;
					this.accountID = account.accountID;
					this.balance = account.balance;
					BankAccount.accountsList.remove(account); // removes the account from accounstList
					account = null; // will me deleted from memory by the garbage collector
					// adds the newly created BankAccount-CheckingAccount object (ref) to the
					// accountList object (ref) to the accountList
					BankAccount.accountsList.add(this);
					System.out.println("The CheckingAccount object was created successfully!"); // success message
					return; // exists method
				}
			} // End for-loop
			throw new IllegalArgumentException("Invalid Account ID.");
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(
					"The BankAccount object was not created successfully.\n" + e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Constructor-5 with account ID and interest rate.This constructor utilizes an
	 * account ID AccountCheck to attache a checking account to an existing bank
	 * account.
	 * 
	 * @param accountID    The account ID.
	 * @param interestRate The interest rate for the checking account.
	 * @throws IllegalArgumentException if the account ID or interest rate is
	 *                                  invalid.
	 */
	public CheckingAccount(Integer accountID, Double interesteRate) throws IllegalArgumentException {
		super(accountID);
		try {
			if (interesteRate < 0) {
				throw new IllegalArgumentException("Invalid Interest Rate, the Interest Rate can not be negative.");
			}
			this.interestRate = interesteRate;
			for (BankAccount account : BankAccount.accountsList) {
				if (account.getAccountID() == accountID) {
					this.firstName = account.firstName;
					this.lastName = account.lastName;
					this.accountID = account.accountID;
					this.balance = account.balance;
					BankAccount.accountsList.remove(account); // removes the account from accounstList
					account = null; // will me deleted from memory by the garbage collector
					// adds the newly created BankAccount-CheckingAccount object (ref) to the
					// accountList object (ref) to the accountList
					BankAccount.accountsList.add(this);
					System.out.println("The CheckingAccount object was created successfully!"); // success message
					return; // exists method
				}
			} // End for-loop
			throw new IllegalArgumentException("Invalid Account ID.");
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
	 * Gets the interest rate of the checking account.
	 * 
	 * @return The interest rate.
	 */
	public double getInterestRate() {
		return interestRate;
	}

	// ==============================================================================================
	/*-----------------
	 |     Setters    |
	 -----------------*/

	/**
	 * Sets the interest rate of the checking account.
	 * 
	 * @param interestRate The interest rate to set.
	 * @throws IllegalArgumentException if the interest rate is negative or zero.
	 */
	public void setInterestRate(double interestRate) throws IllegalArgumentException {
		try {
			if (interestRate <= 0.0) {
				throw new IllegalArgumentException(
						"Invalid Interest Rate, the value of the first Name can not negative or zero.");
			} else {
				this.interestRate = interestRate;
				System.out.println("The Interest Rate was set successfully!"); // success message
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
	 * Processes a withdrawal from the checking account. It allows for overdraft
	 * withdrawals but it applies overdraft a fee.
	 * 
	 * @param amount The amount to withdraw.
	 * @throws IllegalArgumentException if the withdrawal amount is invalid.
	 */
	public void processWithdrawal(Double amount) throws IllegalArgumentException {
		try {
			Double balance = getBalance();
			if (amount > 0 && amount <= balance) {
				this.balance -= amount;
				System.out.println("The Withdrawal was successfully!"); // success message
			} else if (amount > 0 && amount > balance) {
				this.balance -= amount + OVERDRAFT_FEE;
				System.out.println("Overdraft! A $30 fee has been applied.");
			} else {
				throw new IllegalArgumentException("Invalid Withdrawal value.");
			}
		} catch (IllegalArgumentException e) {
			throw new IllegalArgumentException(e.getMessage()); // failure message
		}
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Displays the checking account details including the interest rate.
	 */
	public void displayAccount() {
		System.out.println("\n---- Checking Account Summary ----");
		System.out.println(this);
		System.out.printf("Interest Rate: %.2f\n", interestRate);
	}

	// ---------------------------------------------------------------------------------------------------------

}
