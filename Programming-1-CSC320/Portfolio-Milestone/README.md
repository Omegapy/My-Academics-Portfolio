 -----------------------------------------------------------------------------------------------------------------------------
# Portfolio Milestone  
Program Name: Home Inventory Manager  

Grade:  

-----------------------------------------------------------------------------------------------------------------------------

CSC320 – Programming-1 Java Course  
Professor: Herbert Pensado  
Spring B Semester (24SB) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 05/26/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-21  

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  
Portfolio Milestone – Home Inventory:  
Submit a document with methods for your home class (Portfolio Project choice), and pseudo code indicating functionality of each method.  
Example:  
public String RemoveHome(String homeModel, String homeAddress, int homeZipCode)  
If  
              values entered match values stored in private variables  
              remove home information  
else  
               return message indicating mismatch    

Portfolio Project – Home Inventory Manager:  
Your Portfolio Project for CSC320 will consist of three components:  
•	Program corrections: Make the appropriate corrections to all the programming assignments submitted as Critical Thinking assignments from Modules 1-6. You will need to submit the programs along with the carefully outlined corrections needed in order for programs to run correctly.  
•	Lessons learned reflection: Create a 2-3-page summary that outlines the lessons learned in this Programming I course.
•	Final program: Create a final program that meets the requirements outlined below.   
Final Program Requirements    
Create a home inventory class that will be used by a national builder to maintain inventory of available houses in the country. The following attributes should be present in your home class:  
•	private int square_feet  
•	private string address  
•	private string city  
•	private string state  
•	private int zip_code  
•	private string Model_name  
•	private string sale_status (sold, available, or under contract)
Your program should have appropriate methods such as:  
•	constructor  
•	add a new home  
•	remove a home  
•	update home attributes   
All methods should include try..catch constructs. Except as noted, all methods should return a success or failure message (failure message defined in "catch").    
1.	Create an additional class to call your home class (e.g., Main or HomeInventory). Include a try..catch construct and print it to the console.  
2.	Call home class with parameterized constructor (e.g., "square_feet, address, city, state, zip_code, Model_name, sale_status").  
 	Then, call the method to list the values. Loop through the array and print to the screen.    
3.	Call the remove home method to clear the variables:  
 	Print the return value.  
4.	Add a new home.  
 	Print the return value.  
 	Call the list method and print the new home information to the screen.  
5.	Update the home (change the sale status).  
 	Print the return value.  
 	Call the listing method and print the information to the screen.
6.	Display a message asking if the user wants to print the information to a file (Y or N).  
 	Use a scanner to capture the response. If "Y", print the file to a predefined location (e.g., C:\Temp\Home.txt). Note: you may want to create a method to print the information in the main class.  
 	If "N", indicate that a file will not be printed.  
Your final program submission materials must include your source code and screenshots of the application executing the application and the results.  
Compile your Module 1-6 programs with corrections, lessons learned reflection, and final program course code and application screenshots.  

⚠️ My notes:    
-	This is an alpha version of the Portfolio Project   
-	I got permission from Professor Pensado for the program to manipulate a file  
-	For the source code please see Main.java, Home.java, and HomeInventory.java files.  

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  
This is an Alpha version of the Home Inventory Manager program.  
The program manages a home inventory.  
It provides functionality for adding, removing, updating, and displaying home data.    
The program interacts with the user through a menu-driven interface and stores the home data in a file.  
    
-----------------------------------------------------------------------------------------------------------------------------

#### Project Map  
- Project Report.pdf  
	- Project Description 
	- Class pseudocode  
- README.md – Markdown file, program information 
- Main.java – Main program (Main class)
- Home.java – Home class
- HomeInventory.java – Home Inventory Class

-----------------------------------------------------------------------------------------------------------------------------

My Links:   
[GitHub](https://github.com/Omegapy)  
[LinkedIn](https://www.linkedin.com/in/alex-ricciardi/)   
[YouTube](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)

Related links:  
[CSU Global](https://csuglobal.edu/) 

