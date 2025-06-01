/*
    Program Name: Infix Calculator
    Author: Alejandro (Alex) Ricciardi
    Date: 09/08/2024
    
    Program Description: 
    - The program is an implementation of an Infix calculator that evaluates arithmetic expressions in infix notation.
    - The program converts Infix expressions stored in a text file into Postfix expressions,
      then computes the Postfix expressions and displays the computation results.
    - The program utilizes a Stack Abstract Data Structure (Stack ADT) to manage operators and operands 
      when converting Infix expressions to Postfix form and during evaluation of Postfix expressions.
    - The Stack ADT is a linked list structure or chain using generic types.
      [element | next] -> [element | next] -> [element | next] -> null.
*/

/*-------------------
 |     Packages     |
 -------------------*/
package infixCalculator; // Program Folder

import java.util.StringTokenizer;

/**
 * The PostfixEvaluator class implements methods that evaluate arithmetic
 * expressions written in postfix notation. Performs postfix computations.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 09/08/2024
 */
public class PostfixEvaluator {

	/**
	 * Apply the arithmetic in order and performs the arithmetic operations.
	 *
	 * @param operator the operator character
	 * @param operand1 the first operand (the left operand)
	 * @param operand2 the second operand (the right operand)
	 * @return the result of applying the operator on the two operands
	 * @throws ArithmeticException if there is an attempt to divide by zero
	 */
	private double applyOperator(char operator, double operand1, double operand2) {
		switch (operator) {
		case '+':
			return operand1 + operand2;
		case '-':
			return operand1 - operand2;
		case '*':
			return operand1 * operand2;
		case '/':
			if (operand2 == 0) {
				throw new ArithmeticException("Division by zero");
			}
			return operand1 / operand2;
		case '%':
			return operand1 % operand2;
		case '^':
			return Math.pow(operand1, operand2);
		default:
			return 0; // Return 0 for any unknown operator (should not happen)
		}
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Evaluates a postfix expression. It processes each token (either a number or
	 * an operator) and evaluates the expression using a stack.
	 * 
	 * Steps: - If a number is encountered, push it onto the stack. - If an operator
	 * is encountered, pop two operands from the stack (binary operation), apply the
	 * operator, and push the result back onto the stack. - At the end of the
	 * process, the top of the stack contains the final result of the expression.
	 *
	 * @param postfix the postfix expression
	 * @return the final result of the expression from the top of stack
	 * @throws ArithmeticException if there is a division by zero or invalid
	 *                             operation
	 */
	public double evaluate(String postfix) {
		LinkedStack<Double> operandStack = new LinkedStack<>(); // Stack to hold operands (numbers)
		StringTokenizer tokens = new StringTokenizer(postfix); // Tokenize the postfix string by spaces
		String token; // stores the tokens from the tokenize postfix expression

		// Process number-operator
		while (tokens.hasMoreTokens()) {
			token = tokens.nextToken();

			// Processes positive, negative, and decimals numbers
			if (token.matches("-?\\d+(\\.\\d+)?")) { // Regular expression matches positive/negative numbers and
														// decimals
				operandStack.push(Double.parseDouble(token)); // Convert string to double and push to stack
			}
			// Handle operators (+, -, *, /, %, ^)
			else if (token.matches("[+\\-*/%^]")) {
				// Pop two operands from the stack
				double operand2 = operandStack.pop(); // Right operand
				double operand1 = operandStack.pop(); // Left operand

				double result = applyOperator(token.charAt(0), operand1, operand2);
				operandStack.push(result);
			}
		} // while-loop

		// The final result
		return operandStack.pop();
	}

	// ----------------------------------------------------------------------------------------------
}
