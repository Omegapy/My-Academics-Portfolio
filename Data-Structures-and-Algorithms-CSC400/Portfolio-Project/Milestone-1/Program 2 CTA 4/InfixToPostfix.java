
/*
    Program Name: Infix Calculator
    Author: Alejandro (Alex) Ricciardi
    Date: 09/08/2024
    
    Program Description: 
    - This program implements an Infix calculator that evaluates arithmetic expressions in infix notation.
    - It converts infix expressions from a text file into postfix expressions, computes the postfix expressions, and displays the results.
    - The program uses a Stack Abstract Data Structure (Stack ADT) to manage operators and operands 
      when converting infix expressions to postfix notation and during the evaluation of postfix expressions.
    - The Stack ADT is implemented as a linked list structure or chain using generic types.
      [element | next] -> [element | next] -> [element | next] -> null.
*/

/*-------------------
 |     Packages     |
 -------------------*/
package infixCalculator; // Program Folder

/**
 * The InfixToPostfix implements methods that convert infix arithmetic
 * expressions into postfix expressions for easier evaluation. It supports
 * multi-digit numbers, negative numbers, operators, and parentheses.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 09/08/2024
 */
public class InfixToPostfix {

	/**
	 * Gets the precedence of operators.
	 *
	 * @param operator the operator character
	 * @return an integer value representing the precedence of the operator
	 */
	private int getPrecedence(char operator) {
		switch (operator) {
		case '+':
		case '-':
			return 1;
		case '*':
		case '/':
		case '%':
			return 2;
		case '^':
			return 3;
		default:
			return -1; // Return -1 for invalid operators
		}
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Checks if the operator is right-associative. Most operators are
	 * left-associative, except for exponentiation.
	 *
	 * @param operator the operator character (e.g., ^ for exponentiation)
	 * @return true if the operator is right-associative, false otherwise
	 */
	private boolean isRightAssociative(char operator) {
		return operator == '^';
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * Converts an infix expression (standard arithmetic notation) to postfix
	 * expression. This method handles multi-digit numbers, negative numbers, and
	 * parentheses.
	 *
	 * @param expression the infix expression as a string
	 * @return the corresponding postfix expression
	 * @throws IllegalArgumentException if there are mismatched parentheses in the
	 *                                  input expression.
	 */
	public String convert(String expression) {
		LinkedStack<Character> operatorStack = new LinkedStack<>(); // Stack to store operators
		StringBuilder postFixString = new StringBuilder(); // The postfix expression
		StringBuilder number; // Stores number from the infix expression
		int countOpeningParentheses = 0; // Counter for opening parentheses
		int countClosingParentheses = 0; // Counter for closing parentheses
		char currentChar; // use to store infix expression char.

		// Iterate through the infix expression
		for (int i = 0; i < expression.length(); i++) {
			currentChar = expression.charAt(i);

			// --- if starts, Multi-digit numbers (and decimal numbers)
			if (Character.isDigit(currentChar)) {
				number = new StringBuilder();
				number.append(currentChar);
				i++;
				// Continue appending digits or decimal point if the number is multi-digit
				while (i < expression.length()
						&& (Character.isDigit(expression.charAt(i)) || expression.charAt(i) == '.')) {
					number.append(expression.charAt(i));
					i++; // increment i to check next character
				}
				postFixString.append(number).append(' '); // Append the number to the postfix expression
				// Adjust the index because the loop will automatically increment i after each
				// iteration
				// and i was incremented in this if statement
				i--;
			}
			// Handle opening parentheses
			else if (currentChar == '(') {
				countOpeningParentheses++;
				operatorStack.push(currentChar);
			}
			// Handle closing parentheses
			else if (currentChar == ')') {
				countClosingParentheses++;
				// Pop operators from the stack until matching '(' is found
				while (!operatorStack.isEmpty() && operatorStack.peek() != '(') {
					// Append operators to postfix expression and a space
					postFixString.append(operatorStack.pop()).append(' ');
				}
				if (!operatorStack.isEmpty() && operatorStack.peek() == '(') {
					operatorStack.pop();
				} else {
					throw new IllegalArgumentException("Mismatched parentheses");
				}
			}
			// Handle negative numbers (e.g., -3 or -x) at the start or after a parenthesis
			else if (currentChar == '-' && (i == 0 || expression.charAt(i - 1) == '(')) {
				postFixString.append('-'); // Append negative sign to the output
			}
			// Handle operators (+, -, *, /, %, ^)
			else if ("+-*/%^".indexOf(currentChar) >= 0) {
				// Pop operators from the stack based on precedence and associativity
				while (!operatorStack.isEmpty() && getPrecedence(currentChar) <= getPrecedence(operatorStack.peek())
						&& (!isRightAssociative(currentChar)
								|| getPrecedence(currentChar) < getPrecedence(operatorStack.peek()))) {
					postFixString.append(operatorStack.pop()).append(' ');
				}
				operatorStack.push(currentChar);
			}
			// --- if ends, Multi-digit numbers (and decimal numbers)

		} // for-loop

		// Check if parentheses are balanced
		if (countOpeningParentheses != countClosingParentheses) {
			throw new IllegalArgumentException("Mismatched parentheses");
		}

		// Pop any remaining operators from the stack
		while (!operatorStack.isEmpty()) {
			postFixString.append(operatorStack.pop()).append(' ');
		}

		// Return the final postfix expression as a string
		return postFixString.toString().trim();
	}

	// ----------------------------------------------------------------------------------------------
}
