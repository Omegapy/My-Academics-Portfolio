# -------------------------------------------------------------------------
# Program Name: ITS320_PFA_Option2
# Author: [Alejandro (Alex) Ricciardi
# Date: 04/07/2024
# Program Objective: To manage a home inventory system with functionality to add, update, remove, and display homes data.
# -------------------------------------------------------------------------
# Pseudocode:
# 1. Import necessary modules (os) to manipulate file
# 2. Create banner
# 3. Define the HomeInventory
#   - Define a dictionary to store the home data
#     The dictionary needs to be private to meet the attributes private requirements of the assignment
#   - Constructor (init): Initialize the HomeInventory object with the provided filename
#   - Destructor (del): Perform cleanup when the HomeInventory object is destroyed
#   - Getters: Methods to retrieve home data attributes
#   - Setters: Methods to add, remove, and update homes in the inventory
#   - Class Information Methods: Implement str and repr for string representation of the class
# 4. Define display functions
#   - display_home_data_using_home_id: Display the home data for a specific home using its ID
#   - display_homes: Display a range of homes from the inventory file
# 5. Define menu functions
#   - get_valid_input: Prompt the user for input and validate it based on data type
#   - menus: Display the menus to handle user input and to manipulate the home data
# 6. Define the main function
#   - Create a HomeInventory object
#   - Display class HomeInventory information
#   - Start the user interface menu
#-------------------------------------------------------------------------------------------
# Program Inputs:
#     - User input for adding, updating, and removing homes
#     - User input for displaying home information
#     - User input for navigating the menu options
# -------------------------------------------------------------------------
# Program Inputs: User input for home details, menu choices, and file name.
# Program Outputs: Display of home inventory, updated inventory file, and user prompts.
# -------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------
#          Modules
# ---------------------------
import os

# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------
#     Global Variables
# ---------------------------
# --- string literal
banner = '''
        **********************************
        *     Home Inventory Manager     *
        **********************************
'''

#----------------------------------------------------------------------------------------------------------------------
#---------------------------
#         Classes
#---------------------------
#----------------------------------------------------------------------------------------------------------------------
class HomeInventory:
    """
        The HomeInventory class provides methods for adding, removing, updating, and retrieving
        home data from an inventory file. It keeps track of the number of homes created and
        assigns a unique ID to each home.

        Attributes:
            Static attibute:
                _home_num (int): keeps track of the number of homes created.
            Private attributes:
                __inventory_filename (str): Name of the file to store the home inventory data.
                __home (dict): Dictionary to store the current home data.
                    home_id (int)
                    squarefeet (int)
                    address (str)
                    city (str)
                    state (str)
                    zipcode (int)
                    modelname (str)
                    salestatus (str)
        Methods:
            #--- Constructor
            __init__(inventory_filename: str) -> None:
                Initializes the HomeInventory object with the provided filename.

            #--- Deconstruct
            __del__(self) -> None:
                Destructor method for the HomeInventory class.
                Performs any necessary cleanup.

            #--- Getters
            get_filename(self) -> str:
                Retrieves the inventory filename.

            _get_number_of_homes(cls) -> int:
                Returns the number of homes

            get_home() -> dict:
                Retrieves the current home data stores in the home dictionary.

            get_home_data_by_id(home_id: int) -> bool:
                Retrieves the home data based on the provided home ID.

            get_home_data_by_address(address: str) -> bool:
                Retrieves the home data based on the provided address.

            get_home() -> dict:
                Retrieves the current home data.

            get_squarefeet(home_id: int) -> int:
                Retrieves the square feet of the home with the provided ID.

            get_address(home_id: int) -> str:
                Retrieves the address of the home with the provided ID.

            get_city(home_id: int) -> str:
                Retrieves the city of the home with the provided ID.

            get_state(home_id: int) -> str:
                Retrieves the state of the home with the provided ID.

            get_zipcode(home_id: int) -> int:
                Retrieves the zipcode of the home with the provided ID.

            get_modelname(home_id: int) -> str:
                Retrieves the model name of the home with the provided ID.

            get_salestatus(home_id: int) -> str:
                Retrieves the sale status of the home with the provided ID.

            get_home_id(address: str) -> int:
                Retrieves the ID of the home with the provided address.

            #--- Setters
            add_home(inputted_home: dict) -> bool:
                Adds a home to the inventory file.

            remove_home(home_id: int) -> bool:
                Removes a home from the inventory file based on the given home_id.

            update_home(updated_home: dict) -> bool:
                Updates an existing home's data in the inventory file based on the given home_id.

            #--- Class Information Methods
            __str__() -> str:
             Returns a string representation of the HomeInventory class.

            __repr__(self):
               Returns a string representation of the HomeInventory object initialization.
               This representation can be used to recreate the object.
    """
    # --------------------------------------------------------------------------------------------------
    # -------------------- Class variable --------------------
    # --------------------------------------------------------------------------------------------------
    _home_num = 0  # static variable keeps track of the number of home object created
    # --------------------------------------------------------------------------------------------------
    # -------------------- Constructor --------------------
    # --------------------------------------------------------------------------------------------------
    def __init__(self, inventory_filename: str) -> None:
        """ Initializes the HomeInventory object with the provided filename
                Checks if the file exists and if not it creates it

            :param filename: Name of the file to store the home inventory (str)
            :return: None
        """
        # Name of the home inventory file
        self.__inventory_filename = inventory_filename
        try:
            # Open file in append mode, if the file does not exist it creates a new file
            with open(self.__inventory_filename, 'a'):
                pass
        except Exception as e:
            print(f"\n--- An exception occurred with {self.__inventory_filename}: {str(e)} ---\n")
        # Dictionary to store the current home data
        self.__home = {
                            "home_id": int,
                            "squarefeet": int,
                            "address": str,
                            "city": str,
                            "state": str,
                            "zipcode": int,
                            "modelname": str,
                            "salestatus": str
                        }
        # --------------------------------------------------------------------------------------------------
        # --------------------- Deconstruct --------------------
        # --------------------------------------------------------------------------------------------------
    def __del__(self) -> None:
        """ Destructor method for the HomeInventory class.
            Performs any necessary cleanup.
            Prompts the user the delete or not the inventory file
        """
        while True: # Prompts the user to enter y or n to delete or not the inventory file
            del_file_choice = input(f"\nWould you like to delete the {self.__inventory_filename} file [Y/N]: ")
            if del_file_choice.lower() == 'y':
                while True:  # Prompts the user to enter y or n to confirm  the deletiom of the inventory file
                    del_file_choice = input(f"\nAre you sure you want to delete the file [Y/N]: ")
                    if del_file_choice.lower() == 'y':
                        os.remove(self.__inventory_filename)
                        print(f"HomeInventory object has been destroyed and the {self.__inventory_filename} file has been deleted.")
                        return None
                    elif del_file_choice.lower() == 'n':  # deletion not confirm
                        break # exists the second while loop
            elif del_file_choice.lower() == 'n': 
                print(f"HomeInventory object has been destroyed but the {self.__inventory_filename} file was not deleted.")
                return None

    # --------------------------------------------------------------------------------------------------
    # --------------------- Getters --------------------
    # --------------------------------------------------------------------------------------------------
    def get_filename(self) -> str:
        """ Retrieves the inventory filename. """
        return self.__inventory_filename
    # --------------------------------------------------------------------------------------------------
    def _get_number_of_homes(cls) -> int:
        """ Retrieves the total number of homes created. """
        return HomeInventory._home_num
    # --------------------------------------------------------------------------------------------------
    def get_home(self) -> dict:
        """ Retrieves the current home data stores in the home dictionary. """
        return self.__home
    # --------------------------------------------------------------------------------------------------
    def get_home_data_by_id(self, home_id: int) -> bool:
        """ Retrieves the home data based on the provided home ID.

                This method is utilised by the following class methods:
                    get_squarefeet()
                    get_address()
                    get_city()
                    get_state()
                    get_zipcode()
                    get_modelname()
                    get_salestatus()

            :param home_id: The ID of the home to retrieve (int)
            :return: True if the home is found, False otherwise (bool)
        """
        try:
            with open(self.__inventory_filename, "r") as file:  # Opens file in reading mode
                home_is_found = False
                for line in file:  # Reads file line by line
                    # Checks file's line to find if provided home_id match a home_id in the file
                    if line.startswith(str(home_id) + ","):
                        data = line.strip().split(",")
                        self.__home["home_id"] = int(data[0])
                        self.__home["squarefeet"] = int(data[1])
                        self.__home["address"] = data[2]
                        self.__home["city"] = data[3]
                        self.__home["state"] = data[4]
                        self.__home["zipcode"] = int(data[5])
                        self.__home["modelname"] = data[6]
                        self.__home["salestatus"] = data[7]
                        home_is_found = True
        except Exception as e:
            print(f"\n--- An exception occurred with {self.__inventory_filename}: {str(e)} ---\n")
            return False
        if not home_is_found:
            print(f"\n--- The home id {home_id} does not exist ---\n")
            return False
        else:
            return True
    # --------------------------------------------------------------------------------------------------
    def get_home_data_by_address(self, address: str) -> bool:
        """ Retrieves the home data based on the provided address.
                This method is utilised by the following class methods:
                    getHome_id()

            :param address: The address of the home to retrieve (str)
            :return: True if the home is found, False otherwise (bool)
        """
        try:
            with open(self.__inventory_filename, "r") as file:  # Open file in reading mode
                home_is_found = False  # Keeps track if the house is found in file
                for line in file:
                    data = line.strip().split(",")
                    if data[2] == address:  # Checks line to find if provided address match an address in the file
                        self.__home["home_id"] = int(data[0])
                        self.__home["squarefeet"] = int(data[1])
                        self.__home["address"] = data[2]
                        self.__home["city"] = data[3]
                        self.__home["state"] = data[4]
                        self.__home["zipcode"] = int(data[5])
                        self.__home["modelname"] = data[6]
                        self.__home["salestatus"] = data[7]
                        home_is_found = True
        except Exception as e:
            print(f"\n--- An exception occurred with {self.__inventory_filename}: {str(e)} ---\n")
            return False
        if not home_is_found:
            print("\n--- The the provided address does not exist ---\n")
            return False
        else:
            return True  # house was found
    # --------------------------------------------------------------------------------------------------
    def get_home(self) -> dict:
        """ Retrieves the current home data stores in the home dictionary. """
        return self.__home

    def get_squarefeet(self, home_id: int) -> int:
        """ Retrieves the square feet of the home with the provided ID. """
        # Checks if the provided house id does not matche the data stores in instance distionary
        if home_id != self.__home["home_id"]:
            # Checks if provided home id exists and store home data in __home dictionary
            if self.get_home_data_by_id(self, home_id):
                return int(self.__home["squarefeet"])
            else:
                return -1
        return int(self.__home["squarefeet"])
    # --------------------------------------------------------------------------------------------------
    def get_address(self, home_id: int) -> str:
        """ Retrieves the address of the home with the provided ID. """
        # Checks if the provided house id does not matche the data stores in instance distionary
        if home_id != int(self.__home["home_id"]):
            # Checks if provided home id exists and store home data in __home dictionary
            if self.get_home_data_by_id(self, home_id):
                return self.__home["address"]
            else:
                return "\n--- No address was found ---\n"
        return self.__home["address"]
    # --------------------------------------------------------------------------------------------------
    def get_city(self, home_id: int) -> str:
        """ Retrieves the city of the home with the provided ID. """
        # Checks if the provided house id does not matche the data stores in instance distionary
        if home_id != self.__home["home_id"]:
            # Checks if provided home id exists and store home data in __home dictionary
            if self.get_home_data_by_id(self, home_id):
                return self.__home["city"]
            else:
                return "\n--- No city was found ---\n"
        return self.__home["city"]
    # --------------------------------------------------------------------------------------------------
    def get_state(self, home_id: int) -> str:
        """ Retrieves the state of the home with the provided ID. """
        # Checks if the provided house id does not matche the data stores in instance distionary
        if home_id != self.__home["home_id"]:
            # Checks if provided home id exists and store home data in __home dictionary
            if self.get_home_data_by_id(self, home_id):
                return self.__home["state"]
            else:
                return "\n--- No city was found ---\n"
        return self.__home["state"]
    # --------------------------------------------------------------------------------------------------
    def get_zipcode(self, home_id: int) -> int:
        """ Retrieves the zipcode of the home with the provided ID. """
        # Checks if the provided house id does not matche the data stores in instance distionary
        if home_id != self.__home["home_id"]:
            # Checks if provided home id exists and store home data in __home dictionary
            if self.get_home_data_by_id(self, home_id):
                return self.__home["zipcode"]
            else:
                return -1  # If the zipcodewas not found
        return self.__home["zipcode"]
    # --------------------------------------------------------------------------------------------------
    def get_modelname(self, home_id: int) -> str:
        """ Retrieves the model name of the home with the provided ID. """
        # Checks if the provided house id does not matche the data stores in instance distionary
        if home_id != self.__home["home_id"]:
            # Checks if provided home id exists and store home data in __home dictionary
            if self.get_home_data_by_id(self, home_id):
                return self.__home["modelname"]
            else:
                return "\n--- No model name was found ---\n"
        return self.__home["modelname"]
    # --------------------------------------------------------------------------------------------------
    def get_salestatus(self, home_id: int) -> str:
        """ Retrieves the sale status of the home with the provided ID. """
        # Checks if the provided house id does not matche the data stores in instance distionary
        if home_id != self.__home["home_id"]:
            # Checks if provided home id exists and store home data in __home dictionary
            if self.get_home_data_by_id(self, home_id):
                return self.__home["salestatus"]
            else:
                return "\n--- No sale status was found ---\n"
        return self.__home["salestatus"]
    # --------------------------------------------------------------------------------------------------
    def get_home_id(self, address: str) -> int:
        """ Retrieves the ID of the home with the provided address. """
        # Checks if provided home id exists and store home data in __home dictionary
        if self.get_home_data_by_address(self, address):
            return int(self.__home["home_id"])
        else:
            return -1  # If the ID was not found
    # --------------------------------------------------------------------------------------------------
    # --------------------- Setters --------------------
    # --------------------------------------------------------------------------------------------------
    def add_home(self, inputted_home: dict) -> bool:
        """ Adds a home to the inventory file.

            :param inputted_home: Dictionary of the home information with no home_id (dict)
            :return: True if the home is added successfully, False otherwise (bool)
        """
        HomeInventory._home_num += 1  # Counts how many home were created
        home_id = HomeInventory._home_num  # Assigns the home id to the created home object
        try:
            with open(self.__inventory_filename, "a") as file:  # Open file in appending mode
                # Creates (line) string to be added to the file
                line = f"{home_id},{inputted_home["squarefeet"]},{inputted_home["address"]}," + \
                    f"{inputted_home["city"]},{inputted_home["state"]},{inputted_home["zipcode"]}," + \
                    f"{inputted_home["modelname"]},{inputted_home["salestatus"]}\n"
                file.write(line)  # writes the new home data at the end of the file
        except Exception as e:
            print(f"\n--- An exception occurred with {self.__inventory_filename}: {str(e)} ---\n")
            return False
        return True
    # --------------------------------------------------------------------------------------------------
    def remove_home(self, home_id: int) -> bool:
        """ Removes a home from the inventory file based on the given home_id.

            :param home_id: The ID of the home to remove (int)
            :return: True if the home is removed successfully, False otherwise (bool)
        """
        if self.get_home_data_by_id(home_id):
            try:
                temp_file = "temp.txt"  # Creates a temporary to store file data with removed home data
                # Opens existing file in reading mode and temp file writing mode
                with open(self.__inventory_filename, "r") as file, open(temp_file, "w") as temp:
                    for line in file:  # Reads file line by line
                        # Checks the provided home_id does not match a home_id in the existing file
                        if not line.startswith(str(home_id) + ","):
                            # writs the line in the temp file,
                            # if the provided home_id does not match the home_id in the existing file
                            temp.write(line)
                # Replaces the existing file data with the temp file data, removes the temp file
                os.replace(temp_file, self.__inventory_filename)
            except Exception as e:
                print(f"\n--- An exception occurred with {self.__inventory_filename}: {str(e)} ---\n")
                return False
            return True
        else:
            return False
    # --------------------------------------------------------------------------------------------------
    def update_home(self, updated_home: dict) -> bool:
        """ Updates an existing home's data in the inventory file based on the given home_id.

            :param updated_home: Dictionary of the updated home information (dict)
            :return: True if the home is updated successfully, False otherwise (bool)
        """
        # This line is the home data updated to be added to file
        updated_line = f"{updated_home["home_id"]},{updated_home["squarefeet"]},{updated_home["address"]}," + \
                       f"{updated_home["city"]},{updated_home["state"]},{updated_home["zipcode"]}," + \
                       f"{updated_home["modelname"]},{updated_home["salestatus"]}\n"
        home_id = updated_home["home_id"]
        # Checks if provided home id exists and store home data in __home dictionary
        if self.get_home_data_by_id(home_id):
            try:
                temp_file = "temp.txt"  # Creates a temporary to store file data with updated home data
                # Opens existing file in reading mode and temp file writing mode
                with open(self.__inventory_filename, "r") as file, open(temp_file, "w") as temp:
                    lines = file.readlines()
                    for line in lines:  # Reads file line by line
                        # Checks the provided home_id matches a home_id in the existing file
                        if line.startswith(str(updated_home["home_id"]) + ","):
                            # updated line string with updated home data to be added to the file
                            temp.write(updated_line)  # writes the home data at the end of the temp file
                        else:
                            temp.write(line)  # writes the home data at the end of the temp file
                # Replaces the existing file data with the temp file data, removes the temp file
                os.replace(temp_file, self.__inventory_filename)
            except Exception as e:
                print(f"\n--- An exception occurred with {self.__inventory_filename}: {str(e)} ---\n")
                return False
            return True
        else:
            return False
    # --------------------------------------------------------------------------------------------------
    # --------------------- Class Information Methods  --------------------
    # --------------------------------------------------------------------------------------------------
    def __str__(self) -> str:
        """ Returns a string representation of the HomeInventory class. """
        return """
The HomeInventory class provides methods for adding, removing, updating, and retrieving
home data from an inventory file. It keeps track of the number of homes created and
assigns a unique ID to each home.""" + \
            f"\n-- Number of homes created is {self._get_number_of_homes()}\n\n" + \
            "Example of home data:\n" + \
            "    Home ID: 123\n" + \
            "    Square Feet: 300\n" + \
            "    Address: 123 Loveland\n" + \
            "    City: Cheyenne\n" + \
            "    State: Wyoming\n" + \
            "    Zipcode: 82001\n" + \
            "    Model Name: Model C\n" + \
            "    Sale Status: Sold"
    # --------------------------------------------------------------------------------------------------
    def __repr__(self):
        """ Returns a string representation of the HomeInventory object initialization.
            This representation can be used to recreate the object. """
        return f"HomeInventory('{self.__inventory_filename}')"
# ---------------------------------------------------------------------------------------------------------------------
# ---------------------------
#        Functions
# ---------------------------
# ---------------------------------------------------------------------------------------------------------------------
# -------- Display Functions
# ----------------------------------------------------------------------------------------------------------------------
def display_home_data_using_home_id(inventory: HomeInventory, home_id: int) -> bool:
    '''
        Displays the home data for a specific home using its home ID.

        :param inventory: The HomeInventory object containing the home data (HomeInventory)
        :param home_id: The ID of the home to display (int)
        :return: True if the home was displayed successfully, False otherwise (bool)
    '''
    # Checks if provided home id exists and store home data in __home dictionary
    if inventory.get_home_data_by_id(home_id):
        home = inventory.get_home()  # Gets the home dictionary data from the inventory object
        print(f"\n--- Home data for house number ({home_id}) ---\n",
              f"Square Feet: {home["squarefeet"]}\n",
              f"Address: {home["address"]}\n",
              f"City: {home["city"]}\n",
              f"State: {home["state"]}\n",
              f"Zipcode: {home["zipcode"]}\n",
              f"Model: {home["modelname"]}\n",
              f"Sale Satus: {home["salestatus"]}\n"
              )
    else:
        print(f"\n--- No Home Data for home id ({home_id}) was found!\n")
        return False
    return True
# ---------------------------------------------------------------------------------------------------------------------
def display_homes(inventory: HomeInventory, start: int = 0, count: int = 3) -> bool:
    '''
        Displays a range of homes from the inventory file.

        :param inventory: The HomeInventory object containing the home data (HomeInventory)
        :param start: The starting index of the range (default: 0) (int)
        :param count: The number of homes to display (default: 3) (int)
        :return: True if the homes were displayed successfully, False otherwise (bool)
    '''
    print("\n------- Displaying Homes -------")
    try:
        with open(inventory.get_filename(), 'r') as file:  # Open the inventory file in reading mode
            lines = file.readlines()  # a list of the home data read from file
            end = min(start + count, len(lines))  # Calculate the end index of the file
            if start == 0:
                print("\n--- Begenning of the list")
            elif end == len(lines):
                print("\n --- End of the list")
            for line in lines[start:end]:  # Iterate over the inventory lines list from start value to the end value
                # Split the line by commas and strip whitespace smd '\n' from each item
                home_data = [item.strip() for item in line.split(',')]
                print(f"\n--- Home data for house number ({home_data[0]}) ---\n",
                      f"Square Feet: {home_data[1]}\n",
                      f"Address: {home_data[2]}\n",
                      f"City: {home_data[3]}\n",
                      f"State: {home_data[4]}\n",
                      f"Zipcode: {home_data[5]}\n",
                      f"Model {home_data[6]}\n",
                      f"Sale Status: {home_data[7]}"
                      )
    except Exception as e:
        print(f"\n--- An exception occurred with {inventory.get_filename()}: {str(e)} ---\n")
        return False
    return True
# ---------------------------------------------------------------------------------------------------------------------
# -------- Menu Functions
# ---------------------------------------------------------------------------------------------------------------------
def get_valid_input(prompt: str, data_type: type) -> any:
    '''
        Prompts the user for input and validates it based on the specified data type.

        :param prompt: Prompt message to display to the user (str)
        :param data_type: Expected data type of the input (type)
        :return: Validated user input (any)
    '''
    while True:
        try:
            value = data_type(input(prompt))
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {data_type.__name__}.")
# ---------------------------------------------------------------------------------------------------------------------
def update_menu(inventory: HomeInventory) -> bool:
    '''
        Displays the update menu, handles user input, and update a given home data

        :param inventory: HomeInventory object
        :return: True if the home was updated successfully, False otherwise (bool)
    '''
    is_modify = False # Keeps track if the user modify home data
    print("\n--- Update a Home ---")
    home_id = get_valid_input("Enter the home ID to update: ", int)
    while True:
        if display_home_data_using_home_id(inventory, home_id):
            home = inventory.get_home() # Gets the home dictionary data from the inventory object
            while True:
                print(f"--- Attribute to update for house id ({home_id})---\n",
                      "1. Square feet\n",
                      "2. Address\n",
                      "3. City\n",
                      "4. State\n",
                      "5. Zipcode\n",
                      "6. Model name\n",
                      "7. Sales satus\n",
                      "8. Quite"
                      )
                choice = input("Enter your choice (1-8): ")
                # User Choice
                if choice == "1":
                    home["squarefeet"] = get_valid_input("Enter the square feet: ", int)
                    is_modify = True
                elif choice == "2":
                    home["address"] = input("Enter the address: ")
                    is_modify = True
                elif choice == "3":
                    home["city"] = input("Enter the city: ")
                    is_modify = True
                elif choice == "4":
                    home["state"] = input("Enter the state: ")
                    is_modify = True
                elif choice == "5":
                    home["zipcode"] = get_valid_input("Enter the zipcode: ", int)
                    is_modify = True
                elif choice == "6":
                    home["modelname"] = input("Enter the model name: ")
                    is_modify = True
                elif choice == "7":
                    home["salestatus"] = menu_salestatus(inventory.get_salestatus(home_id))
                    is_modify = True
                elif choice == "8":
                    if is_modify:
                        inventory.update_home(home)
                        return True
                    else:
                        return False
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid choice. Please try again.")
            home_id = get_valid_input("Enter the home ID to update: ", int)
# ---------------------------------------------------------------------------------------------------------------------
def menu_salestatus(status: str) -> str:
    '''
        Displays the sale status menu and handles user input

        :param status: The status of the house that may need to be updated (str)
        :return: The updated status type (str)
    '''
    satus_type = "No status was assigned"
    while True:
        print("    a. Sold\n",
              "   b. Available\n",
              "   c. Under contract\n",
              "   q. Quite"
              )
        choice = input("Enter your choice (a-q): ")
        # User Choice
        if choice.lower() == "a":
            return "Sold"
        elif choice.lower() == "b":
            return "Available"
        elif choice.lower() == "c":
            return "Under Contract"
        elif choice.lower() == "q":
            print("The status was not updated")
            return status
        else:
            print("Invalid choice. Please try again.")
# ---------------------------------------------------------------------------------------------------------------------
def menu(inventory: HomeInventory) -> None:
    '''
        Displays the main menu and handles user input

        :param inventory: HomeInventory object
        :return: None
    '''
    while True:
        print("\n--- Home Inventory Menu ---\n",
              "1. Add a home\n",
              "2. Update a home\n",
              "3. Remove a home\n",
              "4. Display a home information\n",
              "5. Display several homes information\n",
              "6. Quit"
              )
        choice = input("Enter your choice (1-6): ")
        # Add Home
        if choice == "1":
            print("\n--- Add a Home ---")
            # Get home data from user input and stores in distionary
            home_data = {
                "squarefeet": get_valid_input("Enter the square feet: ", int),
                "address": input("Enter the address: "),
                "city": input("Enter the city: "),
                "state": input("Enter the state: "),
                "zipcode": get_valid_input("Enter the zipcode: ", int),
                "modelname": input("Enter the model name: "),
                "salestatus": menu_salestatus("Available")
            }
            # Add the home to the inventory
            if inventory.add_home(home_data):
                print("The home added successfully.")
            else:
                print("\n-- The home was not added.")
        # Update home data
        elif choice == "2":
            if update_menu(inventory):
                print("The home data was updated successfully.")
            else:
                print("\n-- The home data was not updated.")
        # Remove Home
        elif choice == "3":
            print("\n--- Remove a Home ---")
            home_id = get_valid_input("Enter the home ID to remove the home data: ", int)
            if inventory.remove_home(home_id):
                print("The home was removed successfully.")
            else:
                print("\n-- The home was not removed")
        # Display a Home data
        elif choice == "4":
            print("\n--- Home Information ---")
            home_id = get_valid_input("Enter the home ID to display the home data: ", int)
            if not display_home_data_using_home_id(inventory, home_id):
                print("\n-- Something went wrong. Please try again.")
        # Display the list of home data using a range of 3
        elif choice == "5":
            with open(inventory.get_filename(), "r") as file:
                lines_lenght = len(file.readlines())
            start_index = 0
            count = 3
            while True:
                if not display_homes(inventory, start_index, count):
                    print("\n-- Something went wrong. Please try again.")
                display_choice = input("\n--- Enter 'n' for next, 'p' for previous, or 'q' to quit: ")
                if display_choice == 'n':
                        if not (start_index + count >= lines_lenght):
                            start_index += count
                elif display_choice == 'p':
                    start_index = max(0, start_index - count)
                elif display_choice == 'q':
                    break
                else:
                    print("Invalid choice. Please try again.")
        elif choice == "6":
            return None
# ---------------------------------------------------------------------------------------------------------------------
# ---------- Main Function
# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:
    '''
        Creates a HomeInventory object and starts the main menu.

        :return: None
    '''
    print(banner)
    # --- Create a HomeInventory object and start the main menu
    inventory = HomeInventory("home_inventory.txt")
    # --- Class HomeInventory Information
    print("--- Class HomeInventory Information ---")
    print(str(inventory))
    # --- Add 5 home data entries
    home_data = [
        {"squarefeet": 1200, "address": "123 Main St", "city": "Anytown", "state": "CA", "zipcode": 12345,
         "modelname": "Model A", "salestatus": "Sold"},
        {"squarefeet": 1500, "address": "456 Oak Ave", "city": "Somecity", "state": "NY", "zipcode": 67890,
         "modelname": "Model B", "salestatus": "Available"},
        {"squarefeet": 1800, "address": "789 Elm Rd", "city": "Anothercity", "state": "TX", "zipcode": 54321,
         "modelname": "Model C", "salestatus": "Under Contract"},
        {"squarefeet": 2000, "address": "321 Maple Dr", "city": "Somewhere", "state": "FL", "zipcode": 98765,
         "modelname": "Model D", "salestatus": "Sold"},
        {"squarefeet": 1400, "address": "654 Pine Ln", "city": "Nowhere", "state": "WA", "zipcode": 24680,
         "modelname": "Model E", "salestatus": "Available"}
    ]
    for home in home_data:
        inventory.add_home(home)
    print(f"\nThe total number of home created is: {inventory._get_number_of_homes()}")
    # --- User interface menu
    menu(inventory)
    # Destroys the inventory object and prompts the user about deleting or not the inventory file
    del inventory

# Execute the program
if __name__ == '__main__': main()
