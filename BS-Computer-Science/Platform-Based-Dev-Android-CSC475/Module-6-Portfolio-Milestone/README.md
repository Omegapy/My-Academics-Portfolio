-----------------------------------------------------------------------------------------------------------------------------
# Module 6 Portfolio Milestone
Program Name: My Recipe App

Grade: 100% A

-----------------------------------------------------------------------------------------------------------------------------

CSC475 – Platform-Based Development Android Course  
Professor: Herbert Pensado
Winter D (24WD) – 2025   
Student: Alexander (Alex) Ricciardi   
Date: 03/23/2025   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Kotlin
- Android Environment 
- TheMealDB API key (themealdb.com)

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

For your Portfolio Project you will develop an application in four stages, which will be covered in Modules 2, 4, 6, 8. The project can be of your choice, but here are some project ideas to consider:

- Social media aggregator app: Create an app that collects and displays posts from multiple social media platforms.  
- Fitness tracker app: Develop an app that tracks and analyzes users' fitness activities, including steps, calories, and distance.
- Recipe app: Design an app that provides a collection of recipes with search and favorite features.  
- Language learning app: Build an app that offers vocabulary exercises and quizzes for different languages.  
- Event planning app: Create an app to help users organize and manage events, including invitations and reminders.  

Implementation and Source Details (Module 6): This deliverable should contain the actual implementation of the app along with source code details, including screenshots to showcase the app's functionality and appearance. Explain any challenges faced during implementation and how they were overcome.

-----------------------------------------------------------------------------------------------------------------------------

Program Description:

The project contains the document (Module-6-Milestone.pdf) for my portfolio milestone module 6. It is the second step in developing my Android “My Recipe App.” The app allows a user to access meal recipes. The recipes can be stored on the user's device and fetched from TheMealDB (n.d.a) database using API calls. The UI system includes view, search, add, modify, and favorite recipe functionalities. The app is being developed using Kotlin, Jetpack Compose, and the Model-View-ViewModel (MVVM) architecture. This document provides the design details for the app including the architecture, components, and overall layout of the User Interface.

Note that the source code is not available in this repository, I may add a link to the app repository to this README.md file when the app is finished. 

-----------------------------------------------------------------------------------------------------------------------------

<img width="200" height="400" src="https://github.com/user-attachments/assets/eebf0e41-5cad-4433-b1ce-a248445a76b4">
<img width="200" height="400" src="https://github.com/user-attachments/assets/791f786f-328c-4fd3-b1e3-c452a2a6b5b9">

<img width="200" height="400" src="https://github.com/user-attachments/assets/c21ff78d-a015-4cd1-9c75-3d84027ceb1e">
<img width="200" height="400" src="https://github.com/user-attachments/assets/fcc7543d-36a2-4323-8551-325e6794bcd8">

<img width="200" height="400" src="https://github.com/user-attachments/assets/c54a6559-e49b-460c-89ea-1fd070073059">
<img width="200" height="400" src="https://github.com/user-attachments/assets/6e958adf-3afc-4692-8298-66b8f7a2ec12">

<img width="200" height="400" src="https://github.com/user-attachments/assets/05e24bba-365d-4455-a083-3a177ad2eaba">
<img width="200" height="400" src="https://github.com/user-attachments/assets/dee3ed30-5203-485b-9263-a2bf764d89ff">

<br>
<img width="600" height="400" src="https://github.com/user-attachments/assets/8313feca-793d-468d-be3f-4dc475112a20">

-----------------------------------------------------------------------------------------------------------------------------

App Requirements:

- Jetpack Compose (2.7.x)
- Kotlin (2.0.21)
- AndroidX Core KTX (1.15.0): Kotlin extensions for core Android functionality
- Navigation Compose (2.7.7): Navigation between screens 
- Material 3: Material Design 3 components and theming system
- Room (2.6.1): Local database for storing recipes with SQLite abstraction
- Lifecycle Components (2.8.7): ViewModel and LiveData for MVVM architecture
- Retrofit (2.9.0): Type-safe HTTP client for API 
- Moshi (1.15.0): JSON parser for API 
- OkHttp (4.12.0): HTTP client and logging 
- Coil (2.5.0): Image loading library 
- Compose Runtime LiveData (1.6.2)
- Gson (2.10.1): JSON serialization/deserialization library
- Activity Compose (1.10.1): Compose integration with Activity
- Compose BOM: Bill of materials for consistent Compose dependencies
- TheMealDB API key (themealdb.com)

-----------------------------------------------------------------------------------------------------------------------------

Project Map:  
- Module-6 Milesone.pdf – Document about the app.  

⚠️ The following files are not available in this repository
<pre>
├── app
│   ├── main
│   │   ├── AndroidManifest.xml (configuration, permissions, components declaration)
│   │   ├── myrecipapp
│   │   │   ├── MainActivity.kt (Main activity)
│   │   │   ├── RecipeApplication.kt (Application class for initialization)
│   │   │   ├── data/ 
│   │   │   │   └── api/ (-- MODEL LAYER --)
│   │   │   │       ├── MealDbApiResponse.kt (Data classes for JSON from TheMealDB)
│   │   │   │       └── TheMealDbService.kt (Retrofit service interface for API calls)
│   │   │   ├── model/ (-- MODEL LAYER --)
│   │   │   │   ├── Category.kt (Data class for recipe categories)
│   │   │   │   ├── Converters.kt (Type converters for Room database objects)
│   │   │   │   ├── Ingredient.kt (Data class for recipe ingredients)
│   │   │   │   ├── OnlineRecipe.kt (Data class for recipes from TheMealDB)
│   │   │   │   ├── Recipe.kt (Main data class for recipe, stored locally)
│   │   │   │   ├── RecipeDao.kt (Data Access Object for Room database operations)
│   │   │   │   └── RecipeDatabase.kt (Room database configuration and setup)
│   │   │   ├── repository/ (Repository layer)
│   │   │   │   ├── LocalRecipeRepository.kt (local database operations)
│   │   │   │   ├── OnlineMealRepository.kt (TheMealDB API operations)
│   │   │   │   └── RecipeRepository.kt (Interface for repository functionality)
│   │   │   ├── ui/ (-- VIEW LAYER --)
│   │   │   │   ├── components/
│   │   │   │   │   ├── CommonComponents.kt (UI components like headers/footers)
│   │   │   │   │   └── RecipeComponents.kt (Recipe-specific UI components)
│   │   │   │   ├── navigation/
│   │   │   │   │   ├── AppFooter.kt (Bottom navigation bar component)
│   │   │   │   │   └── Navigation.kt (Navigation graph and route definitions)
│   │   │   │   ├── screens/
│   │   │   │   │   ├── HomeScreen.kt (Main app home screen with recent recipes)
│   │   │   │   │   ├── OnlineRecipeDetailScreen.kt (Detail recipe for online recipes)
│   │   │   │   │   ├── PlaceholderScreen.kt (placeholder for unimplemented features)
│   │   │   │   │   ├── RecipeFormScreen.kt (Form/screen for adding/editing recipes)
│   │   │   │   │   ├── RecipeListScreen.kt (List recipe of all saved recipes)
│   │   │   │   │   ├── RecipeViewScreen.kt (Detailed recipe of a single recipe)
│   │   │   │   │   ├── SearchDialog.kt (Dialog for search)
│   │   │   │   │   ├── SearchResultsScreen.kt (Display of search results)
│   │   │   │   │   ├── SearchScreens.kt (search screen implementations)
│   │   │   │   │   ├── TheMealDbScreen.kt (Screen for searching TheMealDB recipes)
│   │   │   │   │   └── UnifiedSearchScreen.kt (Combined search)
│   │   │   │   ├── theme/
│   │   │   │       ├── Color.kt (Color for the app)
│   │   │   │       ├── Theme.kt (Theme including dark/light modes)
│   │   │   │       └── Type.kt (Typography definitions)
│   │   │   └── viewmodel/ (-- VIEWMODEL Layer --)
│   │   │       ├── OnlineRecipeViewModel.kt (ViewModel for TheMealDB recipes)
│   │   │       ├── RecipeViewModel.kt (ViewModel for local recipe operations)
│   │   │       └── SearchViewModel.kt (ViewModel for search functionality)
│   │   └── res/
│   │       ├── drawable/
│   │       │   └── ic_launcher_background.xml (App icon background vector)
│   │       ├── mipmap-*/
│   │       │   └── (App icon resources at different resolutions)
│   │       ├── values/
│   │       │   └── colors.xml (Color for light theme)
│   │       ├── values-night/
│   │       │   └── colors.xml (Color for dark theme)
│   │       └── xml/ (Additional XML configuration files)

</pre>


-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

