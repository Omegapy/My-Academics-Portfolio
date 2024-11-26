
/*=========================================================================================================
    Program Name: Thread Counting Synchronization
    Author: Alexander Ricciardi
    Date: 11/24/2024

    Requirement: Java SE 21 or higher

    Program Description:
    This program demonstrates the use of threads and how to synchronize them using ReentrantLocks and Conditions.
    Thread 1 counts up from 0 to a maximum count, while Thread 2 waits until Thread 1 completes,
    and then counts down from the maximum count to 0.

    The program adheres to the following SEI CERT Oracle Coding Standards for Java:
        - STR00-J. Don't form strings containing partial characters from variable-width encodings
        - STR01-J. Do not assume that a Java char fully represents a Unicode code point
        - ERR00-J. Do not suppress or ignore checked exceptions
        - ERR01-J. Do not allow exceptions to expose sensitive information
        - ERR03-J. Restore prior object state on method failure
        - ERR09-J. Do not allow untrusted code to terminate the JVM
        - LCK00-J. Use private final lock objects to synchronize classes that may interact with untrusted code
        - LCK08-J. Ensure actively held locks are released on exceptional conditions
        - THI02-J. Notify all waiting threads rather than a single thread
        - THI03-J. Always invoke wait() and await() methods inside a loop
        - TSM00-J. Do not override thread-safe methods with methods that are not thread-safe
=========================================================================================================*/

import java.util.concurrent.locks.ReentrantLock;            // For ReentrantLock
import java.util.concurrent.locks.Condition;                // For Condition
import java.util.concurrent.TimeUnit;                       // For TimeUnit
import java.util.concurrent.atomic.AtomicBoolean;            // For atomic flag
import java.util.concurrent.atomic.AtomicInteger;           // For atomic counter

/**
 * Thread Counting Synchronization
 *
 * This class demonstrates the use of threads and synchronization in Java.
 * It follows SEI CERT Oracle Coding Standards for Java.
 */
public class ThreadCountingSynchronization {


    /* ----------------------------------------------------------------------------------------------
          -------------------------
         |    Private Variables    |
          -------------------------
    ------------------------------------------------------------------------------------------------- */
	
    // Banner - multi-line string
    private static final String BANNER = """
                       **************************************
                       *   Thread Counting Synchronization  *
                       **************************************
    """;
    
    // ReentrantLock to protect shared data and does not use a string the name lock (LCK00-J, STR001-J)
    private final ReentrantLock lock = new ReentrantLock();

    // Condition for thread signaling (THI03-J)
    private final Condition condition = lock.newCondition();

    // Atomic flag to indicate completion of counting up (TSM00-J)
    private final AtomicBoolean isCountingUpDone = new AtomicBoolean(false);

    // Atomic counter to prevent data races (TSM00-J)
    private final AtomicInteger counter = new AtomicInteger(0);

    /* ----------------------------------------------------------------------------------------------
          ---------------
         |    Methods    |
          ---------------
    ------------------------------------------------------------------------------------------------- */

    /**
     * Counts up from 0 to maxCount.
     *
     * Adheres to SEI CERT Oracle Coding Standards:
     * 		- STR00-J. Don't form strings containing partial characters from variable-width encodings
     * 		- LCK00-J. Use private final lock objects to synchronize classes that may interact with untrusted code
     *      - LCK08-J: Ensure actively held locks are released on exceptional conditions
     *      - ERR00-J: Do not suppress or ignore checked exceptions
     *      - ERR01-J: Do not allow exceptions to expose sensitive information
     *      - ERR03-J. Restore prior object state on method failure
     *
     * @param threadName Thread's name.
     * @param maxCount   The maximum count for counting up.
     */
    private void countUp(String threadName, int maxCount) {
        try {
            // Ensure that threadName is a valid, non-null string (STR00-J)
            if (threadName == null) {
                throw new IllegalArgumentException("Thread name cannot be null.");
            }

            System.out.println("\n--- " + threadName + " is live ---");

            for (int i = 0; i < maxCount; i++) {
                // Simulate some work with a sleep
                TimeUnit.MILLISECONDS.sleep(100);

                // Lock the mutex using ReentrantLock (LCK00-J)
                lock.lock();
                try {
                    if (i == 0) {
                        System.out.println("\n--- Counting Up " + threadName + " ---");
                    }
                    // Increment the counter atomically
                    counter.incrementAndGet();
                    System.out.println(threadName + " counting up: " + counter);
                } finally {
                    // Ensure that the lock is always released (LCK08-J)
                    lock.unlock();
                }
            }

            // After counting up is done, set the flag and notify (LCK08-J)
            lock.lock();
            try {
                isCountingUpDone.set(true);
                condition.signalAll(); // Notify all waiting threads (THI02-J)
            } finally {
                lock.unlock();
            }

        } catch (InterruptedException e) { // (ERR00-J)
            // Handle InterruptedException without exposing sensitive information (ERR01-J)
            Thread.currentThread().interrupt(); // Restore interrupted status (ERR03-J)
            System.err.println(threadName + " was interrupted.");
        } catch (Exception e) { // (ERR00-J)
            // Handle any other exceptions without exposing sensitive information (ERR01-J)
            System.err.println(threadName + " encountered an error: " + e.getMessage());
        }
    }

    /**
     * Counts down from startCount to 0.
     *
     * Adheres to SEI CERT Oracle Coding Standards:
     * 		- STR00-J. Don't form strings containing partial characters from variable-width encodings
     *      - LCK08-J: Ensure actively held locks are released on exceptional conditions
     *      - LCK00-J. Use private final lock objects to synchronize classes that may interact with untrusted code
     *      - THI03-J: Always invoke wait() and await() methods inside a loop
     *      - ERR00-J: Do not suppress or ignore checked exceptions
     *      - ERR01-J: Do not allow exceptions to expose sensitive information
     *      - ERR03-J. Restore prior object state on method failure
     *
     * @param threadName Thread's name.
     */
    private void countDown(String threadName) {
        try {
            // Ensure that threadName is a valid, non-null string (STR00-J)
            if (threadName == null) {
                throw new IllegalArgumentException("Thread name cannot be null.");
            }

            System.out.println("\n--- " + threadName + " is live ---");

            // Lock the mutex before waiting (LCK00-J)
            lock.lock();
            try {
                // Wait until isCountingUpDone is true (THI03-J)
                while (!isCountingUpDone.get()) {
                    condition.await(); // Releases the lock and waits (THI09-J)
                }

                System.out.println("\n--- Counting down " + threadName + " ---");

                // Start counting down from the current counter value
                for (int i = counter.get(); i > 0; i--) {
                    // Simulate some work with a sleep
                    TimeUnit.MILLISECONDS.sleep(100);

                    // Lock to safely decrement the counter (LCK00-J)
                    lock.lock();
                    try {
                        //int decrementedCount = counter.decrementAndGet();
                        System.out.println(threadName + " counting down: " + counter);
                        // Decrement the value of the counter by 1.
                        counter.decrementAndGet();
                    } finally {
                        // Ensure that the lock is always released (LCK08-J)
                        lock.unlock();
                    }
                }
            } finally {
                // Ensure that the lock is always released if not already (LCK08-J)
                if (lock.isHeldByCurrentThread()) {
                    lock.unlock();
                }
            }

        } catch (InterruptedException e) { // (ERR00-J)
            // Handle InterruptedException without exposing sensitive information (ERR01-J)
            Thread.currentThread().interrupt(); // Restore interrupted status (ERR03-J)
            System.err.println(threadName + " was interrupted.");
        } catch (Exception e) { // (ERR00-J)
            // Handle any other exceptions without exposing sensitive information (ERR01-J)
            System.err.println(threadName + " encountered an error: " + e.getMessage());
        }
    }

    /* ----------------------------------------------------------------------------------------------
          ---------------------
         |    Main Function    |
          ---------------------

         The main function creates threads for counting up and down.

         Adheres to SEI CERT Oracle Coding Standards:
           - STR00-J. Don't form strings containing partial characters from variable-width encodings
           - LCK08-J: Ensure actively held locks are released on exceptional conditions
           - ERR00-J: Do not suppress or ignore checked exceptions
           - ERR01-J: Do not allow exceptions to expose sensitive information
           - ERR09-J: Do not allow untrusted code to terminate the JVM
           - STR04-J: Use compatible character encodings when communicating string data between JVMs
    -------------------------------------------------------------------------------------------------- */

    public static void main(String[] args) {
        ThreadCountingSynchronization program = new ThreadCountingSynchronization();

        // Define thread names for clarity in output (STR00-J)
        String thread1Name = "Thread 1";
        String thread2Name = "Thread 2";

        // Maximum count for Thread 1
        int maxCount = 20;

        try {
            // Output banner
            System.out.println(BANNER);

            // Create Runnable tasks
            Runnable countUpTask = () -> program.countUp(thread1Name, maxCount);
            Runnable countDownTask = () -> program.countDown(thread2Name);

            // Create Thread 1 (Counting Up)
            Thread thread1 = new Thread(countUpTask, thread1Name);

            // Create Thread 2 (Counting Down)
            Thread thread2 = new Thread(countDownTask, thread2Name);

            // Start threads
            thread1.start();
            thread2.start();

            // Join threads to ensure they have completed execution (LCK08-J)
            thread1.join();
            thread2.join();

        } catch (InterruptedException e) { // (ERR00-J)
            // Handle InterruptedException without exposing sensitive information (ERR01-J)
            Thread.currentThread().interrupt(); // Restore interrupted status (ERR03-J)
            System.err.println("Main thread was interrupted.");
            System.exit(1); // Do not abruptly terminate the program (ERR09-J)
        } catch (Exception e) { // (ERR00-J)
            // Handle any other exceptions without exposing sensitive information (ERR01-J)
            System.err.println("An error occurred in the main thread: " + e.getMessage());
            System.exit(1); // Do not abruptly terminate the program (ERR09-J)
        }

        System.out.println("\nBoth threads have completed their counting without errors.");
    }

}
// ----------------------------------------------------------------------------------------------
// End of Program
