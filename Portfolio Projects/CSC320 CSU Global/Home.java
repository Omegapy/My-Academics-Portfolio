/*
    Program Name: Home Inventory Manager
    Home class
    
    Program Description: 
    The program manages a home inventory.
    It provides functionality for adding, removing, updating, and displaying home data. 
    The program interacts with the user through a menu-driven interface 
    and stores the home data in a file.  
    
    Utilized by: HomeInventory
*/

/**
 * Creates a Home object with various attributes such as id, square feet, address,
 * city, state, zip code, model name, and sale status.
 * The class has getters and setters' methods to access and manipulate the Home objects' data
 * 
 * It is utilized by the HomeInventory class
 * 
 * @author Alejandro Ricciardi
 * @version 1
 * @date 05/26/2024
 */
public class Home {
    private Integer id, // Declare and initialize the Integer object to null 
                    squareFeet,
                    zipCode;
    private String address,
                   city,
                   state,
                   modelName,
                   saleStatus;

    /*---------------------
    |     Constructors    |
    ----------------------*/
    
    /**
     * Default construct
     * constructs a Home object with null attributes values
     */
    public Home() {
    	this.id = null;  
        this.squareFeet = -1;
        this.zipCode = -1;
        this.address = "Unknown";
        this.city = "Unknown";
        this.state = "Unknown";
        this.modelName = "Unknown";
        this.saleStatus ="Unknown";
        System.out.println("A Home object with null attributes values was created successfully!");  // success message
    };

    /**
     * Parameterized constructor
     * constructs a Home object with the specified attributes.
     *
     * @param id         the unique identifier of the home
     * @param squareFeet the square feet of the home
     * @param address    the address of the home
     * @param city       the city where the home is located
     * @param state      the state where the home is located
     * @param zipCode    the zipcode of the home
     * @param modelName  the model name of the home
     * @param saleStatus the sale status of the home
     * @throws Exception if any of the parameters are null
     */
    public Home(Integer id, Integer squareFeet, String address, String city, String state, Integer zipCode, String modelName, String saleStatus) throws Exception {
        try {
            if (id == null) {
                throw new Exception("The value of the id is null");
            } else if (squareFeet == null) {
                throw new Exception("The value of the square feet is null");
            } else if (address == null) {
                throw new Exception("The value of the address is null");
            } else if (city == null) {
                throw new Exception("The value of the city is null");
            } else if (state == null) {
                throw new Exception("The value of the state is null");
            } else if (zipCode == null) {
                throw new Exception("The value of the zip code is null");
            } else if (modelName == null) {
                throw new Exception("The value of the model name is null");
            } else if (saleStatus == null) {
                throw new Exception("The value of the sale status is null");
            } else {
                this.id = id;
                this.squareFeet = squareFeet;
                this.address = address;
                this.city = city;
                this.state = state;
                this.zipCode = zipCode;
                this.modelName = modelName;
                this.saleStatus = saleStatus;
                System.out.println("The Home object was created successfully!");  // success message
            }
        } catch (Exception e) {
            throw new Exception(e.getMessage());  // failure message
        }
    }

    // ============================================================================================== 
    /*-----------------
     |     Getters    |
     -----------------*/

    /**
     * Returns the unique identifier of the home.
     *
     * @return the unique identifier of the home
     * @throws NullPointerException if the id is null
     */
    public Integer getId() throws NullPointerException {
        try {
            if (id == null) {
                throw new Exception("The value of the id is null!");
            }
            System.out.println("The Home id: " + id + " was found!");  // success message
            return id;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the square feet of the home.
     *
     * @return the square feet of the home
     * @throws NullPointerException if the square feet value is null
     */
    public Integer getSquareFeet() throws NullPointerException {
        try {
            if (squareFeet == null) {
                throw new Exception("The value of the square feet is null!");
            }
            System.out.println("The square feet were found!");  // success message
            return squareFeet;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the address of the home.
     *
     * @return the address of the home
     * @throws NullPointerException if the address is null
     */
    public String getAddress() throws NullPointerException {
        try {
            if (address == null) {
                throw new Exception("The value of the address is null!");
            }
            System.out.println("The address was found!");  // success message
            return address;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the city where the home is located.
     *
     * @return the city where the home is located
     * @throws NullPointerException if the city is null
     */
    public String getCity() throws NullPointerException {
        try {
            if (city == null) {
                throw new Exception("The value of the city is null!");
            }
            System.out.println("The city was found!");  // success message
            return city;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the state where the home is located.
     *
     * @return the state where the home is located
     * @throws NullPointerException if the state is null
     */
    public String getState() throws NullPointerException {
        try {
            if (state == null) {
                throw new Exception("The value of the state is null!");
            }
            System.out.println("The state was found!");  // success message
            return state;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the zipcode of the home.
     *
     * @return the zipcode of the home
     * @throws NullPointerException if the zip code is null
     */
    public Integer getZipCode() throws NullPointerException {
        try {
            if (zipCode == null) {
                throw new Exception("The value of the zip code is null");
            }
            System.out.println("The zip code was found!");  // success message
            return zipCode;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the model name of the home.
     *
     * @return the model name of the home
     * @throws NullPointerException if the model name is null
     */
    public String getModelName() throws NullPointerException {
        try {
            if (modelName == null) {
                throw new Exception("The value of the model name is null");
            }
            System.out.println("The model name was found!");  // success message
            return modelName;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Returns the sale status of the home.
     *
     * @return the sale status of the home
     * @throws NullPointerException if the sale status is null
     */
    public String getSaleStatus() throws NullPointerException {
        try {
            if (saleStatus == null) {
                throw new Exception("The value of the sale status is null");
            }
            System.out.println("The sale status was found!");  // success message
            return saleStatus;
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }

    // ============================================================================================== 
    /*-----------------
     |     Setters    |
     -----------------*/

    /**
     * Sets the square feet of the home.
     *
     * @param squareFeet the square feet to set
     * @throws NullPointerException if the square feet value is null
     */
    public void setSquareFeet(Integer squareFeet) throws NullPointerException {
        try {
            if (squareFeet == null) {
                throw new Exception("The square feet value is null!");
            }
            this.squareFeet = squareFeet;
            System.out.println("The home's square feet were set successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the address of the home.
     *
     * @param address the address to set
     * @throws NullPointerException if the address value is null
     */
    public void setAddress(String address) throws NullPointerException {
        try {
            if (address == null) {
                throw new Exception("The address value is null!");
            }
            this.address = address;
            System.out.println("The home's address was set successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the city where the home is located.
     *
     * @param city the city to set
     * @throws NullPointerException if the city value is null
     */
    public void setCity(String city) throws NullPointerException {
        try {
            if (city == null) {
                throw new Exception("The city value is null!");
            }
            this.city = city;
            System.out.println("The home's city was set successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the state where the home is located.
     *
     * @param state the state to set
     * @throws NullPointerException if the state value is null
     */
    public void setState(String state) throws NullPointerException {
        try {
            if (state == null) {
                throw new Exception("The state value is null!");
            }
            this.state = state;
            System.out.println("The home's state was set successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the zip code of the home.
     *
     * @param zipCode the zip code to set
     * @throws NullPointerException if the zip code value is null
     */
    public void setZipCode(Integer zipCode) throws NullPointerException {
        try {
            if (zipCode == null) {
                throw new Exception("The zip code value is null!");
            }
            this.zipCode = zipCode;
            System.out.println("The home's zip code was set successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException(e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the model name of the home.
     *
     * @param modelName the model name to set
     * @throws NullPointerException if the model name value is null
     */
    public void setModelName(String modelName) throws NullPointerException {
        try {
            if (modelName == null) {
                throw new Exception("The model name value is null!");
            }
            this.modelName = modelName;
            System.out.println("The home's model name was set successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException("- Error: " + e.getMessage());   // failure message
        }
    }
    
    // ---------------------------------------------------------------------------------------------------------

    /**
     * Sets the sale status of the home.
     *
     * @param saleStatus the sale status to set
     * @throws NullPointerException if the sale status value is null
     */
    public void setSaleStatus(String saleStatus) throws NullPointerException {
        try {
            if (saleStatus == null) {
                throw new Exception("The sale status value is null!");
            }
            this.saleStatus = saleStatus;
            System.out.println("The home's sale status was set successfully!");  // success message
        } catch (Exception e) {
            throw new NullPointerException("- Error: " + e.getMessage());   // failure message
        }
    }

    // ==============================================================================================  
    
    /**
     * Returns a string representation of the home.
     * 
     * It provides a readable output the state of the Home object.
     * When you print a Home object the method is automatically called 
     * to get the string representation of the object. 
     * For example:
     * Home myHome = new Home(1, 1500, "123 Main St", "Anytown", 
     *                        "CA", 12345, "Model A", "Available");
     * System.out.println(myHome);
     * outputs:
     * ---- Home id: 1 ----
     * [ Square Feet: 1500, Address: 123 Main St, City: Anytown, State: CA, Zip Code: 12345, Model Name: Model A, Sale Status: Available ]
     *      
     * @return a string representation of the home
     */
    @Override
    public String toString() {
        return "\n---- Home id: " + id +" ----\n" +
                "[ square feet: " + squareFeet +
                ", Address: " + address +
                ", City: " + city +
                ", State: " + state +
                ", Zip Code: " + zipCode +
                ", Model Name: " + modelName +
                ", Sale Status: " + saleStatus + " ]";
    }
    
    // ---------------------------------------------------------------------------------------------------------
}

