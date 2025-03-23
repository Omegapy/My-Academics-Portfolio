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
==================================================================================================*/

/*
MVVM Architecture: VIEW
    This file contains the TheMealDbScreen composable for searching and displaying online recipes
 */

package com.example.myrecipeapp.ui.screens

import android.util.Log
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.GridItemSpan
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.lazy.grid.rememberLazyGridState
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Button
import androidx.compose.material3.Card
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.getValue
import androidx.compose.runtime.livedata.observeAsState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.myrecipeapp.model.OnlineRecipe
import com.example.myrecipeapp.viewmodel.OnlineRecipeViewModel
import kotlinx.coroutines.delay
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.foundation.isSystemInDarkTheme

/**
 * Screen for TheMealDB recipe search and display
 */
@Composable
fun TheMealDbScreen(
    currentRoute: String,
    onBack: () -> Unit,
    onHome: () -> Unit,
    onSearch: () -> Unit,
    onAdd: () -> Unit,
    onRecipeSelected: (String) -> Unit,
    onMyRecipesClicked: () -> Unit = {},
    onFavoritesClicked: () -> Unit = {},
    viewModel: OnlineRecipeViewModel = viewModel()
) {
    // Observe ViewModel states
    val searchResults by viewModel.searchResults.observeAsState(emptyList())
    val isLoading by viewModel.isLoading.observeAsState(false)
    val errorMessage by viewModel.error.observeAsState(null)
    val categories by viewModel.categories.observeAsState(emptyList())
    val areas by viewModel.areas.observeAsState(emptyList())
    val hasMoreResults by viewModel.hasMoreResults.observeAsState(false)
    
    var searchQuery by remember { mutableStateOf("") }
    var selectedSearchType by remember { mutableStateOf("Name") }
    
    // Add focus manager
    val focusManager = LocalFocusManager.current
    
    // Perform search when query or search type changes
    LaunchedEffect(searchQuery, selectedSearchType) {
        if (searchQuery.isNotEmpty()) {
            // For name searches, require at least 3 characters
            val minQueryLength = if (selectedSearchType == "Name") 3 else 1
            
            if (searchQuery.length >= minQueryLength) {
                // Small delay to avoid searching on every keystroke
                delay(300)
                
                // Add a log to debug search functionality
                Log.d("TheMealDbScreen", "Searching with type: $selectedSearchType, query: $searchQuery")
                
                when (selectedSearchType) {
                    "Name" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.NAME, true)
                    "Category" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.CATEGORY, true)
                    "Ingredient" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.INGREDIENT, true)
                    "Area" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.AREA, true)
                }
            } else if (selectedSearchType == "Name") {
                // Clear results if the query is too short for name searches
                viewModel.clearSearch()
            }
        } else {
            // Clear results when search query is empty
            viewModel.clearSearch()
        }
    }
    
    Scaffold(
        topBar = {
            // Common app header from components
            com.example.myrecipeapp.ui.components.AppHeader(
                onMenuClicked = { /* Menu actions */ },
                onHomeClicked = onHome,
                onMyRecipesClicked = onMyRecipesClicked,
                onFavoritesClicked = onFavoritesClicked,
                onMealDbClicked = { /* Already on this screen */ },
                onSearchClicked = onSearch
            )
        },
        bottomBar = {
            com.example.myrecipeapp.ui.components.AppFooter(
                onHomeClicked = onHome,
                onSearchClicked = onSearch,
                onAddClicked = onAdd,
                currentRoute = currentRoute
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
                .padding(horizontal = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Screen title and back button
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = "TheMealDB Recipes",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold
                )
                IconButton(onClick = onBack) {
                    Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                }
            }

            //-------------------------------------------------
            
            // Search box - similar to UnifiedSearchScreen
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                placeholder = { Text("Search by ${selectedSearchType.lowercase()}... (min. 3 letters)") },
                leadingIcon = { 
                    Icon(
                        Icons.Default.Search, 
                        contentDescription = "Search"
                    )
                },
                trailingIcon = {
                    if (searchQuery.isNotEmpty()) {
                        IconButton(onClick = { searchQuery = "" }) {
                            Icon(
                                Icons.Default.Clear,
                                contentDescription = "Clear"
                            )
                        }
                    }
                },
                singleLine = true,
                keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                keyboardActions = KeyboardActions(
                    onSearch = {
                        // Close keyboard on search
                        focusManager.clearFocus()
                    }
                )
            )

            //-------------------------------------------------
            
            // Info message about minimum search length
            if (searchQuery.length in 1..2) {
                Text(
                    text = "Please enter at least 3 letters for better search results",
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.padding(top = 4.dp)
                )
            }
            
            // Search by options - match the style used in UnifiedSearchScreen
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState())
                    .padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Filter options
                val searchOptions = listOf("Name", "Category", "Ingredient", "Area")
                
                searchOptions.forEach { option ->
                    FilterChip(
                        selected = selectedSearchType == option,
                        onClick = { 
                            selectedSearchType = option
                            if (searchQuery.isNotEmpty()) {
                                // Trigger search with new type
                                when (option) {
                                    "Name" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.NAME, true)
                                    "Category" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.CATEGORY, true)
                                    "Ingredient" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.INGREDIENT, true)
                                    "Area" -> viewModel.searchMeals(searchQuery, OnlineRecipeViewModel.SearchType.AREA, true)
                                }
                            }
                        },
                        label = { 
                            Text(
                                text = option,
                                style = MaterialTheme.typography.bodySmall
                            ) 
                        },
                        leadingIcon = if (selectedSearchType == option) {
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

            //-------------------------------------------------

            // Content display with infinite scroll or pagination
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f),
                contentAlignment = Alignment.Center
            ) {
                when {
                    isLoading && searchResults.isEmpty() -> CircularProgressIndicator()
                    errorMessage != null && searchResults.isEmpty() -> Text(errorMessage ?: "", color = androidx.compose.ui.graphics.Color.Red)
                    searchResults.isEmpty() -> {
                        Column(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center
                        ) {
                            Text(
                                text = "Search for recipes from TheMealDB",
                                style = MaterialTheme.typography.titleMedium,
                                textAlign = TextAlign.Center
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            if (selectedSearchType == "Random") {
                                Text(
                                    text = "Click the button below to get a random recipe",
                                    style = MaterialTheme.typography.bodyMedium,
                                    textAlign = TextAlign.Center
                                )
                            } else {
                                Text(
                                    text = "Start typing to search by ${selectedSearchType.lowercase()}",
                                    style = MaterialTheme.typography.bodyMedium,
                                    textAlign = TextAlign.Center
                                )
                            }
                            
                            Spacer(modifier = Modifier.height(24.dp))
                            Button(
                                onClick = { 
                                    viewModel.getRandomMeal()
                                    selectedSearchType = "Random"
                                },
                                modifier = Modifier.padding(top = 16.dp)
                            ) {
                                Icon(
                                    Icons.Default.Search, 
                                    contentDescription = "Random",
                                    modifier = Modifier.padding(end = 8.dp)
                                )
                                Text("Get Random Recipe")
                            }
                        }
                    }
                    else -> {
                        // Custom LazyVerticalGrid with pagination
                        val gridState = rememberLazyGridState()
                        
                        // Detect when scrolled to end to trigger loading more
                        val endReached by remember {
                            derivedStateOf {
                                val lastVisibleItem = gridState.layoutInfo.visibleItemsInfo.lastOrNull()
                                lastVisibleItem?.index != 0 && lastVisibleItem?.index == gridState.layoutInfo.totalItemsCount - 1
                            }
                        }
                        
                        // Load more when end reached
                        LaunchedEffect(endReached) {
                            if (endReached && hasMoreResults && !isLoading) {
                                when (selectedSearchType) {
                                    "Name" -> viewModel.loadMoreResults(OnlineRecipeViewModel.SearchType.NAME)
                                    "Category" -> viewModel.loadMoreResults(OnlineRecipeViewModel.SearchType.CATEGORY)
                                    "Ingredient" -> viewModel.loadMoreResults(OnlineRecipeViewModel.SearchType.INGREDIENT)
                                    "Area" -> viewModel.loadMoreResults(OnlineRecipeViewModel.SearchType.AREA)
                                }
                            }
                        }
                        
                        LazyVerticalGrid(
                            columns = GridCells.Adaptive(minSize = 160.dp),
                            contentPadding = PaddingValues(8.dp),
                            state = gridState,
                            modifier = Modifier.fillMaxSize()
                        ) {
                            items(searchResults) { recipe ->
                                OnlineRecipeCard(
                                    recipe = recipe,
                                    onClick = { onRecipeSelected(recipe.id) }
                                )
                            }
                            
                            // Add loading indicator at the end for pagination
                            if (hasMoreResults || isLoading) {
                                item(span = { GridItemSpan(maxLineSpan) }) {
                                    Box(
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .padding(16.dp),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        CircularProgressIndicator(
                                            modifier = Modifier.size(32.dp)
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

//--------------------------------------------------------------------------------------------------

/**
 * Card for displaying an online recipe
 */
@Composable
fun OnlineRecipeCard(
    recipe: OnlineRecipe,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .padding(8.dp)
            .fillMaxWidth()
            .clickable(onClick = onClick)
    ) {
        Column {
            // Recipe image with placeholder
            AsyncImage(
                model = ImageRequest.Builder(LocalContext.current)
                    .data(recipe.thumbnailUrl)
                    .crossfade(true)
                    .build(),
                contentDescription = recipe.name,
                contentScale = ContentScale.Crop,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(120.dp)
                    .clip(MaterialTheme.shapes.medium)
            )
            
            Column(modifier = Modifier.padding(8.dp)) {
                Text(
                    text = recipe.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                Text(
                    text = recipe.category,
                    style = MaterialTheme.typography.bodySmall
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                Text(
                    text = recipe.area,
                    style = MaterialTheme.typography.bodySmall
                )
            }
        }
    }
}

//--------------------------------------------------------------------------------------------------

/**
 * Gets the appropriate icon for the search type
 */
@Composable
private fun getIconForSearchType(searchType: OnlineRecipeViewModel.SearchType): ImageVector {
    return Icons.Default.Search
}

/**
 * Gets the appropriate label for the search type
 */
private fun getSearchLabel(searchType: OnlineRecipeViewModel.SearchType): String {
    return when (searchType) {
        OnlineRecipeViewModel.SearchType.NAME -> "Recipe Name"
        OnlineRecipeViewModel.SearchType.INGREDIENT -> "Main Ingredient"
        OnlineRecipeViewModel.SearchType.CATEGORY -> "Category"
        OnlineRecipeViewModel.SearchType.AREA -> "Country/Region"
    }
}

//-------------------------------------------------------------------------------------------------

/**
 * Performs the search based on the selected type
 */
private fun performSearch(
    viewModel: OnlineRecipeViewModel,
    searchType: OnlineRecipeViewModel.SearchType,
    query: String,
    category: String,
    area: String,
    ingredient: String
) {
    when (searchType) {
        OnlineRecipeViewModel.SearchType.NAME -> {
            if (query.isNotBlank()) {
                viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.NAME)
            }
        }
        OnlineRecipeViewModel.SearchType.CATEGORY -> {
            if (category.isNotBlank()) {
                viewModel.searchMeals(category, OnlineRecipeViewModel.SearchType.CATEGORY)
            } else if (query.isNotBlank()) {
                viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.CATEGORY)
            }
        }
        OnlineRecipeViewModel.SearchType.AREA -> {
            if (area.isNotBlank()) {
                viewModel.searchMeals(area, OnlineRecipeViewModel.SearchType.AREA)
            } else if (query.isNotBlank()) {
                viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.AREA)
            }
        }
        OnlineRecipeViewModel.SearchType.INGREDIENT -> {
            if (ingredient.isNotBlank()) {
                viewModel.searchMeals(ingredient, OnlineRecipeViewModel.SearchType.INGREDIENT)
            } else if (query.isNotBlank()) {
                viewModel.searchMeals(query, OnlineRecipeViewModel.SearchType.INGREDIENT)
            }
        }
    }
} 
