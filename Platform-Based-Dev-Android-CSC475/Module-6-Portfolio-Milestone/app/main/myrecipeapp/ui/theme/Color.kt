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
    This file defines color resources for the app's theme
 */

package com.example.myrecipeapp.ui.theme

import androidx.compose.ui.graphics.Color

// Light Theme
val Primary = Color(0xFFFF5722)
val PrimaryVariant = Color(0xFFFF7043)
val Secondary = Color(0xFF000000)
val SecondaryVariant = Color(0xFF333333)
val Background = Color(0xFFFFFFFF)
val Surface = Color(0xFFFFFFFF)
val Error = Color(0xFFB00020)
val OnPrimary = Color.White
val OnSecondary = Color.White
val OnBackground = Color.Black
val OnSurface = Color.Black
val OnError = Color.White
val Accent = Color(0xFFFF5722)
val Border = Color(0xFF000000)

// Dark Theme
val PrimaryDark = Color(0xFFFF7043)
val PrimaryVariantDark = Color(0xFFFF9800)
val SecondaryDark = Color(0xFFBBBBBB)
val SecondaryVariantDark = Color(0xFF666666)
val BackgroundDark = Color(0xFF121212)
val SurfaceDark = Color(0xFF1E1E1E)
val ErrorDark = Color(0xFFCF6679)
val OnPrimaryDark = Color.Black
val OnSecondaryDark = Color.Black
val OnBackgroundDark = Color.White
val OnSurfaceDark = Color.White
val OnErrorDark = Color.Black
val AccentDark = Color(0xFFFF9800)
val BorderDark = Color(0xFF444444)
