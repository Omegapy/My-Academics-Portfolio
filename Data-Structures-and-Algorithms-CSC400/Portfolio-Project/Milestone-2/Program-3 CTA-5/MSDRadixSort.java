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

/**
 * A class that implements MSD (Most Significant Digit) Radix Sort for sorting
 * arrays of lowercase strings using buckets.
 *
 * @author Alejandro Ricciardi
 * @version 4.0
 * @date 09/15/2024
 */
public class MSDRadixSort {

	// Radix is the number of possible characters ('a' to 'z').
	private static final int R = 26; // radix for lower-case letters ('a' to 'z')
	private static int testBucketNum = 0;

	// ------------------------------------------------------------------------------------
	/*----------------------------------
	 |  Public MSD Radix Sort Method   |
	 ----------------------------------*/

	/**
	 * Sorts an array of strings using MSD radix sort algorithm with buckets.
	 * Creates an auxiliary array 'aux'
	 * 
	 * @param array the array of strings to be sorted
	 */
	public static void msdRadixSort(String[] array) {
		if (array == null || array.length <= 1)
			return;
		// Auxiliary array for alphabetic distribution into buckets
		String[] aux = new String[array.length];
		// Start the recursive MSD radix sort from digit position 0
		msdRadixSort(array, aux, 0, array.length - 1, 0, false);
	}

	// ------------------------------------------------------------------------------------

	/**
	 * Sorts an array of strings using MSD radix sort algorithm with buckets and by
	 * utilizing an auxiliary array 'aux'.
	 * 
	 * @param array the array of strings to be sorted
	 * @isBucketTest activates bucket test, displays buckets in console
	 */
	public static void msdRadixSort(String[] array, boolean isBucketTest) {
		if (array == null || array.length <= 1)
			return;
		// Auxiliary array for distribution into buckets
		String[] aux = new String[array.length];
		// Start the recursive MSD radix sort from digit position 0
		msdRadixSort(array, aux, 0, array.length - 1, 0, isBucketTest);
	}

	// ------------------------------------------------------------------------------------
	/*---------------------------------------------
	 |  Private Recursive MSD Radix Sort Method   |
	 ---------------------------------------------*/
	/**
	 * Recursively sorts the array of strings using MSD radix sort algorithm with
	 * buckets.
	 * 
	 * @param array the array of strings to be sorted
	 * @param aux   the auxiliary array used during sorting
	 * @param low   the starting index of the sub-array (bucket) to sort
	 * @param high  the ending index of the sub-array (bucket) to sort
	 * @param digit the current digit position (character index) to sort by
	 */
	private static void msdRadixSort(String[] array, String[] aux, int low, int high, int digit, boolean isBucketTest) {

		// Character numeric value
		int c; // 'a', c = 0; 'z', c = 25

		// --- Base case ---
		if (low >= high)
			return; // Base case: bucket has one or no elements

		// Count array to store frequency counts (bucket sizes)
		// frequency counts track how many strings share the same character
		int[] bucketCount = new int[R + 2]; // R characters plus two extra slots for short strings

		// Step 1: Compute frequency counts for the current digit to determine bucket
		// sizes
		for (int i = low; i <= high; i++) {
			c = charAt(array[i], digit); // Get the character at current digit
			bucketCount[c + 2]++; // Increment count; c + 2 adjusts for -1 index
		}

		// Step 2: Transform counts to indices to determine bucket starting positions
		for (int r = 0; r < R + 1; r++) { // 'a', r = 0; 'z', r = 25
			bucketCount[r + 1] += bucketCount[r];
		}

		// -- Start Test Bucket
		if (isBucketTest) // Test bucket, displays bucket title at current digit
		{
			if (low == 0 && high == array.length - 1) {
				System.out.println("\n-------------- Sort Bucket number: " + ++testBucketNum + " --------------------");
			} else {
				System.out.println("\n-------------- Sort Bucket character '" + array[low].charAt(0)
						+ "' bucket number: " + ++testBucketNum + " --------------------");
			}
		}
		// -- End test
		// Step 3: Distribute strings into buckets in the auxiliary array based on
		// current digit
		for (int i = low; i <= high; i++) {
			c = charAt(array[i], digit);
			aux[bucketCount[c + 1]++] = array[i]; // Place string in correct bucket and increment count

			// -- Start Test Bucket
			if (isBucketTest) // Test bucket, displays word in bucket at current digit
				System.out.println("\'" + array[i] + "'");
			// -- End test
		}
		// Step 4: Copy strings from auxiliary array back to the original
		// array
		for (int i = low; i <= high; i++) {
			array[i] = aux[i - low]; // Adjust index for sub-array
		}

		// Step 5: Recursively sort each bucket for the next digit
		// --- Recursion case ----
		for (int r = 0; r < R; r++) { // 'a', r = 0; 'z', r = 25
			// Compute the low and high for the bucket with character 'a' + r at current
			// digit
			// Note that the recursion will stop when
			// low + bucketCount[r] >= low + bucketCount[r + 1] - 1
			// that is when low >= high, see if statement
			msdRadixSort(array, aux, low + bucketCount[r], low + bucketCount[r + 1] - 1, digit + 1, isBucketTest);
		}
	}

	// ------------------------------------------------------------------------------------

	/**
	 * Returns the numerical value of the character at the specified digit position
	 * in the string.
	 * 
	 * @param s     the string
	 * @param digit the digit position (character index)
	 * @return the integer value of the character ('a' = 0, 'b' = 1, ..., 'z' = 25),
	 *         or -1 if digit is beyond string length
	 * @throws IllegalArgumentException if the character is not a lowercase letter
	 */
	private static int charAt(String s, int digit) throws IllegalArgumentException {
		if (digit < s.length()) {
			int c = s.charAt(digit) - 'a'; // Convert character to integer (0-25)

			// Check if the character is valid (lowercase 'a' to 'z')
			if (c > 25 || c < 0) {
				throw new IllegalArgumentException("Invalid character '" + s.charAt(digit) + "' in word: " + s
						+ " only lowercase letters are allowed!");
			}

			return c;
		} else {
			return -1; // -1 indicates end of string (shorter strings)
		}
	}

	// ------------------------------------------------------------------------------------

}
