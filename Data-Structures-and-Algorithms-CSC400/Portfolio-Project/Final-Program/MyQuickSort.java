/*
    Program Name: Custom Queue ADT and QuickSort
    Author: Alejandro (Alex) Ricciardi
    Date: 10/06/2024
    
    Program Description: 
    This program implements in Java a generic Linked-list queue and sorts the queue using a quicksort algorithm. 
    The queue stores Person objects representing a person first name, last name, and age.
    the Person objects in the queue can be sorted by last name or age.     
*/

/*-------------------
 |     Packages     |
 -------------------*/
package nameAgeQueue;

import java.util.Comparator;
import java.util.LinkedList;

/**
 * A generic implementation of the quicksort algorithm on a linked-list queue
 * that returns a sorted LinkedList without modifying the original queue.
 * 
 * The algorithm implements a Hoare partition to partition the queue. Meaning
 * that the head node of the linked-list queue is picked as the pivot.
 * 
 * Additionally, a queue ADT sort is expected to be stable, preserving the
 * relative (entry) order of elements with equal values.
 * 
 * To partition a linked-list, the element need to be traverseed element by
 * element. Dividing the list into three parts (left, equal, and right) helps
 * simplify the recursion of traversing the list element by element and
 * preserving elements with equal values in order of entry. This also avoids
 * moving elements around in memory, as is required in array-based
 * implementations of quicksort.
 * 
 * @author
 * @version 3.0
 * @date 10/06/2024
 */
public class MyQuickSort {

	// --------------------------------------------------------------------------
	/*-----------------------
	 |  Functionality call  |
	 -----------------------*/

	/**
	 * Performs a quicksort on the given queue. The elements are sorted based on the
	 * provided comparator. The method returns a new sorted LinkedList without
	 * modifying the original queue.
	 *
	 * @param <T>        queue element type - default generic type
	 * @param queue      the queue to be sorted
	 * @param comparator the comparator used to compare elements in the queue
	 * @return a sorted LinkedList containing the elements from the queue
	 */
	public static <T> LinkedList<T> quickSort(MyQueue<T> queue, Comparator<T> comparator) {
		MyQueue<T>.Node<T> head = queue.getFront();
		LinkedList<T> sortedList = quickSortRec(head, comparator);
		return sortedList;
	}

	// --------------------------------------------------------------------------
	/*------------------------
	 |  Recursively Sorting  |
	 ------------------------*/

	/**
	 * Recursively sorts the linked-list of the queue using quicksort and returns a
	 * sorted LinkedList.
	 *
	 * @param <T>        queue element type - default generic type
	 * @param head       the head node of the linked-list queue to be sorted
	 * @param comparator the comparator used to compare elements in the queue
	 * @return a sorted LinkedList containing the elements from the queue
	 */
	private static <T> LinkedList<T> quickSortRec(MyQueue<T>.Node<T> head, Comparator<T> comparator) {
		// --- Base case: if the list is empty or has only one element ---
		if (head == null || head.next == null) {
			LinkedList<T> baseList = new LinkedList<>();
			if (head != null) {
				baseList.add(head.data);
			}
			return baseList;
		}

		// --- Recursion Case ----

		// Partition the list into three parts: left, equal, and right
		PartitionResult<T> partitionResult = partition(head, comparator);

		// -- Recursive calls
		// Recursively sort the left part
		LinkedList<T> leftList = quickSortRec(partitionResult.left, comparator);
		// Recursively sort the right part
		LinkedList<T> rightList = quickSortRec(partitionResult.right, comparator);

		// --- Concatenate the sorted left, equal, and right lists forming the final
		// sorted LinkedList ---
		// Combine the lists to form the sorted list
		LinkedList<T> sortedList = new LinkedList<>();

		// Add left list
		if (leftList != null) {
			sortedList.addAll(leftList);
		}

		// Add equal list
		if (partitionResult.equal != null) {
			MyQueue<T>.Node<T> current = partitionResult.equal;
			while (current != null) {
				sortedList.add(current.data);
				current = current.next;
			}
		}

		// Add right list
		if (rightList != null) {
			sortedList.addAll(rightList);
		}

		return sortedList;
	}

	// --------------------------------------------------------------------------
	/*-----------------
	 |  Partitioning  |
	 -----------------*/

	/**
	 * Holds the partitioned results from the partition method.
	 *
	 * @param <T> the type of elements
	 */
	private static class PartitionResult<T> {
		MyQueue<T>.Node<T> left;
		MyQueue<T>.Node<T> equal;
		MyQueue<T>.Node<T> right;
	}

	// --------------------------------------------------------------------------

	/**
	 * Partitions the linked-list around a pivot element into three lists: elements
	 * less than the pivot, elements equal to the pivot, and elements greater than
	 * the pivot. The head node of the list is picked as the pivot.
	 * 
	 * The algorithm implements a stable partitioning by preserving elements with
	 * equal values order of entry
	 *
	 * @param <T>        queue element type - default generic type
	 * @param head       the head node of the linked-list queue to be partitioned
	 * @param comparator the comparator used to compare elements in the queue
	 * @return Result object containing the left, equal, and right lists
	 */
	private static <T> PartitionResult<T> partition(MyQueue<T>.Node<T> head, Comparator<T> comparator) {
		T pivotData = head.data;

		// Dummy nodes to build the partitions
		MyQueue<T>.Node<T> leftHead = null, leftTail = null;
		MyQueue<T>.Node<T> equalHead = null, equalTail = null;
		MyQueue<T>.Node<T> rightHead = null, rightTail = null;

		MyQueue<T>.Node<T> current = head;

		// Traverse the linked list and partition the nodes
		while (current != null) {
			int cmp = comparator.compare(current.data, pivotData);
			if (cmp < 0) {
				// current.data < pivotData, add to left list
				if (leftHead == null) {
					leftHead = leftTail = new MyQueue<T>().new Node<>(current.data);
				} else {
					leftTail.next = new MyQueue<T>().new Node<>(current.data);
					leftTail = leftTail.next;
				}
			} else if (cmp == 0) {
				// current.data == pivotData, add to equal list
				if (equalHead == null) {
					equalHead = equalTail = new MyQueue<T>().new Node<>(current.data);
				} else {
					equalTail.next = new MyQueue<T>().new Node<>(current.data);
					equalTail = equalTail.next;
				}
			} else {
				// current.data > pivotData, add to right list
				if (rightHead == null) {
					rightHead = rightTail = new MyQueue<T>().new Node<>(current.data);
				} else {
					rightTail.next = new MyQueue<T>().new Node<>(current.data);
					rightTail = rightTail.next;
				}
			}
			current = current.next;
		}

		// Create a PartitionResult object to hold the left, equal, and right partitions
		PartitionResult<T> result = new PartitionResult<>();
		result.left = leftHead;
		result.equal = equalHead;
		result.right = rightHead;

		return result;
	}

	// --------------------------------------------------------------------------

}