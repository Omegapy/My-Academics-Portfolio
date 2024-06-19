package bankAccountGUI;

import java.awt.BorderLayout;
import java.awt.Font;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class FrameBankAccount extends JFrame implements ActionListener {
	private static final long serialVersionUID = 1L;

	private JPanel mainPanel;
	private JPanel welcomePanel;
	private JPanel addBankAccountPanel;
	private JPanel addCheckingAccountPanel;
	private JPanel attachCheckingAccountPanel;
	private JPanel depositPanel;
	private JPanel withdrawPanel;
	private JPanel viewBalancePanel;

	public FrameBankAccount() {
		// Set up the frame
		setTitle("Bank Account GUI");
		setSize(750, 300);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLocationRelativeTo(null);

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

	@Override
	public void actionPerformed(ActionEvent e) {
		mainPanel.removeAll();
		switch (e.getActionCommand()) {
		case "Add New Bank Account" -> mainPanel.add(addBankAccountPanel, BorderLayout.CENTER);
		case "Add New Checking Account" -> mainPanel.add(addCheckingAccountPanel, BorderLayout.CENTER);
		case "Attach Checking Account to Existing Bank Account" ->
			mainPanel.add(attachCheckingAccountPanel, BorderLayout.CENTER);
		case "Deposit Cash" -> mainPanel.add(depositPanel, BorderLayout.CENTER);
		case "Withdraw Cash" -> mainPanel.add(withdrawPanel, BorderLayout.CENTER);
		case "View Balance" -> mainPanel.add(viewBalancePanel, BorderLayout.CENTER);
		}
		mainPanel.revalidate();
		mainPanel.repaint();
	}

	private void returnToWelcomePanel() {
		mainPanel.removeAll();
		mainPanel.add(welcomePanel, BorderLayout.CENTER);
		mainPanel.revalidate();
		mainPanel.repaint();
	}

	private JPanel createWelcomePanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();
		gridBC.insets = new Insets(10, 10, 10, 10);

		JLabel welcomeLabel = new JLabel("Bank Account Manager");
		welcomeLabel.setFont(new Font("Arial", Font.BOLD, 16));
		gridBC.gridx = 0;
		gridBC.gridy = 0;
		gridBC.gridwidth = 2;
		panel.add(welcomeLabel, gridBC);

		JPanel buttonPanel = new JPanel(new GridLayout(3, 2, 10, 10)); // 3 rows, 2 columns, with spacing

		JButton addBankAccountButton = new JButton("Add New Bank Account");
		JButton addCheckingAccountButton = new JButton("Add New Checking Account");
		JButton attachCheckingAccountButton = new JButton("Attach Checking Account to Existing Bank Account");
		JButton depositButton = new JButton("Deposit Cash");
		JButton withdrawButton = new JButton("Withdraw Cash");
		JButton viewBalanceButton = new JButton("View Balance");

		addBankAccountButton.addActionListener(this);
		addCheckingAccountButton.addActionListener(this);
		attachCheckingAccountButton.addActionListener(this);
		depositButton.addActionListener(this);
		withdrawButton.addActionListener(this);
		viewBalanceButton.addActionListener(this);

		buttonPanel.add(addBankAccountButton);
		buttonPanel.add(addCheckingAccountButton);
		buttonPanel.add(attachCheckingAccountButton);
		buttonPanel.add(depositButton);
		buttonPanel.add(withdrawButton);
		buttonPanel.add(viewBalanceButton);

		gridBC.gridx = 0;
		gridBC.gridy = 1;
		gridBC.gridwidth = 2;
		panel.add(buttonPanel, gridBC);

		return panel;
	}

	private JPanel createAddBankAccountPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		JLabel panelTitle = new JLabel("New Bank Account");

		JLabel firstNameLabel = new JLabel("First Name:");
		JTextField firstNameField = new JTextField(15);
		JLabel lastNameLabel = new JLabel("Last Name:");
		JTextField lastNameField = new JTextField(15);
		JLabel balanceLabel = new JLabel("Initial Balance:");
		JTextField balanceField = new JTextField(15);
		JButton createButton = new JButton("Create");

		createButton.addActionListener(e -> {
			String firstName = firstNameField.getText();
			String lastName = lastNameField.getText();
			String strBbalance = balanceField.getText();
			try {
				double balance = Double.parseDouble(strBbalance);
				BankAccount account = new BankAccount(firstName, lastName);
				account.deposit(balance);
				JOptionPane.showMessageDialog(this, "Bank Account created successfully!\n" + account);
				returnToWelcomePanel();
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "Invalid balance amount.", "Error", JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5);

		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(firstNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(firstNameField, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(lastNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(lastNameField, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 3;
		panel.add(balanceLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(balanceField, gridBC);

		gridBC.gridx = 1;
		gridBC.gridy = 4;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(createButton, gridBC);

		return panel;
	}

	private JPanel createAddCheckingAccountPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		JLabel panelTitle = new JLabel("New Checking Account");

		JLabel firstNameLabel = new JLabel("First Name:");
		JTextField firstNameField = new JTextField(15);
		JLabel lastNameLabel = new JLabel("Last Name:");
		JTextField lastNameField = new JTextField(15);
		JLabel balanceLabel = new JLabel("Initial Balance:");
		JTextField balanceField = new JTextField(15);
		JButton createButton = new JButton("Create");

		createButton.addActionListener(e -> {
			String firstName = firstNameField.getText();
			String lastName = lastNameField.getText();
			String strBalance = balanceField.getText();
			try {
				double balance = Double.parseDouble(strBalance);
				CheckingAccount account = new CheckingAccount(firstName, lastName);
				account.deposit(balance);
				JOptionPane.showMessageDialog(this, "Checking Account created successfully!\n" + account);
				returnToWelcomePanel();
			} catch (NumberFormatException ex) {
				JOptionPane.showMessageDialog(this, "Invalid balance amount.", "Error", JOptionPane.ERROR_MESSAGE);
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5);

		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(firstNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(firstNameField, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(lastNameLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(lastNameField, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 3;
		panel.add(balanceLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(balanceField, gridBC);

		gridBC.gridx = 1;
		gridBC.gridy = 4;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(createButton, gridBC);

		return panel;
	}

	private JPanel createAttachCheckingAccountPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		JLabel panelTitle = new JLabel("Add Checking to Existing Bank Account");

		JLabel accountIDLabel = new JLabel("Existing Account ID:");
		JTextField accountIDField = new JTextField(15);
		JButton attachButton = new JButton("Attach");

		attachButton.addActionListener(e -> {
			String strAccountID = accountIDField.getText();
			Integer accountID = Integer.parseInt(strAccountID);
			try {
				CheckingAccount account = new CheckingAccount(accountID);
				JOptionPane.showMessageDialog(this, "Checking Account attached successfully!\n" + account);
				returnToWelcomePanel();
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5);

		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);

		gridBC.gridx = 1;
		gridBC.gridy = 2;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(attachButton, gridBC);

		return panel;
	}

	private JPanel createDepositPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		JLabel panelTitle = new JLabel("Deposite");

		JLabel accountIDLabel = new JLabel("Account ID:");
		JTextField accountIDField = new JTextField(15);
		JLabel amountLabel = new JLabel("Amount to Deposit:");
		JTextField amountField = new JTextField(15);
		JButton depositButton = new JButton("Deposit");

		depositButton.addActionListener(e -> {
			String strAccountID = accountIDField.getText();
			Integer accountID = Integer.parseInt(strAccountID);
			String strAmount = amountField.getText();
			Double amount = Double.parseDouble(strAmount);
			try {
				for (BankAccount account : BankAccount.accountsList) {
					if (account.getAccountID().equals(accountID)) {
						account.deposit(amount);
						JOptionPane.showMessageDialog(this, "Deposit successful!\n" + account);
						returnToWelcomePanel();
						return;
					}
				}
				throw new IllegalArgumentException("Account ID not found.");
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5);

		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(amountLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(amountField, gridBC);

		gridBC.gridx = 1;
		gridBC.gridy = 3;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(depositButton, gridBC);

		return panel;
	}

	private JPanel createWithdrawPanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		JLabel panelTitle = new JLabel("Withdraw");

		JLabel accountIDLabel = new JLabel("Account ID:");
		JTextField accountIDField = new JTextField(15);
		JLabel amountLabel = new JLabel("Amount to Withdraw:");
		JTextField amountField = new JTextField(15);
		JButton withdrawButton = new JButton("Withdraw");

		withdrawButton.addActionListener(e -> {
			String strAccountID = accountIDField.getText();
			Integer accountID = Integer.parseInt(strAccountID);
			String amountStr = amountField.getText();
			Double amount = Double.parseDouble(amountStr);
			try {
				for (BankAccount account : BankAccount.accountsList) {
					if (account.getAccountID().equals(accountID)) {
						account.withdrawalCash(amount);
						JOptionPane.showMessageDialog(this, "Withdrawal successful!\n" + account);
						returnToWelcomePanel();
						return;
					}
				}
				throw new IllegalArgumentException("Account ID not found.");
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5);

		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 1;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 2;
		panel.add(amountLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(amountField, gridBC);

		gridBC.gridx = 1;
		gridBC.gridy = 3;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(withdrawButton, gridBC);

		return panel;
	}

	private JPanel createViewBalancePanel() {
		JPanel panel = new JPanel(new GridBagLayout());
		GridBagConstraints gridBC = new GridBagConstraints();

		JLabel panelTitle = new JLabel("Get Balance");

		JLabel accountIDLabel = new JLabel("Account ID:");
		JTextField accountIDField = new JTextField(15);
		JButton viewBalanceButton = new JButton("View Balance");

		viewBalanceButton.addActionListener(e -> {
			String strAccountID = accountIDField.getText();
			Integer accountID = Integer.parseInt(strAccountID);
			try {
				for (BankAccount account : BankAccount.accountsList) {
					if (account.getAccountID().equals(accountID)) {
						JOptionPane.showMessageDialog(this, "Account Balance: $" + account.getBalance());
						returnToWelcomePanel();
						return;
					}
				}
				throw new IllegalArgumentException("Account ID not found.");
			} catch (IllegalArgumentException ex) {
				JOptionPane.showMessageDialog(this, ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
			}
		});

		gridBC.insets = new Insets(5, 5, 5, 5);

		panelTitle.setFont(new Font("Arial", Font.BOLD, 12));
		gridBC.gridx = 1;
		gridBC.gridy = 0;
		panel.add(panelTitle, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 0;
		panel.add(accountIDLabel, gridBC);
		gridBC.gridx = 1;
		panel.add(accountIDField, gridBC);

		gridBC.gridx = 0;
		gridBC.gridy = 1;
		gridBC.gridwidth = 2;
		gridBC.anchor = GridBagConstraints.CENTER;
		panel.add(viewBalanceButton, gridBC);

		return panel;
	}
}
