-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 2
Program Name: RPG Bag V2 

Grade:  

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

Related links:  
[CSU Global](https://csuglobal.edu/) 

