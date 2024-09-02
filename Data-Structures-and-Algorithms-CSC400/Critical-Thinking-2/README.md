-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 2
Program Name: RPG Bag V2 

Grade:  65/65 A

-----------------------------------------------------------------------------------------------------------------------------

CSC400 – Data Structures and Algorithms - Java Course  
Professor: Hubert Pensado  
Fall B Semester (24FD) – 2024  
Student: Alejandro (Alex) Ricciardi  
Date: 08/25/2024   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Java JDK-22  

-----------------------------------------------------------------------------------------------------------------------------

The Assignment Direction:  

Additional Bag Methods  
In this second assignment, you will extend the functionality of the Java bag data structure by implementing additional methods. You will add methods for calculating the size of the bag, merging two bags together, and finding the distinct elements in the bag.  
1.	Modify the `Bag` class from the previous assignment to include the following additional methods:  
•	`int size()`: This method should return the total number of elements in the bag, including duplicates.  
•	 `void merge(Bag<T> otherBag)`: This method should merge the elements of `otherBag` into the current bag.  
•	 `Bag<T> distinct()`: This method should return a new bag that contains only the distinct elements from the current bag.  
2.	Write a Java program that demonstrates the usage of the additional methods. Your program should perform the following operations:  
•	Create two instances of the `Bag` class.  
•	Add elements to each bag, including duplicates.  
•	Print the size of each bag using the `size` method.    
•	Merge the two bags together using the `merge` method.    
•	Print the merged bag contents.  
•	Create a new bag containing only the distinct elements using the `distinct` method.  
•	Print the distinct bag contents.  
Submit your completed assignment as a .java source code file.  

⚠️ My notes:   
-	The program implements an Item class that acts as the base class for the classes Potion, Armor, and Weapon.  

-	The class Bag implements the Iterable interface and uses a linked list,   
[element | next] -> [element | next] -> [element | next] -> null, to store elements. 
 
-	A popular implementation of the Bag ADT is to use a HashMap. Although a HashMap does not allow duplicate entries, it can store a single entry for each element along with its current count. This would eliminate the need to iterate through the entire Bag to count specific elements. However, for this assignment, I chose to use a linked list structure to show a more traditional approach to implementing a Bag ADT.   

-	In addition to the required functionalities, I added an item ID system that ensures bag elements of the same type are not flagged as duplicates. For instance, two healing potions with different IDs will not be considered duplicates; however, two healing potions with the same ID will be considered duplicates.  
Furthermore, the Bag class contains, count, and remove methods treat item objects of the same type but with different IDs as the same type of element. For instance, two healing potions with different IDs will be treated as the same object by these methods.  
Both these two functionalities were accomplished by overring the equals() from the Java Object Class in the Item class, specifically in its subclasses: Potion, Armor, and Weapon.  

-	The program source code can be found in the following files:  
- Item.java  
- Armor.java  
- Weapon.java  
- Potion.java  
- Bag.java   
- Main.java  

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

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/f8001645-cc85-4b99-beec-74482a83ac87"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 





