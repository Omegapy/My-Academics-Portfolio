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
    This file contains various search screen composables for different search types
 */

package com.example.myrecipeapp.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.myrecipeapp.ui.components.AppFooter
import com.example.myrecipeapp.ui.components.AppHeader

/**
 * Search screen for My Recipes
 */
@Composable
fun MyRecipesSearchScreen(
    onBackPressed: () -> Unit,
    onHomeClicked: () -> Unit,
    onSearchClicked: () -> Unit,
    onAddClicked: () -> Unit,
    onSearchOptionClicked: (String) -> Unit,
    currentRoute: String? = null
) {
    SearchScreenTemplate(
        title = "My Recipes Search",
        onBackPressed = onBackPressed,
        onHomeClicked = onHomeClicked,
        onSearchClicked = onSearchClicked,
        onAddClicked = onAddClicked,
        onSearchOptionClicked = onSearchOptionClicked,
        currentRoute = currentRoute
    )
}

//--------------------------------------------------------------------------------------------------

/**
 * Search screen for Favorite Recipes
 */
@Composable
fun FavoriteRecipesSearchScreen(
    onBackPressed: () -> Unit,
    onHomeClicked: () -> Unit,
    onSearchClicked: () -> Unit,
    onAddClicked: () -> Unit,
    onSearchOptionClicked: (String) -> Unit,
    currentRoute: String? = null
) {
    SearchScreenTemplate(
        title = "My Favorite Recipes Search",
        onBackPressed = onBackPressed,
        onHomeClicked = onHomeClicked,
        onSearchClicked = onSearchClicked,
        onAddClicked = onAddClicked,
        onSearchOptionClicked = onSearchOptionClicked,
        currentRoute = currentRoute
    )
}

/**
 * Search screen for TheMealDB Recipes
 */
@Composable
fun TheMealDBSearchScreen(
    onBackPressed: () -> Unit,
    onHomeClicked: () -> Unit,
    onSearchClicked: () -> Unit,
    onAddClicked: () -> Unit,
    onSearchOptionClicked: (String) -> Unit,
    currentRoute: String? = null
) {
    SearchScreenTemplate(
        title = "TheMealDB Recipes Search",
        onBackPressed = onBackPressed,
        onHomeClicked = onHomeClicked,
        onSearchClicked = onSearchClicked,
        onAddClicked = onAddClicked,
        onSearchOptionClicked = onSearchOptionClicked,
        currentRoute = currentRoute
    )
}

//--------------------------------------------------------------------------------------------------

/**
 * Common template for search screens
 */
@Composable
private fun SearchScreenTemplate(
    title: String,
    onBackPressed: () -> Unit,
    onHomeClicked: () -> Unit,
    onSearchClicked: () -> Unit,
    onAddClicked: () -> Unit,
    onSearchOptionClicked: (String) -> Unit,
    currentRoute: String? = null
) {
    // State for search dialog
    var showSearchInputDialog by remember { mutableStateOf(false) }
    var currentSearchType by remember { mutableStateOf("") }
    var searchQuery by remember { mutableStateOf("") }
    val focusManager = LocalFocusManager.current
    
    // Show search input dialog if needed
    if (showSearchInputDialog) {
        AlertDialog(
            onDismissRequest = { 
                showSearchInputDialog = false
                searchQuery = ""
            },
            title = { 
                Text(
                    text = "Search by $currentSearchType", 
                    style = MaterialTheme.typography.titleMedium
                ) 
            },
            text = {
                Column {
                    OutlinedTextField(
                        value = searchQuery,
                        onValueChange = { searchQuery = it },
                        label = { Text("Enter $currentSearchType") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                        keyboardActions = KeyboardActions(
                            onSearch = {
                                if (searchQuery.isNotBlank()) {
                                    onSearchOptionClicked(currentSearchType + ":" + searchQuery)
                                    showSearchInputDialog = false
                                    searchQuery = ""
                                    focusManager.clearFocus()
                                }
                            }
                        ),
                        modifier = Modifier.fillMaxWidth()
                    )
                }
            },
            confirmButton = {
                Button(
                    onClick = {
                        if (searchQuery.isNotBlank()) {
                            onSearchOptionClicked(currentSearchType + ":" + searchQuery)
                            showSearchInputDialog = false
                            searchQuery = ""
                        }
                    },
                    enabled = searchQuery.isNotBlank()
                ) {
                    Text("Search")
                }
            },
            dismissButton = {
                TextButton(
                    onClick = {
                        showSearchInputDialog = false
                        searchQuery = ""
                    }
                ) {
                    Text("Cancel")
                }
            }
        )
    }
    
    Scaffold(
        topBar = {
            AppHeader(
                onMenuClicked = { /* Handle menu click */ },
                onHomeClicked = onHomeClicked,
                onMyRecipesClicked = { /* Handle navigation */ },
                onFavoritesClicked = { /* Handle navigation */ },
                onMealDbClicked = { /* Handle navigation */ },
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
                    text = title,
                    style = MaterialTheme.typography.titleLarge,
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

            //-------------------------------------------------

            // Search options card
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(8.dp),
                elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
            ) {
                Column(
                    modifier = Modifier.padding(16.dp)
                ) {
                    Text(
                        text = "Search By",
                        style = MaterialTheme.typography.titleMedium,
                        modifier = Modifier.fillMaxWidth(),
                        textAlign = TextAlign.Start
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Search options buttons
                    val searchOptions = listOf(
                        "Name", "First Letter", "ID", "Random Meals",
                        "Category", "Main Ingredient", "Area"
                    )
                    
                    searchOptions.forEach { option ->
                        Button(
                            onClick = { 
                                // Show dialog instead of immediately navigating
                                currentSearchType = option
                                showSearchInputDialog = true
                            },
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color.Black,
                                contentColor = Color.White
                            ),
                            shape = RoundedCornerShape(4.dp)
                        ) {
                            Text(option)
                        }
                        
                        Spacer(modifier = Modifier.height(8.dp))
                    }
                }
            }
        }
    }
} 
