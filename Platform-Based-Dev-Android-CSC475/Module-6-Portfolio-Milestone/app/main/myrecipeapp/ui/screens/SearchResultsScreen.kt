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
    This file contains the SearchResultsScreen composable which displays search results
*/

package com.example.myrecipeapp.ui.screens

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.ui.components.AppFooter
import com.example.myrecipeapp.ui.components.AppHeader
import com.example.myrecipeapp.ui.components.RecipeList
import com.example.myrecipeapp.viewmodel.SearchViewModel

/**
 * Displays search results for recipes based on provided search parameters
 * (my_recipes, favorite_recipes, mealdb)
 */
@Composable
fun SearchResultsScreen(
    sourceType: String,
    searchParams: String,
    onBackPressed: () -> Unit,
    onHomeClicked: () -> Unit,
    onSearchClicked: () -> Unit,
    onAddClicked: () -> Unit,
    onRecipeClicked: (Int) -> Unit,
    onMyRecipesClicked: () -> Unit = {},
    onFavoritesClicked: () -> Unit = {},
    onMealDbClicked: () -> Unit = {},
    currentRoute: String? = null,
    viewModel: SearchViewModel = viewModel()
) {
    // Parse search parameters
    var searchType by remember { mutableStateOf("") }
    var searchQuery by remember { mutableStateOf("") }
    var searchTitle by remember { mutableStateOf("Search Results") }
    
    // Collect state from ViewModel
    val searchResults by viewModel.searchResults.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()

    LaunchedEffect(sourceType, searchParams) {
        // Parse the search parameters
        if (searchParams.contains("=")) {
            val parts = searchParams.split("=")
            searchType = parts[0]
            searchQuery = parts[1]
            
            // Generate search title
            searchTitle = when (sourceType) {
                "my_recipes" -> "My Recipes"
                "favorite_recipes" -> "Favorite Recipes"
                "mealdb" -> "TheMealDB"
                else -> "Recipes"
            }
            searchTitle += " - $searchType: $searchQuery"
            
            // Call the ViewModel to perform the search
            viewModel.searchRecipes(sourceType, searchType, searchQuery)
        } else {
            // Handle when no search parameters are provided
            viewModel.clearResults()
            searchTitle = "No search parameters provided"
        }
    }

    Scaffold(
        topBar = {
            AppHeader(
                onMenuClicked = { /* Handle menu click */ },
                onHomeClicked = onHomeClicked,
                onMyRecipesClicked = onMyRecipesClicked,
                onFavoritesClicked = onFavoritesClicked,
                onMealDbClicked = onMealDbClicked,
                onSearchClicked = onSearchClicked
            )
        },
        bottomBar = {
            AppFooter(
                onHomeClicked = onHomeClicked,
                onSearchClicked = onSearchClicked,
                onAddClicked = onAddClicked,
                currentRoute = currentRoute
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(16.dp)
        ) {
            // Title and back button
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = searchTitle,
                    style = MaterialTheme.typography.titleMedium,
                    modifier = Modifier.weight(1f)
                )
                
                IconButton(onClick = onBackPressed) {
                    Icon(
                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                        contentDescription = "Back"
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))

            //--------------------------------------------------------

            // Content based on state
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                when {
                    isLoading -> {
                        CircularProgressIndicator()
                    }
                    error != null -> {
                        Text(
                            text = error ?: "Unknown error",
                            color = Color.Red,
                            style = MaterialTheme.typography.bodyMedium,
                            modifier = Modifier.padding(16.dp)
                        )
                    }
                    searchResults.isEmpty() -> {
                        Text(
                            text = "No recipes found for your search",
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.Gray
                        )
                    }
                    else -> {
                        // Display search results
                        RecipeList(
                            recipes = searchResults,
                            onRecipeClicked = onRecipeClicked,
                            modifier = Modifier.fillMaxSize(),
                            onFavoriteToggle = { recipe ->
                                viewModel.toggleFavorite(recipe)
                            }
                        )
                    }
                }
            }
        }
    }
}

//--------------------------------------------------------------------------------------------------

/**
 * Helper function to generate dummy recipe data for demonstration or testing purposes.
 * Creates a list of mock Recipe objects based on the provided search parameters.
 */
private fun generateDummyRecipes(sourceType: String, searchType: String, searchQuery: String): List<Recipe> {
    val dummyRecipes = mutableListOf<Recipe>()
    
    // Generate 5 dummy recipes with searchQuery in their name
    for (i in 1..5) {
        dummyRecipes.add(
            Recipe(
                id = i,
                name = "Recipe with $searchQuery $i",
                category = searchType,
                area = "Region $i",
                instructions = "This is a $searchType recipe for demonstration. Steps would go here...",
                ingredients = "ingredient1:measure1,ingredient2:measure2",
                thumbnailUrl = "",
                isFavorite = i % 2 == 0 // Alternate between favorite and not favorite
            )
        )
    }
    
    return dummyRecipes
} 
