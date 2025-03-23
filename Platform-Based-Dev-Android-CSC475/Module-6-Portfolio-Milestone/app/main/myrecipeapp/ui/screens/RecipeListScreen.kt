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
   This file contains the RecipeListScreen composable which displays a list of recipes
   renders UI based on data given by the ViewModel
*/

package com.example.myrecipeapp.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.myrecipeapp.R
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.ui.components.AppFooter
import com.example.myrecipeapp.ui.components.AppHeader
import com.example.myrecipeapp.viewmodel.RecipeViewModel

/**
 * Displays a list of recipes
 */
@Composable
fun RecipeListScreen(
    title: String,
    searchType: String = "all", // "all", "favorites", or "search"
    initialQuery: String = "",
    onRecipeClicked: (Recipe) -> Unit = {},
    onMenuClicked: () -> Unit = {},
    onHomeClicked: () -> Unit = {},
    onSearchClicked: () -> Unit = {},
    onAddClicked: () -> Unit = {},
    onMyRecipesClicked: () -> Unit = {},
    onFavoritesClicked: () -> Unit = {},
    onMealDbClicked: () -> Unit = {},
    currentRoute: String? = null,
    viewModel: RecipeViewModel = viewModel()
) {
    // State for search query
    val cleanedInitialQuery = initialQuery.trim()
    var searchQuery by remember { mutableStateOf(cleanedInitialQuery) }
    
    // Recipe list state
    val allRecipes by when (searchType) {
        "favorites" -> viewModel.favoriteRecipes.collectAsState(initial = emptyList())
        else -> viewModel.recipes.collectAsState(initial = emptyList())
    }
    
    // State for recipe to delete confirmation
    var recipeToDelete by remember { mutableStateOf<Recipe?>(null) }
    
    // Filtered recipes for display
    val displayedRecipes = when {
        searchType == "favorites" -> allRecipes.filter { it.isFavorite }
        searchQuery.isNotBlank() -> allRecipes.filter { 
            it.name.contains(searchQuery, ignoreCase = true) ||
            it.category.contains(searchQuery, ignoreCase = true) ||
            it.area.contains(searchQuery, ignoreCase = true)
        }
        else -> allRecipes
    }
    
    // Focus manager for clearing keyboard focus
    val focusManager = LocalFocusManager.current
    
    // Delete confirmation dialog
    recipeToDelete?.let { recipe ->
        DeleteConfirmationDialog(
            recipe = recipe,
            onConfirm = {
                viewModel.deleteRecipe(recipe)
                recipeToDelete = null
            },
            onDismiss = {
                recipeToDelete = null
            }
        )
    }
    
    Scaffold(
        topBar = {
            AppHeader(
                onMenuClicked = onMenuClicked,
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
        ) {
            // Title row with search toggle
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 16.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.headlineMedium
                )
                
                IconButton(onClick = {
                    if (searchQuery.isNotBlank()) {
                        searchQuery = ""
                    }
                    onSearchClicked()
                }) {
                    Icon(
                        imageVector = if (searchQuery.isBlank()) Icons.Default.Search else Icons.Default.Clear,
                        contentDescription = if (searchQuery.isBlank()) "Search" else "Clear search"
                    )
                }
            }

            //--------------------------------------------------------
            
            // Search bar (visible if initialQuery is not empty or user is in search mode)
            if (searchType == "search" || cleanedInitialQuery.isNotBlank()) {
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    label = { Text("Search recipes") },
                    placeholder = { Text("Enter search term") },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search") },
                    trailingIcon = {
                        if (searchQuery.isNotBlank()) {
                            IconButton(onClick = { searchQuery = "" }) {
                                Icon(Icons.Default.Clear, contentDescription = "Clear search")
                            }
                        }
                    },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                    keyboardActions = KeyboardActions(
                        onSearch = { focusManager.clearFocus() }
                    )
                )
            }

            //--------------------------------------------------------
            
            // Recipe list
            if (displayedRecipes.isEmpty()) {
                // Empty state
                Box(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = if (searchQuery.isBlank()) 
                            "No recipes available. Add a new recipe to get started." 
                        else 
                            "No recipes found matching \"$searchQuery\"",
                        style = MaterialTheme.typography.bodyLarge,
                        textAlign = TextAlign.Center,
                        modifier = Modifier.padding(16.dp)
                    )
                }
            } else {
                // List of recipes
                LazyColumn(
                    modifier = Modifier
                        .weight(1f)
                        .fillMaxWidth(),
                    contentPadding = PaddingValues(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(displayedRecipes) { recipe ->
                        RecipeCard(
                            recipe = recipe,
                            onRecipeClicked = onRecipeClicked,
                            onToggleFavorite = { viewModel.toggleFavorite(recipe) },
                            onDeleteClicked = { recipeToDelete = it }
                        )
                    }
                }
            }
        }
    }
}

//-------------------------------------------------------------------------------------------------

/**
 * Renders a single recipe card with thumbnail, details, and action buttons
 */
@Composable
fun RecipeCard(
    recipe: Recipe,
    onRecipeClicked: (Recipe) -> Unit,
    onToggleFavorite: () -> Unit,
    onDeleteClicked: (Recipe) -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { onRecipeClicked(recipe) },
        shape = RoundedCornerShape(8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .height(120.dp)
        ) {
            // Recipe thumbnail
            Box(
                modifier = Modifier
                    .width(120.dp)
                    .fillMaxHeight()
                    .background(Color.LightGray)
            ) {
                if (recipe.thumbnailUrl.isNotEmpty() && !recipe.thumbnailUrl.contains("drawable")) {
                    // Load from URL if available
                    AsyncImage(
                        model = ImageRequest.Builder(LocalContext.current)
                            .data(recipe.thumbnailUrl)
                            .crossfade(true)
                            .build(),
                        contentDescription = recipe.name,
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                } else {
                    // Fallback to default image
                    Image(
                        painter = painterResource(id = R.drawable.thumbnails_main_recipe_pic),
                        contentDescription = recipe.name,
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                }
            }
            
            // Recipe details
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(16.dp)
            ) {
                Text(
                    text = recipe.name,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                Row(
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = recipe.category,
                            style = MaterialTheme.typography.bodySmall
                        )
                        
                        Text(
                            text = recipe.area,
                            style = MaterialTheme.typography.bodySmall
                        )
                    }
                    
                    // Actions row
                    Row {
                        // Delete button
                        IconButton(
                            onClick = { onDeleteClicked(recipe) },
                            modifier = Modifier.size(32.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Delete,
                                contentDescription = "Delete Recipe",
                                tint = Color.Gray
                            )
                        }
                        
                        // Favorite button
                        IconButton(
                            onClick = onToggleFavorite,
                            modifier = Modifier.size(32.dp)
                        ) {
                            Icon(
                                imageVector = if (recipe.isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                                contentDescription = if (recipe.isFavorite) "Remove from favorites" else "Add to favorites",
                                tint = if (recipe.isFavorite) Color(0xFFE91E63) else Color.Gray
                            )
                        }
                    }
                }
            }
        }
    }
}

//-------------------------------------------------------------------------------------------------

/**
 * Displays a confirmation dialog when deleting a recipe
 */
@Composable
fun DeleteConfirmationDialog(
    recipe: Recipe,
    onConfirm: () -> Unit,
    onDismiss: () -> Unit
) {
    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Delete Recipe") },
        text = { Text("Are you sure you want to delete '${recipe.name}'? This action cannot be undone.") },
        confirmButton = {
            Button(
                onClick = onConfirm,
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Red,
                    contentColor = Color.White
                )
            ) {
                Text("Delete")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
} 
