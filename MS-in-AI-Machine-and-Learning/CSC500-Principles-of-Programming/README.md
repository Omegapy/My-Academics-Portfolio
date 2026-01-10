# Principles of Programming – CSC500 

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omega.py)      

created date: 09/08/2025  

---

**Project Description:**    
This repository is a collection of Python programs from CSC500 – Principles of Programming at Colorado State University Global - CSU Global.  

**CSC500 - Principles of Programming**  
In this graduate course, students are provided with a detailed overview of fundamental programming, design, and testing concepts. Students are introduced to programming constructs and learn how to plan and create basic programming applications. Students will develop applications using common programming structures, which include conditional statements, switches, loops, iteration control structures, and arrays.

Course Learning Outcomes:
1. Explain the terminology used in programming and the tasks performed by a programmer.
2. Develop applications using variables, constants, selection structures, and repetition structures.
3. Implement a solution that uses arrays.
4. Identify constructs for reading and writing of text files in programming.
5. Develop an application using function procedures and string manipulation.

---

Principles of Programming CSC500 – Python Programming   
Professor: Brian Holbert  
Fall C (25FC) – 2025   
Student: Alexander (Alex) Ricciardi   

Final grade: 100% A

---

Requirements:  
 [![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)

---

My Links:   

<i><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></i>
<i><a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></i>
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
<i><a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></i>
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)
<i><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></i>
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)  
   
---

#### Project Map  

- [Critical Thinking 1](#critical-thinking-1)
- [Critical Thinking Module 3](#critical-thinking-module-3)
- [Portfolio Milestone Module 4](#portfolio-milestone-module-4)
- [Critical Thinking Module 5](#critical-thinking-module-5)
- [Portfolio Milestone Module 6](#portfolio-milestone-module-6)
- [Critical Thinking Module 7](#critical-thinking-module-7)
- [Portfolio Project Module 8](#portfolio-project-module-8)
- [Discussions](#discussions)


---
---

## Portfolio Project Module 8
Directory: [Portfolio-Project-Module-8](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Portfolio-Project-Module-8)   
Title: Portfolio Milestone Module 8 – Online Shopping Cart V3

---
---

Assignment Description:  

Online Shopping Cart

**From Milestone 1:**

**Step 1:**  
Build the ItemToPurchase class with the following specifications:  
Attributes   
- item_name (string)  
- item_price (float)  
- item_quantity (int)  
- Default constructor  
- Initializes item's name = "none", item's price = 0, item's quantity = 0  

Method  
- print_item_cost()  

Example of print_item_cost() 
output:    
Bottled Water 10 @ $1 = $10

**Step 2:**  
In the main section of your code, prompt the user for two items and create two objects of the ItemToPurchase class.  

Example:  

Item 1  
Enter the item name:  
Chocolate Chips  
Enter the item price:  
3  
Enter the item quantity:  
1 

Item 2  
Enter the item name:  
Bottled Water  
Enter the item price:  
1  
Enter the item quantity:  
10  

**Step 3:**  
Add the costs of the two items together and output the total cost.  

Example:  

TOTAL COST  
Chocolate Chips 1 @ $3 = $3  
Bottled Water 10 @ $1 = $10  
Total: $13  

Fix any issues from milestone 1 submission prior to submitting the Portfolio Project.

**From Milestone 2:**

**Step 4:**  
Build the ShoppingCart class with the following data attributes and related methods. Note: Some can be method stubs (empty methods) initially, to be completed in later steps.

Parameterized constructor, which takes the customer name and date as parameters  

Attributes  
- customer_name (string) - Initialized in default constructor to "none"  
- current_date (string) - Initialized in default constructor to "January 1, 2020"  
- cart_items (list)  

Methods
- add_item()  
    - Adds an item to cart_items list. Has parameter ItemToPurchase. Does not return anything.  
- remove_item()  
    - Removes item from cart_items list. Has a string (an item's name) parameter. Does not return anything.  
    - If item name cannot be found, output this message: Item not found in cart. Nothing removed.  
- modify_item()  
    - Modifies an item's description, price, and/or quantity. Has parameter ItemToPurchase. Does not return anything.   
    - If item can be found (by name) in cart, check if parameter has default values for description, price, and quantity. If not, modify item in cart.  
    - If item cannot be found (by name) in cart, output this message: Item not found in cart. Nothing modified.  
- get_num_items_in_cart()  
    - Returns quantity of all items in cart. Has no parameters.  
- get_cost_of_cart()
    - Determines and returns the total cost of items in cart. Has no parameters.
- print_total()
    - Outputs total of objects in cart.
    - If cart is empty, output this message: SHOPPING CART IS EMPTY
- print_descriptions()
    - Outputs each item's description.

Example of print_total() output:  

John Doe's Shopping Cart - February 1, 2020  
Number of Items: 8  
Nike Romaleos 2 @ $189 = $378  
Chocolate Chips 5 @ $3 = $15  
Powerbeats 2 Headphones 1 @ $128 = $128  
Total: $521  

Example of print_descriptions() output:  

John Doe's Shopping Cart - February 1, 2020  
Item Descriptions  
Nike Romaleos: Volt color, Weightlifting shoes  
Chocolate Chips: Semi-sweet  
Powerbeats 2 Headphones: Bluetooth headphones  

**Step 5:**  
In the main section of your code, implement the print_menu() function. print_menu() has a ShoppingCart parameter and outputs a menu of options to manipulate the shopping cart. Each option is represented by a single character. Build and output the menu within the function.  
If an invalid character is entered, continue to prompt for a valid choice. Hint: Implement Quit before implementing other options. Call print_menu() in the main() function. Continue to execute the menu until the user enters q to Quit.

Example: 

MENU  
a - Add item to cart  
r - Remove item from cart  
c - Change item quantity  
i - Output items' descriptions  
o - Output shopping cart  
q - Quit  
Choose an option:  

**Step 6:**  
Implement Output shopping cart menu option. Implement Output item's description menu option.

Example of shopping cart menu option:

OUTPUT SHOPPING CART  
John Doe's Shopping Cart - February 1, 2020  
Number of Items: 8  
Nike Romaleos 2 @ $189 = $378  
Chocolate Chips 5 @ $3 = $15  
Powerbeats 2 Headphones 1 @ $128 = $128  
Total: $521  

Example of item description menu option. 

OUTPUT ITEMS' DESCRIPTIONS  
John Doe's Shopping Cart - February 1, 2020  
Item Descriptions  
Nike Romaleos: Volt color, Weightlifting shoes  
Chocolate Chips: Semi-sweet  
Powerbeats 2 Headphones: Bluetooth headphones  

Fix any issues from milestone 2 submission prior to submitting the Portfolio Project.

**Additional tasks for the final project submission:**

**Step 7:**  
In the main section of your code, prompt the user for a customer's name and today's date. Output the name and date. Create an object of type ShoppingCart.

Example:

Enter customer's name:  
John Doe  
Enter today's date:  
February 1, 2020  
Customer name: John Doe  
Today's date: February 1, 2020  

**Step 8:**
Implement Add item to cart menu option.

Example:

ADD ITEM TO CART  
Enter the item name:  
Nike Romaleos  
Enter the item description:  
Volt color, Weightlifting shoes  
Enter the item price:  
189  
Enter the item quantity:
2  

**Step 9:**  
Implement remove item menu option.

Example: 
REMOVE ITEM FROM CART   
Enter name of item to remove:  
Chocolate Chips  

**Step 10:**  
Implement Change item quantity menu option. Hint: Make new ItemToPurchase object before using ModifyItem() method.

Example: 

CHANGE ITEM QUANTITY  
Enter the item name:  
Nike Romaleos  
Enter the new quantity:  
3

Compile and submit your pseudocode, source code, screenshots of the application executing the code, the results and GIT repository in a single document (Word is preferred).

---

Program Description:

The Online Shopping Cart Version 3 is a console online shopping cart program that implements the functionality of an online shopping cart:
- it displays simple banners and a menu.
- it provides a menu for the shopping cart.
- it allows users to add, remove, and modify items through a menu.

---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking Module 7
Directory: [Critical-Thinking-Module 7](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Critical-Thinking-Module-7)   
Title: Critical Thinking Module 7 – Course Information

---
---

Assignment Description:  

Creating Python Programs

Write a program that creates a dictionary containing course numbers and the room numbers of the rooms where the courses meet. The dictionary should have the following key–value pairs:

Key–Value Pairs: Room Number

| Course Number (key) | Room Number (value) |
|---|---|
| CSC101 | 3004 |
| CSC102 | 4501 |
| CSC103 | 6755 |
| NET110 | 1244 |
| COM241 | 1411 |

The program should also create a dictionary containing course numbers and the names of the instructors that teach each course. The dictionary should have the following key–value pairs:

Key–Value Pairs: Instructors

| Course Number (key) | Instructor (value) |
|---|---|
| CSC101 | Haynes |
| CSC102 | Alvarado |
| CSC103 | Rich |
| NET110 | Burke |
| COM241 | Lee |

The program should also create a dictionary containing course numbers and the meeting times of each course. The dictionary should have the following key–value pairs:

Key–Value Pairs: Meeting Time

| Course Number (key) | Meeting Time (value) |
|---|---|
| CSC101 | 8:00 a.m. |
| CSC102 | 9:00 a.m. |
| CSC103 | 10:00 a.m. |
| NET110 | 11:00 a.m. |
| COM241 | 1:00 p.m. |

Program Behavior: 
The program should let the user enter a course number and then display the course’s room number, instructor, and meeting time.

Submission:

Compile and submit a single document containing all of the following:
- Source code
- Screenshots of the application executing the code and the results
- Link to your Git repository

---

Program Description:

The program is a small terminal app that allows a user to view 
an ‘university’ course(s) information (course number, room, instructor, and time) 
by entering a course number. 
The course information (data) is stored in three dictionaries, 
and the course numbers are used as keys within the dictionaries.

---

[Go back to the Project Map](#project-map)  


---
---

## Portfolio Milestone Module 6
Directory: [Portfolio-Milestone-Module-6](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Portfolio-Milestone-Module-6)   
Title: Portfolio Milestone Module 6 – Online Shopping Cart V2

---
---

Assignment Description:  

Online Shopping Cart
Step 4: Build the ShoppingCart class with the following data attributes and related methods. Note: Some can be method stubs (empty methods) initially, to be completed in later steps
- Parameterized constructor, which takes the customer name and date as parameters
- Attributes
- customer_name (string) - Initialized in default constructor to "none"
- current_date (string) - Initialized in default constructor to "January 1, 2020"
- cart_items (list)
- Methods
- add_item()
    - Adds an item to cart_items list. Has parameter ItemToPurchase. Does not return anything.
- remove_item()
    - Removes item from cart_items list. Has a string (an item's name) parameter. Does not return anything.
    - If item name cannot be found, output this message: Item not found in cart. Nothing removed.
- modify_item()
    - Modifies an item's description, price, and/or quantity. Has parameter ItemToPurchase. Does not return anything.
    - If item can be found (by name) in cart, check if parameter has default values for description, price, and quantity. If not, modify item in cart.
    - If item cannot be found (by name) in cart, output this message: Item not found in cart. Nothing modified.
- get_num_items_in_cart()
    - Returns quantity of all items in cart. Has no parameters.
- get_cost_of_cart()
    - Determines and returns the total cost of items in cart. Has no parameters.
- print_total()
    - Outputs total of objects in cart.
    - If cart is empty, output this message: SHOPPING CART IS EMPTY
    - print_descriptions()
    - Outputs each item's description.

Example of print_total() output:  
John Doe's Shopping Cart - February 1, 2020  
Number of Items: 8  
Nike Romaleos 2 @ $189 = $378  
Chocolate Chips 5 @ $3 = $15  
Powerbeats 2 Headphones 1 @ $128 = $128  
Total: $521

Example of print_descriptions() output:  
John Doe's Shopping Cart - February 1, 2020  
Item Descriptions  
Nike Romaleos: Volt color, Weightlifting shoes  
Chocolate Chips: Semi-sweet  
Powerbeats 2 Headphones: Bluetooth headphones  

Step 5: In the main section of your code, implement the print_menu() function. print_menu() has a ShoppingCart parameter and outputs a menu of options to manipulate the shopping cart. Each option is represented by a single character. Build and output the menu within the function.

If an invalid character is entered, continue to prompt for a valid choice. Hint: Implement Quit before implementing other options. Call print_menu() in the main() function. Continue to execute the menu until the user enters q to Quit.

Example:  
MENU  
a - Add item to cart  
r - Remove item from cart  
c - Change item quantity  
i - Output items' descriptions  
o - Output shopping cart  
q - Quit  
Choose an option:  

Step 6: Implement Output shopping cart menu option. Implement Output item's description menu option.

Example of shopping cart menu option:  
OUTPUT SHOPPING CART  
John Doe's Shopping Cart - February 1, 2020  
Number of Items: 8  
Nike Romaleos 2 @ $189 = $378  
Chocolate Chips 5 @ $3 = $15  
Powerbeats 2 Headphones 1 @ $128 = $128  
Total: $521  

Example of item description menu option.  
OUTPUT ITEMS' DESCRIPTIONS  
John Doe's Shopping Cart - February 1, 2020  
Item Descriptions  
Nike Romaleos: Volt color, Weightlifting shoes  
Chocolate Chips: Semi-sweet  
Powerbeats 2 Headphones: Bluetooth headphones  

Your program submission materials must include your source code and screenshots of the application executing the code and the results.

---

Program Description:

The program is a small terminal app. It is an implementation of an online shopping cart. This version implements Steps 4-6 (ShoppingCart class and menu system). It provides a menu for the shopping cart. Users can add, remove, and modify items through the menu.

---

[Go back to the Project Map](#project-map)  

---
---

## Critical Thinking Module 5
Directory: [Critical-Thinking-Module 5](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Critical-Thinking-Module-5)   
Title: Critical Thinking Module 5 – Rainfall Average Calculator and Bookstore Points

---
---

Assignment Description:  

Creating Python Programs

Part 1:  
Write a program that uses nested loops to collect data and calculate the average rainfall over a period of years. The program should first ask for the number of years. The outer loop will iterate once for each year. The inner loop will iterate twelve times, once for each month. Each iteration of the inner loop will ask the user for the inches of rainfall for that month. After all iterations, the program should display the number of months, the total inches of rainfall, and the average rainfall per month for the entire period.

Part 2:  
The CSU Global Bookstore has a book club that awards points to its students based on the number of books purchased each month. The points are awarded as follows:  
•	If a customer purchases 0 books, they earn 0 points.  
•	If a customer purchases 2 books, they earn 5 points.  
•	If a customer purchases 4 books, they earn 15 points.  
•	If a customer purchases 6 books, they earn 30 points.  
•	If a customer purchases 8 or more books, they earn 60 points.  
Write a program that asks the user to enter the number of books that they have purchased this month and then displays the number of points awarded.

Submission:  
Compile and submit your pseudocode, source code, and screenshots of the application executing the code from Parts 1 and 2, the results and GIT repository in a single document (Word is preferred).

---

Program Description:

The program is a small console-based program consisting of 2 parts.

-	Part 1 - Rainfall Average Calculator captures rainfall data from user inputs and calculates the rainfall average from the inputted per-month rainfall for the inputted number of years. Then display the results in the console.
-	Part 2 - Bookstore Points calculates the Bookstore club points based on a tier system from the user inputted number of books purchased and displays the results.

---

[Go back to the Project Map](#project-map)  

----
----

## Portfolio Milestone Module 4
Directory: [Portfolio-Milestone-Module-4](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Portfolio-Milestone-Module-4)   
Title: Portfolio Milestone Module 4 – Online Shopping Cart

---
---

Assignment Description:  

Online Shopping Cart  
Step 1: Build the ItemToPurchase class with the following specifications:  
- Attributes
- item_name (string)
- item_price (float)
- item_quantity (int)
- Default constructor

Initializes item's name = "none", item's price = 0, item's quantity = 0  
Method  
print_item_cost()  
Example of print_item_cost() output:  
Bottled Water 10 @ $1 = $10  

Step 2: In the main section of your code, prompt the user for two items and create two objects of the ItemToPurchase class.  
Example:  
Item 1  
Enter the item name:  
Chocolate Chips  
Enter the item price:  
3  
Enter the item quantity:  
1  
Item 2  
Enter the item name:  
Bottled Water  
Enter the item price:  
1  
Enter the item quantity:  
10  

Step 3: Add the costs of the two items together and output the total cost.  
Example:  
TOTAL COST  
Chocolate Chips 1 @ $3 = $3  
Bottled Water 10 @ $1 = $10  
Total: $13  

Your program submission materials must include your source code and screenshots of the application executing the code and the results. Please refer to the video as a recourse and reference: Python Classes and Objects (With Examples)..

---

Program Description:

The program is a small terminal app. It is an implementation of an online shopping cart.  
The program renders banners and a menu, and it calculates the total cost of items based on each item's price and quantity.  
Only two items are asked to be entered in this implementation.

---

[Go back to the Project Map](#project-map)  

----
----

## Critical Thinking Module 3
Directory: [Critical-Thinking-Module 3](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Critical-Thinking-Module-3)   
Title: Critical Thinking Assignment Module 3 – Meal Bill Calculator & Alarm Clock

---
---

Assignment Description:  

Creating Python Programs   
Part 1:  
Write a program that calculates the total amount of a meal purchased at a restaurant. The program should ask the user to enter the charge for the food and then calculate the amounts with an 18 percent tip and 7 percent sales tax. Display each of these amounts and the total price.

Part 2:  
Many people keep time using a 24-hour clock (11 is 11am and 23 is 11pm, 0 is midnight). If it is currently 13 and you set your alarm to go off in 50 hours, it will be 15 (3pm). Write a Python program to solve the general version of the above problem. Ask the user for the time now (in hours) and then ask for the number of hours to wait for the alarm. Your program should output what the time will be on a 24-hour clock when the alarm goes off.

Submission:  
Compile and submit your pseudocode, source code, and screenshots of the application executing the code from Parts 1 and 2, the results and GIT repository in a single document (Word is preferred).

---

Program Description:

The program is a small terminal app. that has two parts:
- Part 1 (Restaurant Bill): Total meal calculator based on food charges/tips/taxes
- Part 2 (24-Hour Alarm): Alarm time calculator based on military time (24hours)  and (added functionality) labels the day the alarm will go off (Today, Tomorrow, or In N days).  
It also includes input validation.

---

[Go back to the Project Map](#project-map)  

----
----

## Critical Thinking 1
Directory: [Critical-Thinking-1](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Critical-Thinking-1)   
Title: Critical Thinking Assignment 1 – Basic Calculator

---
---

Assignment Description:  

Creating Python Programs  
Part 1:  
Write a Python program to find the addition and subtraction of two numbers.

Ask the user to input two numbers (num1 and num2). Given those two numbers, add them together to find the output. Also, subtract the two numbers to find the output.

Part 2:  
Write a Python program to find the multiplication and division of two numbers.

Ask the user to input two numbers (num1 and num2). Given those two numbers, multiply them together to find the output. Also, divide num1/num2 to find the output.

Compile and submit your pseudocode, source code, and screenshots of the application executing the code from parts 1 and 2, the results and GIT repository in a single document (Word is preferred).

Note: Refer to the Module 1 Overview for resources and help using GIT

---

Program Description:

The program is a basic calculator for addition/subtraction, multiplication/division.  
Part 1: addition/subtraction 
Part 2: multiplication/division. 

---

[Go back to the Project Map](#project-map)  

----
----

## Discussions 
This repository is a collection of discussion posts from CSC500 – Principles of Programming     
Directory: [Discussions](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/MS-in-AI-Machine-and-Learning/CSC500-Principles-of-Programming/Discussions)

---

[Go back to the Project Map](#project-map)


