-----------------------------------------------------------------------------------------------------------------------------
# Module 3 Critical Thinking 
Program Name: To Do List App

Grade: 100% A

-----------------------------------------------------------------------------------------------------------------------------

CSC475 – Platform-Based Development Android Course  
Professor: Herbert Pensado
Winter D (24WD) – 2025   
Student: Alexander (Alex) Ricciardi   
Date: 03/02/2025   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Kotlin
- Jetpack Compose 

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

Option #1: “To Do List”   
Challenge: Develop a to-do list application that allows users to add, delete, and mark tasks as completed. Implement data storage using SQLite database to store and retrieve the to-do items. Focus on understanding data persistence concepts in Android.

Please ensure that your submission includes the following components:

Source code file(s) containing the program implementation.
A 1-page paper explaining the program's purpose, the obstacles faced during its development, and the skills acquired. The paper should also include screenshots showcasing the successful execution of the program.
Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and GIT repository in a single document.

-----------------------------------------------------------------------------------------------------------------------------

<img width="200" height="400" src="https://github.com/user-attachments/assets/f3bf6bb7-3438-4d3b-af59-c53f9d9b7a0c">
<img width="200" height="400" src="https://github.com/user-attachments/assets/198d2ae2-81f5-465f-b0df-e827a1169199">
<img width="200" height="400" src="https://github.com/user-attachments/assets/2224f1b8-58f5-4b53-bfef-c9de2d5156a0">

-----------------------------------------------------------------------------------------------------------------------------

Program Description:

The program is a small Android application that allows the user to manage a to do list.  
- The app uses the Model-View-ViewModel (MVVM) architecture.
- The app uses Jetpack Compose to generate its UI.
- The user can add, delete, and complete tasks.
- The tasks are prioritized by relevance.
- The tasks can be displayed sorted by priority.
- The app uses SQLite to store task data.

⚠️My notes:

- I added a sort functionality allowing the user to display tasks by priorities from Urgent to Low.
- Methods to update tasks and update task priorities are added to the database backend operation, but not implemented in the front end, this needs to be implemented in the future version of the app.  

-----------------------------------------------------------------------------------------------------------------------------

Project Map:

-	Module 3 Critical Thinking Assignment.docx (App documentation)

The project used files from the Android Studio’s Empty View Activity template. Additionally, only the template files that were modified to accommodate the functionality of the application are listed below: 

<pre>
├── MainActivity.kt
├── model/                        # Model layer
│   └── Task.kt                      # Core data structures
├── data/                         # ViewModel layer
│   ├── TaskRepository.kt            # Data operations
│   ├── DatabaseInitializer.kt       # Database setup
│   └── database/                    # Database 
│       └── TaskDatabase.kt             # SQLite operations
└── ui/                           # View layer
    ├── screens/                     # Main screens
    │   └── TodoListScreen.kt           # Main task list screen
    ├── components/                  # UI components
    │   ├── TaskItem.kt                 # Individual task 
    │   └── AddTaskDialog.kt            # Task creation dialog
    └── theme/                       # UI styling
        ├── Theme.kt                    # Material theme 
        ├── Color.kt               
        └── Type.kt     </pre>

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

