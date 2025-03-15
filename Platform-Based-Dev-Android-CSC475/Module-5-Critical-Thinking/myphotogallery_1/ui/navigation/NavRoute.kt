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

/* Part of MVVM Architecture: VIEW */

package com.example.myphotogallery_1.ui.navigation


/**
 * Sealed class containing all navigation routes for the app
 * 
 * This class defines navigation destinations in the application
 * A sealed class check that all routes are known
 * at compile time and prevents navigation to undefined routes
 * Each route object represents a screen in the application
 *
 * @property route The route string used for navigation
 */
sealed class NavRoute(val route: String) {
    /**
     * Main gallery screen, displaying a grid of photos.
     * 
     * This is the home screen of the application, showing a grid of curated
     * photos with search functionality at launch.
     */
    object Gallery : NavRoute("gallery")

    //-------------------------------------------------------------------------------------------

    /**
     * Detail screen showing a single photo with more information.
     * 
     * This screen displays detailed information about a selected photo.
     */
    object PhotoDetail : NavRoute("photo/{photoId}") {
        /**
         * Creates a route path with the specified photo ID
         *
         * @param photoId The ID of the photo to navigate to
         * @return A route string with the photo ID
         */
        fun createRoute(photoId: Int): String = "photo/$photoId"
    }

    //-------------------------------------------------------------------------------------------
} 