 -----------------------------------------------------------------------------------------------------------------------------
# Portfolio Project 
Program Name: Home Inventory Manager  

Grade: 350/350 A 

-----------------------------------------------------------------------------------------------------------------------------

CSC320 – Programming-1 Java Course  
Professor: Herbert Pensado  
Spring B Semester (24SB) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 06/09/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-21  

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  
Portfolio Project – Home Inventory Manager Option2  
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
o	Then, call the method to list the values. Loop through the array and print to the screen    
3.	Call the remove home method to clear the variables:  
o	Print the return value.  
4.	Add a new home.  
o	Print the return value.  
o	Call the list method and print the new home information to the screen.  
5.	Update the home (change the sale status).  
o	Print the return value.  
o	Call the listing method and print the information to the screen.  
6.	Display a message asking if the user wants to print the information to a file (Y or N).  
o	Use a scanner to capture the response. If "Y", print the file to a predefined location (e.g., C:\Temp\Home.txt). Note: you may want to create a method to print the information in the main class.  
o	If "N", indicate that a file will not be printed.  

Your final program submission materials must include your source code and screenshots of the application executing the application and the results.  
Compile your Module 1-6 programs with corrections, lessons learned reflection, and final program course code and application screenshots.  

⚠️ My notes:  
-	I got permission from Professor Pensado for the program to manipulate a file.  
-	The program utilizes BufferedReader and BufferedWriter classes to read and write a file, the program also uses the ArrayList class the access and modify the homes’ data.  
-	In the HomeInventory class the functionalities of methods getHomeByAddress, removeHomeByAddress, and updateHomeByAddress are not implemented in version 1 of the program. However, they are available for future versions of the program.  
-	The program handles exceptions by passing them from the Home class to the HomeInventory class, and then to the Main class, where the exceptions and errors are displayed to the user.  
-	For the source code please see Main.java, InputValidation. Java, Home.java, and HomeInventory.java files.  

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  
The program manages a home inventory.  
It provides functionality for adding, removing, updating, and displaying home data.  
The program interacts with the user through a menu-driven interface and stores the home data in a file.   
    
-----------------------------------------------------------------------------------------------------------------------------

#### Project Map 
-  Program Corrections Folder: All my Critical Thinking assignments from Modules 1-6  
- Programming I Lessons Learned and Reflection Lessons Learned and Reflection.doc  
- Project Report.pdf  
	- Project Description 
	- Class pseudocode  
- README.md – Markdown file, program information 
- Main.java – Main program (Main class)
- Home.java – Home class
- HomeInventory.java – Home Inventory Class  
- The InputValidation.java - The InputValidation Class

-----------------------------------------------------------------------------------------------------------------------------

My Links:

<a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" align="left" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></a>
<a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" align="left" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></a>

[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)

<a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></a>
<a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></a>

Related links:  
[CSU Global](https://csuglobal.edu/) 

