-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 4
Program Name: Critical Thinking 4 

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
public class InfixCalculator {  
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
[GitHub](https://github.com/Omegapy) 
[Omegapy: Code Chronicles](https://www.alexomegapy.com/)
[LinkedIn](https://www.linkedin.com/in/alex-ricciardi/)  
[Medium] (https://medium.com/@alex.omegapy)    
[YouTube](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)

Related links:  
[CSU Global](https://csuglobal.edu/) 

