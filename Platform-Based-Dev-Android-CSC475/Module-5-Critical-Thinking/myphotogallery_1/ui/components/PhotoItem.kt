/*==================================================================================================
    Program Name: My Photo Gallery App
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

package com.example.myphotogallery_1.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import coil.compose.SubcomposeAsyncImage
import coil.request.ImageRequest
import com.example.myphotogallery_1.R
import com.example.myphotogallery_1.data.model.Photo

/**
 * Composable function that displays a single photo item in the grid.
 * 
 * Displays a photo as a card with the image loaded asynchronously
 * using Coil. It is designed to be used in a grid layout and maintains a 1:1 aspect ratio.
 * 
 * @param photo The photo model object to display
 * @param onClick Callback function invoked when the photo is clicked
 * @param modifier Modifier to apply to the component for customizing layout
 */
@Composable
fun PhotoItem(
    photo: Photo,
    onClick: (Photo) -> Unit,
    modifier: Modifier = Modifier
) {
    Card(
        modifier = modifier
            .padding(4.dp)
            .clickable { onClick(photo) },
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
        shape = MaterialTheme.shapes.medium
    ) {
        // load states (loading, success, error)
        SubcomposeAsyncImage(
            model = ImageRequest.Builder(LocalContext.current)
                .data(photo.src.medium)
                .crossfade(true)
                .build(),
            contentDescription = photo.alt,
            contentScale = ContentScale.Crop,
            modifier = Modifier
                .fillMaxSize()
                .aspectRatio(1f),
            loading = {
                // Loading state UI
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    CircularProgressIndicator(
                        color = MaterialTheme.colorScheme.primary,
                        modifier = Modifier.padding(8.dp)
                    )
                }
            },
            error = {
                // Error state UI
                AsyncImage(
                    model = R.drawable.ic_launcher_foreground,
                    contentDescription = "Error loading image",
                    modifier = Modifier.fillMaxSize(),
                    contentScale = ContentScale.Crop
                )
            }
        )
    }
} 