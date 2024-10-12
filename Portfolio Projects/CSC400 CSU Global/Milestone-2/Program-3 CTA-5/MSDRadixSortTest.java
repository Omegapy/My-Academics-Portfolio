/*
    Program Name: Infix Calculator
    Author: Alejandro (Alex) Ricciardi
    Date: 09/15/2024
    
    Program Description: 
    MSD RadixSort is an implementation of a Most Significant Digit (MSD) radix sort, 
    which sorts an array of lowercase strings in alphabetical order by examining each character from left to right. 
    The program uses recursion to sort subarrays (buckets) based on character positions. 
*/

/*-------------------
 |     Packages     |
 -------------------*/
package radixSort;

import java.util.Arrays;

/**
 * Test class for MSD Radix Sort. Contains test cases for the MSD Radix Sort
 * algorithm.
 * 
 * Test cases: 1. Regular unsorted array 2. Array with words of varying lengths
 * 3. Array with duplicates 4. Empty array 5. Array with one element 6. Array
 * with all identical elements 7. Array with upper and lower case characters 8.
 * Array with special characters 9. Display buckets during sorting
 * 
 * @author Alejandro Ricciardi
 * @version 3.0
 * @date 09/15/2024
 */
public class MSDRadixSortTest {

	/**
	 * The main method runs all test cases for MSD Radix Sort.
	 * 
	 * Test cases: 1. Regular unsorted array 2. Array with words of varying lengths
	 * 3. Array with duplicates 4. Empty array 5. Array with one element 6. Array
	 * with all identical elements 7. Array with upper and lower case characters 8.
	 * Array with special characters 9. Display buckets during sorting
	 * 
	 * @param args command-line arguments (not used)
	 */
	public static void main(String[] args) {

		String banner = """

				        ******************************
				        *                            *
				        *    MSD Radix Sort Test     *
				        *                            *
				        ******************************
				""";

		System.out.println(banner);

		// Test case 1: Regular unsorted array
		System.out.println("\n---------- Test case 1: Regular unsorted array ----------\n");
		String[] words1 = { "joke", "book", "back", "dig", "desk", "word", "fish", "ward", "dish", "wit", "deed",
				"fast", "dog", "bend" };
		System.out.println("Test Case 1 - Original Array: " + Arrays.toString(words1));
		MSDRadixSort.msdRadixSort(words1);
		System.out.println("Test Case 1 - Sorted Array: " + Arrays.toString(words1));

		// Test case 2: Array with words of different lengths
		System.out.println("\n---------- Test case 2: Array with words of varying lengths ----------\n");
		String[] words2 = { "apple", "cat", "b", "banana", "abc", "zebra", "a" };
		System.out.println("Test Case 2 - Original Array: " + Arrays.toString(words2));
		MSDRadixSort.msdRadixSort(words2);
		System.out.println("Test Case 2 - Sorted Array: " + Arrays.toString(words2));

		// Test case 3: Array with duplicates
		System.out.println("\n---------- Test case 3: Array with duplicates ----------\n");
		String[] words3 = { "apple", "apple", "banana", "dog", "cat", "dog", "banana" };
		System.out.println("Test Case 3 - Original Array: " + Arrays.toString(words3));
		MSDRadixSort.msdRadixSort(words3);
		System.out.println("Test Case 3 - Sorted Array: " + Arrays.toString(words3));

		// Test case 4: Empty array
		System.out.println("\n---------- Test case 4: Empty array ----------\n");
		String[] words4 = {};
		System.out.println("Test Case 4 - Original Array: " + Arrays.toString(words4));
		MSDRadixSort.msdRadixSort(words4);
		System.out.println("Test Case 4 - Sorted Array: " + Arrays.toString(words4));

		// Test case 5: Array with one element
		System.out.println("\n---------- Test case 5: Array with one element ----------\n");
		String[] words5 = { "single" };
		System.out.println("Test Case 5 - Original Array: " + Arrays.toString(words5));
		MSDRadixSort.msdRadixSort(words5);
		System.out.println("Test Case 5 - Sorted Array: " + Arrays.toString(words5));

		// Test case 6: Array with all identical elements
		System.out.println("\n---------- Test case 6: Array with all identical elements ----------\n");
		String[] words6 = { "same", "same", "same", "same", "same" };
		System.out.println("Test Case 6 - Original Array: " + Arrays.toString(words6));
		MSDRadixSort.msdRadixSort(words6);
		System.out.println("Test Case 6 - Sorted Array: " + Arrays.toString(words6));

		// Test case 7: Array with upper and lower case characters
		try {
			System.out.println("\n---------- Test case 7: Array with upper and lower case characters ----------\n");
			String[] words7 = { "Apple", "apple", "Banana", "banana", "Cat", "cat" };
			System.out.println("Test Case 7 - Original Array: " + Arrays.toString(words7));
			MSDRadixSort.msdRadixSort(words7);
			System.out.println("Test Case 7 - Sorted Array: " + Arrays.toString(words7));
		} catch (IllegalArgumentException e) {
			// Catch and handle the exception
			System.err.println("Error: " + e.getMessage());
		}

		// Test case 8: Array with special characters
		try {
			System.out.println("\n---------- Test case 8: Array with special characters ----------\n");
			String[] words8 = { "@home", "#world", "1apple", "Banana", "apple!" };
			System.out.println("Test Case 8 - Original Array: " + Arrays.toString(words8));
			MSDRadixSort.msdRadixSort(words8);
			System.out.println("Test Case 8 - Sorted Array: " + Arrays.toString(words8));
		} catch (IllegalArgumentException e) {
			// Catch and handle the exception
			System.err.println("Error: " + e.getMessage());
		}

		// Test case 9: Display buckets test
		System.out.println("\n---------- Test case 9: Display buckets test" + " ----------\n");
		System.out.println("Test Case 9 - Original Array: " + Arrays.toString(words1));
		MSDRadixSort.msdRadixSort(words1, true);
		System.out.println("\nTest Case 1 - Sorted Array: " + Arrays.toString(words1));
	}
}
