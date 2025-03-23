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
         The app allows a user to access meal recipes. The recipes can be stored on the user\'s device and 
          fetched from TheMealDB database using API calls. The UI system includes view, search, add, 
          modify, and favorite recipe functionalities.

    MVVM Architecture: VIEW
    This file contains the UnifiedSearchScreen composable that combines local and online recipe search.
    Part of the View layer in MVVM architecture, providing an integrated search interface.
==================================================================================================*/

/*
MVVM Architecture: VIEW
    This file contains the UnifiedSearchScreen composable that combines local and online recipe search
 */

package com.example.myrecipeapp.ui.screens

import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
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
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.myrecipeapp.ui.components.AppFooter
import com.example.myrecipeapp.ui.components.RecipeList
import com.example.myrecipeapp.viewmodel.SearchViewModel
import kotlinx.coroutines.delay
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.verticalScroll

/**
 * A unified search interface that allows searching across different recipe collections
 * Provides real-time search results as the user types with filter options for search type
 * source types (my_recipes, favorite_recipes, mealdb)
 *
 * Features:
 * - Real-time search with debounce (300ms)
 * - Filter chips for different search types (Name, Category, Ingredient, Area)
 * - Clear search button
 * - Focus management for the search field
 * - Responsive feedback for search status
 *
 */
@Composable
fun UnifiedSearchScreen(
    sourceType: String,
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
    // Search state
    var searchQuery by remember { mutableStateOf("") }
    var searchTitle by remember { mutableStateOf("Search") }
    var selectedSearchType by remember { mutableStateOf("Name") }
    
    // Focus management
    val focusRequester = remember { FocusRequester() }
    val focusManager = LocalFocusManager.current
    
    // Collect state from ViewModel
    val searchResults by viewModel.searchResults.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val error by viewModel.error.collectAsState()
    
    // Set title based on sourceType
    LaunchedEffect(sourceType) {
        searchTitle = when (sourceType) {
            "my_recipes" -> "Search My Recipes"
            "favorite_recipes" -> "Search Favorite Recipes"
            "mealdb" -> "Search TheMealDB"
            else -> "Search Recipes"
        }
        
        // Request focus on the search field when the screen is shown
        focusRequester.requestFocus()
    }
    
    // Perform search as user types with debounce
    LaunchedEffect(searchQuery, selectedSearchType) {
        if (searchQuery.isNotEmpty()) {
            // Small delay to avoid searching on every keystroke
            delay(300)
            
            // Search with any length query
            viewModel.searchRecipes(sourceType, selectedSearchType, searchQuery)
        } else {
            viewModel.clearResults()
        }
    }

    Scaffold(
        topBar = {
            com.example.myrecipeapp.ui.components.AppHeader(
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
                .padding(horizontal = 12.dp)
        ) {
            // Title and back button
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 4.dp),
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
            
            // Single row search filters with horizontal scroll
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(vertical = 8.dp)
            ) {
                // Filter types without First Letter
                val searchTypes = listOf("Name", "Category", "Ingredient", "Area")
                
                searchTypes.forEach { searchType ->
                    FilterChip(
                        selected = selectedSearchType == when(searchType) {
                            "Ingredient" -> "Main Ingredient"
                            else -> searchType
                        },
                        onClick = { 
                            selectedSearchType = when(searchType) {
                                "Ingredient" -> "Main Ingredient"
                                else -> searchType
                            }
                            // Perform new search with current query
                            if (searchQuery.isNotEmpty()) {
                                viewModel.searchRecipes(sourceType, selectedSearchType, searchQuery)
                            }
                        },
                        label = { 
                            Text(
                                text = searchType,
                                style = MaterialTheme.typography.bodySmall,
                            )
                        },
                        leadingIcon = if (selectedSearchType == when(searchType) {
                            "Ingredient" -> "Main Ingredient"
                            else -> searchType
                        }) {
                            {
                                Icon(
                                    imageVector = Icons.Default.Check,
                                    contentDescription = "Selected",
                                    modifier = Modifier.size(16.dp)
                                )
                            }
                        } else null,
                        modifier = Modifier.padding(end = 8.dp, start = 4.dp),
                        shape = RoundedCornerShape(8.dp),
                        colors = FilterChipDefaults.filterChipColors(
                            containerColor = Color.LightGray.copy(alpha = 0.15f),
                            selectedContainerColor = Color.LightGray.copy(alpha = 0.3f),
                            selectedLabelColor = if (isSystemInDarkTheme()) Color.White else Color.Black,
                            selectedLeadingIconColor = if (isSystemInDarkTheme()) Color.White else Color.Black
                        )
                    )
                }
            }
            
            // Search field
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { newValue -> 
                    searchQuery = newValue
                },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp)
                    .focusRequester(focusRequester),
                placeholder = { Text("Search by ${selectedSearchType.lowercase()}...") },
                leadingIcon = { 
                    Icon(
                        imageVector = Icons.Default.Search,
                        contentDescription = "Search"
                    )
                },
                trailingIcon = {
                    if (searchQuery.isNotEmpty()) {
                        IconButton(onClick = { 
                            searchQuery = ""
                            viewModel.clearResults()
                        }) {
                            Icon(
                                imageVector = Icons.Default.Clear,
                                contentDescription = "Clear search"
                            )
                        }
                    }
                },
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(
                    onSearch = { focusManager.clearFocus() }
                ),
                shape = RoundedCornerShape(8.dp)
            )
            
            // Show category suggestions when Category is selected
            if (selectedSearchType == "Category") {
                // Fetch available categories when Category is selected
                LaunchedEffect(sourceType, selectedSearchType) {
                    viewModel.getAvailableCategories(sourceType)
                }
                
                // Get available categories
                val categories by viewModel.availableCategories.collectAsState()
                
                if (categories.isNotEmpty()) {
                    Text(
                        text = "Available Categories:",
                        style = MaterialTheme.typography.bodyMedium,
                        modifier = Modifier.padding(top = 8.dp, bottom = 4.dp)
                    )
                    
                    // Add a scrollable container with maximum height
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .heightIn(max = 200.dp) // Maximum height before scrolling
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(bottom = 8.dp)
                                // Make container scrollable if content exceeds max height
                                .verticalScroll(rememberScrollState())
                        ) {
                            // Group categories into rows of 3
                            val rows = categories.chunked(3)
                            
                            rows.forEach { rowCategories ->
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 4.dp, horizontal = 4.dp),
                                    horizontalArrangement = androidx.compose.foundation.layout.Arrangement.Start
                                ) {
                                    rowCategories.forEach { category ->
                                        FilterChip(
                                            selected = searchQuery == category,
                                            onClick = { 
                                                searchQuery = category
                                            },
                                            label = { 
                                                Text(
                                                    text = category,
                                                    style = MaterialTheme.typography.bodySmall,
                                                    textAlign = androidx.compose.ui.text.style.TextAlign.Center
                                                )
                                            },
                                            modifier = Modifier.padding(end = 8.dp),
                                            shape = RoundedCornerShape(8.dp),
                                            colors = FilterChipDefaults.filterChipColors(
                                                containerColor = Color.LightGray.copy(alpha = 0.15f),
                                                selectedContainerColor = Color.LightGray.copy(alpha = 0.3f),
                                                selectedLabelColor = if (isSystemInDarkTheme()) Color.White else Color.Black,
                                                selectedLeadingIconColor = if (isSystemInDarkTheme()) Color.White else Color.Black
                                            )
                                        )
                                    }
                                }
                            }
                        }
                    }
                    
                    // Add spacer to ensure separation from results
                    Spacer(modifier = Modifier.height(8.dp))
                }
            }
            
            HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
            
            // Results
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(bottom = 24.dp),
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
                    searchQuery.isEmpty() -> {
                        Text(
                            text = "Start typing to search recipes",
                            style = MaterialTheme.typography.bodyLarge,
                            color = Color.Gray
                        )
                    }
                    searchResults.isEmpty() -> {
                        Column(
                            modifier = Modifier.padding(16.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "No recipes found",
                                style = MaterialTheme.typography.bodyLarge,
                                color = Color.Gray
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = "Search type: $selectedSearchType",
                                style = MaterialTheme.typography.bodyMedium,
                                color = Color.Gray
                            )
                            Text(
                                text = "Query: \"$searchQuery\"",
                                style = MaterialTheme.typography.bodyMedium,
                                color = Color.Gray
                            )
                            Text(
                                text = "Source: ${
                                    when (sourceType) {
                                        "my_recipes" -> "My Recipes"
                                        "favorite_recipes" -> "Favorite Recipes"
                                        "mealdb" -> "TheMealDB"
                                        else -> sourceType
                                    }
                                }",
                                style = MaterialTheme.typography.bodyMedium,
                                color = Color.Gray
                            )
                        }
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
