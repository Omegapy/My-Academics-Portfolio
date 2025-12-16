# Critical Thinking 5
Program Name: Critical Thinking Assignment 5 – PHTRS

Data:  12/14/2025  
Grade: 

---

CSC505 Principal of Software Development – Python Programming   
Professor: Dr. Joseph Issa  
Winter A (25WA) – 2025   
Student: Alexander (Alex) Ricciardi

---

**Program Description:**

Part of Write a Python Summary Script that:  
Defines the actors and use cases shown in your diagram
Prints out each actor and a brief description of their associated use cases  
Outputs a short textual summary of your diagram structure  

---

Requirements:  
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

---

**Assignment Directions:**  

The department of public works for a large city has decided to develop a web-based pothole tracking and repair system (PHTRS). A description follows:

Citizens can log onto a website and report the location and severity of potholes. As potholes are reported, they are logged within a "public works department repair system" and are assigned an identifying number. Potholes are stored by street address, size (on a scale of 1 to 10), location (e.g., middle of road, curb), district (determined from the address), and repair priority (determined from pothole size).

Work order data are associated with each pothole and include:

- Pothole location and size
- Repair crew identifying number
- Number of people on the crew
- Equipment assigned
- Hours applied to repair
- Hole status (work in progress, repaired, temporary repair, not repaired)
- Amount of filler material used
- Cost of repair (calculated based on time, labor, equipment, and materials)

A damage file is also maintained to record citizen-reported damages caused by potholes. This file includes:

- Citizen’s name, address, and phone number
- Type of damage (e.g., tire, alignment, body)
- Dollar amount of damage

PHTRS is an online system, and all interactions and queries are performed interactively through digital interfaces.


**Interface Examples and Assumptions:**

- Citizen Portal Interface: A web form with fields for street address, pothole size (slider or dropdown), pothole location (radio buttons), and optional image upload. Citizens may also have a dashboard to track the status of previously submitted reports or submit damage claims.
- Admin Interface: A secure login-based dashboard that allows authorized public works employees to view reported potholes, filter by district or priority, assign work crews, and update repair status.
- Repair Crew Mobile Interface: A tablet-optimized or mobile-responsive page allowing crews to log hours, update pothole repair status, and enter filler material used.
- Damage Claims Form: An online claims submission form that routes to the department's claims processing system with required fields for contact information, damage description, and evidence upload.
 
**Instructions:**

- Draw a UML Use Case Diagram
- Create a UML Use Case diagram that represents all major actors and their interactions with the PHTRS system. You’ll need to make assumptions about how users interact with the system based on the interfaces described above. Your diagram should include:
    - Actors such as Citizen, Public Works Admin, and Repair Crew
    - Use cases such as Report Pothole, Submit Damage Claim, Assign Repair Crew, Update Repair Status, and Generate Reports
- Use one of the following tools to create your diagram:
    - UMLetLinks to an external site.
    - GliffyLinks to an external site.
    - Microsoft Visio (if you already have access)
- Export your diagram as .png or .pdf.
- Write a Python Summary Script that:
    - Defines the actors and use cases shown in your diagram
    - Prints out each actor and a brief description of their associated use cases
    - Outputs a short textual summary of your diagram structure
Submission Requirements
- Submit the following in a zipped folder:
    - Your Python script (phtrs_summary.py)
    - A screenshot of successful script execution
    - Your UML diagram in .png or .pdf format
    - (Optional) A brief README.txt outlining your design assumptions
- Reference Requirements
Include at least two credible references in addition to the course textbook. Use the CSU Global Library (available in the left hand navigation menu) or professional sources on software design, UML, and civic technology systems. Format references in APA 7 according to the CSU Global Writing Center.
---

PHTRS - Use Case Diagram
<img width="2183" height="2809" alt="PHTRS - Use Case Diagram" src="https://github.com/user-attachments/assets/22edd637-4dbb-4476-97b2-5d16d9efa4c0" />

 
---

**Articles and tutorials used**
 
- IBM’s *Use-case diagrams* documentation (IBM, 2023) was used to learn the use-case diagram notation, such as how actors connect to use cases, and when to use the <<include>> and <<extend>> relationships.
- The OMG *UML specification (Version 2.5.1)* (OMG, 2017) was used to learn about UML relationships (association, generalization, include/extend).
- The PlantUML *Use case diagram* guide (PlantUML, n.d.) was used to learn about the diagram syntax (actors, system boundary, stereotypes, and relationships) and to verify correct rendering of the use-case model.
- The course textbook (Pressman & Maxim, 2020) was used to support requirements-level modeling decisions—keeping the diagram at the “what the system must do” level (actors/goals/interactions).
- Ricciardi’s (2025) prior UML use-case analysis article was used as a template for actors/use cases, explaining relationship choices, and it was used to populate the phtrs_summary.py summary output (tables + brief structure summary).
- The UML Diagrams *Component diagrams* tutorial (UML Diagrams, n.d.) was used as a UML reference to validate notation (naming, relationship functionalities).

---

**References**: 

IBM. (2023, September 21). *Use-case diagrams*. IBM Documentation.
https://www.ibm.com/docs/en/rational-soft-arch/9.7.0?topic=diagrams-use-case

OMG. (2017). *Unified Modeling Language (UML) specification (Version 2.5.1)*. Object Management Group
https://www.omg.org/spec/UML/2.5.1/

PlantUML. (n.d.). *Use case diagram*. PlantUML. https://plantuml.com/use-case-diagram

Pressman, R. S., & Maxim, B. R. (2020). Software engineering: A practitioner's approach (9th ed.). McGraw-Hill Education. 

Ricciardi, A. S. (2025, January 5). *A UML use-case analysis of an online shopping system: Actors, use cases, and relationships*. Omega.py. https://www.alexomegapy.com/post/a-uml-use-case-analysis-of-an-online-shopping-system-actors-use-cases-and-relationships

UML Diagrams. (n.d.). *UML component diagrams*. UML Diagrams. https://www.uml-diagrams.org/component-diagrams.html

---
**Assumptions**

System boundary  
PHTRS is a web-based system used by citizens to report the location of potholes, it also used by city empployes to fetch those reports (manage citizen damage claims) to prioritize, track, and close pothole repairs claims.

Core records (conceptual)
- Pothole record includes: street address, size (1–10), location-in-road, district,
  and repair priority derived from size (priority rules are simplified at the use-case level).
- Work order record includes: crew id, crew size, equipment, hours, status, material used,
  and a computed repair cost (exact cost formula is an implementation detail).
- Damage claim record includes citizen contact info, damage type, and claimed dollar amount.

External services
- A05-GIS/Address is an external service/system that can validate addresses and determine districts.
- A06-Notification is an external service/system that can be used to deliver notifications (email/SMS/in-app).

Authentication
- Staff roles authenticate (US00-Authenticate Staff User) before performing using system.
- Citizen actions can access a restricted part of system open to the public.

Reporting repository
- UC21-Representing storing and retrieving reports in the PHTRS report database (report records and supporting attachments) for validation, tracking, and processing.

Modeling Choices (Use-Case Relationships)
- <<include>> is used for required steps that always occur as part of a larger use case.
- <<extend>> is used for optional behavior that may occur under certain conditions.
- Generalization is used for actor inheritance: staff roles specialize A00-Staff User
  to reduce duplication and make role relationships explicit.

Actor Roles (High-level)
- A01-Citizen: reports potholes, optionally uploads evidence, and may submit a damage claim.
- A00-Staff User (abstract): parent role for staff accounts.
  - A02-Public Works Admin: triage/prioritize/assign/dispatch work; manages records.
  - A03-Repair Crew: updates work orders, status, materials, hours, and completion info.
  - A04-Claims Processor: reviews, validates, and resolves damage claims.
- A05-GIS/Address Service: supports address validation and district determination.
- A06-Notification Service: supports user/staff notifications.

Naming / Numbering Conventions
- Actors: A00..A## (A00 is abstract staff user)
- Use cases: UC01..UC21; Authentication is US00
- Relationship stereotypes follow PlantUML conventions: <<include>>, <<extend>>, and
  actor generalization.

---

**Project Map:**

- phtrs_summary.py - This file contains the PHTRS summarizer Python program 
- Screetshoots Module 5.pdf - This file contains the PHTRS summarizer Python program console outputs
- PHTRS - Use Case Diagram.png - This file contains the PHTRS use case diagram
- README.md - this document contains notes and references
- utilities/ - utilities module containing utilities files (banner)

---

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

