/*
	Program Name: Capture Grade Statistics 
	Author: Alejandro (Alex) Ricciardi
	Date: 05/12/2024
	
	Program Description: Performs calculations to determine the tax withholding based on weekly income.
*/

/*---------------------------
 |     Imported modules     |
 ---------------------------*/
import java.util.ArrayList;
import java.util.Scanner;


/**
 * The Main class runs the program and handles user interaction to capture and process grade statistics.
 * It reads user input, validates it, and displays computed results.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 05/12/2024
 */
public class Main {

	/**
     * Main method, entry point for the program.
     * It uses a loop to continuously capture user input until a quit condition is met.
     * 
     * @param args Command line arguments (not used in this application).
     */
	public static void main(String[] args) {
		//--- Variables
    	String banner = """ 
    			
    	        ************************************
    	        *     Capture Grade Statistics     *
    	        ************************************ 
    	""";
		Scanner scanner = new Scanner(System.in);
		String inputGrade = "",  // Use to store user input
			   quitProgram = "";  // Use to quit program or continue program
        double max,  // Stores the highest grade 
               min,  // Stores the lowest grade
               average;  // Store the average grade
        ArrayList<Double> grades = new ArrayList<>();  // stores a list of grades
        
        System.out.println(banner); 
        
        //---- Program loop
        while(!quitProgram.equals("q")) {
		    System.out.println("\n------ Enter Grades ------");
	    	while(true) {
	    		System.out.print("Please enter grade number or enter 'done' to finish: ");
	    		inputGrade = scanner.nextLine().toLowerCase();
	    		if (inputGrade.equals("done")) {break;}  // exits loop
	    		if (inputGrade.matches("\\d+(\\.\\d+)?")) { // Regex, checks if the number is a non-negative floating-point or a non-negative integer
	    			grades.add(Double.parseDouble(inputGrade));
	    		} else {
	    			System.out.println("-- Invalid input. Please enter a non-negative number.");
	    		}
	    	} // grade while-loop
	    	
	    	// Computes grades statistics 
	    	if(!grades.isEmpty()) {  // Checks if grades were entered by user
		    	max = GradesStatCalculator.findMaximum(grades.toArray(new Double[grades.size()]));  // Captures the highest grades, and covert the listArray grades to an array
		    	min = GradesStatCalculator.findMinimum(grades.toArray(new Double[grades.size()]));  // Captures the lowest grades, and covert the listArray grades to an array
		    	average = GradesStatCalculator.findAverage(grades.toArray(new Double[grades.size()]));  // Calculates the average grades, and covert the listArray grades to an array
		    	
		    	// Display results
		    	System.out.println("\n------ Grade Statistics ------");
		    	System.out.println("Average value: " + average);
		    	System.out.println("Maximum value: " + max);
		    	System.out.println("Minimum value: " + min);
	    	} else {
	    		System.out.print("-- No grades were entered!\n");
	    	}
		  
	    	// Quit or continue the program 
	    	grades.clear();
	    	System.out.println("\n----------------------------------------------------------------------------");
	    	System.out.print("Enter 'Q' to exit program, or press enter to input another set of grades: ");
	    	quitProgram = scanner.nextLine().toLowerCase();  
	    	System.out.println("----------------------------------------------------------------------------\n");   
	    	
	    }  // Program While Loop
        scanner.close();
        System.out.println("Thank you for using the Capture Grade Statistics program!");
	}
}
