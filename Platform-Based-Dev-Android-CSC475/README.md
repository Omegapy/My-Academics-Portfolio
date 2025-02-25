-----------------------------------------------------------------------------------------------------------------------------
# Platform-Based Development Android (Koltin, XML) – CSC475  
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

- [Module 2 Portfolio Milestone](#module-2-portfolio-milestone)  
- [Module 1 Critical Thinking](#module-1-critical-thinking)   
- [Discussions](#discussions)

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
Title: Critical Thinking Assignment 1:       

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


