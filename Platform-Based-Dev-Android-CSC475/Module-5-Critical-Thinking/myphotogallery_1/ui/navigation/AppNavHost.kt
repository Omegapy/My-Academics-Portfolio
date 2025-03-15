/*==================================================================================================
    Program Name: To Do List App
    Author: Alexander Ricciardi
    Date: 03/16/2025

    Requirement:
        Jetpack Compose (2.7.x): UI
        Retrofit (2.9.0): API communication
        OkHttp (4.11.0): HTTP client
        Gson (1.6.0): JSON serialization/deserialization
        Coil (2.50): For asynchronous image loading with Compose integration
        Kotlin Coroutines (1.7.3):
        Navigation Compose (2.7.7): navigation between screens
        Material 3: Material Design components and theming

    Program Description:
    The program is a small Android application that allows a user to browse images from pexels.com
    (a website that provides free stock photos).
        •	When launched, the home page of the app displays
            a browsable list of curated professional photographs selected by Pexels.
        •	Search for specific images using keywords.
        •	View detailed information about each photograph, including photographer credits.
        •	The app User Interface (UI) follows Material Design principles.
==================================================================================================*/

/* Part of MVVM Architecture: VIEW/MODELVIEW */

package com.example.myphotogallery_1.ui.navigation


import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.viewmodel.compose.viewModel
// Explicit navigation imports
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.example.myphotogallery_1.data.model.Photo
import com.example.myphotogallery_1.ui.screens.GalleryScreen
import com.example.myphotogallery_1.ui.screens.PhotoDetailScreen
import com.example.myphotogallery_1.ui.viewmodel.PhotoViewModel

/**
 * Main navigation for the app.
 * 
 * This composable function sets up the navigation graph for the application,
 * managing navigation between different screens. It creates and provides ViewModels
 * to the screens that need them, and handles passing data between screens.
 * 
 * @param navController  The NavController for navigation
 * @param startDestination The starting destination route (defaults to the Gallery screen)
 */
@Composable
fun AppNavHost(
    navController: NavHostController,
    startDestination: String = NavRoute.Gallery.route
) {
    // Create the ViewModel
    val photoViewModel: PhotoViewModel = viewModel()
    
    // Collect state from ViewModel
    // State observation
    val photoState by photoViewModel.photoState.collectAsState()
    val searchQuery by photoViewModel.searchQuery.collectAsState()
    
    // Track selected photo for detail screen
    var selectedPhoto by remember { mutableStateOf<Photo?>(null) }
    
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        // Gallery screen
        composable(route = NavRoute.Gallery.route) {
            GalleryScreen(
                photoState = photoState,
                searchQuery = searchQuery,
                onPhotoClick = { photo ->
                    // Store the selected photo and navigate to detail screen
                    selectedPhoto = photo
                    navController.navigate(NavRoute.PhotoDetail.createRoute(photo.id))
                },
                onSearchQueryChange = { query ->
                    // Update search query in ViewModel
                    // VIEW-VIEWMODEL - Action delegation
                    photoViewModel.search(query)
                },
                onRefresh = {
                    // Refresh data in ViewModel
                    // VIEW-VIEWMODEL - Action delegation
                    photoViewModel.refresh()
                }
            )
        }
        
        // Photo detail screen
        composable(
            route = NavRoute.PhotoDetail.route,
            arguments = listOf(
                navArgument("photoId") {
                    type = NavType.IntType
                }
            )
        ) {
            PhotoDetailScreen(
                photo = selectedPhoto,
                onBackClick = {
                    // Navigate back to gallery screen
                    navController.popBackStack()
                }
            )
        }
    }
} 