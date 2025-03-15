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

package com.example.myphotogallery_1

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.navigation.compose.rememberNavController
import com.example.myphotogallery_1.ui.navigation.AppNavHost
import com.example.myphotogallery_1.ui.theme.MyPhotoGallery1Theme

/**
 * Main class
 * it is the single activity in the app following
 * the single-activity architecture pattern with Jetpack Compose
 */
class MainActivity : ComponentActivity() {
    
    /**
     * Called when the activity is first created
     * method initializes the UI components, sets up edge-to-edge display,
     * and configures the navigation system for the application.
     * 
     * @param savedInstanceState Contains data supplied in onSaveInstanceState if the activity
     *                           is being re-initialized after being shut down
     */
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MyPhotoGallery1Theme {
                // A surface container using the 'background' color from the theme
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    // Create navigation controller
                    val navController = rememberNavController()
                    
                    // Set up navigation
                    AppNavHost(navController = navController)
                }
            }
        }
    }
}