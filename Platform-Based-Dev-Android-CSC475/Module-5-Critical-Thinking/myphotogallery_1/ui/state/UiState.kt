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

/* Part of MVVM Architecture: VIEWMODEL */

package com.example.myphotogallery_1.ui.state

import com.example.myphotogallery_1.data.model.Photo

/**
 * Sealed interface to represent different UI states for photo-related screens
 * Using a sealed interface allows for representing multiple unique states
 */
sealed interface PhotoUiState {
    /**
     * Initial loading state,
     * indicates that data is currently being fetched,
     * and the UI should display a loading indicator to the user
     */
    object Loading : PhotoUiState

    //-------------------------------------------------------------------------------------------

    /**
     * Success state with a list of photos,
     * indicates that data was successfully fetched and
     * contains the list of photos
     *
     * @property photos The list of photo objects
     */
    data class Success(val photos: List<Photo>) : PhotoUiState

    //-------------------------------------------------------------------------------------------

    /**
     * Empty state when no photos are available
     *  indicates that the operation was successful but
     * returned no photos, and the UI should display an empty state message
     */
    object Empty : PhotoUiState

    //-------------------------------------------------------------------------------------------
    
    /**
     * Error state when something goes wrong,
     * indicates that an error occurred during data fetching,
     * and the UI should display an error message to the user
     *
     * @property message The error message
     */
    data class Error(val message: String) : PhotoUiState
} 