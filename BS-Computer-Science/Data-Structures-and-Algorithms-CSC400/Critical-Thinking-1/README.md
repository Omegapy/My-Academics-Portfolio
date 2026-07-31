-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 1
Program Name: RPG Bag  

Grade:  65/65 A

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


