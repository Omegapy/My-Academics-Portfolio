-----------------------------------------------------------------------------------------------------------------------------
# Module-8 Portfolio Project 
Assignment Name: Portfolio Project

Grade: 

-----------------------------------------------------------------------------------------------------------------------------

ITS410 - Database Management  
Professor: Dr. Murthy Rallapalli  
Spring B Semester (25SB) – 2025  
Student: Alexander (Alex) Ricciardi  
Date: 06/08/2025  

-----------------------------------------------------------------------------------------------------------------------------

Project Map:   
Module-8 Portfolio.pdf – Portfolio Project

-----------------------------------------------------------------------------------------------------------------------------

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

![image](https://github.com/user-attachments/assets/9320fa7f-3d63-4faf-905b-bbef5cf34c4e)

Submit your labeled results screenshots in a Word file.  

-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 


