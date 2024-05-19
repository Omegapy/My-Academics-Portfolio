/*
    Program Name: Get Monthly Temperatures
    Author: Alejandro (Alex) Ricciardi
    Date: 05/19/2024
    
    Program Description: 
    Displays monthly average temperatures, 
    and allows the user to view individual monthly temperatures or a yearly summary 
    that includes the yearly average temperature as well as the highest and lowest monthly averages. 
*/

/*---------------------------
 |     Imported modules     |
 ---------------------------*/
import java.util.Scanner;

/**
 * The Main class is used to run the Get Monthly Temperatures program.
 * It prompts the user to view and display both the month and average temperature.
 * If "year" is entered, it displays the temperature for each month along with
 * the yearly average as well as the highest and lowest monthly averages.
 * Utilizes the MonthlyAvgTemps class.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 05/19/2024
 */
public class Main {  
    /**
     * The main method to run the Get Monthly Temperatures program.
     * 
     * @param args The command line arguments (not used in this application).
     */
    public static void main(String[] args) {
        String banner = """ 
                
                ************************************
                *     Get Monthly Temperatures     *
                ************************************ 
        """;
        Scanner scanner = new Scanner(System.in);
        String monthChoice = "", 
        	   quitProgram = "";  // Use to quit program or continue program

        // Stores monthly temperatures for a year
        int[] avgTemps = {30, 32, 45, 55, 65, 75, 80, 78, 70, 60, 50, 35};
        // Initializes MonthlyAvgTemps object with the monthly temperatures array
        MonthlyAvgTemps avgMonthlyTemps = new MonthlyAvgTemps(avgTemps);  

        System.out.println(banner);  // Display banner

        //--- Program loop ---
        while (!quitProgram.equals("q")) {  // if 'q' is entered exit program
            //--- Menu
        	System.out.println("Enter the month corresponding 'number' to see its average temperature\nor 'year' to see the yearly monthly temperature averages summary:\n");
            for (int i = 0; i < 12; i++) {  // Displays months corresponding number choices
                System.out.println((i + 1) + ": " + avgMonthlyTemps.getMonths()[i]);
            }
            System.out.println("\n'year': yearly summary");
            System.out.print("\nEnter your choice: ");
            monthChoice = scanner.nextLine().toLowerCase();
            // Processes user's choice
            if (monthChoice.equals("year")) {  // Display yearly summary
                displayYearlySummary(avgMonthlyTemps); 
                // Prompts the user to quit program or continue program
                System.out.println("\n----------------------------------------------------------------------------");
                System.out.print("Enter 'Q' to exit program, or press enter to input another set of grades: ");
                quitProgram = scanner.nextLine().toLowerCase();
                System.out.println("----------------------------------------------------------------------------\n");
            } else if (monthChoice.matches("\\d{1,2}")) {  // Regex Check if input is a one or two-digit number
                switch (Integer.parseInt(monthChoice)) {  // Processes user's month choice
                    case 1:
                    case 2:
                    case 3:
                    case 4:
                    case 5:
                    case 6:
                    case 7:
                    case 8:
                    case 9:
                    case 10:
                    case 11:
                    case 12:
                        displayMonthlyTemperature(avgMonthlyTemps, Integer.parseInt(monthChoice) - 1);  // Display selected month temperature
                        // Prompts the user to quit program or continue program
                        System.out.println("\n----------------------------------------------------------------------------");
                        System.out.print("Enter 'Q' to exit program, or press enter to input another set of grades: ");
                        quitProgram = scanner.nextLine().toLowerCase();
                        System.out.println("----------------------------------------------------------------------------\n");
                        break;
                    default:
                        System.out.println("--- Invalid choice. Please enter a number between 1 and 12.\n");
                        break;
                }  // end switch user's month choice
            } else {
                System.out.println("--- Invalid value entered, try again!\n");
            }  // end if user's choice
            
        }  // Program while loop
        
        scanner.close();
        System.out.println("Thank you for using the Get Monthly Temperatures program!");
    
    }  // end main method
    
    /*----------------------------
    |     Main Class Methods     |
    -----------------------------*/

    /**
     * Displays the temperature for a specific month.
     * 
     * @param monthlyTemps The MonthlyAvgTemps object containing monthly temperatures data.
     * @param monthIndex The index of the month to display.
     */
    public static void displayMonthlyTemperature(MonthlyAvgTemps monthlyTemps, int monthIndex) {
        String[] months = monthlyTemps.getMonths();
        int[] temps = monthlyTemps.getTemps();
        System.out.println(months[monthIndex] + ": " + temps[monthIndex] + "°F");
    }

    /**
     * Displays the yearly summary of temperatures.
     * 
     * @param monthlyTemps The MonthlyAvgTemps object containing monthly temperatures data.
     */
    public static void displayYearlySummary(MonthlyAvgTemps monthlyTemps) {
        String[] months = monthlyTemps.getMonths();
        int[] temps = monthlyTemps.getTemps();
        
        int yearlyAvg = monthlyTemps.getYearlyAvg();
        int highestTempIndex = monthlyTemps.getHighestMonthIndex();
        int lowestTempIndex = monthlyTemps.getLowestMonthIndex();

        System.out.println("\nMonthly Average Temperatures:");
        for (int i = 0; i < months.length; i++) {
            System.out.println(months[i] + ": " + temps[i] + "°F");
        }

        System.out.println("\nYearly Average Temperature: " + yearlyAvg + "°F");
        System.out.println("Highest Monthly Average: " + months[highestTempIndex] + " with " + temps[highestTempIndex] + "°F");
        System.out.println("Lowest Monthly Average: " + months[lowestTempIndex] + " with " + temps[lowestTempIndex] + "°F");
    }
}