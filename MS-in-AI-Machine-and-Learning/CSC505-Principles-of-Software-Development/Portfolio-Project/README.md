## Portfolio Project Module 8
Program Name: ATM Operations

Data:  01/11/2025  
Grade: 

---

CSC505 Principal of Software Development – Python Programming   
Professor: Dr. Joseph Issa  
Winter A (25WA) – 2025   
Student: Alexander (Alex) Ricciardi

---

#### Program Description:

The Python script is a small console application that print all the steps in sequence 
for all the operations at an automated teller machine (ATM) shown in 
the "ATM State Machine UML Diagram.png" diagram.

---

Requirements:  
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

---

#### Assignment Directions: 

##### **Portfolio Project**  

Your Own UML Diagram   
Your Portfolio Project for CSC505 consists of the following:   
- Module 4 Milestone (due in Module 4)
- Module 7 Milestone (due in Module 7)
- Lessons Learned Reflection Modules

###### Final Project  
In Week 8, the components left to complete for your Portfolio Project are the Lessons Learned Reflection and the Final Project. Carefully review the requirements below:

###### Lessons Learned Reflection  
Write a two to three-page summary that outlines the lessons you have learned in this course.   Reflect on how these lessons can be applied to real-world problems or to a specific real-world application. How have they affected your life?

###### Final Project  
For your final project, you are going to create a UML diagram of your choice (e.g., Sequence, Class, Activity, etc.) for an automated teller machine (ATM). Your diagram should include the 
following:
- The customer must pass authentication before withdrawing money.
- Authentication is performed by checking a PIN.
- The PIN can be correct or not.
- Unsuccessful attempts are counted.
- If the counter exceeds a limit, then the customer is rejected.
- If the account balance is zero, then the account is closed.

Annotate your state box in one of two ways. For internal state transitions, use the following state box:

![alt text]

State box for internal state transitions with state above event/action.

If a state transitions to itself, use the following notation in the state box:
- entry/Action
- exit/Action. 

A transition from one state to another is a link arrow connecting the two states and is labeled with event, guard, or action. The "event" is the action that causes a state to transition to another; e.g., "CheckPin." The "guard" is a possible outcome of an event; e.g., "correct PIN" or "incorrect PIN". The "action" is the result of the outcome of an event; e.g., if the guard is "incorrect PIN" then the "action" may be something like "increment error counter." Format your transition labels as follows:

- Event [guard] / action

Diagram showing a transition from one state to another labeled with event, guard, and action.

Use one of the following UML tools to create your diagrams for the Final Project:
- UMLet Links 
- Gliffy Links 
- Microsoft VisioLinks (No purchase required, though you can use it if you already have access to the tool.)

Write a Python Script that will the steps in sequence the operations at the teller machine as shown in your diagram(s). Submit the source file (.py), the screenshots of a successful execution of your progra related diagrams, and the Lesson Learned document in a zipped folder.

Include at least two credible references in addition to the course textbook. The CSU Global Library or the Internet are good places to find these references. The CSU Global Library and Writing Center links can be found in the course navigation panel. Format your document according to the CSU Global Writing Center requirements.
 
---

UML Activity Diagram


---

#### Program Description:

The Python script in a small console application that print all the steps in sequence 
for all the operations at an automated teller machine (ATM) shown in 
the "ATM State Machine UML Diagram.png" diagram. 

---

#### Articles and tutorials used

- Dwivedi’s LinkedIn Learning lesson on state machine diagrams (Dwivedi, 2019) was used to learn about for what a state machine diagram represents (states + event-driven transitions) confirming that the ATM diagram needs to be a behavioral state machine diagram.
- FastBitLab’s “UML state machine types of transitions” lesson (FastBitLab, 2022) was used to learn about diffence between external and internal/self transitions. I used to define what is an external behaviors (arrows)and what is an internal behaviors (entry/, do/, and exit/).
- GeeksforGeeks’ UML state diagram article (GeeksforGeeks, 2025) was used as a reference for notation (initial/final nodes, state boxes, guards/actions).
- IBM’s “Creating transitions between states” documentation (IBM, 2023) was used to learn about transition terminology (trigger/event, guard condition, and effect/action) and required transition label format: Event [guard] / action.
- Pressman & Maxim (2020) was used to support software-design decisions—using UML as a communication artifact, keeping the model focused on required behavior (authentication → withdrawal) rather than low-level implementation details.
- Ricciardi’s “UML State machine diagrams: Modeling dynamic system behavior” article (Ricciardi, 2025) was used to check if the digram was missing guards, ambiguous transitions notations.
- Ricciardi’s “A Guide to UML sequence diagrams: notation, strengths, and limitations” (Ricciardi, 2025) was used to help translate the state-machine diagram flow into a step-by-step sequences for integration into the Python script.

---

#### References: 


Dwivedi, N. (2019, September 9.). Software design: Modeling with UML. *State machine diagram. Modeling with the Unified Modeling Language (UML)*. LinkedIn Learning. https://www.linkedin.com/learning/software-design-modeling-with-uml/state-machine-diagram?u=2245842


FastBitLab (2022, January 20). *FSM Lecture 11- UML state machine types of transitions.* FasBitLab. https://fastbitlab.com/fsm-lecture-11-uml-state-machine-types-of-transitions/


GeeksforGeeks (2025, January 3). *State machine diagrams | Unified Modeling Language (UML).* GeeksforGeeks. https://www.geeksforgeeks.org/unified-modeling-language-uml-state-diagrams/


IBM (2023, September 2018). *Creating transitions between states*. IBM DevOps Model Architect. IBM Documentation. https://www.ibm.com/docs/en/dma?topic=diagrams-creating-transitions-between-states

Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A practitioner's approach (9th ed.). McGraw-Hill Education. 

Ricciardi, A. (2025, February 8). *UML State machine diagrams: Modeling dynamic system sehavior*. Code Chronicles - Omega.py. https://www.alexomegapy.com/post/uml-state-machine-diagrams-modeling-dynamic-system-behavior

Ricciardi, A. (2025, January 27). *A Guide to UML sequence diagrams: notation, strengths, and Limitations*. Code Chronicles - Omega.py. https://www.alexomegapy.com/post/a-guide-to-uml-sequence-diagrams-notation-strengths-and-limitations

---

#### Assumptions

**ATM session scope**
-  The customer session begins when the ATM is ready (Idle) an the  customer introduces a card then the flow go to -> authentication -> withdrawal. The session ends when the customer removes the card or when the card is rejected as invalid card or after too many failed PIN attempts.

**Card validation**
- Card validation is Boolean -> validCard=false (invalid card) or validCard=true (valid card). Invalid cards are rejected and the session ends.

**PIN attempts and lockout**
- The attempt counter starts at 0 and is incremented before the authentication decision.
- Max_tries = 3 means the customer is allowed three failed attempts; the card is rejected when IsValidPin=false and attempt > 3 (the 4th failed attempt triggers lockout).

**Withdrawal amount validation**
- Withdrawal requests are whole-dollar amounts -> integers.
- If computedAmount = accountAmount - withdrawAmount is negative, the withdrawal is invalid/insufficient funds, and the customer is prompted to enter a new amount.

**Balance check and account closure**
- After dispensing cash, the account balance becomes the computed amount.
- If the new balance is 0, the account is closed (assignment requirement).
- If the new balance is greater than 0, the new balance is displayed and the session ends when the customer removes the card.

---

#### Project Map:
- atm_operations.py - This file contains the Python script that print all the steps in sequence 
for all the operations at an automated teller machine (ATM) shown in the "ATM State Machine UML Diagram.png" diagram.  
- Screetshoots Portfolio Module 8.pdf - This file contains the program console outputs
- ATM State Machine UML Diagram.png - This file contains ATM State diagram 
- CSC505 Lessons Learned Reflection Plan.docx - This file contains Lessons Learned Reflection, a summary that outlines the lessons I have learned in the course 
- README.md - this document contains notes and references
- utilities/ - utilities module containing utilities files (banner)
- Portfolio-Milestone-Module-4 - Directory containing the files of the Module 4 Milestone
- Portfolio-Milestone-Module-7 - Directory containing the files of the Module 7 Milestone
---

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

