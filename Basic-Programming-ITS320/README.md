-----------------------------------------------------------------------------------------------------------------------------
# Basic Programming Python – IT320
-----------------------------------------------------------------------------------------------------------------------------

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/f8f3f73f-c5e7-40cd-a9d1-f60aa32ca4a7"> Alejandro (Alex) Ricciardi (Omegapy)   
  
 created date: 04/04/2024  

-----------------------------------------------------------------------------------------------------------------------------

Projects Description: 
This repository is a collection of Python scripts from IT320 - Basic Programming Python Course  
at Colorado State University Global- CSU Global.  
 

-----------------------------------------------------------------------------------------------------------------------------

IT320 - Basic Programming Python Course  
Professor: Dr. Reinaldo Fernandez  
Winter Semester (24WD) – 2023  
Student: Alejandro (Alex) Ricciardi  

Final grade: A+ 100%

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- [Python](https://www.python.org/)

-----------------------------------------------------------------------------------------------------------------------------

My Links:   
[GitHub](https://github.com/Omegapy)   
[Code Chronicles](https://www.alexomegapy.com/)  
[LinkedIn](https://www.linkedin.com/in/alex-ricciardi/)    
[Medium](https://medium.com/@alex.omegapy)     
[YouTube](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)  

Related links:  
[CSU Global](https://csuglobal.edu/)   

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- [ITS320 PFA Option2](#its320-pfa-option2)  
- [ITS320 CTA6 Option2](#its320-cta6-option1)  
- [ITS320 CTA5 Option2](#its320-cta5-option2)  
- [ITS320 CTA4 Option2](#its320-cta4-option2)  
- [ITS320 CTA3 Option2](#its320-cta3-option2)  
- [ITS320 CTA2 Option2](#its320-cta2-option2)  
- [ITS320 CTA1 Option1](#its320-cta1-option1)  
- [Discussions](#discussions) 

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 PFA Option2
Portfolio Assignment Option 2
File: ITS320_PFA.Option2.py  
Date: 04/07/2024

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
To manage a home inventory system with functionality to add, update, remove, and display homes data.

-------------------------------------------------------------------------------------------

Assignment Directions:  
Option #2: Program Corrections, Lessons Learned, and Home Inventory Program  
Create a home inventory class that will be used by a National Builder to maintain an inventory of available houses in the country.    
The following attributes should be present in your home class:  

- private int squarefeet  
- private string address  
- private string city  
- private string state  
- private int zipcode  
- private string Modelname  
- private string salestatus (sold, available, under contract)  

Your program should have appropriate methods such as:

- Constructor   
- add a new home  
- remove a home
- update home attributes  
At the end of your program, be sure that it allows the user to output all home inventory to a text file.

-------------------------------------------------------------------------------------------

Pseudocode:
1. Import necessary modules (os) to manipulate file  
2. Create banner  
3. Define the HomeInventory
    - Define a dictionary to store the home data  
      The dictionary needs to be private to meet the attributes private requirements of the assignment  
    - Constructor (init): Initialize the HomeInventory object with the provided filename  
    - Destructor (del): Perform cleanup when the HomeInventory object is destroyed  
    - Getters: Methods to retrieve home data attributes  
    - Setters: Methods to add, remove, and update homes in the inventory  
    - Class Information Methods: Implement str and repr for string representation of the class  
4. Define display functions
    - display_home_data_using_home_id: Display the home data for a specific home using its ID  
    - display_homes: Display a range of homes from the inventory file  
5. Define menu functions   
    - get_valid_input: Prompt the user for input and validate it based on data type  
    - menus: Display the menus to handle user input and to manipulate the home data  
6. Define the main function  
    - Create a HomeInventory object  
    - Display class HomeInventory information  
    - Start the user interface menu  
-------------------------------------------------------------------------------------------

Program Inputs:
    - User input for adding, updating, and removing homes  
    - User input for displaying home information  
    - User input for navigating the menu options  
    
-------------------------------------------------------------------------------------------

Program Inputs: User input for home details, menu choices, and file name.  
Program Outputs: Display of home inventory, updated inventory file, and user prompts.  

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 CTA6 Option1  
Critical Thinking Assignment 6 Option 1  
File: ITS320_CTA6.Option1.py   
Date: 03/24/2024  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
To perform arithmetic operations (addition, subtraction, multiplication, division, and modulus)  
on complex numbers input by the user.

-------------------------------------------------------------------------------------------

Assignment Directions:  
Option #1: Working with Python Classes  
For this assignment, you are given two complex numbers.  
You will print the result of their addition, subtraction, multiplication, division, and modulus operations.  
The real and imaginary precision part should be correct up to two decimal places.

Input Format  
One line of input: The real and imaginary part of a number separated by a space.  

Output Format  
For two complex numbers and the output should be in the following sequence on separate lines:  
C + D  
C – D  
C * D  
C / D  
mod(C)  
mod(D) 
 
For complex numbers with non-zero real and complex part, the output should be in the following format:  
A + Bi  
Replace the plus symbol (+) with a minus symbol (-) when B 0.  

For complex numbers with a zero complex part, i.e. real numbers, the output should be:   
A + 0.00i  

For complex numbers where the real part is zero and the complex part is non-zero, the output should be:  
0.00 + Bi

Sample Input  
2 1  
5 6  
Sample Output  
7.00+7.00i  
-3.00-5.00i  
4.00+17.00i  
0.26-0.11i  
2.24+0.00i  
7.81+0.00i  

-------------------------------------------------------------------------------------------

Pseudocode:  
1. Display a banner for the program.  
2. Prompt the user to enter the real and imaginary parts of two complex numbers.  
   a. Check if the numbers are valid floats  
3. Create a complex number class  
   a. Create methods that perform arithmetic operations on complex number  
     - addition   
     - subtraction  
     - multiplication  
     - division  
     - modulus operations  
   b. create a method that the string representation of the complex number  
4. Display the results of these operations.

-------------------------------------------  

Program Inputs:  
- Two sets of real and imaginary parts of complex numbers entered by the user as a set of floats.
  
-------------------------------------------

Program Outputs:  
- The results of the operations on the input complex numbers:  
addition, subtraction, multiplication, division, and modulus operations.  

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 CTA5 Option2  
Critical Thinking Assignment 5 Option 2  
File: ITS320_CTA5.Option2.py   
Date: 03/17/2024

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
Concatenate the first two given strings and reverse order the third given string.  

-------------------------------------------------------------------------------------------

Assignment Directions:
Option #2: Third String in Reverse Order  
Write a Python function that will work on three strings. The function will return a concatenation of the first two strings  
and will print the third string in reverse order. The function is to be called from the main program.  
In the main program, prompt the user for the three strings and pass these values to the function.  

-------------------------------------------------------------------------------------------

Pseudocode:  
1. Display a banner.  
2. Prompt the user to enter three strings.  
  a. For each user input, check if a string was entered, if not prompts the user to reenter a string.  
  b. Store the three strings in a list  
3. Call the process_strings function  
     * NOTE: This function breaks the Golden Rule of Modularization, but it is compliant with the assignment instructions.  
       * Assignment Instructions:  
         Write a Python function that will work on three strings.  
         The function will return a concatenation of the first two strings  
         and will print the third string in reverse order. The function is to be called from the main program.   
         In the main program, prompt the user for the three strings and pass these values to the function.

    a. Call the concatenated_strings function  
      - Concatenate the first two strings.  
      - Return concatenated string
     b. Call the concatenated_strings function  
      - Reverse the third string.  
      - Return reversed string
         
    c. Print the concatenated string  
    d. Return concatenated string from the return concatenated_strings function
   
6. Print the reversed third string.  
7. Print the concatenated string.
   
-------------------------------------------

Program Inputs:  
- Three strings entered by the user.
  
-------------------------------------------

Program Outputs:  
- reversed_string, the reversed third string.  
- concatenated_str, the concatenated string of the first two strings.  

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 CTA4 Option2  
Critical Thinking Assignment 4 Option 2  
File: ITS320_CTA4.Option2.py   
Date: 03/10/2024

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
Calculate grade statistics (Average, Maximum, Minimum) form of a set of user-inputted grades  

-------------------------------------------------------------------------------------------

Assignment Directions:
Option #2: Repetition Control Structure - Grade Statistics  
Write a program that will provide important statistics for the grades in a class.   
- The program will utilize a loop to read five floating-point grades from user input.   
Ask the user to enter the values, then print the following data:  
- Average  
- Maximum  
- Minimum
  
-------------------------------------------------------------------------------------------

Pseudocode:  
1. Initialize program banner  
2. Create - initialize a global dictionary to store average, maximum, and minimum grades statistics.  
3. Define a function to check if a string can be converted to a float.  
4. Define a function to prompt the user to enter five valid grades.  
   a. validate each user inputted to ensure it is a float between 0 and 100 included  
   b. return a list of float grades  
5. Define a function to calculate and store the average, maximum, and minimum of the grades.  
6. Define a function to display the calculated grade statistics.  
7. In the main function, allow input grades, calculate and display statistics,  
   and then offer the user to exit the program or enter another set of grades.
   
-------------------------------------------  

Program Inputs:
Five grades inputted (str) by the user  

-------------------------------------------  

Program Outputs:  
- banner (str)  
- average (float)  
- maximum (float)  
- minimum  (float)  

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 CTA3 Option2  
Critical Thinking Assignment 3 Option 2  
File: ITS320_CTA3.Option2.py   
Date: 03/03/2024

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
Calculate the weekly average tax withholding for a customer.  
-------------------------------------------------------------------------------------------

Assignment Directions:  
Option #2: Creating a Program to Calculate Weekly Average Tax Withholding  
Create a program that will calculate the weekly average tax withholding for a customer, given the following weekly income guidelines:  
- Income less than $500: tax rate 10%  
- Incomes greater than/equal to $500 and less than $1500: tax rate 15%  
- Incomes greater than/equal to $1500 and less than $2500: tax rate 20%  
- Incomes greater than/equal to $2500: tax rate 30%  
- Store the income brackets and rates in a dictionary.  
- Write a statement that prompts the user for an income and then looks up the tax rate from the dictionary  
  and prints the income, tax rate, and tax.  
- Develop Python code that implements the program requirements.
   
-------------------------------------------------------------------------------------------

Pseudocode:  
1. Create a dictionary to store the  weekly income brackets (as keys) and related tax rates (as values).
2. Display program banner.
3. Prompt the user to enter weekly income.
 emsp a. Validate the input to ensure it is a positive whole number or a positive two decimal number (currency)
5. Calculate the tax based the brackets weekly income and related tax rates dictionary values.
      a. Handle errors.
7. Display the weekly income, tax rate, and the average tax withholding to the user.
   
-------------------------------------------

Program Inputs:
- weekly_income (str) entered by the user
  
-------------------------------------------

Program Outputs:
- banner (str)
- weekly_income (float)
- tax_rate (percentage as float)
- tax 'withholding amount' (float)

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 CTA2 Option2  
Critical Thinking Assignment 2 Option 2  
File: ITS320_CTA2.Option2.py   
Date: 02/25/2024

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
Store user-input data in a dictionary and print out the contents of the dictionary.  

-------------------------------------------------------------------------------------------

Assignment Directions:  
Option #2: Creating a Python Application  
Develop a Python application that incorporates using appropriate data types and provides program output in a logical manner.  
Your program should prompt a user to enter a car brand, model, year, starting odometer reading, an ending odometer reading,  
and the estimated miles per gallon consumed by the vehicle. Store your data in a dictionary  
and print out the contents of the dictionary.  

-------------------------------------------------------------------------------------------

Pseudocode:
1. Print the banner Car Brand
2. Prompt the user for car details:
   - brand
   - model
   - year
   - starting odometer
   - ending odometer
   - miles per gallon
3. Validate each input:
   - year must be an integer between 1886 and the current year. 1886 is when the first car was made.
   - starting odometer reading and miles per gallon must be a non-negative integer
   - ending odometer reading must be greater than or equal to the starting odometer reading
     (starting odometer reading must not be greater than or not equal to the ending odometer reading)
4. Store the validated inputs in a dictionary
5. Print the car details stored in the dictionary
   
-------------------------------------------

Program Inputs:
- brand (string)
- model (string)
- year (4 digit integer between 1886 and the current year)
- starting odometer reading (non-negative integer)
- ending odometer reading (non-negative integer, greater than or equal to starting odometer)
- miles per gallon (non-negative integer)

-------------------------------------------

Program Outputs:
- brand (string)
- model (string)
- year (int)
- starting odometer (int)
- ending odometer (int)
- miles per gallon (int)

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## ITS320 CTA1 Option1  
Critical Thinking Assignment 1 Option 1  
File: ITS320_CTA1.Option1.py   
Date: 02/15/2024

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Program Objective:  
Display a mouse.  
-------------------------------------------------------------------------------------------

Assignment Directions:  
Option #1: Create a Python Application  
Write a Python Program that outputs this mouse:  

An image of a mouse created using symbols from a computer keyboard  
  
Assignment Instructions:  
Install Python3 on your computer if you have not already installed it.  
Make sure you check the box to include the Python executable in your environment path.  
Edit your Python program using your choice of editor such as Notepad, Notepad++,  
or Idle. Idle is a simple Python interactive development environment that installed with your Python package. 

-------------------------------------------------------------------------------------------

Pseudocode:  
1. Define a banner string for a decorative header.  
2. Define three different representations of the same mouse using ASCII art  
   a. A multi-line string representation.  
   b. A single string using newline characters string.  
   c. An array of strings, each representing a line of the mouse.  
3. Print the banner  
4. Print each mouse representation using three different methods:  
   - Method-1, using a multi-line string  
   - Method-2, using new-line characters strings  
   - Method-3, using a string array
     
-------------------------------------------  

Program Inputs: None  
Program Outputs:  
1. A decorative banner.  
2. Three ASCII art representations of the same mouse.

[Go back to the Project Map](#project-map)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Discussions 
This repository is a collection of discussion posts from IT320 - Basic Programming Python Course  
Directory: [Discussions](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Basic-Programming-ITS320/Discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)
