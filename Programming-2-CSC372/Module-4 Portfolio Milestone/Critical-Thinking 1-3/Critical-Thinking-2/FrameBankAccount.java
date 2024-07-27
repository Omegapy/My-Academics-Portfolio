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
package bankAccountGUI;// Program Folder

/*---------------------------
 |    Imported modules      |
 ---------------------------*/
//--- Abstract Window Toolkit (AWT)
import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

//--- swing GUI
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;

/**
 * FrameBankAccount class utilizes the swing library to provide a GUI for
 * managing bank accounts. It allows users to utilize various operation to
 * manage bank accounts. Operations such as adding new bank accounts, attaching
 * checking accounts, depositing, and withdrawing funds, and viewing account
 * balances.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 06/23/2024
 */
public class FrameBankAccount extends JFrame implements ActionListener {
	private static final long serialVersionUID = 1L;

	private JPanel mainPanel; // Main panel for the GUI
	private JPanel welcomePanel; // Panel for the welcome screen
	private JPanel addBankAccountPanel; // Panel for adding new bank accounts
	private JPanel addCheckingAccountPanel; // Panel for adding new checking accounts
	private JPanel attachCheckingAccountPanel; // Panel for attaching checking accounts to existing accounts
	private JPanel depositPanel; // Panel for depositing cash
	private JPanel withdrawPanel; // Panel for withdrawing cash
	private JPanel viewBalancePanel; // Panel for viewing account balances

	private ImageIcon icon; // Icon for the application

	/*---------------------
	 |     Constructors    |
	 ----------------------*/
	/**
	 * Constructs the FrameBankAccount object and initializes the GUI components.
	 */
	public FrameBankAccount() {
		// Set up the frame
		setTitle("Bank Account GUI");
		setSize(750, 300);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLocationRelativeTo(null);

		this.icon = new ImageIcon("logo.png");
		this.setIconImage(icon.getImage());

		// Create the main panel with BorderLayout
		mainPanel = new JPanel(new BorderLayout());

		// Create operation panels
		welcomePanel = createWelcomePanel();
		addBankAccountPanel = createAddBankAccountPanel();
		addCheckingAccountPanel = createAddCheckingAccountPanel();
		attachCheckingAccountPanel = createAttachCheckingAccountPanel();
		depositPanel = createDepositPanel();
		withdrawPanel = createWithdrawPanel();
		viewBalancePanel = createViewBalancePanel();

		// Add the welcome panel to the main panel
		mainPanel.add(welcomePanel, BorderLayout.CENTER);

		// Add the main panel to the frame
		add(mainPanel);

		// Display the frame
		setVisible(true);
	}

	// ==============================================================================================
	/*------------------------------
	 |    Functionality Methods    |
	 ------------------------------*/

	/**
	 * Handles button click events and switches between different panels.
	 * 
	 * @param e the action event triggered by a button click
	 */
	@Override
	public void actionPerformed(ActionEvent e) {
		mainPanel.removeAll(); // Clears existing components from the mainPanel.
		switch (e.getActionCommand()) { // Adds mainPanel menu buttons
		case "Add New Bank Account" -> mainPanel.add(addBankAccountPanel, BorderLayout.CENTER);
		case "Add New Checking Account" -> mainPanel.add(addCheckingAccountPanel, BorderLayout.CENTER);
		case "Attach Checking Account to Existing Bank Account" ->
			mainPanel.add(attachCheckingAccountPanel, BorderLayout.CENTER);
		case "Deposit Cash" -> mainPanel.add(depositPanel, BorderLayout.CENTER);
		case "Withdraw Cash" -> mainPanel.add(withdrawPanel, BorderLayout.CENTER);
		case "View Balance" -> mainPanel.add(viewBalancePanel, BorderLayout.CENTER);
		}
		mainPanel.revalidate(); // Revalidates the mainPanel after its component hierarchy has changed
		mainPanel.repaint(); // Redraws welcomePanel on the screen
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Resets and displays the welcome panel.
	 */
	private void resetDisplayWelcomePanel() {
		mainPanel.removeAll(); // Clears existing components from the mainPanel.
		mainPanel.add(welcomePanel, BorderLayout.CENTER);
		mainPanel.revalidate(); // Revalidates the mainPanel after its component hierarchy has changed
		mainPanel.repaint(); // Redraws welcomePanel on the screen
	}

	// ==============================================================================================
	/*----------------------
	 |    Panel Methods    |
	 -----------------------*/

	/**
	 * Creates the welcome panel with a menu.
	 * 
	 * @return the welcome panel
	 */
	private JPanel createWelcomePanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();
		gridBC.insets = new Insets(10, 10, 10, 10); // Padding around components

		// Display Panel title using JLabel
		JLabel welcomeLabel = new JLabel("Bank Account Manager");
		welcomeLabel.setFont(new Font("Arial", Font.BOLD, 16));
		gridBC.gridx = 0;
		gridBC.gridy = 0;
		gridBC.gridwidth = 2;
		panel.add(welcomeLabel, gridBC);

		// Creates menu buttons panel
		JPanel buttonPanel = new JPanel(new GridLayout(3, 2, 10, 10)); // 3 rows, 2 columns, with spacing
		// Menu buttons object
		JButton addBankAccountButton = new JButton("Add New Bank Account");
		JButton addCheckingAccountButton = new JButton("Add New Checking Account");
		JButton attachCheckingAccountButton = new JButton("Attach Checking Account to Existing Bank Account");
		JButton depositButton = new JButton("Deposit Cash");
		JButton withdrawButton = new JButton("Withdraw Cash");
		JButton viewBalanceButton = new JButton("View Balance");
		// Adds action listener to buttons
		addBankAccountButton.addActionListener(this);
		addCheckingAccountButton.addActionListener(this);
		attachCheckingAccountButton.addActionListener(this);
		depositButton.addActionListener(this);
		withdrawButton.addActionListener(this);
		viewBalanceButton.addActionListener(this);
		// Adds the the buttons to the button panel
		buttonPanel.add(addBankAccountButton);
		buttonPanel.add(addCheckingAccountButton);
		buttonPanel.add(attachCheckingAccountButton);
		buttonPanel.add(depositButton);
		buttonPanel.add(withdrawButton);
		buttonPanel.add(viewBalanceButton);
		// Positions button panel within the welcome panel
		gridBC.gridx = 0;
		gridBC.gridy = 1;
		gridBC.gridwidth = 2;
		panel.add(buttonPanel, gridBC);

		return panel;
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Creates the panel for adding a new bank account.
	 * 
	 * @return the panel for adding a new bank account
	 */
	private JPanel createAddBankAccountPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		// Panel title using JLabel
		JLabel panelTitle = new JLabel("New Bank Account");
		// Components text and fields
		JLabel firstNameLabel = new JLabel("First Name:");
		JTextField firstNameField = new JTextField(15);
		JLabel lastNameLabel = new JLabel("Last Name:");
		JTextField lastNameField = new JTextField(15);
		JLabel balanceLabel = new JLabel("Initial Balance:");

		// Button
		JTextField balanceField = new JTextField(15);
		JButton createButton = new JButton("Create");
		// Button Action Listener
		createButton.addActionListener(e -> {
			try {
				String firstName = firstNameField.getText();
				String lastName = lastNameField.getText();
				String strBalance = balanceField.getText();

				// Saves user inputed data
				Double balance = Double.parseDouble(strBalance);
				BankAccount account = new BankAccount(firstName, lastName);
				account.deposit(balance);
				// Displays data
				JOptionPane.showMessageDialog(this, "Bank Account created successfully!\n" + account);
				// Clears fields
				firstNameField.setText("");
				lastNameField.setText("");
				balanceField.setText("");
				// Returns to main menu
				resetDisplayWelcomePanel();
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "A field is empty or the wrong data type was entered.", "Error",
						JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5); // Padding around components
		// Positions Panel title
		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);
		// Positions first name's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(firstNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(firstNameField, gridBC);
		// Positions last name's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(lastNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(lastNameField, gridBC);
		// Positions balance's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 3;
		panel.add(balanceLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(balanceField, gridBC);
		// Positions button
		gridBC.gridx = 1;
		gridBC.gridy = 4;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(createButton, gridBC);

		return panel;
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Creates the panel for adding a new checking account.
	 * 
	 * @return the panel for adding a new checking account
	 */
	private JPanel createAddCheckingAccountPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		// Panel title using JLabel
		JLabel panelTitle = new JLabel("New Checking Account");
		// Components text and fields
		JLabel firstNameLabel = new JLabel("First Name:");
		JTextField firstNameField = new JTextField(15);
		JLabel lastNameLabel = new JLabel("Last Name:");
		JTextField lastNameField = new JTextField(15);
		JLabel balanceLabel = new JLabel("Initial Balance:");
		JTextField balanceField = new JTextField(15);

		// Button
		JButton createButton = new JButton("Create");
		// Button Action Listener
		createButton.addActionListener(e -> {
			try {
				String firstName = firstNameField.getText();
				String lastName = lastNameField.getText();
				String strBalance = balanceField.getText();

				// Saves user inputed data
				Double balance = Double.parseDouble(strBalance);
				CheckingAccount account = new CheckingAccount(firstName, lastName, 0.01);
				account.deposit(balance);
				// Displays data
				String strInterestRate = String.format("%.2f", account.getInterestRate());
				JOptionPane.showMessageDialog(this,
						"Checking Account created successfully!\n" + account + "\nInterest Rate: " + strInterestRate);
				firstNameField.setText("");
				lastNameField.setText("");
				balanceField.setText("");
				// Returns to main menu
				resetDisplayWelcomePanel();
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "A field is empty or the wrong data type was entered.", "Error",
						JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5); // Padding around components
		// Positions Panel title
		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);
		// Positions first name's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(firstNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(firstNameField, gridBC);
		// Positions last name's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(lastNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(lastNameField, gridBC);
		// Positions balance's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 3;
		panel.add(balanceLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(balanceField, gridBC);
		// Positions button
		gridBC.gridx = 1;
		gridBC.gridy = 4;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(createButton, gridBC);

		return panel;
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Creates the panel for attaching a checking account to an existing bank
	 * account.
	 * 
	 * @return the panel for attaching a checking account
	 */
	private JPanel createAttachCheckingAccountPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		// Panel title using JLabel
		JLabel panelTitle = new JLabel("Add Checking to Existing Bank Account");
		// Components text and fields
		JLabel accountIDLabel = new JLabel("Existing Account ID:");
		JTextField accountIDField = new JTextField(15);

		// Button
		JButton attachButton = new JButton("Attach");
		// Button Action Listener
		attachButton.addActionListener(e -> {
			try {
				String strAccountID = accountIDField.getText();
				Integer accountID = Integer.parseInt(strAccountID);

				for (BankAccount account : BankAccount.accountsList) { // Finds account using account-ID
					if (account.getAccountID().equals(accountID)) {
						if (account.getHasCheckingAccount()) {
							throw new IllegalArgumentException(
									"The bank account already has a checking account attached to it.");
						}
						// Saves user inputed data
						CheckingAccount accountAttachedChecking = new CheckingAccount(accountID, 0.01);
						// Displays data
						String strInterestRate = String.format("%.2f", accountAttachedChecking.getInterestRate());
						JOptionPane.showMessageDialog(this, "Checking Account attached successfully!\n"
								+ accountAttachedChecking + "\nInterest Rate: " + strInterestRate);
						// Clears fields
						accountIDField.setText("");
						// Returns to main menu
						resetDisplayWelcomePanel();
						return;
					}
				}
				throw new IllegalArgumentException("Account ID not found.");
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "No account-ID was entered or the wrong data type was entered.",
						"Error", JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5); // Padding around components
		// Positions Panel title
		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);
		// Positions account-ID's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);
		// Positions button
		gridBC.gridx = 1;
		gridBC.gridy = 2;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(attachButton, gridBC);

		return panel;
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Creates the panel for depositing cash into an account.
	 * 
	 * @return the panel for depositing cash
	 */
	private JPanel createDepositPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		// Panel title using JLabel
		JLabel panelTitle = new JLabel("Deposit");
		// Components text and fields
		JLabel accountIDLabel = new JLabel("Account ID:");
		JTextField accountIDField = new JTextField(15);
		JLabel amountLabel = new JLabel("Amount to Deposit:");
		JTextField amountField = new JTextField(15);

		// Button
		JButton depositButton = new JButton("Deposit");
		// Button Action Listener
		depositButton.addActionListener(e -> {
			try {
				String strAccountID = accountIDField.getText();
				Integer accountID = Integer.parseInt(strAccountID);
				String strAmount = amountField.getText();
				Double amount = Double.parseDouble(strAmount);

				for (BankAccount account : BankAccount.accountsList) { // Finds account using account-ID
					if (account.getAccountID().equals(accountID)) {
						// Saves user inputed data
						account.deposit(amount);
						// Displays data
						JOptionPane.showMessageDialog(this, "Deposit successful!\n" + account);
						// Clears fields
						accountIDField.setText("");
						amountField.setText("");
						// Returns to main menu
						resetDisplayWelcomePanel();
						return;
					}
				}
				throw new IllegalArgumentException("Account ID not found.");
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "A field is empty or the wrong data type was entered.", "Error",
						JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5); // Padding around components
		// Positions Panel title
		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);
		// Positions account-ID's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);
		// Positions deposit-amount's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(amountLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(amountField, gridBC);
		// Positions button
		gridBC.gridx = 1;
		gridBC.gridy = 3;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(depositButton, gridBC);

		return panel;
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Creates the panel for withdrawing cash from an account.
	 * 
	 * @return the panel for withdrawing cash
	 */
	private JPanel createWithdrawPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		// Panel title using JLabel
		JLabel panelTitle = new JLabel("Withdraw");
		// Components text and fields
		JLabel accountIDLabel = new JLabel("Account ID:");
		JTextField accountIDField = new JTextField(15);
		JLabel amountLabel = new JLabel("Amount to Withdraw:");
		JTextField amountField = new JTextField(15);

		// Button
		JButton withdrawButton = new JButton("Withdraw");
		// Button Action Listener
		withdrawButton.addActionListener(e -> {
			try {
				String strAccountID = accountIDField.getText();
				Integer accountID = Integer.parseInt(strAccountID);
				String amountStr = amountField.getText();
				Double amount = Double.parseDouble(amountStr);

				for (BankAccount account : BankAccount.accountsList) { // Finds account using account-ID
					if (account.getAccountID().equals(accountID)) {
						// Saves user inputed data
						account.withdrawalCash(amount);
						// Clears fields
						JOptionPane.showMessageDialog(this, "Withdrawal successful!\n" + account);
						// Clears fields
						accountIDField.setText("");
						amountField.setText("");
						// Returns to main menu
						resetDisplayWelcomePanel();
						return;
					}
				}
				throw new IllegalArgumentException("Account ID not found.");
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "A field is empty or the wrong data type was entered.", "Error",
						JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5); // Padding around components
		// Positions Panel title
		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);
		// Positions account-ID's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);
		// Positions withdraw-amount's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(amountLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(amountField, gridBC);
		// Positions button
		gridBC.gridx = 1;
		gridBC.gridy = 3;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(withdrawButton, gridBC);

		return panel;
	}

	// ---------------------------------------------------------------------------------------------------------

	/**
	 * Creates the panel for viewing the balance of an account.
	 * 
	 * @return the panel for viewing the balance
	 */
	private JPanel createViewBalancePanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		// Panel title using JLabel
		JLabel panelTitle = new JLabel("View Balance");
		// Components text and fields
		JLabel accountIDLabel = new JLabel("Account ID:");
		JTextField accountIDField = new JTextField(15);

		// Button
		JButton viewBalanceButton = new JButton("View Balance");
		// Button Action Listener
		viewBalanceButton.addActionListener(e -> {
			try {
				String strAccountID = accountIDField.getText();
				Integer accountID = Integer.parseInt(strAccountID);
				for (BankAccount account : BankAccount.accountsList) { // Finds account using account-ID
					if (account.getAccountID().equals(accountID)) {
						// Displays data
						JOptionPane.showMessageDialog(this, "Account Balance: $" + account.getBalance());
						// Clears fields
						accountIDField.setText("");
						// Returns to main menu
						resetDisplayWelcomePanel();
						return;
					}
				}
				throw new IllegalArgumentException("Account ID not found.");
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "No account-ID was entered or the wrong data type was entered.",
						"Error", JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5); // Padding around components
		// Positions Panel title
		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);
		// Positions account-ID's text and field
		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);
		// Positions button
		gridBC.gridx = 1;
		gridBC.gridy = 2;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(viewBalanceButton, gridBC);

		return panel;
	}

	// ---------------------------------------------------------------------------------------------------------
}
