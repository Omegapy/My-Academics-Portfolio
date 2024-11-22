/*=========================================================================================================
    Program Name: Thread Counting Synchronization
    Author: Professor Computer Science
    Date: 11/24/2024

    Requirement: C++17 or higher

    Program Description:
    This program demonstrates the use of threads and how to synchronize them using mutexes and condition variables.
    Thread 1 counts up from 0 to a maximum count, while Thread 2 waits until Thread 1 completes,
    and then counts down from the maximum count to 0.

    The program adheres to the following SEI CERT C++ Coding Standards:
        - CON50-CPP. Do not destroy a mutex while it is locked
        - CON51-CPP. Ensure actively held locks are released on exceptional conditions
        - CON52-CPP. Prevent data races when accessing bit-fields from multiple threads
        - CON54-CPP. Wrap functions that can spuriously wake up in a loop
        - CON55-CPP. Preserve thread safety and liveness when using condition variables
        - ERR50-CPP. Do not abruptly terminate the program
        - ERR51-CPP. Handle all exceptions
        - ERR55-CPP. Honor Exception Specifications
        - STR50-CPP. Guarantee that storage for strings has sufficient space
        - STR51-CPP. Do not attempt to create a std::string from a null pointer
        - STR52-CPP. Use valid references, pointers, and iterators to reference elements of a basic_string

=========================================================================================================*/

/* ----------------------------------------------------------------------------------------------
      ------------------
     |    Libraries     |
      ------------------
------------------------------------------------------------------------------------------------- */
#include <iostream>             // For std::cout and std::cerr (Input and Output streams)
#include <thread>               // For std::thread (Creating and managing threads)
#include <mutex>                // For std::mutex, std::lock_guard, std::unique_lock (Synchronization primitives)
#include <condition_variable>   // For std::condition_variable (Thread synchronization)
#include <string>               // For std::string (String manipulation)
#include <exception>            // For std::exception
#include <system_error>         // For std::system_error
#include <cstdlib>              // For EXIT_FAILURE, EXIT_SUCCESS

/* ----------------------------------------------------------------------------------------------
      -------------------------
     |    Global Variables     |
      -------------------------
------------------------------------------------------------------------------------------------- */

// Banner - multi-line string
const std::string banner = R"(
                   **************************************
                   *   Thread Counting Synchronization  *
                   **************************************
)";

// Mutex to protect shared data
std::mutex mtx;

// Condition variable for thread signaling
std::condition_variable cv;

// Flag to indicate completion of counting up
bool isCountingUpDone = false;

/* ----------------------------------------------------------------------------------------------
      ----------------------------
     |    Function Declarations   |
      ----------------------------
------------------------------------------------------------------------------------------------- */

/**
 * Counts up from 0 to maxCount.
 *
 * Handles Rules:
 *      - CON50-CPP. Do not destroy a mutex while it is locked
 *      - CON51-CPP. Ensure actively held locks are released on exceptional conditions
 *      - CON52-CPP. Prevent data races when accessing bit-fields from multiple threads
 *      - CON54-CPP. Wrap functions that can spuriously wake up in a loop
 *      - STR51-CPP: Do Not Attempt to Create a std::string from a Null Pointer
 *      - STR52-CPP: Use Valid References, Pointers, and Iterators to Reference Elements of a basic_string
 *      - ERR51-CPP: Handle All Exceptions
 *      - ERR55-CPP: Honor Exception Specifications
 *
 * @param threadName thread's name.
 * @param counter the data to be modify by the thread.
 */
void countUp(const std::string& threadName, int& counter);

/**
 * Counts down from startCount to 0.
 *
 * Handles Rules:
 *      - CON54-CPP: Wrap Functions That Can Spuriously Wake Up in a Loop
 *      - CON55-CPP: Preserve Thread Safety and Liveness When Using Condition Variables
 *      - ERR51-CPP: Handle All Exceptions
 *      - ERR55-CPP: Honor Exception Specifications
 *      - STR52-CPP: Use Valid References, Pointers, and Iterators to Reference Elements of a basic_string
 *      - STR51-CPP: Do Not Attempt to Create a std::string from a Null Pointer
 *
 * @param threadName thread's name.
 * @param counter The data to be modify by the thread.
 */
void countDown(const std::string& threadName, int& counter);

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ---------------------
     |    Main Function    |
      ---------------------

     The main function creates threads for counting up and down.

     Handles Rules:
       - CON50-CPP: Do Not Destroy a Mutex While It Is Locked
       - ERR51-CPP: Handle All Exceptions
       - ERR50-CPP: Do Not Abruptly Terminate the Program
       - ERR55-CPP: Honor Exception Specifications
       - STR50-CPP: Guarantee that storage for strings has sufficient space

-------------------------------------------------------------------------------------------------- */
// ========================================================================================================
int main() {
    // Define thread names for clarity in output
    // (STR50-CPP: Guarantee that storage for strings has sufficient space)
    std::string thread1Name = "Thread 1";
    std::string thread2Name = "Thread 2";

    // Maximum count for Thread 1
    int counter = -1;

    try {
        // Output banner
        std::cout << banner << std::endl;

        // Create Thread 1 (Counting Up)
        std::thread thread1(countUp, thread1Name, std::ref(counter));

        // Create Thread 2 (Counting Down)
        std::thread thread2(countDown, thread2Name, std::ref(counter));

        // Join threads to ensure they have completed execution 
        // (CON50-CPP: Do not destroy a mutex while it is locked)
        thread1.join();
        thread2.join();
    }
    catch (const std::system_error& e) {
        // Ensure actively held locks are released on exceptional conditions (ERR51-CPP)
        std::cerr << "Thread system error: " << e.what() << std::endl;
        return EXIT_FAILURE; // Do not abruptly terminate the program (ERR50-CPP)
    }
    catch (const std::exception& e) {
        // Handle any other standard exceptions
        std::cerr << "Exception: " << e.what() << std::endl;
        return EXIT_FAILURE; // Do not abruptly terminate the program (ERR50-CPP)
    }
    catch (...) {
        // Catch-all handler for any other exceptions
        std::cerr << "Unknown exception occurred." << std::endl;
        return EXIT_FAILURE; // Do not abruptly terminate the program (ERR50-CPP)
    }

    // Final output indicating completion
    // (STR52-CPP: Use valid references, pointers, and iterators to reference elements of a basic_string)
    std::cout << "\nBoth threads have completed their counting without errors." << std::endl;

    return EXIT_SUCCESS;
}

// ========================================================================================================
/* ----------------------------------------------------------------------------------------------
      ----------------------------
     |    Function Definitions    |
      ----------------------------
------------------------------------------------------------------------------------------------- */
// ========================================================================================================

/**
 * Counts up from 0 to maxCount.
 *
 * Handles Rules:
 *      - CON50-CPP. Do not destroy a mutex while it is locked
 *      - CON51-CPP. Ensure actively held locks are released on exceptional conditions
 *      - CON54-CPP. Wrap functions that can spuriously wake up in a loop
 *      - STR51-CPP: Do Not Attempt to Create a std::string from a Null Pointer
 *      - STR52-CPP: Use Valid References, Pointers, and Iterators to Reference Elements of a basic_string
 *      - ERR51-CPP: Handle All Exceptions
 *      - ERR55-CPP: Honor Exception Specifications
 *
 * @param threadName thread's name.
 * @param counter the data to be modify by the thread.
 */
void countUp(const std::string& threadName, int& counter) {
    try {
        // Ensure that threadName is a valid, non-null string (STR51-CPP)

        std::cout << "\n--- Thread 1 is live ---" << std::endl;

        
        for (int i = 0; i <= 20; i++) {
            // Simulate some work with a sleep
			// Note: The mutex is not locked, other threads can access the shared data (counter) during this time
            std::this_thread::sleep_for(std::chrono::milliseconds(100));

            // Using std::lock_guard ensures that the mutex is automatically released when the scope ends,
            // even if an exception is thrown (CON51-CPP)
            // std::lock_guard is used to to lock exactly one mutex for an entire scope
            // (Using RAII to manage mutex unlocking automatically - Related to Unlocking a mutex via RAII)
            { // Scope for lock_guard allows for automatic unlocking of the mutex when the scope ends
				std::lock_guard<std::mutex> lock(mtx); // (CON51-CPP: Automatically unlocks mutex) (at the end of the scope)

                if (i == 0) {
                    std::cout << "\n--- Counting Up Thread 1 ---" << std::endl;
                }

                // Use valid references to elements of a basic_string (STR52-CPP)
                std::cout << threadName << " counting up: " << ++counter << std::endl;
            } // RAII ensures mutex is unlocked automatically when the scope ends
        }

        // After counting up is done, set the flag
        { // Lock mutex before modifying shared flag to prevent data races (CON52-CPP)
            std::lock_guard<std::mutex> lock(mtx); // (CON51-CPP)
            isCountingUpDone = true;
        }

        // Notify one waiting thread to start counting down
        // (CON54-CPP: Wrap functions that can spuriously wake up in a loop)
        cv.notify_one();

        // (CON50-CPP: Do not destroy a mutex while it is locked)
        // The mutex mtx remains valid, it is declared globally and threads are properly joined before the program is terminated.
    }
    catch (const std::exception& e) {
        // Handle exceptions within the thread (ERR51-CPP)
        std::cerr << threadName << " encountered an exception: " << e.what() << std::endl;
    }
    catch (...) {
        std::cerr << threadName << " encountered an unknown exception." << std::endl;
    }
}

// ----------------------------------------------------------------------------------------------

/**
 * Counts down from startCount to 0.
 *
 * Handles Rules:
 *      - CON54-CPP: Wrap Functions That Can Spuriously Wake Up in a Loop
 *      - CON55-CPP: Preserve Thread Safety and Liveness When Using Condition Variables
 *      - ERR51-CPP: Handle All Exceptions
 *      - ERR55-CPP: Honor Exception Specifications
 *      - STR52-CPP: Use Valid References, Pointers, and Iterators to Reference Elements of a basic_string
 *      - STR51-CPP: Do Not Attempt to Create a std::string from a Null Pointer
 *
 * @param threadName thread's name.
 * @param counter The data to be modify by the thread.
 */
void countDown(const std::string& threadName, int& counter) {
    try {
        // Ensure that threadName is a valid, non-null string (STR51-CPP)

        std::cout << "\n--- Thread 2 is live ---" << std::endl;

        // std::unique_lock<std::mutex> is used to lock the mutex and work with the condition variable (wait).
        // Provides more flexibility compared to std::lock_guard, such as manual unlocking.
        std::unique_lock<std::mutex> lock(mtx); // (CON51-CPP: Ensures mutex is unlocked on exceptions)

        // Wait until isCountingUpDone is true
        // (CON54-CPP: Wrap functions that can spuriously wake up in a loop)
        cv.wait(lock, [] { return isCountingUpDone; }); // Mutex is unlocked during wait

        std::cout << "\n--- Counting down Thread 2 ---" << std::endl;

        // Start counting down
        for (int i = counter; i >= 0; --i) {
            lock.unlock(); // Unlock the mutex before sleeping (Explicit Unlock - Using std::unique_lock)

            // Simulate some work with a sleep
            // Note: The mutex is not locked, other threads can access the shared data (counter) during this time
            std::this_thread::sleep_for(std::chrono::milliseconds(100));

            { // Scope for lock_guard allows for automatic unlocking of the mutex when the scope ends
                std::lock_guard<std::mutex> guard(mtx); // (CON51-CPP: Automatically unlocks mutex)

                // Use valid references to elements of a basic_string (STR52-CPP)
                std::cout << threadName << " counting down: " << counter-- << std::endl;
            } // RAII ensures mutex is unlocked automatically when the scope ends

            lock.lock(); // Re-lock the mutex after sleeping (Explicit Lock - Using std::unique_lock)
        }

        // Ensure that threads terminate properly, maintaining liveness and thread safety
        // (CON55-CPP: Preserve thread safety and liveness when using condition variables)
    }
    catch (const std::exception& e) {
        // Handle exceptions within the thread (ERR51-CPP)
        std::cerr << threadName << " encountered an exception: " << e.what() << std::endl;
    }
    catch (...) {
        std::cerr << threadName << " encountered an unknown exception." << std::endl;
    }
}

// ----------------------------------------------------------------------------------------------
// End of Program
