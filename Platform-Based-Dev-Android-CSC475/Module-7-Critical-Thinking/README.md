-----------------------------------------------------------------------------------------------------------------------------
# Module 7 Critical Thinking 
Program Name: Unit Converter Testing

Grade: 

-----------------------------------------------------------------------------------------------------------------------------

CSC475 – Platform-Based Development Android Course  
Professor: Herbert Pensado
Winter D (24WD) – 2025   
Student: Alexander (Alex) Ricciardi   
Date: 03/30/2025   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Kotlin
- Jetpack Compose 
- JUnit
- Hamcrest

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

Option #1: "Unit Converter Testing"  
Challenge: Create a unit conversion app that converts between different units (e.g., temperature, length, weight). Write and execute unit tests using the Android Testing Framework to ensure the accuracy of the conversion calculations.

Please ensure that your submission includes the following components:

- Source code file(s) containing the program implementation.
- A 1-page paper explaining the program's purpose, the obstacles faced during its development, and the skills acquired. The paper should also include screenshots showcasing the successful execution of the program.
- Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and GIT repository in a single document.  

-----------------------------------------------------------------------------------------------------------------------------

<img width="200" height="400" src="https://github.com/user-attachments/assets/3bb73b69-c2f7-452d-94f7-3fe8da4cd6ac">
<img width="200" height="400" src="https://github.com/user-attachments/assets/fd5c1cf7-3e0b-4353-8506-a5c8863a3b21">
<img width="200" height="400" src="https://github.com/user-attachments/assets/adf48891-e3f6-4ca2-8271-8b602d8febf0">
<img width="200" height="400" src="https://github.com/user-attachments/assets/782d4191-7213-4f83-abc3-916475f61382">
<img width="200" height="400" src="https://github.com/user-attachments/assets/7721f699-e70d-47f8-aec3-558138939895">

-----------------------------------------------------------------------------------------------------------------------------

Program Description:

The program is a small Android app that allows a user to convert
-	Temperatures from Celsius to Fahrenheit, and vice versa.
-	Length from meters to feet and from kilometers to miles, and vice versa.
-	Weight from kilograms to pounds, and vice versa. 
The app code also provides unit tests using the Android Testing Framework to ensure the accuracy of the conversion calculations. Note, this is the main goal of this project.

⚠️My notes:

The application is developed using Kotlin 2.0.21 and the following:
•	Jetpack Compose (composeBom = "2024.09.00"): UI
•	JUnit (4): API communication
•	Hamcrest (1.3)

-----------------------------------------------------------------------------------------------------------------------------

Project Map:

- Module-7-CTA-UnitCoverterTest-App.docx (this file, App documentation)
- index.html (Test report)

The project used files from the Android Studio’s Empty View Activity template. Additionally, only the template files that were modified to accommodate the functionality of the application are listed below: 

<pre>📁 UnitConverterTesting/
├── 📁 app/                         # Application module
│   ├── 📁 src/                     # Source code
│   │   ├── 📁 main/                # Main source code
│   │   │   ├── 📁 java/            # Java/Kotlin source code
│   │   │   │   └── 📁 com/example/unitconvertertesting/
│   │   │   │       ├── 📄 MainActivity.kt         # Main app activity with UI
│   │   │   │       ├── 📄 UnitConverter.kt        # Conversion logic
│   │   │   │       └── 📁 ui/theme/              # UI theme components
│   │   │   │           ├── 📄 Color.kt           # Color definitions
│   │   │   │           ├── 📄 Theme.kt           # Theme configurations
│   │   │   │           └── 📄 Type.kt            # Typography definitions
│   │   │   ├── 📁 res/             # Android resources
│   │   │   │   ├── 📁 drawable/     # Graphics/drawable resources
│   │   │   │   ├── 📁 mipmap-*/     # App icon resources (various densities)
│   │   │   │   ├── 📁 values/       # String, style and other resources
│   │   │   │   └── 📁 xml/          # XML configuration files
│   │   │   └── 📄 AndroidManifest.xml  # App manifest
│   │   │
│   │   ├── 📁 test/                # Unit tests
│   │   │   └── 📁 java/com/example/unitconvertertesting/
│   │   │       └── 📄 UnitConverterTest.kt       # Tests for conversion logic
</pre>

-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

