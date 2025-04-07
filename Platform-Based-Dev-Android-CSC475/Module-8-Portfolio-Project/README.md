-----------------------------------------------------------------------------------------------------------------------------
# Module 8 Portfolio Project
Program Name: My Recipe App  
Grade: 

CSC475 – Platform-Based Development Android Course  
Professor: Herbert Pensado  
Winter D (24WD) – 2025  
Student: Alexander (Alex) Ricciardi   
Date: 04/06/2025   

-----------------------------------------------------------------------------------------------------------------------------

Requirements:  
- Kotlin
- Android Environment 
- TheMealDB API key (themealdb.com)

-----------------------------------------------------------------------------------------------------------------------------

Assignment Directions:  

Portfolio Project (125 Points)
Review the Portfolio Project instructions in the Module 2: Portfolio Milestone. For this week's assignment, you are required to submit the Testing, Deployment, and Maintenance document. This final document should encompass the testing process, including details of any unit tests or UI tests that were conducted. Additionally, explain the deployment process of the app and address any challenges encountered during the deployment phase. Finally, discuss strategies for ongoing maintenance, bug fixes, and potential future enhancements for the app.

Please ensure that your paper adheres to APA guidelines, which can be found in the CSU Global Writing Center available in the left-hand navigation panel. The paper should be 2 pages long, excluding the references section.   

-----------------------------------------------------------------------------------------------------------------------------

Program Description:

The project contains the document (Module-8-Porfolio-Project.pdf) for my portfolio project module 8. It is the last step in developing my Android “My Recipe App.” This essay contains a description of the testing process, including details of unit tests and UI tests that were conducted. Additionally, it explains the deployment process of the app and addresses challenges encountered during the deployment phase. Finally, it discusses strategies for ongoing maintenance, bug fixes, and potential future enhancements for the app.
Note that the main source code is not available in this repository. I may add a link to the app repository to this README.md file when the app is finished. 

-----------------------------------------------------------------------------------------------------------------------------

<img width="200" height="400" src="https://github.com/user-attachments/assets/eebf0e41-5cad-4433-b1ce-a248445a76b4">
<img width="200" height="400" src="https://github.com/user-attachments/assets/791f786f-328c-4fd3-b1e3-c452a2a6b5b9">

<img width="200" height="400" src="https://github.com/user-attachments/assets/c21ff78d-a015-4cd1-9c75-3d84027ceb1e">
<img width="200" height="400" src="https://github.com/user-attachments/assets/fcc7543d-36a2-4323-8551-325e6794bcd8">

<img width="200" height="400" src="https://github.com/user-attachments/assets/c54a6559-e49b-460c-89ea-1fd070073059">
<img width="200" height="400" src="https://github.com/user-attachments/assets/6e958adf-3afc-4692-8298-66b8f7a2ec12">

<img width="200" height="400" src="https://github.com/user-attachments/assets/05e24bba-365d-4455-a083-3a177ad2eaba">
<img width="200" height="400" src="https://github.com/user-attachments/assets/dee3ed30-5203-485b-9263-a2bf764d89ff">

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

Testing 
- Jubit 4
- Hamcrest
- Robolectric
- UIAutomated
- Firebase

-----------------------------------------------------------------------------------------------------------------------------

Project Map:  
- Module-8-Porfolio-Project.pdf – Document about the app.  

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

⚠️ The following files are available in this repository  
Tests
<pre>
├── app  
│   ├── src  
│   │   ├── androidTest (-- Instrumentation/Integration Tests --)  
│   │   │   ├── AndroidManifest.xml (Test manifest configuration)  
│   │   │   └── java/com/example/myrecipeapp/  
│   │   │       ├── AppNavTest.kt (tests with complex testing scenarios)  
│   │   │       └── ui/  
│   │   │           └── screens/  
│   │   │               ├── RecipeListScreenTest.kt (recipe list screen interactions)  
│   │   │               └── RecipeFormScreenTest.kt (recipe form screen interactions)  
│   │   │
│   │   └── test (-- Unit Tests --)  
│   │       └── java/com/example/myrecipeapp/  
│   │           ├── viewmodel/ (-- VIEWMODEL LAYER TESTS --)  
│   │           │   ├── RecipeViewModelTest.kt (RecipeViewModel-lifecycle-LiveData)  
│   │           │   ├── TestRules.kt (JUnit rules for ViewModel testing)  
│   │           │   ├── OnlineRecipeViewModelTest.kt (OnlineRecipeViewModel- API)  
│   │           ├── util/  
│   │           │   ├── UtilityFunctionsTest.kt (utility functions in the app)  
│   │           │   ├── RecipeFilteringTest.kt (recipe filtering and sorting)  
│   │           │   ├── SimpleTest.kt (simple utility test)  
│   │           │   ├── TestHelper.kt (helper functions for tests)  
│   │           │   ├── ConvertersTest.kt (Room database TypeConverters)  
│   │           │   └── MainDispatcherRule.kt (Rule for testing coroutines)  
│   │           ├── repository/ (-- REPOSITORY LAYER TESTS --)  
│   │           │   ├── RepositoryTest.kt (repository CRUD operations)  
│   │           │   ├── CombinedRepositoryTest.kt (combined local/online repository)  
│   │           ├── api/ (-- API LAYER TESTS --)  
│   │           │   └── TheMealDbApiTest.kt (TheMealDB API client)  
│   │           └── database/ (-- DATABASE LAYER TESTS --)  
│   │               └── RecipeDatabaseTest.kt (Room database operations - migrations)  
</pre>


-----------------------------------------------------------------------------------------------------------------------------

My Links:   

<span><a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></span>    [![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)    [![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)    [![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)    <span><a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></span>    [![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)    [![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA) 

