/*==================================================================================================
    Program Name: My Photo Gallery App
    Author: Alexander Ricciardi
    Date: 03/17/2025

    Requirement:
         Jetpack Compose (2.7.x)
         Kotlin (2.0.21)
         AndroidX Core KTX (1.15.0): Kotlin extensions for core Android functionality
         Navigation Compose (2.7.7): Navigation between screens 
         Material 3: Material Design 3 components and theming system
         Room (2.6.1): Local database for storing recipes with SQLite abstraction
         Lifecycle Components (2.8.7): ViewModel and LiveData for MVVM architecture
         Retrofit (2.9.0): Type-safe HTTP client for API 
         Moshi (1.15.0): JSON parser for API 
         OkHttp (4.12.0): HTTP client and logging 
         Coil (2.5.0): Image loading library 
         Compose Runtime LiveData (1.6.2)
          Gson (2.10.1): JSON serialization/deserialization library
         Activity Compose (1.10.1): Compose integration with Activity
         Compose BOM: Bill of materials for consistent Compose dependencies

    Program Description:
         The app allows a user to access meal recipes. The recipes can be stored on the user's device and
          fetched from TheMealDB database using API calls. The UI system includes view, search, add, 
          modify, and favorite recipe functionalities.
==================================================================================================*/

/*
MVVM Architecture: VIEW
    This file handles navigation between different screens in the application
    flow between UI components
 */

package com.example.myrecipeapp.ui.navigation

import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.navArgument
import com.example.myrecipeapp.ui.screens.HomeScreen
import com.example.myrecipeapp.ui.screens.OnlineRecipeDetailScreen
import com.example.myrecipeapp.ui.screens.RecipeListScreen
import com.example.myrecipeapp.ui.screens.SearchDialog
import com.example.myrecipeapp.ui.screens.RecipeFormScreen
import com.example.myrecipeapp.ui.screens.TheMealDbScreen
import com.example.myrecipeapp.ui.screens.UnifiedSearchScreen
import com.example.myrecipeapp.ui.screens.SearchResultsScreen
import com.example.myrecipeapp.ui.screens.RecipeViewScreen

/**
 * Object containing all route definitions used for navigation
 */
object Routes {
    const val HOME = "home"
    const val MY_RECIPES = "my_recipes"
    const val FAVORITE_RECIPES = "favorite_recipes"
    const val MEALDB_RECIPES = "mealdb_recipes"
    const val ONLINE_RECIPE_DETAIL = "online_recipe/{recipeId}"
    const val ADD_RECIPE = "add_recipe"
    const val EDIT_RECIPE = "edit_recipe/{recipeId}"
    const val VIEW_RECIPE = "view_recipe/{recipeId}"
    const val SEARCH_RESULTS = "search_results/{searchType}/{query}"
    
    // Unified search screen routes
    const val UNIFIED_SEARCH = "unified_search/{sourceType}"
    
    /**
     * route for editing a specific recipe
     */
    fun editRecipe(recipeId: Int) = "edit_recipe/$recipeId"

    //-------------------------------------------------------------------

    /**
     * route for viewing a specific recipe
     *
     */
    fun viewRecipe(recipeId: Int) = "view_recipe/$recipeId"

    //-------------------------------------------------------------------

    /**
     * route for displaying details of an online recipe
     *
     */
    fun onlineRecipeDetail(recipeId: String) = "online_recipe/$recipeId"

    //-------------------------------------------------------------------
    
    /**
     * route for the unified search screen with a specific source type
     *
     */
    fun unifiedSearch(sourceType: String) = "unified_search/$sourceType"

    //-------------------------------------------------------------------
}

/**
 * Navigation graph for the entire application
 * Defines all possible screen destinations and the navigation between them
 * handles the search dialog state and navigation events
 *
 * @param navController The NavHostController that manages app navigation
 * @param modifier Optional Modifier for customizing the NavHost's appearance
 */
@Composable
fun AppNavHost(
    navController: NavHostController,
    modifier: Modifier = Modifier
) {
    // Get current back stack entry to determine current route
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route
    
    // State for search dialog
    var showSearchDialog by remember { mutableStateOf(false) }
    
    if (showSearchDialog) {
        SearchDialog(
            onDismiss = { showSearchDialog = false },
            onMyRecipesSearch = { sourceType ->
                showSearchDialog = false
                navController.navigate(Routes.unifiedSearch(sourceType))
            },
            onFavoriteRecipesSearch = { sourceType ->
                showSearchDialog = false
                navController.navigate(Routes.unifiedSearch(sourceType))
            },
            onMealDBSearch = {
                showSearchDialog = false
                navController.navigate(Routes.MEALDB_RECIPES)
            }
        )
    }
    
    NavHost(
        navController = navController,
        startDestination = Routes.HOME,
        modifier = modifier
    ) {

        //------------------------------------------------------------------

        // Home Screen
        composable(Routes.HOME) {
            HomeScreen(
                onMyRecipesClicked = { 
                    navController.navigate(Routes.MY_RECIPES) 
                },
                onFavoritesClicked = { 
                    navController.navigate(Routes.FAVORITE_RECIPES) 
                },
                onMealDbClicked = { 
                    navController.navigate(Routes.MEALDB_RECIPES) 
                },
                onMenuClicked = { 
                    // Handle menu action here
                },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { 
                    showSearchDialog = true
                },
                onAddClicked = { 
                    navController.navigate(Routes.ADD_RECIPE) 
                },
                onRecipeClicked = { recipe ->
                    navController.navigate(Routes.viewRecipe(recipe.id))
                },
                currentRoute = currentRoute
            )
        }

        //------------------------------------------------------------------
        
        // My Recipes Screen
        composable(Routes.MY_RECIPES) {
            RecipeListScreen(
                title = "My Recipes",
                searchType = "all",
                onRecipeClicked = { recipe ->
                    navController.navigate(Routes.viewRecipe(recipe.id))
                },
                onMenuClicked = { 
                    // Handle menu action here
                },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { 
                    showSearchDialog = true
                },
                onAddClicked = { 
                    navController.navigate(Routes.ADD_RECIPE) 
                },
                onMyRecipesClicked = { navController.navigate(Routes.MY_RECIPES) },
                onFavoritesClicked = { navController.navigate(Routes.FAVORITE_RECIPES) },
                onMealDbClicked = { navController.navigate(Routes.MEALDB_RECIPES) },
                currentRoute = currentRoute
            )
        }

        //------------------------------------------------------------------
        
        // Favorite Recipes Screen
        composable(Routes.FAVORITE_RECIPES) {
            RecipeListScreen(
                title = "My Favorite Recipes",
                searchType = "favorites",
                onRecipeClicked = { recipe ->
                    navController.navigate(Routes.viewRecipe(recipe.id))
                },
                onMenuClicked = { 
                    // Handle menu action here
                },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { 
                    showSearchDialog = true
                },
                onAddClicked = { 
                    navController.navigate(Routes.ADD_RECIPE) 
                },
                onMyRecipesClicked = { navController.navigate(Routes.MY_RECIPES) },
                onFavoritesClicked = { navController.navigate(Routes.FAVORITE_RECIPES) },
                onMealDbClicked = { navController.navigate(Routes.MEALDB_RECIPES) },
                currentRoute = currentRoute
            )
        }

        //------------------------------------------------------------------
        
        // MealDB Recipes Screen
        composable(Routes.MEALDB_RECIPES) {
            TheMealDbScreen(
                currentRoute = currentRoute ?: Routes.MEALDB_RECIPES,
                onBack = { 
                    navController.popBackStack()
                },
                onHome = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearch = { 
                    showSearchDialog = true
                },
                onAdd = { 
                    navController.navigate(Routes.ADD_RECIPE) 
                },
                onRecipeSelected = { recipeId ->
                    // Navigate to the online recipe detail screen
                    navController.navigate(Routes.onlineRecipeDetail(recipeId))
                },
                onMyRecipesClicked = { navController.navigate(Routes.MY_RECIPES) },
                onFavoritesClicked = { navController.navigate(Routes.FAVORITE_RECIPES) }
            )
        }

        //------------------------------------------------------------------
        
        // Online Recipe Detail Screen
        composable(
            route = Routes.ONLINE_RECIPE_DETAIL,
            arguments = listOf(navArgument("recipeId") { type = NavType.StringType })
        ) { backStackEntry ->
            val recipeId = backStackEntry.arguments?.getString("recipeId") ?: ""
            OnlineRecipeDetailScreen(
                recipeId = recipeId,
                currentRoute = currentRoute ?: Routes.MEALDB_RECIPES,
                onBack = { 
                    navController.popBackStack()
                },
                onHome = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearch = { 
                    showSearchDialog = true
                },
                onAdd = { 
                    navController.navigate(Routes.ADD_RECIPE) 
                },
                onMyRecipesClicked = { navController.navigate(Routes.MY_RECIPES) },
                onFavoritesClicked = { navController.navigate(Routes.FAVORITE_RECIPES) },
                onMealDbClicked = { navController.navigate(Routes.MEALDB_RECIPES) }
            )
        }

        //------------------------------------------------------------------
        
        // Add Recipe Screen
        composable(Routes.ADD_RECIPE) {
            RecipeFormScreen(
                onNavigateBack = { 
                    navController.popBackStack()
                },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { 
                    showSearchDialog = true
                },
                onAddClicked = { 
                    // No action needed since we're already on Add screen
                },
                currentRoute = currentRoute
            )
        }

        //------------------------------------------------------------------
        
        // Edit Recipe Screen
        composable(
            route = Routes.EDIT_RECIPE,
            arguments = listOf(navArgument("recipeId") { type = NavType.IntType })
        ) { backStackEntry ->
            val recipeId = backStackEntry.arguments?.getInt("recipeId") ?: 0
            RecipeFormScreen(
                recipeId = recipeId,
                onNavigateBack = { 
                    navController.popBackStack()
                },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { 
                    showSearchDialog = true
                },
                onAddClicked = { 
                    navController.navigate(Routes.ADD_RECIPE) 
                },
                currentRoute = currentRoute
            )
        }

        //------------------------------------------------------------------
        
        // View Recipe Screen
        composable(
            route = Routes.VIEW_RECIPE,
            arguments = listOf(navArgument("recipeId") { type = NavType.IntType })
        ) { backStackEntry ->
            val recipeId = backStackEntry.arguments?.getInt("recipeId") ?: 0
            RecipeViewScreen(
                recipeId = recipeId,
                onNavigateBack = { navController.popBackStack() },
                onNavigateToEdit = { recipeId -> 
                    navController.navigate(Routes.editRecipe(recipeId))
                },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { showSearchDialog = true },
                onAddClicked = { navController.navigate(Routes.ADD_RECIPE) },
                currentRoute = currentRoute
            )
        }

        //------------------------------------------------------------------
        
        // Search Results
        composable(
            route = Routes.SEARCH_RESULTS,
            arguments = listOf(
                navArgument("searchType") { type = NavType.StringType },
                navArgument("query") { type = NavType.StringType }
            )
        ) { backStackEntry ->
            val searchType = backStackEntry.arguments?.getString("searchType") ?: "all"
            val query = backStackEntry.arguments?.getString("query") ?: ""
            
            SearchResultsScreen(
                sourceType = searchType,
                searchParams = query,
                onBackPressed = { navController.popBackStack() },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { showSearchDialog = true },
                onAddClicked = { navController.navigate(Routes.ADD_RECIPE) },
                onRecipeClicked = { recipeId -> 
                    // In a real app, we'd navigate to the recipe detail
                    // For now, this is just a demo so we'll navigate back
                    navController.popBackStack()
                },
                onMyRecipesClicked = { navController.navigate(Routes.MY_RECIPES) },
                onFavoritesClicked = { navController.navigate(Routes.FAVORITE_RECIPES) },
                onMealDbClicked = { navController.navigate(Routes.MEALDB_RECIPES) },
                currentRoute = currentRoute
            )
        }

        //------------------------------------------------------------------
        
        // Unified Search Screen
        composable(
            route = Routes.UNIFIED_SEARCH,
            arguments = listOf(navArgument("sourceType") { type = NavType.StringType })
        ) { backStackEntry ->
            val sourceType = backStackEntry.arguments?.getString("sourceType") ?: "all"
            
            UnifiedSearchScreen(
                sourceType = sourceType,
                onBackPressed = { navController.popBackStack() },
                onHomeClicked = { 
                    navController.navigate(Routes.HOME) {
                        popUpTo(Routes.HOME) { inclusive = true }
                    }
                },
                onSearchClicked = { showSearchDialog = true },
                onAddClicked = { navController.navigate(Routes.ADD_RECIPE) },
                onRecipeClicked = { recipeId -> 
                    navController.navigate(Routes.editRecipe(recipeId))
                },
                onMyRecipesClicked = { navController.navigate(Routes.MY_RECIPES) },
                onFavoritesClicked = { navController.navigate(Routes.FAVORITE_RECIPES) },
                onMealDbClicked = { navController.navigate(Routes.MEALDB_RECIPES) },
                currentRoute = currentRoute
            )
        }
    }
}

