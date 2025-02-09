/*
	Program Name:  
	Author: Alejandro (Alex) Ricciardi
	Date: 05/05/2024
	
	Program Description: Performs calculations to determine the tax withholding based on weekly income.
*/

/*---------------------------
 |     Imported modules     |
 ---------------------------*/
import java.util.Scanner;

/**
 * The Main class runs the program, it calculates the taxes and displays the results
 * based the user entered income.
 * It performs input validation and uses the TaxCalculator class to determine taxes.
 * 
 * @author Alejandro Ricciardi
 */
public class Main {
	 /**
     * This is the main method that starts the tax calculation process.
     * It prompts the user for their weekly income, validates it, and calculates tax values.
     * It repeatedly prompts for user to enter an income until the user decides to quit.
     * 
     * @param args The command line arguments (not used in this application).
     */
    public static void main(String[] args) {
    	//--- Variables
    	String banner = """ 
    			
        *****************************************
        *     Calculate Average Withholding     *
        ***************************************** 
        """;
        Scanner scanner = new Scanner(System.in);
        String strIncome = "";  // Income enter by user, validate by Regex
        double income = 0,  // Income before tax, enter by user
        	   taxRate,  // Tax rate based on entered income 
        	   withholdingAmount,  // Amount of withhold
        	   netIncome;  // Income after taxes 
        String quiteProgram;
        
        System.out.println(banner);
        
        //---- Program loop 
        while(true) {
	        // Input validation loop
	        while (true) {
	            System.out.print("Please enter your weekly income: ");
	            strIncome = scanner.nextLine();  // User enters income
	            // Regex decimal validation
	            if (strIncome.matches("\\d+\\.\\d{2}")  // Regex two decimals
	            	|| strIncome.matches("\\d+\\.\\d{1}")  // Regex one decimal
	             	|| strIncome.matches("\\d+")  // Regex integer
	            	) {
	            	income = Double.valueOf(strIncome);  //  Validate  income to double type
	            	break;  // exist while loop
	            }
	            
	             System.out.println("\n--- Invalid input. Please enter a positive decimal number.");   
	        }  // Input validation loop
	            
	        // Tax calculations
	        taxRate = TaxCalculator.calculateTaxRate(income) * 100;  // Computes tax rate base on income convert into percentage 
	        withholdingAmount = TaxCalculator.calculateWithholdingAmount(income);  // Calculates Amount withhold
	        netIncome = TaxCalculator.calculateNetIncome(income);  // Calculates income after taxes
	        
	        // Displaying results
	        System.out.println("\n---- Tax Withholding Summary ----");
	        System.out.printf("Gross Income: $%.2f\n", income);
	        System.out.printf("Withholding Percentage: %.0f%%\n", taxRate);
	        System.out.printf("Amount Withheld: $%.2f\n", withholdingAmount);
	        System.out.printf("Net Income: $%.2f\n\n", netIncome);
	        
	        // Quite the program or enter another weekly income
	        System.out.print("Enter 'Q' to exit, or any other key to enter another weekly income: ");
	        quiteProgram = scanner.nextLine();  // User choice
	        if (quiteProgram.length() == 1 && quiteProgram.toLowerCase().charAt(0) == 'q' ) {
	        	System.out.println("\nThank you for using the Calculate Average Withholding program!");
	        	scanner.close();
	        	break;  // exist Program loop
	        }   
	        System.out.println("\n-------------------------------------------------------------------------------\n");
        }  // Program loop
    }  
}
