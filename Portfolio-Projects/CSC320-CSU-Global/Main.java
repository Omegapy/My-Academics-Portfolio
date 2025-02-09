/*
    Program Name: Home Inventory Manager
    Author: Alejandro (Alex) Ricciardi
    Date: 05/26/2024
    
    Program Description: 
    The program manages a home inventory.
    It provides functionality for adding, removing, updating, and displaying home data. 
    The program interacts with the user through a menu-driven interface 
    and stores the home data in a file. 
*/

/*---------------------------
 |     Imported modules     |
 ---------------------------*/
import java.io.File;
import java.util.ArrayList;
import java.util.Scanner;

/**
 * The Main class is used to run the Home Inventory Manager program.
 * It initializes the HomeInventory object,
 * provides a menu for user interaction, 
 * and handles user inputs to manage the home inventory.
 *  
 * @author Alejandro Ricciardi
 * @version 1
 * @date 05/26/2024
 */
public class Main {

    /**
     * The main method is the entry point of the application. 
     * It initializes the HomeInventory object,
     * provides a menu for user interaction, 
     * and handles user inputs to manage the home inventory.
     *
     * @param args command-line arguments (not used)
     */
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        HomeInventory inventory;
        boolean quitProgram = false;  // used to quit program or continue program
        @SuppressWarnings("unused")
		boolean isHomesChangesSaved = true;  // keeps track if changes the home data are saved into a file
        char saveChoice,  // used to store user choice about saving home data to file
             deleteChoice;  // used to store user choice about deleting the file
        String choice;  // used to store user choice main menu
        String banner = """ 
                
                **********************************
                *     Home Inventory Manager     *
                **********************************
        """;

        System.out.println(banner);

        inventory = createInventory(scanner);

        while (!quitProgram) {
        	System.out.println("");
        	System.out.println("""
           Menu        
    1. Add a new home 
    2. Remove a home		
    3. Update a home
    4. List all homes
    5. Display a home
    6. Save changes
    7. Exit    			""");
        			
            choice = scanner.nextLine();
            
            switch (choice) {
                case "1":
                    try {
                    	addHome(scanner, inventory);
                		isHomesChangesSaved = false;
                	} catch (Exception e){
                		System.out.println("-- An error occurred: " + e.getMessage());
                		System.out.println("Please try again.");
                	}
                    break;
                case "2":
                    try {
                    	removeHome(scanner, inventory);
                		isHomesChangesSaved = false;
                	} catch (Exception e){
                		System.out.println("-- An error occurred: " + e.getMessage());
                		System.out.println("Please try again.");
                	}
                    break;
                case "3":
                    try {
                    	updateHome(scanner, inventory);
                		isHomesChangesSaved = false;
                	} catch (Exception e){
                		System.out.println("-- An error occurred: " + e.getMessage());
                		System.out.println("Please try again.");
                	}
                    break;
                case "4":
                    listHomes(inventory);
                    break;
                case "5":
                    displayHome(scanner, inventory);
                    break;
                case "6":
                	try {
                		System.out.println("\n------------------ Saving Homes arrayList to file ----------------------------");
                		saveHome(inventory);
                		System.out.println("------------------------------------------------------------------------------");
                		isHomesChangesSaved = true;
                	} catch (Exception e){
                		System.out.println("An error occurred: " + e.getMessage());
                		System.out.println("Please try again.");
                	}
                	break;
                case "7":
                	if (isHomesChangesSaved == false) {  // Prompts user to save changes if changes were made but not saved on a file
	                    saveChoice = InputValidation.yesOrNo(scanner, "Do you want to save the changes? [Y/N]: ");
	                    if (saveChoice == 'y') {
	                    	try {
	                    		System.out.println("\n------------------ Saving Homes arrayList to file ----------------------------");
	                    		saveHome(inventory);
	                    		System.out.println("------------------------------------------------------------------------------");
	                    	} catch (Exception e){
	                    		System.out.println("An error occurred: " + e.getMessage());
	                    		System.out.println("Please try again.");
	                    	}
	                    }  // End If saveChoice
            		}  // End If
                    // Deleting file 
                    deleteChoice = InputValidation.yesOrNo(scanner, "Do you want to delete the inventory file? [Y/N]: ");
                    if (deleteChoice == 'y') {
                        deleteFile(inventory.getPathFile());
                    }  // else the user entered 'N'
                    quitProgram = true;
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }  // End switch 
        }  // End while-loop
        scanner.close();
        System.out.println("\nThank you for using the Home Inventory Manager program!");
    
    }   // ----End Main Method
    
    // ==============================================================================================  
    /*-----------------------------------
    |     Data Manipulation Methods     |
    ------------------------------------*/
    
    /**
     * Creates a HomeInventory object by prompting the user for the file path and optionally populating it with fake data.
     *
     * @param scanner the Scanner object for user input
     * @return the created HomeInventory object
     */
    public static HomeInventory createInventory(Scanner scanner) {
        String filePath;
        char choiceFakeData;

        while (true) {
            try {
                System.out.println("Please enter the inventory file path-name of an existing file or the path-name of a new file:");
                filePath = scanner.nextLine();

                // Create a File object
                File file = new File(filePath);
                if (file.createNewFile()) {  // true if a new file is created, false if the file already exists
                    while (true) {
                        System.out.println("\nThe file path-name that you entered is a new file!");
                        choiceFakeData = InputValidation.yesOrNo(scanner, "If you want to create a file populated with fake data, enter [Y]."
                        		+ "\nOtherwise, to create a new empty file, enter [N]: ");
                        // Adds fake data to file
                        if (choiceFakeData == 'y') {
                            HomeInventory inventory = new HomeInventory(filePath);
                            System.out.println("\n----------------- Adding fake homes to the homes arrayList --------------------");
                            inventory.addHome(1200, "123 Main St", "Anytown", "CA", 12345, "Model A", "Available");
                            inventory.addHome(1500, "456 Oak Ave", "Somecity", "NY", 67890, "Model B", "Sold");
                            inventory.addHome(1800, "789 Elm Rd", "Anothercity", "TX", 54321, "Model C", "Under Contract");
                            inventory.addHome(2000, "321 Maple Dr", "Somewhere", "FL", 98765, "Model D", "Available");
                            inventory.addHome(1400, "654 Pine Ln", "Nowhere", "WA", 24680, "Model E", "Sold");
                            System.out.println("------------------------------------------------------------------------------");
                            System.out.println("\n------------------ Saving Homes arrayList to file ----------------------------");
                            inventory.saveHomes();
                            System.out.println("The file " + filePath + " was successfully created and populated with fake data!");
                            System.out.println("------------------------------------------------------------------------------");
                            return inventory;  // Exits Method
                        } else {  // User entered 'N', creates an empty file
                            HomeInventory inventory = new HomeInventory(filePath);
                            System.out.println("The file " + filePath + " was successfully created!");
                            return inventory;  // Exits Method
                        }  
                    }  // End While-Loop
                } else {
                    System.out.println("The file " + filePath + " already exists!");
                    System.out.println("\n---------------------------- Loading File Data -------------------------------");
                    HomeInventory inventory = new HomeInventory(filePath);
                    System.out.println("------------------------------------------------------------------------------");
                    return inventory;
                }  // End if
            } catch (Exception e) {
                System.out.println("-- An error occurred: " + e.getMessage());
                System.out.println("Please try again!");
            }
        }  // End While-Loop
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Adds a new home to the inventory by prompting the user for data.
     * The home id is set by the HomeInventory class not the user.
     *
     * @param scanner   the Scanner object for user input
     * @param inventory the HomeInventory object containing the Homes arrayList 
     * @throw Exception if the Homes can not be added to Homes arraList
     */
    private static void addHome(Scanner scanner, HomeInventory inventory) throws Exception {
        try {
            
            Integer squareFeet = InputValidation.squareFeet(scanner, "Enter square feet: ");

            System.out.print("Enter address: ");
            String address = scanner.nextLine();

            System.out.print("Enter city: ");
            String city = scanner.nextLine();

            System.out.print("Enter state: ");
            String state = scanner.nextLine();

            Integer zipCode = InputValidation.zipCode(scanner, "Enter zip code: ");
            
            System.out.print("Enter the home model: ");
            String modelName = scanner.nextLine();

            String saleStatus = InputValidation.saleStatus(scanner, "Enter sale status (sold, available, under contract): ");
            
            System.out.println("\n------------------- Adding home to the Homes arrayList -----------------------");
            inventory.addHome(squareFeet, address, city, state, zipCode, modelName, saleStatus);
            System.out.println("\nHome added successfully.");
            System.out.println("------------------------------------------------------------------------------");
            System.out.println("\n------------ Getting the Home id from the newly created home ------------------");
            Integer homeId = inventory.getHomesList().get(inventory.getHomesList().size() - 1).getId();
            System.out.println("------------------------------------------------------------------------------");
            System.out.println("\n--------------------- Displaying the added home data -------------------------");
            displayHomeUsingId(homeId, inventory);
            System.out.println("------------------------------------------------------------------------------");
        } catch (Exception e) {
        	throw new Exception("Error adding home: " + e.getMessage());
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------
	
    /**
     * Removes a home from the inventory by prompting the user for the home id.
     *
     * @param scanner   the Scanner object for user input
     * @param inventory the HomeInventory object containing the Homes arrayList 
     * @throw Exception if the Homes can not be removed from the Homes arrayList
     */
    private static void removeHome(Scanner scanner, HomeInventory inventory) throws Exception {
        try {
        	System.out.print("Enter the ID of the home to remove: ");
        	String idStr = scanner.nextLine();
        	//------------------------------------------------------------------------------------ Validation input ID
            if (idStr.matches("\\d+")) {  // Regex Check if input is a positive integer
                Integer id = Integer.parseInt(idStr);
                System.out.println("\n-------------------------- Finding home to remove -----------------------------");
                inventory.removeHomeById(id);
                System.out.println("------------------------------------------------------------------------------");
            } else {
            	System.out.println("Invalid id, the id needs to be a possitive integer.");
            	System.out.println("Please try again!");
        	}  //---------------------------------------------------------------------------------- End If validation input ID
        } catch (Exception e) {
        	throw new Exception("Error removing home: " + e.getMessage());
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Updates a home in the inventory by prompting the user for the home id and new new data.
     * Prompts user to choose which home data to update, 
     * and continues updating other fields until user exist the update menu.
     * 
     * @param scanner   the Scanner object for user input
     * @param inventory the HomeInventory object containing the Homes arrayList 
     * @throw Exception if the Homes can not be updated the arrayList
     */
    private static void updateHome(Scanner scanner, HomeInventory inventory) throws Exception {
    	Integer newSquareFeet,
    	        newZipCode;
    	String newAddress,
    	       newCity,
    	       newState,
    	       newModelName,
    	       newSaleStatus;
    	
        try {
	        System.out.print("Enter the id of the home to update: ");
	        String idStr = scanner.nextLine();
	        //------------------------------------------------------------------------------------ Validation input ID as an integer
            if (idStr.matches("\\d+")) {  // Regex Check if input is a positive integer  
            	Integer id = Integer.parseInt(idStr);
	            System.out.println("\n-------------------------- Finding home to update -----------------------------");
	            Home homeToUpdate = inventory.getHomeById(id);
	            System.out.println("------------------------------------------------------------------------------");
	            //------------------------------------------------------------------------ Validation home object to update
	            if (homeToUpdate != null) {
	            	//---------------------------------------------------------- While loop Continue Updating Home Data
	                boolean continueUpdating = true;
	                while (continueUpdating) {
	                	System.out.println("");
	                	System.out.println("""
             Update Home Menu
    Choose the information to update:  
    1. Square Feet 
    2. Address		
    3. City
    4. State
    5. Zip Code
    6. Home Model
    7. Sale Status
    8. Exit update menu """);
	                    String updateChoice = scanner.nextLine();
	                    
	                    switch (updateChoice) {
	                        case "1":
	                            newSquareFeet = InputValidation.squareFeet(scanner, "Enter new square feet: ");
	                            homeToUpdate.setSquareFeet(newSquareFeet);
	                            break;
	                        case "2":
	                            System.out.print("Enter new address: ");
	                            newAddress = scanner.nextLine();
	                            homeToUpdate.setAddress(newAddress);
	                            break;
	                        case "3":
	                            System.out.print("Enter new city: ");
	                            newCity = scanner.nextLine();
	                            homeToUpdate.setCity(newCity);
	                            break;
	                        case "4":
	                            System.out.print("Enter new state: ");
	                            newState = scanner.nextLine();
	                            homeToUpdate.setState(newState);
	                            break;
	                        case "5":
	                            newZipCode = InputValidation.zipCode(scanner, "Enter new zip code: ");
	                            homeToUpdate.setZipCode(newZipCode);
	                            System.out.println("Zip code updated successfully.");
	                            break;
	                        case "6":
	                            System.out.print("Enter new model name: ");
	                            newModelName = scanner.nextLine();
	                            homeToUpdate.setModelName(newModelName);
	                            System.out.println("Model name updated successfully.");
	                            break;
	                        case "7":
	                            newSaleStatus = InputValidation.saleStatus(scanner, "Enter sale status (sold, available, under contract): ");
	                            homeToUpdate.setSaleStatus(newSaleStatus);
	                            System.out.println("Sale status updated successfully.");
	                            break;
	                        case "8":
	                            continueUpdating = false;
	                            break;
	                        default:
	                            System.out.println("Invalid choice. Please try again.");
	                    }  // End switch
	                }  //------------- End While-loop continueUpdating
	                System.out.println("\n-------------------------- Finding home to update -----------------------------");
	                inventory.updateHomeById(id, homeToUpdate);
	                System.out.println("------------------------------------------------------------------------------");
	                System.out.println("\n--------------------- Displaying the updated home data -------------------------");
	                displayHomeUsingId(id, inventory);
	                System.out.println("--------------------------------------------------------------------------------");
	            } else {
	                System.out.println("Home not found.");
	            }  //----------------------------------------------------------------- End If validation home object to update
            } else {
            	System.out.println("Invalid id, the id needs to be a possitive integer.");
            	System.out.println("Please try again!");
        	}  //------------------------------------------------------------------------------- End If validation input ID as an integer
        } catch (Exception e) {
        	throw new Exception("Error updating home: " + e.getMessage());
        }
    }
    
    // ============================================================================================== 
    /*------------------------------
     |     Display Data Methods    |
     ------------------------------*/

    /**
     * Lists-dispalys all homes in the inventory.
     *
     * @param inventory the HomeInventory object containing the homes to arrayList
     */
    private static void listHomes(HomeInventory inventory) {
    	System.out.println("\n--------------------- Displaying the list of homes --------------------------");
        try {
            ArrayList<Home> homesList = inventory.getHomesList();
            if (homesList.isEmpty()) {
                System.out.println("No homes in inventory.");
            } else {
                for (Home home : homesList) {
                    System.out.println(home);
                }
            }
            System.out.println("\n------------------------------------------------------------------------------");
        } catch (Exception e) {
            System.out.println("Error listing homes: " + e.getMessage());
            System.out.println("Please try again.");
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Displays information of a specific home by prompting the user for the home id.
     *
     * @param scanner the Scanner object for user input
     * @param inventory the HomeInventory object containing the homes arrayList
     */
    private static void displayHome(Scanner scanner, HomeInventory inventory) {
        try {
            System.out.print("Enter the id of the home to display: ");
            String idStr = scanner.nextLine();
            //------------------------------------------------------------------------------------ Validation input ID
            if (idStr.matches("\\d+")) {  // Regex Check if input is a positive integer
                Integer id = Integer.parseInt(idStr);
	            scanner.nextLine(); // consume 
	            System.out.println("\n-------------------------- Finding home to display -----------------------------");
	            Home home = inventory.getHomeById(id);
	            System.out.println("-------------------------------------------------------------------------------");
	            //------------------------------------------------------------------------ If validation home object to display
	            if (home != null) {
	                System.out.println(home);
	            } else {
	                System.out.println("Home not found.");
	            }  //----------------------------------------------------------------- End If validation home object to display
            } else {
            	System.out.println("Invalid id, the id needs to be a possitive integer.");
            	System.out.println("Please try again!");
        	}  //---------------------------------------------------------------------------------- End If validation input ID 
        } catch (Exception e) {
        	scanner.nextLine(); // consume newline
            System.out.println("Error displaying home: " + e.getMessage());
            System.out.println("Please try again.");
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------
    
    /**
     * Displays information of a specific home using its id
     *
     * @param scanner the Scanner object for user input
     * @param inventory the HomeInventory object containing the homes
     */
    private static void displayHomeUsingId(Integer id, HomeInventory inventory) {
        try {
            Home home = inventory.getHomeById(id);
            if (home != null) {
                System.out.println(home);
            } else {
                System.out.println("Home not found.");
            }
        } catch (Exception e) {
            System.out.println("Error displaying home: " + e.getMessage());
        }
    }

    // ============================================================================================== 
    /*-----------------------------------
     |     File Manipulation Methods    |
     ------------------------------------*/
    
    /**
     * Deletes the home file.
     *
     * @param filePath the path of the file to delete
     */
    private static void deleteFile(String filePath) {
        // Create a File object
        File file = new File(filePath);

        try {
            // Attempt to delete the file
            boolean result = file.delete();
            System.out.println(result ? "File deleted successfully." : "Failed to delete the file.");
        } catch (SecurityException se) {
            System.out.println("Permission denied cannot delete the file: " + se.getMessage());
        } catch (Exception e) {
            System.out.println("An error occurred cannot delete the file: " + e.getMessage());
        }
    }

    // ---------------------------------------------------------------------------------------------------------

	/**
	 * Saves the data from inventory to a file
	 *
	 * @param inventory the HomeInventory object containing the Homes arrayList 
	 * @throw Exception if the Homes can not be save on file
	 */
	private static void saveHome(HomeInventory inventory) throws Exception {
		try {
	        inventory.saveHomes();  // save changes
	    } catch (Exception e) {
	        throw new Exception("Error saving homes: " + e.getMessage());
	    }
		
	}
	
	// ---------------------------------------------------------------------------------------------------------
}
