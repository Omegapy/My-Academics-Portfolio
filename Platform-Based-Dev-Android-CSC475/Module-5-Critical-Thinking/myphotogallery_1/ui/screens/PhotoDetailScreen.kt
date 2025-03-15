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

package com.example.myphotogallery_1.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import coil.compose.SubcomposeAsyncImage
import coil.request.ImageRequest
import com.example.myphotogallery_1.data.model.Photo

/**
 * Composable function for displaying detailed information about a photo
 * 
 * This screen shows a larger version of the selected photo with detailed
 * information about it, like the photographer, dimensions, and attribution.
 * It has a back button for navigation and handles the case when the photo
 * data is not yet available by showing a loading indicator
 * The screen content is scrollable to accommodate various screen sizes and
 * mobile device orientation changes
 *
 * 
 * @param photo The photo object
 * @param onBackClick Callback, the back button is clicked
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PhotoDetailScreen(
    photo: Photo?,
    onBackClick: () -> Unit
) {
    val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior()
    
    Scaffold(
        modifier = Modifier
            .fillMaxSize()
            .nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            TopAppBar(
                title = { Text("Photo Details") },
                navigationIcon = {
                    IconButton(onClick = onBackClick) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back"
                        )
                    }
                },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        }
    ) { paddingValues ->
        if (photo == null) {
            // loading indicator if photo data is not yet available
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else {
            // photo details if data is available
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(paddingValues)
                    .verticalScroll(rememberScrollState())
            ) {
                // Photo image
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(300.dp)
                        .background(Color(android.graphics.Color.parseColor(photo.avgColor))),
                    contentAlignment = Alignment.Center
                ) {
                    SubcomposeAsyncImage(
                        model = ImageRequest.Builder(LocalContext.current)
                            .data(photo.src.large)
                            .crossfade(true)
                            .build(),
                        contentDescription = photo.alt,
                        contentScale = ContentScale.Fit,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(8.dp),
                        loading = {
                            CircularProgressIndicator(
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                    )
                }
                
                // Photo details
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp)
                ) {
                    // Title
                    Text(
                        text = photo.alt,
                        style = MaterialTheme.typography.headlineSmall,
                        fontWeight = FontWeight.Bold
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Photographer
                    Text(
                        text = "Photographer: ${photo.photographer}",
                        style = MaterialTheme.typography.bodyLarge
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Dimensions
                    Text(
                        text = "Dimensions: ${photo.width} x ${photo.height}",
                        style = MaterialTheme.typography.bodyMedium
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Attribution
                    Text(
                        text = "Photo provided by Pexels",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    
                    Text(
                        text = "View on Pexels: ${photo.url}",
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.primary
                    )
                }
            }
        }
    }
} 