-----------------------------------------------------------------------------------------------------------------------------
# Critical Thinking 1
Program Name: Hello Android App

Grade: 100% A

-----------------------------------------------------------------------------------------------------------------------------

CSC475 – Platform-Based Development Android Course  
Professor: Herbert Pensado
Winter D (24WD) – 2025   
Student: Alexander (Alex) Ricciardi   
Date: 02/16/2025   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Kotlin
- XML  

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

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

