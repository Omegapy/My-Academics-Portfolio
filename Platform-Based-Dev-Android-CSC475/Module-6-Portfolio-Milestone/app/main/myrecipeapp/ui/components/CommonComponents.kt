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
    This file contains common reusable UI components like headers and footers
*/

package com.example.myrecipeapp.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.wrapContentSize
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

/**
 * App header with 'logo' and menu button.
 */
@Composable
fun AppHeader(
    onMenuClicked: () -> Unit = {},
    onHomeClicked: () -> Unit = {},
    onMyRecipesClicked: () -> Unit = {},
    onFavoritesClicked: () -> Unit = {},
    onMealDbClicked: () -> Unit = {},
    onSearchClicked: () -> Unit = {}
) {
    var showDropdownMenu by remember { mutableStateOf(false) }
    
    // Use Material colors for dark mode support
    val backgroundColor = MaterialTheme.colorScheme.surface
    val borderColor = MaterialTheme.colorScheme.outline
    val textColor = MaterialTheme.colorScheme.onSurface
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .statusBarsPadding()
            .padding(horizontal = 16.dp, vertical = 2.dp)
            .padding(top = 0.dp)
            .border(1.dp, borderColor, RoundedCornerShape(8.dp))
            .background(backgroundColor, RoundedCornerShape(8.dp))
            .padding(4.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(6.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Custom styled logo with appropriate background color
                Box(
                    modifier = Modifier
                        .size(38.dp)
                        .background(
                            if (isSystemInDarkTheme()) Color(0xFF212121) else MaterialTheme.colorScheme.primary, 
                            CircleShape
                        )
                        .padding(5.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "🍽️",  // Emoji as logo
                        fontSize = 20.sp,
                        color = MaterialTheme.colorScheme.onPrimary
                    )
                }
                
                Text(
                    text = "My Recipe App",
                    style = MaterialTheme.typography.titleLarge.copy(
                        fontWeight = FontWeight.Bold,
                        fontSize = 22.sp
                    ),
                    color = textColor,
                    modifier = Modifier.padding(start = 6.dp)
                )
            }
            
            Box(
                modifier = Modifier
                    .wrapContentSize(Alignment.TopEnd)
            ) {
                IconButton(onClick = { 
                    showDropdownMenu = true
                    onMenuClicked()
                }) {
                    Icon(
                        imageVector = Icons.Default.MoreVert,
                        contentDescription = "Menu",
                        tint = textColor
                    )
                }
                
                DropdownMenu(
                    expanded = showDropdownMenu,
                    onDismissRequest = { showDropdownMenu = false },
                    modifier = Modifier
                        .background(
                            color = if (isSystemInDarkTheme()) 
                                Color(0xFF303030) // Slightly darker than surface color in dark mode
                            else 
                                Color.White,
                            shape = RoundedCornerShape(8.dp)
                        )
                        .border(
                            width = 1.dp,
                            color = if (isSystemInDarkTheme()) 
                                Color(0xFF424242) // Dark grey for dark mode
                            else 
                                Color(0xFFBDBDBD), // Light grey for light mode
                            shape = RoundedCornerShape(8.dp)
                        )
                ) {
                    DropdownMenuItem(
                        text = { 
                            Text(
                                "Home",
                                color = if (isSystemInDarkTheme()) Color.White else Color.Black
                            ) 
                        },
                        onClick = {
                            onHomeClicked()
                            showDropdownMenu = false
                        }
                    )
                    
                    DropdownMenuItem(
                        text = { 
                            Text(
                                "My Favorite Recipes",
                                color = if (isSystemInDarkTheme()) Color.White else Color.Black
                            ) 
                        },
                        onClick = {
                            onFavoritesClicked()
                            showDropdownMenu = false
                        }
                    )
                    
                    DropdownMenuItem(
                        text = { 
                            Text(
                                "My Recipes",
                                color = if (isSystemInDarkTheme()) Color.White else Color.Black
                            ) 
                        },
                        onClick = {
                            onMyRecipesClicked()
                            showDropdownMenu = false
                        }
                    )
                    
                    DropdownMenuItem(
                        text = { 
                            Text(
                                "TheMealDB Recipes",
                                color = if (isSystemInDarkTheme()) Color.White else Color.Black
                            ) 
                        },
                        onClick = {
                            onMealDbClicked()
                            showDropdownMenu = false
                        }
                    )
                    
                    DropdownMenuItem(
                        text = { 
                            Text(
                                "Search",
                                color = if (isSystemInDarkTheme()) Color.White else Color.Black
                            ) 
                        },
                        onClick = {
                            onSearchClicked()
                            showDropdownMenu = false
                        }
                    )
                }
            }
        }
    }
}

//--------------------------------------------------------------------------------------------------

/**
 * App footer with home, search, and add buttons
 */
@Composable
fun AppFooter(
    onHomeClicked: () -> Unit = {},
    onSearchClicked: () -> Unit = {},
    onAddClicked: () -> Unit = {},
    currentRoute: String? = null
) {
    // Use Material Theme colors for proper dark mode support
    val backgroundColor = MaterialTheme.colorScheme.surface
    val selectedColor = MaterialTheme.colorScheme.primary
    val unselectedColor = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f)
    val indicatorColor = MaterialTheme.colorScheme.primaryContainer
    
    NavigationBar(
        modifier = Modifier
            .fillMaxWidth()
            .padding(bottom = 12.dp),  // Increased bottom padding from 8.dp to 12.dp
        containerColor = backgroundColor
    ) {
        NavigationBarItem(
            icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
            label = { Text("Home") },
            selected = currentRoute == "home",
            onClick = onHomeClicked,
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = selectedColor,
                selectedTextColor = selectedColor,
                indicatorColor = indicatorColor,
                unselectedIconColor = unselectedColor,
                unselectedTextColor = unselectedColor
            )
        )
        
        NavigationBarItem(
            icon = { Icon(Icons.Default.Search, contentDescription = "Search") },
            label = { Text("Search") },
            selected = currentRoute == "search" || currentRoute?.startsWith("search_") == true,
            onClick = onSearchClicked,
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = selectedColor,
                selectedTextColor = selectedColor,
                indicatorColor = indicatorColor,
                unselectedIconColor = unselectedColor,
                unselectedTextColor = unselectedColor
            )
        )
        
        NavigationBarItem(
            icon = { Icon(Icons.Default.Add, contentDescription = "Add Recipe") },
            label = { Text("Add") },
            selected = currentRoute == "add" || currentRoute == "edit",
            onClick = onAddClicked,
            colors = NavigationBarItemDefaults.colors(
                selectedIconColor = selectedColor,
                selectedTextColor = selectedColor,
                indicatorColor = indicatorColor,
                unselectedIconColor = unselectedColor,
                unselectedTextColor = unselectedColor
            )
        )
    }
} 