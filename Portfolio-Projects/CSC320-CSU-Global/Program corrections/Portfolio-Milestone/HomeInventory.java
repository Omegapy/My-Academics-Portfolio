/*
    Program Name: Home Inventory Manager
    HomeInventory class
    
    Program Description: 
    This is an Alpha version of the Home Inventory Manager program.
    The program manages a home inventory.
    It provides functionality for adding, removing, updating, and displaying home data. 
    The program interacts with the user through a menu-driven interface 
    and stores the home data in a file. 
    
    Utilized by: Main class
*/

/*---------------------------
 |     Imported modules     |
 ---------------------------*/

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Creates an Inventory object that manages home data
 * allowing for adding, removing, updating, and saving home data.
 * The class can also create, read, write, and delete a home file text containing the home data.
 * The class has getters and setters’ methods to access and manipulate the Home and Inventory objects’ data.
 * 
 * It is utilized by the Main class.
 * 
 * @author Alejandro Ricciardi
 * @version Alpha
 * @date 05/26/2024 
 */
public class HomeInventory {
    private static Integer numHome = 0;
    
    private ArrayList<Home> homes;
    private String filePath = null;
    
    /*--------------------
    |     Constructor    |
    ---------------------*/

    /**
     * Constructs a HomeInventory object with the specified file path.
     * Loads homes data from the file into the homes array list.
     * 
     * @param filePath the path of the file containing homes data
     * @throws Exception if the file path is null or an error occurs while loading homes
     */
    public HomeInventory(String filePath) throws Exception {
        try {
            if (filePath == null) {
                throw new NullPointerException("File name-path is null!");
            }
            this.filePath = filePath;
            this.homes = new ArrayList<>();
            loadHomes();  // load homes data in the homes array list
            if (!homes.isEmpty()) {
                numHome = homes.get(homes.size() - 1).getId();  // gets the last home id value entered
            }
            System.out.println("The Home object was created successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }   
    }
  
    /*-----------------
    |     Getters    |
    -----------------*/
    
    /**
     * Gets the file path of the home inventory.
     * 
     * @return the file path
     * @throws NullPointerException if the file path is null
     */
    public String getPathFile() throws NullPointerException {
        try {
            if (filePath == null) { 
                throw new NullPointerException("File name-path is null!");
            }
            System.out.println("The file name-path was found!");  // success message
            return filePath;
        } catch (NullPointerException e) {
            throw new NullPointerException(e.getMessage()); 
        }
    }
    
    /**
     * Gets the home by its ID.
     * 
     * @param id the ID of the home
     * @return the home with the specified ID
     * @throws Exception if the home with the specified ID is not found or an error occurs
     */
    public Home getHomeById(Integer id) throws Exception {
        try {
            for (Home home : homes) {
                if (home.getId() == id) {
                    System.out.println("The home was found!"); // success message
                    return home;  // exists for-loop and method
                }
            }
            throw new Exception("The provided id does not match a home!");
        } catch (Exception e) {
            throw new Exception(e.getMessage());   // failure message   
        }   
    }
    
    /**
     * Gets the home by its address.
     * 
     * @param address the address of the home
     * @return the home with the specified address
     * @throws Exception if the home with the specified address is not found or an error occurs
     */
    public Home getHomeByAddress(String address) throws Exception {
        try {
            for (Home home : homes) {
                if (home.getAddress().equals(address)) {
                    System.out.println("The home address was found!"); // success message
                    return home;  // exists for-loop and method
                }
            }
            throw new Exception("The provided home address was not found!");
        } catch (Exception e) {
            throw new Exception(e.getMessage());   // failure message   
        }    
    }
    
    /**
     * Gets the list of all homes in the inventory.
     * 
     * @return the list of homes
     * @throws Exception if the homes list is null or an error occurs
     */
    public ArrayList<Home> getHomesList() throws Exception {
        try {
            if (homes == null) {
                throw new Exception("The homes list is null");
            }
            System.out.println("The homes list was retrieved successfully!"); // success message
            return homes;
        } catch (Exception e) {
            throw new Exception(e.getMessage());   // failure message   
        }
    }
    
    /*-----------------
    |     Setters    |
    -----------------*/
    
    /**
     * Adds a new home to the inventory.
     * 
     * @param squareFeet the square footage of the home
     * @param address    the address of the home
     * @param city       the city where the home is located
     * @param state      the state where the home is located
     * @param zipCode    the zip code of the home
     * @param modelName  the model name of the home
     * @param saleStatus the sale status of the home
     * @throws Exception if an error occurs while adding the home
     */
    public void addHome(Integer squareFeet, String address, String city, String state, Integer zipCode, String modelName, String saleStatus) throws Exception {
        try {
            Home home = new Home(++numHome, squareFeet, address, city, state, zipCode, modelName, saleStatus);
            homes.add(home);
            System.out.println("The Home was added successfully");  // success message
        } catch (Exception e) {
            throw new Exception(e.getMessage());   // failure message   
        }
    }
    
    /**
     * Removes a home from the inventory by its id.
     * 
     * @param id the ID of the home to remove
     * @throws Exception if the home with the specified ID is not found or an error occurs
     */
    public void removeHomeById(Integer id) throws Exception {
        try {
            boolean removed = homes.removeIf(home -> home.getId() == id);
            if (removed) {
                System.out.println("The home was removed successfully!");  // success message
            } else {
                throw new Exception("The home with the provided ID was not found!");
            }
        } catch (Exception e) {
            throw new Exception(e.getMessage());   // failure message   
        }
    }
    
    /**
     * Removes a home from the inventory by its address.
     * 
     * @param address the address of the home to remove
     * @throws Exception if the home with the specified address is not found or an error occurs
     */
    public void removeHomeByAddress(String address) throws Exception {
        try {
            boolean removed = homes.removeIf(home -> home.getAddress().equals(address));
            if (removed) {
                System.out.println("The home was removed successfully!");  // success message
            } else {
                throw new Exception("The home with the provided address was not found!");
            }
        } catch (Exception e) {
            throw new Exception (e.getMessage());   // failure message   
        }
    }
    
    /**
     * Updates a home in the inventory by its id.
     * 
     * @param id          the ID of the home to update
     * @param updatedHome the updated home data
     * @throws Exception if the home with the specified ID is not found or an error occurs
     */
    public void updateHomeById(Integer id, Home updatedHome) throws Exception {
        try {
            for (int i = 0; i < homes.size(); i++) {
                if (homes.get(i).getId() == id) {
                    homes.set(i, updatedHome);
                    System.out.println("The home was updated successfully!");  // success message
                    return;  // exit the method after updating
                }
            }
            throw new Exception("The home with the provided id was not found!");
        } catch (Exception e) {
            throw new Exception(e.getMessage());   // failure message    
        }
    }
    
    /**
     * Updates a home in the inventory by its address.
     * 
     * @param address     the address of the home to update
     * @param updatedHome the updated home data
     * @throws Exception if the home with the specified address is not found or an error occurs
     */
    public void updateHomeByAddress(String address, Home updatedHome) throws Exception {
        try {
            for (int i = 0; i < homes.size(); i++) {
                if (homes.get(i).getAddress().equals(address)) {
                    homes.set(i, updatedHome);
                    System.out.println("The home was updated successfully!");  // success message
                    return;  // exit the method after updating
                }
            }
            throw new Exception("The home with the provided address was not found!");
        } catch (Exception e) {
            throw new Exception(e.getMessage());   // failure message   
        }
    }
    
    /*---------------------------------------------
    |     Methods for Saving and Loading Data     |
    -----------------------------------------------*/
    
    /**
     * Saves the homes data to the file.
     * 
     * @throws Exception if an error occurs while saving the homes data
     */
    public void saveHomes() throws IOException {
        BufferedWriter writer = null;
        try {
            writer = new BufferedWriter(new FileWriter(filePath));
            for (Home home : homes) {
                writer.write(home.getId() + "," + home.getSquareFeet() + "," + home.getAddress() + "," + home.getCity() + "," +
                        home.getState() + "," + home.getZipCode() + "," + home.getModelName() + "," +
                        home.getSaleStatus() + "\n");
            }
            System.out.println("The home inventory was saved successfully!");  // success message
        } catch (IOException e) {
            throw new IOException("Error saving homes: " + e.getMessage());   // failure message   
        } finally {
            try {
                if (writer != null) {
                    writer.close();
                }
            } catch (IOException e) {
                throw new IOException("An error occurred while closing the writer: " + e.getMessage());   // failure message   
            }
        }
    }

    /**
     * Loads the homes data from the file into the homes list.
     * 
     * @throws IOException if an error occurs while loading the homes data
     */
    private void loadHomes() throws IOException {
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(filePath));
            String line;
            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                try {
                    Home home = new Home(
                            Integer.parseInt(parts[0]),
                            Integer.parseInt(parts[1]),
                            parts[2],
                            parts[3],
                            parts[4],
                            Integer.parseInt(parts[5]),
                            parts[6],
                            parts[7]
                    );
                    homes.add(home);
                    System.out.println("The Home with the id: " + home.getId() + " was loaded into the buffered reader.");  // success message
                } catch (Exception e) {
                    System.out.println("The Home with the address " + parts[4] + " could not be loaded into the buffered reader.");  // Failure message 
                }         
            }
        } catch (IOException e) {
            throw new IOException("Error loading homes: " + e.getMessage());
        } finally {
            try {
                if (reader != null) {
                    reader.close();
                }
            } catch (IOException e) {
                throw new IOException("An error occurred while closing the reader: " + e.getMessage());
            }
        }
    }   
}


