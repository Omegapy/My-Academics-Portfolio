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
    This file contains reusable UI components for recipes
*/

package com.example.myrecipeapp.ui.components

import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.FavoriteBorder
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.example.myrecipeapp.R
import com.example.myrecipeapp.model.Recipe
import java.io.File

/**
 * A list of recipes that can be displayed in various screens
 */
@Composable
fun RecipeList(
    recipes: List<Recipe>,
    onRecipeClicked: (Int) -> Unit,
    modifier: Modifier = Modifier,
    onFavoriteToggle: ((Recipe) -> Unit)? = null
) {
    if (recipes.isEmpty()) {
        Box(
            modifier = Modifier.fillMaxSize(),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "No recipes found",
                style = MaterialTheme.typography.titleMedium,
                color = Color.Gray
            )
        }
    } else {
        LazyColumn(
            modifier = modifier.fillMaxSize(),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(recipes) { recipe ->
                RecipeCard(
                    recipe = recipe,
                    onClick = { onRecipeClicked(recipe.id) },
                    onFavoriteToggle = onFavoriteToggle
                )
            }
        }
    }
}

//--------------------------------------------------------------------------------------------------

/**
 * A card that displays information about a recipe
 */
@Composable
fun RecipeCard(
    recipe: Recipe,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    onFavoriteToggle: ((Recipe) -> Unit)? = null
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(vertical = 4.dp),
        shape = RoundedCornerShape(8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Recipe image
            Box(
                modifier = Modifier
                    .size(80.dp)
                    .clip(RoundedCornerShape(4.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant)
            ) {
                if (recipe.thumbnailUrl.isNotEmpty() && !recipe.thumbnailUrl.contains("drawable")) {
                    // Handle different image sources (file path, content URI, or remote URL)
                    val imageModel = if (recipe.thumbnailUrl.startsWith("/")) {
                        // Local file path
                        File(recipe.thumbnailUrl)
                    } else if (recipe.thumbnailUrl.startsWith("content://")) {
                        // Content URI
                        Uri.parse(recipe.thumbnailUrl)
                    } else {
                        // Remote URL
                        recipe.thumbnailUrl
                    }
                    
                    // Load image from URL or file
                    AsyncImage(
                        model = ImageRequest.Builder(LocalContext.current)
                            .data(imageModel)
                            .crossfade(true)
                            .build(),
                        contentDescription = recipe.name,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                } else {
                    // Load default image
                    androidx.compose.foundation.Image(
                        painter = painterResource(id = R.drawable.thumbnails_main_recipe_pic),
                        contentDescription = recipe.name,
                        contentScale = ContentScale.Crop,
                        modifier = Modifier.fillMaxSize()
                    )
                }
            }

            //------------------------------------------------------------

            // Recipe details
            Column(
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 12.dp)
            ) {
                Text(
                    text = recipe.name,
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                
                Spacer(modifier = Modifier.height(4.dp))
                
                // Get the first few characters of the instructions for the description
                val description = recipe.instructions.take(100) + if (recipe.instructions.length > 100) "..." else ""
                
                Text(
                    text = description,
                    style = MaterialTheme.typography.bodyMedium,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    color = Color.DarkGray
                )
                
                Row(
                    modifier = Modifier.padding(top = 4.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // Show category and area instead of prep time and servings
                    if (recipe.category.isNotEmpty()) {
                        Text(
                            text = "🍽️ ${recipe.category}",
                            style = MaterialTheme.typography.bodySmall,
                            color = Color.Gray
                        )
                    }
                    
                    if (recipe.area.isNotEmpty()) {
                        Text(
                            text = " • 🌍 ${recipe.area}",
                            style = MaterialTheme.typography.bodySmall,
                            color = Color.Gray
                        )
                    }
                }
            }

            //------------------------------------------------------------

            // Favorite icon toggle onFavoriteToggle
            Icon(
                imageVector = if (recipe.isFavorite) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                contentDescription = if (recipe.isFavorite) "Remove from favorites" else "Add to favorites",
                tint = if (recipe.isFavorite) Color.Red else Color.Gray,
                modifier = Modifier
                    .size(24.dp)
                    .padding(start = 4.dp)
                    .let { mod ->
                        if (onFavoriteToggle != null) {
                            mod.clickable { onFavoriteToggle(recipe) }
                        } else {
                            mod
                        }
                    }
            )
        }
    }
} 
