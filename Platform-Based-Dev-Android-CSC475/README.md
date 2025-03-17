-----------------------------------------------------------------------------------------------------------------------------
# Platform-Based Development Android (Koltin) – CSC475  
-----------------------------------------------------------------------------------------------------------------------------

<img width="30" height="30" align="center" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"> Alexander Ricciardi (Omegapy)      

created date: 02/10/2025  

-----------------------------------------------------------------------------------------------------------------------------

Projects Description:    
This repository is a collection of simple Android Apps from CSC475 – Platform-Based Development Android Course at Colorado State University Global - CSU Global.  

-----------------------------------------------------------------------------------------------------------------------------

CSC475 – Platform-Based Development – Android Course    
Professor: Herbert Pensado
Winter D (24WD) – 2025   
Student: Alexander (Alex) Ricciardi   

Final grade:  

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Kotlin
- Jetpack Compose
- XML  

-----------------------------------------------------------------------------------------------------------------------------
My Links:   

<i><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></i>
<i><a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></i>
[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
<i><a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></i>
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)
<i><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></i>
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)  
   
-----------------------------------------------------------------------------------------------------------------------------

#### Project Map  

- [Module 5 Critical Thinking](#module-5-critical-thinking)
- [Module 4 Portfolio Milestone](#module-4-portfolio-milestone)  
- [Module 3 Critical Thinking](#module-3-critical-thinking)  
- [Module 2 Portfolio Milestone](#module-2-portfolio-milestone)  
- [Module 1 Critical Thinking](#module-1-critical-thinking)   
- [Discussions](#discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 5 Critical Thinking 
Directory: [Module-5-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Platform-Based-Dev-Android-CSC475/Module-5-Critical-Thinking)   
Title: Critical Thinking Assignment 5: My Photo Gallery App      

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

Option #1: "Photo Gallery"
Challenge: Build a photo gallery application that displays a grid of images fetched from the device's storage or an online source. Implement basic image loading and rendering functionalities, allowing users to view and scroll through a collection of photos.  
Please ensure that your submission includes the following components:
- Source code file(s) containing the program implementation.  
- A 1-page paper explaining the program's purpose, the obstacles faced during its development, and the skills acquired. The paper should also include screenshots showcasing the successful execution of the program.  
- Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and GIT repository in a single document.  

-----------------------------------------------------------------------------------------------------------------------------

<img width="100" height="200" src="https://github.com/user-attachments/assets/e762d3cf-6156-421f-b914-c232dfb4f085">
<img width="100" height="200" src="https://github.com/user-attachments/assets/3f92b392-390d-4573-84f0-35b52369fadc">
<img width="100" height="200" src="https://github.com/user-attachments/assets/1318d45d-4c51-4141-a07a-a4871bd02fbe">

-----------------------------------------------------------------------------------------------------------------------------

Program Description:

The program is a small Android application that allows a user to browse images from pexels.com (a website that provides free stock photos).
- When launched, the home page of the app displays a browsable list of curated professional photographs selected by Pexels.
- Search for specific images using keywords
- View detailed information about each photograph, including photographer credits
- The app User Interface (UI) follows Material Design principles

⚠️My notes:

The application is developed using Kotlin 2.0.21 and the following:
- Jetpack Compose (2.7.x): UI
- Retrofit (2.9.0): API communication
- OkHttp (4.11.0): HTTP client 
- Coil (2.50): For asynchronous image loading with Compose integration
- Kotlin Coroutines (1.7.3): 
- Navigation Compose (2.7.7): navigation between screens
- Material 3: Material Design components and theming

-----------------------------------------------------------------------------------------------------------------------------

Project Map:

- Module-5-CTA-MuPhotoGalery-App.docx (this file, App documentation)

The project used files from the Android Studio’s Empty View Activity template. Additionally, only the template files that were modified to accommodate the functionality of the application are listed below: 

<pre>myphotogallery_1/
 ├── AndroidManifest.xml
 ├── MainActivity.kt      # Main activity (VIEW)
 │                        # navigation and UI components
 │
 ├── data/                # MODEL LAYER
 │   │                    # data operations and business logic
 │   │
 │   ├── api/             # API service 
 │   │   └── PexelsApiService.kt  # API interface for Pexels API
 │   │                    # fetching photos
 │   │
 │   ├── model/           # Data model classes
 │   │   ├── Photo.kt     # Data class 
 │   │   │                # photo objects
 │   │   │
 │   │   └── PhotosResponse.kt  # API response data structure
 │   │                    # photo lists from API
 │   │
 │   ├── network/         # Network configuration
 │   │   └── NetworkModule.kt  # setup and API client
 │   │                         # Retrofit
 │   │
 │   └── repository/      # Repository layer - mediates between data sources and ViewModels
 │       ├── PhotoRepository.kt  # Repository interface
 │       │                       # data access methods
 │       │
 │       └── PhotoRepositoryImpl.kt   # Repository implementation
 │                                    # data access using API service
 │
 ├── ui/   # UI components (VIEW & VIEWMODEL)
 ├── components/    # UI components
 │   │   └── PhotoItem.kt # VIEW - photo card component
 │   │                    # individual photos in the grid
 │   │
 │   ├── navigation/  # Navigation components
 │   │   ├── AppNavHost.kt # VIEW - Navigation 
 │   │   │                # Manages navigation
 │   │   │
 │   │   └── NavRoute.kt  # VIEW - route definitions
 │   │                    # app's navigation paths
 │   │
 │   ├── screens/  # App screens (composables)
 │   │   ├── GalleryScreen.kt   # VIEW - gallery screen
 │   │   │                      # photo grid and search
 │   │   │
 │   │   └── PhotoDetailScreen.kt  # VIEW - Photo detail screen
 │   │                             # detailed view of a selected photo
 │   │
 │   ├── state/           # UI state definitions
 │   │   └── UiState.kt   # VIEWMODEL - UI state classes
 │   │                    # Loading, Success, Empty, Error states
 │   │
 │   ├── theme/           # UI theming
 │   │   └── Theme.kt     # VIEW - App theme 
 │   │                    # colors and shapes
 │   │
 │   └── viewmodel/       # ViewModels
 │       └── PhotoViewModel.kt  # VIEWMODEL - Photo manager
 │                              # state and user actions
 │
 └── util/                # Utility classes
      └── NetworkUtils.kt  # MODEL (utility) - Network connectivity 
                           # Checks if device has internet connection    </pre>

-----------------------------------------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  



-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 4 Portfolio Milestone 
Directory: [Module-4-Portfolio-Milestone](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Platform-Based-Dev-Android-CSC475/Module-4-Portfolio-Milestone)   
Title: Module-4 Portfolio Milestone: My Recipe App    

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

For your Portfolio Project you will develop an application in four stages, which will be covered in Modules 2, 4, 6, 8. The project can be of your choice, but here are some project ideas to consider:

- Social media aggregator app: Create an app that collects and displays posts from multiple social media platforms.  
- Fitness tracker app: Develop an app that tracks and analyzes users' fitness activities, including steps, calories, and distance.
- Recipe app: Design an app that provides a collection of recipes with search and favorite features.  
- Language learning app: Build an app that offers vocabulary exercises and quizzes for different languages.  
- Event planning app: Create an app to help users organize and manage events, including invitations and reminders.  

Design (Module 4): Deliver a document (2 pages) that provides the design details for the app. This includes the architecture, components, and overall layout of the user interface. Include wireframes or mockups to illustrate the app's design.

-----------------------------------------------------------------------------------------------------------------------------

Program Description:

- This document provides the design details for the app including the architecture, components, and overall layout of the User Interface.
- The app will be developed using Kotlin and Jetpack Compose, with plans for future integration of a Large Language Model (LLM) chatbot and the TheMealDB API to access and share recipe data.

-----------------------------------------------------------------------------------------------------------------------------
<img width="400" height="420" src="https://github.com/user-attachments/assets/a54a42fc-7cdc-4ea9-9d1c-3081582fa52b">

-----------------------------------------------------------------------------------------------------------------------------

Project Map:  
- Module-2 Milesone.pdf – Document about the requirements, UI/UX analysis, audience, and scope of an Android recipe app.

-----------------------------------------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 3 Critical Thinking 
Directory: [Module-3-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Platform-Based-Dev-Android-CSC475/Module-3-Critical-Thinking)   
Title: Critical Thinking Assignment 3: To Do List App      

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:  

Option #1: “To Do List”   
Challenge: Develop a to-do list application that allows users to add, delete, and mark tasks as completed. Implement data storage using SQLite database to store and retrieve the to-do items. Focus on understanding data persistence concepts in Android.

Please ensure that your submission includes the following components:

Source code file(s) containing the program implementation.
A 1-page paper explaining the program's purpose, the obstacles faced during its development, and the skills acquired. The paper should also include screenshots showcasing the successful execution of the program.
Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and GIT repository in a single document.

-----------------------------------------------------------------------------------------------------------------------------

<img width="100" height="200" src="https://github.com/user-attachments/assets/f3bf6bb7-3438-4d3b-af59-c53f9d9b7a0c">
<img width="100" height="200" src="https://github.com/user-attachments/assets/198d2ae2-81f5-465f-b0df-e827a1169199">
<img width="100" height="200" src="https://github.com/user-attachments/assets/2224f1b8-58f5-4b53-bfef-c9de2d5156a0">

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

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 2 Portfolio Milestone 
Directory: [Module-2-Portfolio-Milestone](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Platform-Based-Dev-Android-CSC475/Module-2-Portfolio-Milestone)   
Title: Module-2 Portfolio Milestone: Recipe App    

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:  

Portfolio Milestone (125 Points)
For your Portfolio Project you will develop an application in four stages, which will be covered in Modules 2, 4, 6, 8. The project can be of your choice, but here are some project ideas to consider:

Social media aggregator app: Create an app that collects and displays posts from multiple social media platforms.
Fitness tracker app: Develop an app that tracks and analyzes users' fitness activities, including steps, calories, and distance.
Recipe app: Design an app that provides a collection of recipes with search and favorite features.
Language learning app: Build an app that offers vocabulary exercises and quizzes for different languages.
Event planning app: Create an app to help users organize and manage events, including invitations and reminders.
The project should be completed in four parts, following agile methodology:

Requirements Gathering and Analysis (Module 2):  
Deliver a document (2 pages) that outlines the purpose and scope of the app. Identify the target audience and their needs. List the key features and functionalities of the app. Analyze any specific UI/UX requirements.

-----------------------------------------------------------------------------------------------------------------------------

Program Description:

This is a simple Hello Android Application written in Kotlin. It displays a simple animation where a TextView ("Hello Android!") bounces around within the screen's boundaries. It also provides a toggle button allowing the user to stop and restart the text animation.

- This project contains a document that describes the requirements, UI/UX analysis, audience, and scope of an Android recipe app. The app's scope is to provide access to meal recipes to a user through a UI system that includes view, search, add, modify, and favorite recipe functionalities. 
- The app will be developed using Kotlin and Jetpack Compose, with plans for future integration of a Large Language Model (LLM) chatbot and the TheMealDB API (n.d.) to access and share recipe data.
  
-----------------------------------------------------------------------------------------------------------------------------

Project Map:
- Module-2 Milesone.pdf – Document about the requirements, UI/UX analysis, audience, and scope of an Android recipe app.

-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Module 1 Critical Thinking 
Directory: [Module-1-Critical-Thinking](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Platform-Based-Dev-Android-CSC475/Module-1-Critical-Thinking)   
Title: Critical Thinking Assignment 1: Hello Android App   

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

Assignment Description:  

Option #1: "Hello Android" 
Create a simple Android application that displays a "Hello, Android!" message on the screen when launched. Familiarize yourself with the basic structure of an Android app and practice using Kotlin syntax.

Please ensure that your submission includes the following components:

Source code file(s) containing the program implementation.
A 1-page paper explaining the program's purpose, the obstacles faced during its development, and the skills acquired. The paper should also include screenshots showcasing the successful execution of the program.
Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and GIT repository in a single document.

-----------------------------------------------------------------------------------------------------------------------------

<img width="427" height="200" src="https://github.com/user-attachments/assets/3354f4fd-b43a-4bb3-bdbb-ee177fb65797"></span>
<img width="427" height="200" src="https://github.com/user-attachments/assets/2d941907-a20a-4965-90f1-6d88031e4fbc"></span>

Program Description:

This is a simple Hello Android Application written in Kotlin. It displays a simple animation where a TextView ("Hello Android!") bounces around within the screen's boundaries. It also provides a toggle button allowing the user to stop and restart the text animation.

⚠️Note:

- The program uses a background thread to run a text animation within an infinite loop.  
This loop updates the TextView's position and, when hitting a screen boundary the text bounces and changes color. This ‘hands-on’ animation approach is implemented for learning purposes, it is generally better and good practice to use Android API’s built‑in animation classes (like those in AnimationUtils).  

- To initialize the application, I used the Empty View Activity Template from Android Studio. Then I modify the file to implement the text animation and my own icon.  

-----------------------------------------------------------------------------------------------------------------------------

Project Map:

-	CTA1 Hello Android App.docx (this file, App documentation)
-	MainActivityPseudo.txt (Main Activity pseudocode)

The project used files from the Android Studio’s  Empty View Activity template. Additionally, only the template files that were modified to accommodate the functionality of the application are listed below: 

-	MainActivity.kt (Kotlin code, application logic)
-	Main_activity.xml (XML code, main UI layout)
-	Value
       - string.xml (resource file storing strings)

The following files have been overridden or modified to accommodate my icon. If you do not want to use my logo, do not use these files. The template will automatically use the Android icon.

-	Value
       - color.xml
       - theme.xml (this file was not modified or overridden, but it is part of the value folder)
-	drawable
       - ic_launcher_background.xml 
       - ic_launcher_foreground.xml 
-	mipmap-anydpi-v26
       - ic_launcher.xml 
       - ic_launcher_round.xml
-	mipmap folders (hdpi; mdpi; xhdpi; xxhdpi; xxxhdp – different variation of my icon)


-------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)  

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------
## Discussions 
This repository is a collection of discussion posts from CSC475 – Platform-Based Development – Android Course    
Directory: [Discussions](https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Platform-Based-Dev-Android-CSC475/Discussions)

-----------------------------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------------------------

[Go back to the Project Map](#project-map)


