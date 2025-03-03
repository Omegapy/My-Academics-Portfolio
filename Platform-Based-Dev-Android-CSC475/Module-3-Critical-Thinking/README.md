-----------------------------------------------------------------------------------------------------------------------------
# Module 2 Critical Thinking 
Program Name: To Do List App

Grade: 

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

-	CTA1 To Do List App.docx (this file, App documentation)
-	ToDoListAppPseudo.txt (app pseudocode)

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

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

