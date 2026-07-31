-----------------------------------------------------------------------------------------------------------------------------
# Module 5 Critical Thinking 
Program Name: My Photo Gallery App

Grade: 100% A

-----------------------------------------------------------------------------------------------------------------------------

CSC475 – Platform-Based Development Android Course  
Professor: Herbert Pensado
Winter D (24WD) – 2025   
Student: Alexander (Alex) Ricciardi   
Date: 03/16/2025   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Kotlin
- Jetpack Compose 
- Gson
- Retrofit
- Pexels API Key

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

Option #1: "Photo Gallery"
Challenge: Build a photo gallery application that displays a grid of images fetched from the device's storage or an online source. Implement basic image loading and rendering functionalities, allowing users to view and scroll through a collection of photos.  
Please ensure that your submission includes the following components:
- Source code file(s) containing the program implementation.  
- A 1-page paper explaining the program's purpose, the obstacles faced during its development, and the skills acquired. The paper should also include screenshots showcasing the successful execution of the program.  
- Compile and submit your pseudocode, source code, and screenshots of the application executing the application, the results and GIT repository in a single document.  

-----------------------------------------------------------------------------------------------------------------------------

<img width="200" height="400" src="https://github.com/user-attachments/assets/e762d3cf-6156-421f-b914-c232dfb4f085">
<img width="200" height="400" src="https://github.com/user-attachments/assets/3f92b392-390d-4573-84f0-35b52369fadc">
<img width="200" height="400" src="https://github.com/user-attachments/assets/1318d45d-4c51-4141-a07a-a4871bd02fbe">

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

