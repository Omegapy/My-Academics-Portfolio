/*
    Program Name: Home Inventory Manager
    Home InputValidation class
    
    Program Description: 
    The program manages a home inventory.
    It provides functionality for adding, removing, updating, and displaying home data. 
    The program interacts with the user through a menu-driven interface 
    and stores the home data in a file.  
    
    Utilized by: Main
*/

/*---------------------------
 |     Imported modules     |
 ---------------------------*/
import java.util.Scanner;

/**
 * The InputValidation class provides methods to validate user inputs for 
 * the Home Inventory Manager program.
 * It is utilized by the Main class.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @since 2024-05-26
 */
public class InputValidation {

    /**
     * Prompts the user to enter a positive integer for square feet.
     * Re-prompts if the input is invalid.
     *
     * @param scanner the Scanner object for user input
     * @param prompt the prompt message to display to the user
     * @return the validated positive integer for square feet
     */
    public static Integer squareFeet(Scanner scanner, String prompt) {
        String input;
        while (true) {
            System.out.print(prompt);
            input = scanner.nextLine();
            if (input.matches("\\d+")) {
                return Integer.parseInt(input);  // exits while-loop and method
            }
            System.out.println("-- Error: Invalid square feet. Please enter a positive integer.");
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Prompts the user to enter a valid 5-digit zip code.
     * Re-prompts if the input is invalid.
     *
     * @param scanner the Scanner object for user input
     * @param prompt the prompt message to display to the user
     * @return the validated 5-digit zip code
     */
    public static Integer zipCode(Scanner scanner, String prompt) {
        String input;
        while (true) {
            System.out.print(prompt);
            input = scanner.nextLine();
            if (input.matches("\\d{5}")) {
                return Integer.parseInt(input);  // exits while-loop and method
            }
            System.out.println("-- Error: Invalid zip code. Please enter a 5-digit zip code.");
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Prompts the user to enter a valid sale status.
     * Re-prompts if the input is invalid.
     *
     * @param scanner the Scanner object for user input
     * @param prompt the prompt message to display to the user
     * @return the validated sale status ("sold", "available", or "under contract")
     */
    public static String saleStatus(Scanner scanner, String prompt) {
        String[] validStatuses = {"sold", "available", "under contract"};
        String input;
        while (true) {
            System.out.print(prompt);
            input = scanner.nextLine().toLowerCase();
            for (String status : validStatuses) {
                if (input.equals(status)) {
                    return input;  // exits while-loop and method
                }
            }
            System.out.println("-- Error: Invalid sale status. Please enter 'sold', 'available', or 'under contract'.");
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------
    
    /**
     * Prompts the user to enter a valid yes or no answer.
     * Re-prompts if the input is invalid.
     *
     * @param scanner the Scanner object for user input
     * @param prompt the prompt message to display to the user
     * @return the validated yes ('y') or no ('n') answer
     */
    public static char yesOrNo(Scanner scanner, String prompt) {
        String input;
        while (true) {
            System.out.print(prompt);
            input = scanner.nextLine().toLowerCase();
            if (input.equals("y") || input.equals("n")) {
                return input.charAt(0);  // exits while-loop and method
            }
            System.out.println("Invalid input. Please try again!");
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------
    
}
