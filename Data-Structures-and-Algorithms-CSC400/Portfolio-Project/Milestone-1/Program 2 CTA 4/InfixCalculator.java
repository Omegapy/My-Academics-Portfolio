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

/**
 * The InfixCalculator class test and evaluates infix arithmetic expressions by
 * converting them to postfix notation and then computing the result.
 * 
 * @author Alejandro Ricciardi
 * @version 1.0
 * @date 09/08/2024
 */
public class InfixCalculator {

	private InfixToPostfix converter = new InfixToPostfix(); // For conversion
	private PostfixEvaluator evaluator = new PostfixEvaluator(); // For evaluation

	/**
	 * Converts infix expression to postfix expressions using the functionality of
	 * the InfixToPostfix class. Evaluates the postfix expressions PostfixEvaluator
	 * class and display the results using the and displays the results.
	 * 
	 * @param expression the infix expression to evaluate
	 */
	public void evaluateExpression(String expression) {
		System.out.println("Infix: " + expression);
		try {
			String postfix = converter.convert(expression);
			System.out.println("Postfix: " + postfix);
			double result = evaluator.evaluate(postfix);
			System.out.println("Result: " + result);
		} catch (IllegalArgumentException e) {
			System.out.println("Error: Invalid infix expression - " + e.getMessage());
		} catch (ArithmeticException e) {
			System.out.println("Error: " + e.getMessage());
		} catch (Exception e) {
			System.out.println("Error: Invalid infix expression - " + e.getMessage());
		}
		System.out.println();
	}

	// ----------------------------------------------------------------------------------------------

	/**
	 * The main method the program entry point. It uses the evaluateExpression to
	 * evaluate infix expressions and display the results.
	 * 
	 * @param args command-line arguments (not used in this program)
	 */
	public static void main(String[] args) {

		String banner = """

				        ***************************
				        *                         *
				        *    Infix Calculator     *
				        *                         *
				        ***************************
				""";

		InfixCalculator calculator = new InfixCalculator();

		System.out.println(banner);

		// Test valid expressions with different operators and precedence orders

		// --- division and addition
		System.out.println("----- Evaluating division and addition ------\n");
		calculator.evaluateExpression("10/(2+3)");
		calculator.evaluateExpression("(2+3.2)/10");
		System.out.println();

		// --- addition and multiplication no ()
		System.out.println("----- Evaluating addition and multiplication no () ------\n");
		calculator.evaluateExpression("4.5+2*3");
		calculator.evaluateExpression("7*5+3");
		System.out.println();

		// ---- exponents
		System.out.println("----- Evaluating exponents ------\n");
		calculator.evaluateExpression("8+(5*2)^2");
		calculator.evaluateExpression("8^2*2");
		calculator.evaluateExpression("8^(2*2)");
		calculator.evaluateExpression("8^(-1)");
		calculator.evaluateExpression("8^(-2)");
		System.out.println();

		// --- multiplication, addition, subtraction, and negative numbers
		System.out.println("----- Evaluating multiplication, addition, subtraction, and negative numbers ------\n");
		calculator.evaluateExpression("6*(4+5)-2");
		calculator.evaluateExpression("(-6)*(4+(-5))-2");
		System.out.println();

		// --- Modulus
		System.out.println("----- Evaluating modulus -----\n");
		calculator.evaluateExpression("10%3+2^3");
		calculator.evaluateExpression("2^3+10%3");
		// modulus occupies the same place in the order of operations as multiplication
		// and division.
		System.out.println(
				"Note that Modulus occupies the same place in the order of operations as multiplication and division \n");
		calculator.evaluateExpression("2^3*(10%3)");
		calculator.evaluateExpression("10%3*2^3");
		calculator.evaluateExpression("(10%3)*2^3");
		calculator.evaluateExpression("2^3*10%3"); // ((2^8)*10)%3
		System.out.println();

		// Test invalid expressions
		System.out.println("----- Evaluating invalid expressions ------\n");
		calculator.evaluateExpression("5+"); // Missing operand after operator
		calculator.evaluateExpression("3*/4"); // Invalid operator sequence
		calculator.evaluateExpression("(2+3"); // Missing closing parenthesis
		calculator.evaluateExpression("10/(5-5)"); // Division by zero
	}

	// ----------------------------------------------------------------------------------------------
}
