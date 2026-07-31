-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 6  
Program Name: Custom Deque ADT  

Grade:  60/60 A

-----------------------------------------------------------------------------------------------------------------------------

CSC400 – Data Structures and Algorithms - Java Course  
Professor: Hubert Pensado  
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 09/22/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-22  

-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:  

Basic implementation of a custom Deque ADT
Implement a custom Deque ADT with an iterator in Java. The Deque should support the basic operations:  

Insertion  
Deletion  
traversal using an iterator  
Requirements  
Implement a class named CustomDeque with the following methods:  

enqueueFront(int data): Inserts a new element at the front of the deque.  
enqueueRear(int data): Inserts a new element at the rear of the deque.  
dequeueFront(): Removes and returns the element from the front of the deque.  
dequeueRear(): Removes and returns the element from the rear of the deque.  
iterator(): Returns an iterator for traversing the deque.
Implement an inner class named DequeIterator within CustomDeque to serve as the iterator. 

The iterator should have the following methods:  
hasNext(): Returns true if there is a next element, false otherwise.  
next(): Returns the next element and moves the iterator to the next position.  

Demonstrate the functionality of the CustomDeque by iterating through its elements using the custom iterator. To get things started, used the following starter code:  

``` Java
import java.util.Deque;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.NoSuchElementException;

public class CustomDeque {
    private Deque<Integer> deque;

    public CustomDeque() {
        this.deque = new LinkedList<>();
    }

    public void enqueueFront(int data) {
        deque.addFirst(data);
    }

    public void enqueueRear(int data) {
        deque.addLast(data);
    }

    public int dequeueFront() {
        if (isEmpty()) {
            throw new NoSuchElementException("Deque is empty");
        }
        return deque.removeFirst();
    }

    public int dequeueRear() {
        if (isEmpty()) {
            throw new NoSuchElementException("Deque is empty");
        }
        return deque.removeLast();
    }

    public Iterator<Integer> iterator() {
        return new DequeIterator();
    }

    public boolean isEmpty() {
        return deque.isEmpty();
    }

    private class DequeIterator implements Iterator<Integer> {
        private Iterator<Integer> iterator = deque.iterator();

        @Override
        public boolean hasNext() {
            return iterator.hasNext();
        }

        @Override
        public Integer next() {
            if (!hasNext()) {
                throw new NoSuchElementException();
            }
            return iterator.next();
        }
    }

    public static void main(String[] args) {
        CustomDeque customDeque = new CustomDeque();

        // Enqueue elements
        customDeque.enqueueFront(1);
        customDeque.enqueueRear(2);
        customDeque.enqueueFront(3);

        // Iterate and display elements
        Iterator<Integer> iterator = customDeque.iterator();
        while (iterator.hasNext()) {
            System.out.print(iterator.next() + " ");
        }
    }
}
```

Testing:
There is no need for file I/O. Test your program using an array of ten random integers.
Submit your completed assignment as a .java source code file.. 
 
⚠️ My notes:   
- I changed the Deque data type parameter from the Integer data type to the generic data type; public class CustomDeque<T>.  
- In the TestCustomDeque class the integers are directly enqueued into the instantiated Custom Deque object instead of getting them from an array and then enqueuing them.

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  

The program is a custom double-ended queue (deque) implementation in Java using Java's LinkedList.  
It tests the deque insertion and iteration functionalities by enqueuing random integers from both the front and rear; and by iterating starting from the front and then starting from the rear.  

-------------------------------------------------------------------------
----------------------------------------------------

#### Project Map
- Project Report.pdf  
	- Program Explanation 
	- Results and test scenarios   
	- Screenshots  
- README.md – Markdown file, program information  
- CustomDeque.java - The CustomDeque<T> class.  
- TestCustomDeque.java - The TestCustomDeque class.  

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


