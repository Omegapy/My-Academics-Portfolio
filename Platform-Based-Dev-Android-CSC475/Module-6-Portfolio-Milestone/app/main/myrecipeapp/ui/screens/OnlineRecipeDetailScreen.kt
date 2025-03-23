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
    This file contains the OnlineRecipeDetailScreen composable for displaying
    the details of online recipes
 */

package com.example.myrecipeapp.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.SnackbarHost
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.livedata.observeAsState
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.myrecipeapp.model.OnlineRecipe
import com.example.myrecipeapp.ui.navigation.AppFooter
import com.example.myrecipeapp.ui.components.AppHeader
import com.example.myrecipeapp.viewmodel.OnlineRecipeViewModel
import kotlinx.coroutines.launch
import androidx.compose.foundation.isSystemInDarkTheme

/**
 * Screen for viewing details of an online recipe
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun OnlineRecipeDetailScreen(
    recipeId: String,
    currentRoute: String,
    onBack: () -> Unit,
    onHome: () -> Unit,
    onSearch: () -> Unit,
    onAdd: () -> Unit,
    onMyRecipesClicked: () -> Unit = {},
    onFavoritesClicked: () -> Unit = {},
    onMealDbClicked: () -> Unit = {}
) {
    val viewModel: OnlineRecipeViewModel = viewModel()
    
    // States
    val recipe by viewModel.currentRecipe.observeAsState(initial = null as OnlineRecipe?)
    val isLoading by viewModel.isLoading.observeAsState(initial = false)
    val errorMessage by viewModel.error.observeAsState(initial = null as String?)
    
    // UI state
    val snackbarHostState = remember { SnackbarHostState() }
    val coroutineScope = rememberCoroutineScope()
    
    // Fetch recipe details
    LaunchedEffect(recipeId) {
        viewModel.getMealById(recipeId)
    }
    
    Scaffold(
        topBar = {
            AppHeader(
                onMenuClicked = { /* No menu action needed */ },
                onHomeClicked = onHome,
                onMyRecipesClicked = onMyRecipesClicked,
                onFavoritesClicked = onFavoritesClicked,
                onMealDbClicked = onMealDbClicked,
                onSearchClicked = onSearch
            )
        },
        bottomBar = {
            AppFooter(
                currentRoute = currentRoute,
                onHomeClick = onHome,
                onSearchClick = onSearch,
                onAddClick = onAdd
            )
        },
        floatingActionButton = {
            if (recipe != null) {
                FloatingActionButton(
                    onClick = {
                        // Save recipe to local collection
                        viewModel.saveRecipeToCollection()
                        coroutineScope.launch {
                            snackbarHostState.showSnackbar("Recipe saved to your collection")
                        }
                    },
                    containerColor = if (isSystemInDarkTheme()) 
                        Color(0xFF424242) // Dark grey color for dark mode
                    else 
                        Color(0xFF64B5F6) // Soft blue color for light mode
                ) {
                    Text(
                        "Save",
                        color = if (isSystemInDarkTheme()) Color.White else Color.Black
                    )
                }
            }
        },
        snackbarHost = { SnackbarHost(snackbarHostState) }
    ) { padding ->
        Box(
            modifier = Modifier
                .padding(padding)
                .fillMaxSize()
        ) {
            if (isLoading) {
                // Loading state
                CircularProgressIndicator(
                    modifier = Modifier.align(Alignment.Center)
                )
            } else if (errorMessage != null) {
                // Error state
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    Text(
                        text = "Error loading recipe",
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.error
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        text = errorMessage ?: "Unknown error",
                        style = MaterialTheme.typography.bodyMedium,
                        textAlign = TextAlign.Center
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Button(onClick = { viewModel.getMealById(recipeId) }) {
                        Text("Retry")
                    }
                }
            } else if (recipe != null) {
                // Recipe content
                val scrollState = rememberScrollState()
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(scrollState)
                        .padding(16.dp)
                ) {
                    // Recipe image
                    AsyncImage(
                        model = ImageRequest.Builder(LocalContext.current)
                            .data(recipe?.thumbnailUrl)
                            .crossfade(true)
                            .build(),
                        contentDescription = recipe?.name,
                        contentScale = ContentScale.FillWidth,
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(200.dp)
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))

                    //------------------------------------------------------

                    // Recipe metadata
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        Column {
                            Text(
                                text = recipe?.category ?: "",
                                style = MaterialTheme.typography.labelLarge
                            )
                            Text(
                                text = recipe?.area ?: "",
                                style = MaterialTheme.typography.labelMedium
                            )
                        }
                        
                        if (recipe?.tags?.isNotEmpty() == true) {
                            Text(
                                text = recipe?.tags ?: "",
                                style = MaterialTheme.typography.labelMedium,
                                fontStyle = FontStyle.Italic
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    Divider()
                    Spacer(modifier = Modifier.height(16.dp))

                    //------------------------------------------------------

                    // Ingredients section
                    Text(
                        text = "Ingredients",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    recipe?.let { currentRecipe ->
                        // Display ingredients from the recipe
                        currentRecipe.getIngredientsList().forEach { ingredient ->
                            Row(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(vertical = 4.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Text(
                                    text = "•",
                                    style = MaterialTheme.typography.bodyLarge,
                                    modifier = Modifier.width(16.dp)
                                )
                                Text(
                                    text = ingredient.getFormattedIngredient(),
                                    style = MaterialTheme.typography.bodyMedium
                                )
                            }
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    Divider()
                    Spacer(modifier = Modifier.height(16.dp))

                    //------------------------------------------------------

                    // Instructions section
                    Text(
                        text = "Instructions",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    Text(
                        text = recipe?.instructions ?: "",
                        style = MaterialTheme.typography.bodyMedium
                    )
                    
                    // Source information
                    if (!recipe?.source.isNullOrBlank()) {
                        Spacer(modifier = Modifier.height(24.dp))
                        Text(
                            text = "Source: ${recipe?.source}",
                            style = MaterialTheme.typography.bodySmall,
                            fontStyle = FontStyle.Italic
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                }
            } else {
                // Empty state
                Text(
                    text = "Recipe not found",
                    modifier = Modifier.align(Alignment.Center),
                    style = MaterialTheme.typography.titleMedium
                )
            }
        }
    }
} 
