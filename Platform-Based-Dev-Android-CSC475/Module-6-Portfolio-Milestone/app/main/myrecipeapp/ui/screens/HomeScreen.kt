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
    This file contains the HomeScreen composable which serves as the app's main dashboard
    displays UI and handling user interactions
 */

package com.example.myrecipeapp.ui.screens

import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.myrecipeapp.R
import com.example.myrecipeapp.model.Recipe
import com.example.myrecipeapp.ui.components.AppFooter
import com.example.myrecipeapp.ui.components.AppHeader
import com.example.myrecipeapp.ui.theme.MyRecipeAppTheme
import com.example.myrecipeapp.viewmodel.RecipeViewModel

/**
 * Home screen composable that serves as the app's main dashboard.
 */
@Composable
fun HomeScreen(
    onMyRecipesClicked: () -> Unit = {},
    onFavoritesClicked: () -> Unit = {},
    onMealDbClicked: () -> Unit = {},
    onMenuClicked: () -> Unit = {},
    onHomeClicked: () -> Unit = {},
    onSearchClicked: () -> Unit = {},
    onAddClicked: () -> Unit = {},
    onRecipeClicked: (Recipe) -> Unit = {},
    currentRoute: String? = null,
    viewModel: RecipeViewModel = viewModel()
) {
    // Collect recipes from ViewModel
    val recipes by viewModel.recipes.collectAsState(initial = emptyList())
    val recentRecipes = recipes.take(6) // Show only the first 6 recipes in the grid
    
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
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState()),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                // Featured recipe image
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                        .height(160.dp)
                        .border(2.dp, Color.Black, RoundedCornerShape(8.dp))
                        .clip(RoundedCornerShape(8.dp))
                ) {
                    Image(
                        painter = painterResource(id = R.drawable.thumbnails_main_recipe_pic),
                        contentDescription = "Featured Recipe",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )
                }
                
                Spacer(modifier = Modifier.height(16.dp))

                //-------------------------------------------------------------------

                // Recent recipes thumbnails
                if (recentRecipes.isNotEmpty()) {
                    Text(
                        text = "Recent Recipes",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(start = 16.dp, bottom = 8.dp),
                        textAlign = TextAlign.Start
                    )
                    
                    RecipeGrid(
                        recipes = recentRecipes,
                        onRecipeClicked = onRecipeClicked
                    )
                }
                
                Spacer(modifier = Modifier.height(24.dp))

                //-------------------------------------------------------------------

                // Main menu buttons - use themed colors
                Column(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    // My Recipes button
                    Button(
                        onClick = onMyRecipesClicked,
                        modifier = if (isSystemInDarkTheme()) {
                            Modifier
                                .width(300.dp)
                                .height(52.dp)
                                .border(
                                    2.dp, 
                                    Color.Black, 
                                    RoundedCornerShape(8.dp)
                                )
                        } else {
                            Modifier
                                .width(300.dp)
                                .height(52.dp)
                                .border(
                                    2.dp, 
                                    MaterialTheme.colorScheme.outline, 
                                    RoundedCornerShape(8.dp)
                                )
                        },
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isSystemInDarkTheme()) Color(0xFF333333) else Color.Black,
                            contentColor = Color.White
                        )
                    ) {
                        Text(
                            text = "My Recipes",
                            textAlign = TextAlign.Center,
                            style = MaterialTheme.typography.titleMedium,
                            fontSize = 18.sp
                        )
                    }

                    //-------------------------------------------------------------------
                    
                    // My Favorite Recipes button
                    Button(
                        onClick = onFavoritesClicked,
                        modifier = if (isSystemInDarkTheme()) {
                            Modifier
                                .width(300.dp)
                                .height(52.dp)
                                .border(
                                    2.dp, 
                                    Color.Black, 
                                    RoundedCornerShape(8.dp)
                                )
                        } else {
                            Modifier
                                .width(300.dp)
                                .height(52.dp)
                                .border(
                                    2.dp, 
                                    MaterialTheme.colorScheme.outline, 
                                    RoundedCornerShape(8.dp)
                                )
                        },
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isSystemInDarkTheme()) Color(0xFF333333) else Color.Black,
                            contentColor = Color.White
                        )
                    ) {
                        Text(
                            text = "My Favorite Recipes",
                            textAlign = TextAlign.Center,
                            style = MaterialTheme.typography.titleMedium,
                            fontSize = 18.sp
                        )
                    }

                    //-------------------------------------------------------------------
                    
                    // TheMealDB Recipes button
                    Button(
                        onClick = onMealDbClicked,
                        modifier = if (isSystemInDarkTheme()) {
                            Modifier
                                .width(300.dp)
                                .height(52.dp)
                                .border(
                                    2.dp, 
                                    Color.Black, 
                                    RoundedCornerShape(8.dp)
                                )
                        } else {
                            Modifier
                                .width(300.dp)
                                .height(52.dp)
                                .border(
                                    2.dp, 
                                    MaterialTheme.colorScheme.outline, 
                                    RoundedCornerShape(8.dp)
                                )
                        },
                        shape = RoundedCornerShape(8.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = if (isSystemInDarkTheme()) Color(0xFF333333) else Color.Black,
                            contentColor = Color.White
                        )
                    ) {
                        Text(
                            text = "TheMealDB Recipes",
                            textAlign = TextAlign.Center,
                            style = MaterialTheme.typography.titleMedium,
                            fontSize = 18.sp
                        )
                    }
                }

                //-------------------------------------------------------------------

                // Spacer to ensure there's room at the bottom for footer
                Spacer(modifier = Modifier.height(24.dp))
            }
        }
    }
}

//-------------------------------------------------------------------------------------------------

/**
 * Displays a grid of recipe thumbnails in a 2-column layout.
 * Used to show a limited set of recipes in a compact view on the home screen.
 *
 * @param recipes List of Recipe objects to display in the grid
 * @param onRecipeClicked Callback function triggered when a recipe thumbnail is clicked
 */
@Composable
fun RecipeGrid(
    recipes: List<Recipe>,
    onRecipeClicked: (Recipe) -> Unit
) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(2),
        modifier = Modifier
            .height(220.dp)
            .fillMaxWidth()
            .padding(horizontal = 16.dp),
        contentPadding = PaddingValues(4.dp),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        items(recipes) { recipe ->
            RecipeThumbnail(
                recipe = recipe,
                onRecipeClicked = onRecipeClicked
            )
        }
    }
}


//-------------------------------------------------------------------------------------------------

/**
 * Single recipe thumbnail card with an image and title overlay
 * Handles both remote images (via URL) and local (fallback) images
 * The thumbnail is clickable
 *
 * @param recipe The Recipe object to display
 * @param onRecipeClicked Callback function triggered when this thumbnail is clicked
 */
@Composable
fun RecipeThumbnail(
    recipe: Recipe,
    onRecipeClicked: (Recipe) -> Unit
) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(1f)
            .border(1.dp, Color.Black, RoundedCornerShape(8.dp))
            .clip(RoundedCornerShape(8.dp))
            .clickable { onRecipeClicked(recipe) }
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

            //-------------------------------------------------------------------

            // Fallback to default image
            Image(
                painter = painterResource(id = R.drawable.thumbnails_main_recipe_pic),
                contentDescription = recipe.name,
                modifier = Modifier.fillMaxSize(),
                contentScale = ContentScale.Crop
            )
        }
        
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.BottomCenter)
                .background(Color.Black.copy(alpha = 0.7f))
                .padding(8.dp)
        ) {
            Text(
                text = recipe.name,
                style = MaterialTheme.typography.bodyMedium,
                color = Color.White,
                modifier = Modifier.align(Alignment.Center),
                textAlign = TextAlign.Center,
                maxLines = 2
            )
        }
    }
}

//-------------------------------------------------------------------------------------------------

/**
 * Preview HomeScreen
 * This is used by Android Studio's preview panel to render a preview of the HomeScreen
 */
@Preview(showBackground = true)
@Composable
fun HomeScreenPreview() {
    MyRecipeAppTheme {
        HomeScreen()
    }
} 
