/*
    Program Name: Home Inventory Manager
    Author: Alejandro (Alex) Ricciardi
    Date: 05/26/2024
    
    Program Description: 
    This is Alpha version of the Home Inventory Manager program.
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
 * The Main class is used to run the the Home Inventory Manager program.
 * It initializes the HomeInventory object,
 * provides a menu for user interaction, 
 * and handles user inputs to manage the home inventory.
 *  
 * @author Alejandro Ricciardi
 * @version Alpha
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
        boolean quitProgram = false;  // Use to quit program or continue program
        Integer choice;
        String banner = """ 
                
                **********************************
                *     Home Inventory Manager     *
                **********************************
        """;

        System.out.println(banner);

        inventory = createInventory(scanner);

        while (!quitProgram) {
            System.out.println("1. Add a new home");
            System.out.println("2. Remove a home");
            System.out.println("3. Update a home");
            System.out.println("4. List all homes");
            System.out.println("5. Display a home");
            System.out.println("6. Exit");
            System.out.print("Enter your choice: ");
            choice = scanner.nextInt();
          
            switch (choice) {
                case 1:
                    addHome(scanner, inventory);
                    break;
                case 2:
                    removeHome(scanner, inventory);
                    break;
                case 3:
                    updateHome(scanner, inventory);
                    break;
                case 4:
                    listHomes(inventory);
                    break;
                case 5:
                    displayHome(scanner, inventory);
                    break;
                case 6:
                    System.out.print("Do you want to save the changes? [Y/N]: ");
                    String saveChoice = scanner.nextLine().toLowerCase();
                    if (saveChoice.equals("y")) {
                        try {
                            inventory.saveHomes();  // save changes
                        } catch (Exception e) {
                            System.out.println("Error saving homes: " + e.getMessage());
                        }
                    }
                    
                    System.out.print("Do you want to delete the inventory file? [Y/N]: ");
                    String deleteChoice = scanner.nextLine().toLowerCase();
                    if (deleteChoice.equals("y")) {
                        deleteFile(inventory.getPathFile());
                    }
                    quitProgram = true;
                    break;
                default:
                    System.out.println("Invalid choice. Please try again.");
            }  // End switch 
        }  // End while-loop
        scanner.close();
        System.out.println("Thank you for using the Home Inventory Manager program!");
    }   // End Main Method
    
    // -----------------------------------------------------------------------------------------------
    
    /*----------------------------
    |     Main Class Methods     |
    -----------------------------*/

    /**
     * Adds a new home to the inventory by prompting the user for data.
     * The home id is set by the HomeInventory class not the user.
     *
     * @param scanner   the Scanner object for user input
     * @param inventory the HomeInventory object to add the home to
     */
    private static void addHome(Scanner scanner, HomeInventory inventory) {
        try {
            System.out.print("Enter square feet: ");
            Integer squareFeet = scanner.nextInt();
            scanner.nextLine(); // consume newline

            System.out.print("Enter address: ");
            String address = scanner.nextLine();

            System.out.print("Enter city: ");
            String city = scanner.nextLine();

            System.out.print("Enter state: ");
            String state = scanner.nextLine();

            System.out.print("Enter zip code: ");
            Integer zipCode = scanner.nextInt();
            scanner.nextLine(); // consume newline

            System.out.print("Enter model name: ");
            String modelName = scanner.nextLine();

            System.out.print("Enter sale status (sold, available, under contract): ");
            String saleStatus = scanner.nextLine();

            inventory.addHome(squareFeet, address, city, state, zipCode, modelName, saleStatus);
            System.out.println("Home added successfully.");
            // Display the added home data using its id
            Integer homeId = inventory.getHomesList().get(inventory.getHomesList().size()).getId();
            displayHomeUsingId(homeId, inventory);
        } catch (Exception e) {
            System.out.println("Error adding home: " + e.getMessage());
        }
    }

    /**
     * Removes a home from the inventory by prompting the user for the home id.
     *
     * @param scanner   the Scanner object for user input
     * @param inventory the HomeInventory object to remove the home from
     */
    private static void removeHome(Scanner scanner, HomeInventory inventory) {
        try {
            System.out.print("Enter the ID of the home to remove: ");
            Integer id = scanner.nextInt();
            scanner.nextLine(); // consume newline
            inventory.removeHomeById(id);
            System.out.println("Home removed successfully.");
        } catch (Exception e) {
            System.out.println("Error removing home: " + e.getMessage());
        }
    }

    /**
     * Updates a home in the inventory by prompting the user for the home id and new new data.
     * Prompts user to choose which home data to update, 
     * and continues updating other fields until user exist the update menu.
     * 
     * @param scanner   the Scanner object for user input
     * @param inventory the HomeInventory object to update the home in
     */
    private static void updateHome(Scanner scanner, HomeInventory inventory) {
        try {
            System.out.print("Enter the ID of the home to update: ");
            int id = scanner.nextInt();
            scanner.nextLine(); // consume newline

            Home homeToUpdate = inventory.getHomeById(id);
            if (homeToUpdate != null) {
                boolean continueUpdating = true;
                while (continueUpdating) {
                    System.out.println("Choose the information to update:");
                    System.out.println("1. Square feet");
                    System.out.println("2. Address");
                    System.out.println("3. City");
                    System.out.println("4. State");
                    System.out.println("5. Zip code");
                    System.out.println("6. Model name");
                    System.out.println("7. Sale status");
                    System.out.println("8. Exit update menu");
                    System.out.print("Enter your choice: ");
                    int updateChoice = scanner.nextInt();
                    scanner.nextLine(); // consume newline

                    switch (updateChoice) {
                        case 1:
                            System.out.print("Enter new square feet: ");
                            int newSquareFeet = scanner.nextInt();
                            scanner.nextLine(); // consume newline
                            homeToUpdate.setSquareFeet(newSquareFeet);
                            System.out.println("Square feet updated successfully.");
                            break;
                        case 2:
                            System.out.print("Enter new address: ");
                            String newAddress = scanner.nextLine();
                            homeToUpdate.setAddress(newAddress);
                            System.out.println("Address updated successfully.");
                            break;
                        case 3:
                            System.out.print("Enter new city: ");
                            String newCity = scanner.nextLine();
                            homeToUpdate.setCity(newCity);
                            System.out.println("City updated successfully.");
                            break;
                        case 4:
                            System.out.print("Enter new state: ");
                            String newState = scanner.nextLine();
                            homeToUpdate.setState(newState);
                            System.out.println("State updated successfully.");
                            break;
                        case 5:
                            System.out.print("Enter new zip code: ");
                            int newZipCode = scanner.nextInt();
                            scanner.nextLine(); // consume newline
                            homeToUpdate.setZipCode(newZipCode);
                            System.out.println("Zip code updated successfully.");
                            break;
                        case 6:
                            System.out.print("Enter new model name: ");
                            String newModelName = scanner.nextLine();
                            homeToUpdate.setModelName(newModelName);
                            System.out.println("Model name updated successfully.");
                            break;
                        case 7:
                            System.out.print("Enter new sale status (sold, available, under contract): ");
                            String newSaleStatus = scanner.nextLine();
                            homeToUpdate.setSaleStatus(newSaleStatus);
                            System.out.println("Sale status updated successfully.");
                            break;
                        case 8:
                            continueUpdating = false;
                            break;
                        default:
                            System.out.println("Invalid choice. Please try again.");
                    }
                }

                inventory.updateHomeById(id, homeToUpdate);
                System.out.println("Home updated successfully.");
                // Display the updated home data using its id
                displayHomeUsingId(id, inventory);
            } else {
                System.out.println("Home not found.");
            }
        } catch (Exception e) {
            System.out.println("Error updating home: " + e.getMessage());
        }
    }

    /**
     * Lists-dispalys all homes in the inventory.
     *
     * @param inventory the HomeInventory object containing the homes to list
     */
    private static void listHomes(HomeInventory inventory) {
        try {
            ArrayList<Home> homesList = inventory.getHomesList();
            if (homesList.isEmpty()) {
                System.out.println("No homes in inventory.");
            } else {
                for (Home home : homesList) {
                    System.out.println(home);
                }
            }
        } catch (Exception e) {
            System.out.println("Error listing homes: " + e.getMessage());
        }
    }

    /**
     * Displays information of a specific home by prompting the user for the home id.
     *
     * @param scanner the Scanner object for user input
     * @param inventory the HomeInventory object containing the homes
     */
    private static void displayHome(Scanner scanner, HomeInventory inventory) {
        try {
            System.out.print("Enter the id of the home to display: ");
            Integer id = scanner.nextInt();
            scanner.nextLine(); // consume newline
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

    /**
     * Creates a HomeInventory object by prompting the user for the file path and optionally populating it with fake data.
     *
     * @param scanner   the Scanner object for user input
     * @return the created HomeInventory object
     */
    public static HomeInventory createInventory(Scanner scanner) {
        String filePath;
        String choiceFakeData;

        while (true) {
            try {
                System.out.print("Please enter the inventory file path-name of an existing file or the path-name of a new file: ");
                filePath = scanner.nextLine();

                // Create a File object
                File file = new File(filePath);
                if (file.createNewFile()) {  // true if a new file is created, false if the file already exists
                    while (true) {
                        System.out.println("\nThe file path-name that you entered is a new file!");
                        System.out.println("If you want to create a file populated with fake data, enter [Y].");
                        System.out.println("Otherwise, to create a new empty file, enter [N]");
                        choiceFakeData = scanner.nextLine().toLowerCase();
                        if (choiceFakeData.equals("y")) {
                            HomeInventory inventory = new HomeInventory(filePath);
                            inventory.addHome(1200, "123 Main St", "Anytown", "CA", 12345, "Model A", "Available");
                            inventory.addHome(1500, "456 Oak Ave", "Somecity", "NY", 67890, "Model B", "Sold");
                            inventory.addHome(1800, "789 Elm Rd", "Anothercity", "TX", 54321, "Model C", "Under Contract");
                            inventory.addHome(2000, "321 Maple Dr", "Somewhere", "FL", 98765, "Model D", "Available");
                            inventory.addHome(1400, "654 Pine Ln", "Nowhere", "WA", 24680, "Model E", "Sold");
                            System.out.println("The file " + filePath + " was successfully created and populated with fake data!");
                            return inventory;
                        } else if (choiceFakeData.equals("n")) {
                            HomeInventory inventory = new HomeInventory(filePath);
                            System.out.println("The file " + filePath + " was successfully created!");
                            return inventory;
                        } else {
                            System.out.println("-- Invalid Entry! Please try again.");
                        }
                    }
                } else {
                    HomeInventory inventory = new HomeInventory(filePath);
                    System.out.println("The file path-name that you entered is an already existing file!");
                    return inventory;
                }
            } catch (Exception e) {
                System.out.println("An error occurred: " + e.getMessage());
                System.out.println("Please try again!");
            }
        }
    }

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
}
