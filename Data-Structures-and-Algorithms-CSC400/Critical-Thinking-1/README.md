-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 1
Program Name: RPG Bag  

Grade:  

-----------------------------------------------------------------------------------------------------------------------------

CSC400 – Data Structures and Algorithms - Java Course  
Professor: Hubert Pensado  
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 08/18/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-22  

-----------------------------------------------------------------------------------------------------------------------------

Java Bag Data Structure
In this assignment, you will implement a Java bag data structure, also known as a multiset. A bag is a collection of elements that allows duplicates and does not enforce any particular order. Your task is to design and implement a bag class in Java that supports basic operations such as adding elements, removing elements, checking if an element exists, and counting the occurrences of an element.  
1.	Design a Java class called `Bag` that implements the bag data structure.  
2.	The `Bag` class should have the following methods:  
- `void add(T item)`: This method should add an item of type T to the bag.
- `void remove(T item)`: This method should remove one occurrence of the item from the bag, if it exists.
- `boolean contains(T item)`: This method should return true if the item exists in the bag; otherwise, it should return false.   
3.	Write a Java program that demonstrates the usage of the `Bag` class. Your program should perform the following operations: 
4.	Comment your code appropriately to explain the functionality of each method.
- Create an instance of the `Bag` class.
- Add several elements to the bag, including duplicates.
- Print the bag contents.
- Test the `contains` method for a few elements.
- Test the `count` method for a few elements.
- Remove an element from the bag.
- Print the bag contents again
- Test the `contains` method for the removed element.
- Test the `count` method for the removed element.
Submit your completed assignment as a .java source code file.

⚠️ My notes:   
- The program implements an Item class that acts as the base class for the classes Potion, Armor, and Weapon.  
- The class Bag implements the Iterable and uses a list structure, 
[element | next] -> [element | next] -> [element | next] -> null, to store elements.  
- A popular implementation of the Bag ADT is to use a HashMap. Although a HashMap does not allow duplicate entries, it can store a single entry for each element along with its current count. This would eliminate the need to iterate through the entire Bag to count specific elements. However, for this assignment, I chose to use a linked list structure to show a more traditional approach to implementing a Bag ADT. 
- In addition to the required functionalities, the program includes an extra feature that allows changing the price of an item object.  
- The program source code can be found in the following files:  
o Item.java  
o Armor.java  
o Weapon.java  
o Potion.java  
o Bag.java  
o Main.java  

-----------------------------------------------------------------------------------------------------------------------------

Program Description:  
The program is an implementation of a Bag Abstract Data Structure (Bag ADT) using a Linked list structure.  
[element | next] -> [element | next] -> [element | next] -> null.   
The Bag class represents the inventory of an RPG video game player.  
The Bag allows for the storage and management of game items such as Potions, Armor, and Weapons.  
The Bag ADT is implemented as a generic class that can store any element object type.  

-----------------------------------------------------------------------------------------------------------------------------

#### Project Map
- Project Report.pdf  
	- Program Explanation  
	- Results and test scenarios   
	- Screenshots  
- README.md – Markdown file, program information  
- Armor.java - The Armor class.  
- Weapon.java - The Weapon class.  
- Potion.java - The Potion class.  
- Item.java - The Item class. 
- Potion.java - The Potion class.  
- Bag.java – The Bag class.  
- Main.java – The Main class.  


-----------------------------------------------------------------------------------------------------------------------------

My Links:   
[GitHub](https://github.com/Omegapy)   
[Code Chronicles](https://www.alexomegapy.com/)  
[LinkedIn](https://www.linkedin.com/in/alex-ricciardi/)    
[Medium](https://medium.com/@alex.omegapy)     
[YouTube](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)  

Related links:  
[CSU Global](https://csuglobal.edu/)   
[CSU Global](https://csuglobal.edu/)   

