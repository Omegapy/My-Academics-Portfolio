-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 1
Program Name: Bank Account

Grade: 70/70 A

-----------------------------------------------------------------------------------------------------------------------------

CSC372 – Programming-2 Java Course  
Professor: Dr. Vanessa Cooper  
Spring D Semester (24SD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 06/16/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-21  

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  
Option #1:  Implementing a Superclass Bank Account  

Part 1: Implement a superclass BankAccount that has the following fields and methods.

Fields:  
string firstName  
string lastName  
int accountID  
double balance  

Methods:  
constructor():  initialize balance to zero  
deposit() - will accept a single value double parameter; the parameter value is added to the existing balance  
withdrawal() - accepts a single value double dollar amount; the parameter value is subtracted from the existing balance  
Setters and getters for firstName, lastName, and accountID
getBalance() getter to return the balance  
accountSummary() - prints all account information  

Part 2: Implement a CheckingAccount class that inherits from the BankAccount class, that:   
Has an interest rate attribute  
Allows overdraft withdrawals and charges a $30 fee  

Methods:  
processWithdrawal() - will display a negative balance that includes a $30 overdraft fee and denotes that a fee has been accessed  
displayAccount() - should display all superclass attributes and provides an additional interest rate  

Ensure that your program has the two required classes and a test class.  
Place each Java class into a separate Java source file.  

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  
The program is a small Java program that manages bank accounts with basic functionalities such as deposit, withdrawal, and account information management.   
It includes a BankAccount class and a CheckingAccount class that extends the BankAccount with additional features like interest rates and overdraft fees.  

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- Project Report.pdf  
	- Program Explanation  
	- Results and test scenarios   
	- Screenshots of the console outputs  
- README.md – Markdown file, program information 
- Main.java – Main program (Main class) tests program
- BankAccount.java – BankAccount class
- CheckingAccount java – CheckingAccoun class

-----------------------------------------------------------------------------------------------------------------------------

My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img width="27" height="27" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53" alt="Code Chronicles logo"></a><a href="https://www.alexomegapy.com"><img height="30" src="https://img.shields.io/badge/Code%20Chronicles%20%7C%20Omegapy-0D1117?style=for-the-badge" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>

Related links:  
[CSU Global](https://csuglobal.edu/) 

