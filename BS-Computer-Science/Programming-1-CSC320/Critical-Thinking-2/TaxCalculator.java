
/*
	Program: Calculate Average Withholding
	Description: Performs calculations to determine the tax withholding based on weekly income.
 	Utilized by: Main class
 
*/

/**
 * The TaxCalculator class provides methods to calculate tax rates, withholding amounts, 
 * and net income based on an income brackets. This class is utilized by the Main class
 * to perform tax calculations based on inputted incomes.
 * 
 * @author Alejandro Ricciardi
 */
public class TaxCalculator {
	
	/**
     * Computes the tax rate based on income.
     * The tax rate is determined by the income brackets:
     * - Less than $500: 10%
     * - $500 to $1499.99: 15%
     * - $1500 to $2499.99: 20%
     * - $2500 and above: 30%
     *
     * @param income The weekly income.
     * @return The tax rate as a decimal (e.g., 0.10 for 10%).
     */
    public static double calculateTaxRate(double income) {
        if (income < 500) {
            return 0.10; // 10% tax rate
        } else if (income >= 500 && income < 1500) {
            return 0.15; // 15% tax rate
        } else if (income >= 1500 && income < 2500) {
            return 0.20; // 20% tax rate
        } else {
            return 0.30; // 30% tax rate
        }
    }

    /**
     * Calculates the amount of income to be withheld as tax.
     * This method uses the tax rate determined by the calculateTaxRate method.
     *
     * @param income The weekly income from which the tax is to be withheld.
     * @return The amount of tax withheld.
     */
    public static double calculateWithholdingAmount(double income) {
        double taxRate = calculateTaxRate(income);
        return income * taxRate;
    }

    /**
     * Calculates the net income after tax has been withheld
     * by deducting the calculated withholding amount from the gross income.
     *
     * @param income The gross income from which tax is withheld.
     * @return The net income after tax.
     */
    public static double calculateNetIncome(double income) {
        double withholdingAmount = calculateWithholdingAmount(income);
        return income - withholdingAmount;
    }
}