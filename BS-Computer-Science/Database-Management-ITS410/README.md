-----------------------------------------------------------------------------------------------------------------------------
# Database Management - ITS410
-----------------------------------------------------------------------------------------------------------------------------

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omegapy)      

created date: 04/14/2025  

-----------------------------------------------------------------------------------------------------------------------------

Projects Description:    
This repository is a collection of assignments from ITS410 - Database Management Course at Colorado State University Global - CSU Global.  

-----------------------------------------------------------------------------------------------------------------------------

ITS410 - Database Management  
Professor: Murthy Rallapalli  
Spring B (25SB) – 2025   
Student: Alexander (Alex) Ricciardi   

Final grade:  4.0 A

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  

-----------------------------------------------------------------------------------------------------------------------------
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
   
-----------------------------------------------------------------------------------------------------------------------------

#### Project Map  

- [Module 8 Portfolio Project](#module-8-portfolio-project)
- [Module 6 Critical Thinking](#module-6-critical-thinking)
- [Module 5 Critical Thinking](#module-5-critical-thinking)
- [Module 4 Critical Thinking](#module-4-critical-thinking) 
- [Module 3 Critical Thinking](#module-3-critical-thinking) 
- [Module 2 Critical Thinking](#module-2-critical-thinking)  
- [Module 1 Critical Thinking](#module-1-critical-thinking)   
- [Discussions](#discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 8 Portfolio Project  
Directory: [Module-8-Portfolio-Project](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Module-8-Portfolio-Project)   
Title: Module 8 Portfolio Project: Portfolio Project

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:    

The Assignment Direction:    

Stored Procedures  
Using the My Guitar Shop database you installed in Module 1, develop the following queries.
1. Write a script that creates and calls a stored procedure named insert_category.
2. First, code a statement that creates a procedure that adds a new row to the Categories table. 
   - To do that, this procedure should have one parameter for the category name.
3. Code at least two CALL statements that test this procedure. (Note that this table doesn’t allow duplicate category names.) 
   - Execute the query and take a screenshot of the query and the results.
4. Write a script that creates and calls a stored function named discount_price that calculates the discount price of an item in the Order_Items table (discount amount subtracted from item price). 
   - To do that, this function should accept one parameter for the item ID, and it should return the value of the discount price for that item. 
   - Execute the query and take a screenshot of the query and the results.
5. Write a script that creates and calls a stored function named item_total that calculates the total amount of an item in the Order_Items table (discount price multiplied by quantity).
   - To do that, this function should accept one parameter for the item ID, it should use the discount_price function that you created in exercise 2, and it should return the value of the total for that item. 
   - Execute the query and take a screenshot of the query and the results.

All the screenshots should show current date. Example of screenshot.

Submit your labeled results screenshots in a Word file.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 6 Critical Thinking 
Directory: [Module-6-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Module-6-Critical-Thinking)   
Title: Critical Thinking Assignment 5: Stored Procedures 

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:    

The Assignment Direction:    

**Part 1**: Lessons Learned and Reflection

Write a 2- to 3-page summary that outlines the lessons you learned in this database class. Reflect on how these lessons can be applied toward more effective database management and reporting.


**Part 2**: Queries 

The Assignment Direction:  
Using the My Guitar Shop database you installed in Module 1, develop the following queries.  
SUBMIT A SCREENSHOT OF EACH STEP.  

1.	Write a SELECT statement that returns these column names and data from the Products table:  
product_name               The product_name column  
list_price                        The list_price column  
discount_percent            The discount_percent column  
discount_amount            A column that’s calculated from the previous two columns  
discount_price               A column that’s calculated from the previous three columns  
- Round the discount_amount and discount_price columns to two decimal places. 
- Sort the result set by the discount_price column in descending sequence. 
- Use the LIMIT clause so the result set contains only the first five rows. 
- Submit a screenshot.


2.	Write a SELECT statement that returns these column names and data from the Order_Items table:  
item_id                           The item_id column  
item_price                      The item_price column  
discount_amount            The discount_amount column  
quantity                          The quantity column  
price_total                       A column that’s calculated by multiplying the item price by the quantity  
discount_total                  A column that’s calculated by multiplying the discount amount by the quantity  
item_total                         A column that’s calculated by subtracting the discount amount from the item price and then multiplying by the quantity  
- Only return rows where the item_total is greater than 500. 
- Sort the result set by the item_total column in descending sequence. 
- Submit a screenshot.

3.	Write a SELECT statement that returns the product_name and list_price columns from the Products table.  
- Return one row for each product that has the same list price as another product.
- Hint: Use a self-join to check that the product_id columns aren’t equal but the list_price columns are equal.
- Sort the result set by the product_name column. Submit a screenshot.

4.	Write a SELECT statement that returns these two columns:  
category_name        The category_name column from the Categories table  
product_id               The product_id column from the Products table  
- Return one row for each category that has never been used. 
- Hint: Use an outer join and only return rows where the product_id column contains a null value. 
- Submit a screenshot.

5.	Write an INSERT statement that adds this row to the Customers table:  
email_address:         rick@raven.com  
password:                (empty string)  
first_name:                Rick  
last_name:                 Raven  
- Use a column list for this statement. 
- Submit a screenshot.

6.	Write a SELECT statement that answers this question: Which customers have ordered more than one product? 
- Return these columns:  
The email_address column from the Customers table
The count of distinct products from the customer’s orders
- Sort the result set in ascending sequence by the email_address column. 
- Submit a screenshot.

7.	Write a SELECT statement that answers this question: What is the total quantity purchased for each product within each category?   
- Return these columns
-	The category_name column from the category table
-	The product_name column from the products table
-	The total quantity purchased for each product with orders in the Order_Items table
-	Use the WITH ROLLUP operator to include rows that give a summary for each category name as well as a row that gives the grand total.
-	Use the IF and GROUPING functions to replace null values in the category_name and product_name columns with literal values if they’re for summary rows. 
- Submit a screenshot.

8.	Write and execute a script that creates a user with a username using your firstname initial and lastname and password of your choosing.   This user should be able to connect to MySQL from any computer.  
- This user should have SELECT, INSERT, UPDATE, and DELETE privileges for the Customers, Addresses, Orders, and Order_Items tables of the My Guitar Shop database.
- However, this user should only have SELECT privileges for the Products and Categories tables. - - Also, this user should not have the right to grant privileges to other users.
- Check the privileges for the user by using the SHOW GRANTS statement. 
- Submit a screenshot.

All the screenshots should show current date. Example of screenshot.

Submit your labeled results screenshots in a Word file.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 5 Critical Thinking 
Directory: [Module-5-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Module-5-Critical-Thinking)   
Title: Critical Thinking Assignment 4: Modifying Tables

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:    

The Assignment Direction:    

Writing Queries

Using the My Guitar Shop database you installed in Module 1, develop the following queries.

1. Write a SELECT statement that returns these columns:  
The count of the number of orders in the Orders table  
he sum of the tax_amount columns in the Orders table  
Execute the query and take a screenshot of the query and the results.  

2. Write a SELECT statement that returns one row for each category that has products with these
columns:  
The category_name column from the Categories table  
The count of the products in the Products table  
The list price of the most expensive product in the Products table.  
Sort the result set so the category with the most products appears first.  
Execute the query, and take a screenshot of the query and the results.  

3. Write a SELECT statement that returns one row for each customer that has orders with these
columns:  
The email_address column from the Customers table  
The sum of the item price in the Order_Items table multiplied by the quantity in the Order_Items table  
The sum of the discount amount column in the Order_Items table multiplied by the quantity in the Order_Items table  
Sort the result set in descending sequence by the item price total for each customer.  
Execute the query and take a screenshot of the query and the results.  

4. Write a SELECT statement that returns one row for each customer that has orders with these
columns:  
The email_address column from the Customers table  
A count of the number of orders  
The total amount for each order (Hint: First, subtract the discount amount from the price. Then, multiply by the quantity.)  
Return only those rows where the customer has more than one order.  
Sort the result set in descending sequence by the sum of the line item amounts.  
Execute the query and take a screenshot of the query and the results  


All the screenshots should show current date. Example of screenshot.

Submit your labeled results screenshots in a Word file.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 4 Critical Thinking 
Directory: [Module-4-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Module-4-Critical-Thinking)   
Title: Critical Thinking Assignment 4: Modifying Tables

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:    

Modifying Tables
Using the My Guitar Shop database you installed in Module 1, develop the following queries.  
To test whether a table has been modified correctly as you do these exercises, you can write and run an appropriate SELECT statement.

1. Write an INSERT statement that adds this row to the Categories table:
category_name:               Brass
Code the INSERT statement so MySQL automatically generates the category_id column. Execute the query and take a screenshot of the query and the results.  
2. Write an UPDATE statement that modifies the row you just added to the Categories table. This statement should change the category_name column to “Woodwinds,” and it should use the category_id column to identify the row. Execute the query and take a screenshot of the query and the results.  
3. Write a DELETE statement that deletes the row you added to the Categories table in exercise 1. This statement should use the category_id column to identify the row. Execute the query and take a screenshot of the query and the results.  
4. Write an INSERT statement that adds this row to the Products table:
product_id:			The next automatically generated ID  
category_id: 		4    
product_code:		dgx_640  
product_name:		Yamaha DGX 640 88-Key Digital Piano  
description:		Long description to come.  
list_price:			799.99	
discount_percent:		0  
date_added:			Today’s date/time.	

All the screenshots should show current date. Example of screenshot.

Submit your labeled results screenshots in a Word file.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 3 Critical Thinking 
Directory: [Module-3-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Module-3-Critical-Thinking)   
Title: Critical Thinking Assignment 3: Using Joins

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:  

Using Joins  
Using the My Guitar Shop database you installed in Module 1, develop the following queries.

1. Write a SELECT statement that joins the Categories table to the Products table and returns these columns: category_name, product_name, list_price.
Sort the result set by the category_name column and then by the product_name column in ascending sequence. Execute the query and take a screenshot of the query and the results.
2. Write a SELECT statement that joins the Customers table to the Addresses table and returns these columns: first_name, last_name, line1, city, state, zip_code.
Return one row for each address for the customer with an email address of allan.sherwood@yahoo.com. Execute the query and take a screenshot of the query and the results.
3. Write a SELECT statement that joins the Customers table to the Addresses table and returns these columns: first_name, last_name, line1, city, state, zip_code.
Return one row for each customer, but only return addresses that are the shipping address for a customer. Execute the query and take a screenshot of the query and the results.
4. Write a SELECT statement that joins the Customers, Orders, Order_Items, and Products tables. This statement should return these columns: last_name, first_name, order_date, product_name, item_price, discount_amount, and quantity.

All the screenshots should show current date. Example of screenshot.

Submit your labeled results screenshots in a Word file.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 2 Critical Thinking 
Directory: [Module-2-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Module-2-Critical-Thinking)   
Title: Critical Thinking Assignment 2: Guitar Shop Database  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:  

Guitar Shop Database
Using the My Guitar Shop database you installed in Module 1, develop the following queries.

1. Write a SELECT statement that returns four columns from the Products table: product_code, product_name, list_price, and discount_percent. Then, run this statement to make sure it works correctly. Take a screenshot of the query and results.  
2. Write a SELECT statement that returns one column from the Customers table named full_name that joins the last_name and first_name columns.  
Format this column with the last name, a comma, a space, and the first name like this:  
Doe, John  
Sort the result set by the last_name column in ascending sequence.
Return only the customers whose last names begin with letters from M to Z. Execute the query and take a screenshot of the query and the results.  
NOTE: When comparing strings of characters, ‘M’ comes before any string of characters that begins with ‘M’. For example, ‘M’ comes before ‘Murach’.
3. Write a SELECT statement that returns these columns from the Products table:  
product_name                  The product_name column  
list_price                           The list_price column  
date_added                      The date_added column  
Return only the rows with a list price that’s greater than 500 and less than 2000.  
Sort the result set by the date_added column in descending sequence. Execute the query and take a screenshot of the query and the results..

All the screenshots should show current date. Example of screenshot.

Submit your labeled results screenshots in a Word file.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 1 Critical Thinking 
Directory: [Module-1-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Module-1-Critical-Thinking)   
Title: Critical Thinking Assignment 1:  Create MySQL Database  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:  

Create MySQL Database
You will use MySQL Workbench to create the My Guitar Shop database to review the tables in this database and to enter SQL statements and run them against this database.

**Make sure the MySQL server is running**

1. Start MySQL Workbench and open a connection for the root user.
2. Check whether the MySQL server is running. If it isn’t, start it.

**Use MySQL Workbench to create the My Guitar Shop database.**

3. Download and open the script file named my_guitar_shop.sql Download my_guitar_shop.sqlby clicking the Open SQL Script File button in the SQL Editor toolbar. Then, use the resulting dialog box to locate and open the file. 
4. Execute the entire script by clicking the Execute SQL Script button in the SQL editor toolbar or by pressing Ctrl+Shift+Enter. When you do, the Output window displays messages that indicate whether the script executed successfully. Take a screenshot.

**Use MySQL Workbench to enter and run SQL statements**

5. Double-click on the my_guitar_shop database to set it as the default database. When you do that, MySQL Workbench should display the database in bold.
6. Open a SQL editor tab. Then, enter and run this SQL statement:

SELECT product_name FROM products

Take a resulting screenshot.

7. Delete the e at the end of product_name and run the statement again. Note the error number and the description of the error. Take a resulting screenshot.
8. Open another SQL editor tab. Then, enter and run this statement:

SELECT COUNT(*) AS number_of_products

FROM products

**Use MySQL Workbench to open and run scripts**

9. Download and open the script named product_details.sql Download product_details.sql. Note that this script contains just one SQL statement. Then, run the statement. Take a resulting screenshot.
10. Download and open the script named product_summary.sql Download product_summary.sql. Note that this opens another SQL editor tab. Then, run the statement. Take a resulting screenshot.

11. Download and open the script named product_statements.sql Download product_statements.sql. Notice that this script contains two SQL statements that end with semicolons. Then, run the statement. Take a resulting screenshot.

All the screenshots should show current date. Example of screenshot.

Submit your labeled results screenshots in a Word file.  

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Discussions 
This repository is a collection of discussion posts from ITS410 - Database Management    
Directory: [Discussions](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/BS-Computer-Science/Database-Management-ITS410/Discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)


