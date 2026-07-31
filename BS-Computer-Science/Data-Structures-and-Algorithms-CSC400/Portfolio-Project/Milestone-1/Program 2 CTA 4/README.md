-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 4
Program Name: Infix Calculator

Grade:  

-----------------------------------------------------------------------------------------------------------------------------

CSC400 – Data Structures and Algorithms - Java Course  
Professor: Hubert Pensado  
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 09/08/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-22  

-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:  

Create an Infix Calculator  
Implement an infix calculator in Java that evaluates arithmetic expressions in infix notation. The program should support the basic arithmetic operations:  
•	addition (+)  
•	subtraction (-)  
•	multiplication (*)  
•	two division operations:  (/ and %)  
Additionally, the program should handle operands and display the final result. 
 
Requirements:  
1.	Your java code.  
2.	Screenshots showing the test of your code, where the following should be tested:  
1.	The program should handle both single-digit and multi-digit operands.  
2.	The program should handle valid postfix expressions.  
3.	Display an error message for invalid expressions.  
4.	Display the result for valid expressions.  
Example:  
<pre>public class InfixCalculator {  
    public int evaluateInfix(String infixExpression) {  
        // Your implementation here  
        // ...  
        return 0; // Placeholder  
    }  

    public static void main(String[] args) {  
        InfixCalculator calculator = new InfixCalculator();  

        // Example 1: Valid Expression   
        String expression1 = "(4+2)*3";  
        System.out.println("Result 1: " + calculator.evaluateInfix(expression1));  

        // Example 2: Valid Expression  
        String expression2 = "5+(3*7)";  
        System.out.println("Result 2: " + calculator.evaluateInfix(expression2));  

        // Example 3: Invalid Expression  
        String expression3 = "4+2*3"; // Missing parentheses  
        System.out.println("Result 3: " + calculator.evaluateInfix(expression3));  
    }  
}  
</pre>pre>
Sample Output:  
Result 1: 18  
Result 2: 26  
Error: Invalid infix expression  

Submit your completed assignment as a .java source code file. 
 
⚠️ My notes:   
-	In addition to the required arithmetic operations it handles exponents (^), decimal numbers, and parentheses.  
-	 The program implements my Linked Stack ADT, a stack implementation that uses a linked list structure, a chain.  

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

-	The program is an implementation of an Infix calculator that evaluates arithmetic expressions in infix notation.  
-	The program converts Infix expressions stored in a text file into Postfix expressions, then computes the Postfix expressions and displays the computation results.  
-	The program utilizes a Stack Abstract Data Structure (Stack ADT) to manage operators and operands when converting Infix expressions to Postfix form and during the evaluation of Postfix expressions.
-	The Stack ADT is a linked list structure or chain using generic types.   
[element | next] -> [element | next] -> [element | next] -> null.  

-------------------------------------------------------------------------
----------------------------------------------------

#### Project Map
- Project Report.pdf  
	- Program Explanation  
	- Results and test scenarios   
	- Screenshots  
- README.md – Markdown file, program information  
- LinkedStack.java - The LinkedStack class.  
- InfixToPostfix.java - The InfixToPostfix class.  
- PostfixEvaluator.java - The PostfixEvaluator class.  
- InfixCalculator.java - The InfixCalculator class. 

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


