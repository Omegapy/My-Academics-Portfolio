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

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

