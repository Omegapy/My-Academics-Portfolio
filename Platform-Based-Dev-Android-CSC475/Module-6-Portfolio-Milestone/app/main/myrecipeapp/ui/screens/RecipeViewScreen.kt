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
    This file contains the RecipeViewScreen composable which displays recipe details to the user
*/

package com.example.myrecipeapp.ui.screens

import android.net.Uri
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Create
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.Divider
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.myrecipeapp.R
import com.example.myrecipeapp.ui.components.AppFooter
import com.example.myrecipeapp.viewmodel.RecipeViewModel
import java.io.File

@OptIn(ExperimentalMaterial3Api::class)
/**
 * Displays detailed information about a recipe in read-only mode
 * recipe thumbnail, name, category, ingredients, and step-by-step instructions.
 * options to toggle favorite status and navigate to edit mode
 *
 * @param recipeId ID of the recipe to display
 * @param onNavigateBack Callback for navigating back to previous screen
 * @param onNavigateToEdit Callback for navigating to edit screen
 * @param onHomeClicked Callback for navigating to home screen
 * @param onSearchClicked Callback for opening search
 * @param onAddClicked Callback for navigating to add recipe screen
 * @param currentRoute Current navigation route
 * @param viewModel ViewModel for accessing recipe data

 */
@Composable
fun RecipeViewScreen(
    recipeId: Int,
    onNavigateBack: () -> Unit,
    onNavigateToEdit: (Int) -> Unit,
    onHomeClicked: () -> Unit,
    onSearchClicked: () -> Unit,
    onAddClicked: () -> Unit,
    currentRoute: String? = null,
    viewModel: RecipeViewModel = viewModel()
) {
    // Load recipe data
    LaunchedEffect(recipeId) {
        viewModel.getRecipeById(recipeId)
    }
    
    // Get current recipe
    val recipe by viewModel.currentRecipe.collectAsState()
    val context = LocalContext.current
    
    Scaffold(
        topBar = {
            TopAppBar(
                title = { 
                    Text(
                        "Recipe Details",
                        color = if (isSystemInDarkTheme()) Color.White else MaterialTheme.colorScheme.onSurface
                    )
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(
                            Icons.Default.ArrowBack, 
                            contentDescription = "Back",
                            tint = if (isSystemInDarkTheme()) Color.White else MaterialTheme.colorScheme.onSurface
                        )
                    }
                },
                actions = {
                    // Toggle favorite button
                    IconButton(
                        onClick = { 
                            recipe?.let { 
                                viewModel.toggleFavorite(it)
                                // Force refresh the recipe to update UI
                                viewModel.getRecipeById(it.id)
                            }
                        }
                    ) {
                        Icon(
                            imageVector = if (recipe?.isFavorite == true) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                            contentDescription = if (recipe?.isFavorite == true) "Remove from favorites" else "Add to favorites",
                            tint = if (recipe?.isFavorite == true) Color(0xFFE91E63) else MaterialTheme.colorScheme.onSurfaceVariant
                        )
                    }

                    //------------------------------------------------------------

                    // Edit button
                    IconButton(
                        onClick = { recipe?.let { onNavigateToEdit(it.id) } }
                    ) {
                        Icon(
                            imageVector = Icons.Default.Edit,
                            contentDescription = "Edit Recipe",
                            tint = if (isSystemInDarkTheme()) Color.White else MaterialTheme.colorScheme.onSurface
                        )
                    }
                }
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
                .verticalScroll(rememberScrollState()),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Recipe doesn't exist or hasn't loaded yet
            if (recipe == null) {
                Text(
                    text = "Recipe not found",
                    style = MaterialTheme.typography.titleLarge
                )
                return@Column
            }
            
            recipe?.let { currentRecipe ->
                // Recipe name
                Text(
                    text = currentRecipe.name,
                    style = MaterialTheme.typography.headlineMedium,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(modifier = Modifier.height(16.dp))

                //------------------------------------------------------------

                // Recipe thumbnail if available
                if (currentRecipe.thumbnailUrl.isNotEmpty()) {
                    // Handle different image sources (file path, content URI, or remote URL)
                    val imageModel = if (currentRecipe.thumbnailUrl.startsWith("/")) {
                        // Local file path
                        File(currentRecipe.thumbnailUrl)
                    } else if (currentRecipe.thumbnailUrl.startsWith("content://")) {
                        // Content URI
                        Uri.parse(currentRecipe.thumbnailUrl)
                    } else {
                        // Remote URL
                        currentRecipe.thumbnailUrl
                    }
                    
                    AsyncImage(
                        model = ImageRequest.Builder(context)
                            .data(imageModel)
                            .crossfade(true)
                            .build(),
                        contentDescription = "Recipe Image",
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(200.dp)
                            .clip(RoundedCornerShape(8.dp)),
                        contentScale = ContentScale.Crop,
                        error = androidx.compose.ui.res.painterResource(R.drawable.recipe_app_logo)
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                }

                //------------------------------------------------------------

                // Recipe metadata (category, area)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Row {
                            Text(
                                text = "Category: ",
                                fontWeight = FontWeight.Bold,
                                style = MaterialTheme.typography.bodyLarge
                            )
                            Text(
                                text = currentRecipe.category,
                                style = MaterialTheme.typography.bodyLarge
                            )
                        }
                        
                        if (currentRecipe.area.isNotBlank()) {
                            Row {
                                Text(
                                    text = "Cuisine: ",
                                    fontWeight = FontWeight.Bold,
                                    style = MaterialTheme.typography.bodyLarge
                                )
                                Text(
                                    text = currentRecipe.area,
                                    style = MaterialTheme.typography.bodyLarge
                                )
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                Divider()
                Spacer(modifier = Modifier.height(16.dp))

                //------------------------------------------------------------

                // Ingredients section
                Text(
                    text = "Ingredients",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                val ingredients = currentRecipe.getIngredientsList()
                ingredients.forEach { ingredient ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(12.dp),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                text = "•",
                                style = MaterialTheme.typography.bodyLarge,
                                modifier = Modifier.width(16.dp)
                            )
                            Text(
                                text = ingredient.name,
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.Medium,
                                modifier = Modifier.weight(1f)
                            )
                            if (ingredient.measure != null) {
                                Text(
                                    text = ingredient.measure,
                                    style = MaterialTheme.typography.bodyMedium
                                )
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                Divider()
                Spacer(modifier = Modifier.height(16.dp))

                //------------------------------------------------------------

                // Instructions section
                Text(
                    text = "Instructions",
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.fillMaxWidth()
                )
                
                Spacer(modifier = Modifier.height(8.dp))
                
                // Split instructions into steps
                val instructionSteps = currentRecipe.instructions
                    .split("\\. |\\.\n|\\n".toRegex())
                    .filter { it.isNotBlank() }
                    .map { it.trim() }
                
                instructionSteps.forEachIndexed { index, instruction ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 4.dp)
                    ) {
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(12.dp),
                            verticalAlignment = Alignment.Top
                        ) {
                            Text(
                                text = "${index + 1}.",
                                style = MaterialTheme.typography.bodyLarge,
                                fontWeight = FontWeight.Bold,
                                modifier = Modifier
                                    .padding(end = 8.dp, top = 2.dp)
                                    .width(24.dp)
                            )
                            
                            Text(
                                text = instruction,
                                style = MaterialTheme.typography.bodyMedium,
                                modifier = Modifier.weight(1f)
                            )
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))

                //------------------------------------------------------------

                // Edit button
                Button(
                    onClick = { onNavigateToEdit(currentRecipe.id) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isSystemInDarkTheme()) Color(0xFF333333) else Color.Black
                    )
                ) {
                    Icon(
                        imageVector = Icons.Default.Create,
                        contentDescription = "Edit Recipe",
                        modifier = Modifier.size(20.dp),
                        tint = Color.White
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("View and Edit Recipe", color = Color.White)
                }

                //------------------------------------------------------------
                
                Spacer(modifier = Modifier.height(16.dp))
            }
        }
    }
} 
