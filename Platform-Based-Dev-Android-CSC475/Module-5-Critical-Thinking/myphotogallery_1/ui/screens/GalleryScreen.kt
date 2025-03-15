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

package com.example.myphotogallery_1.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.input.nestedscroll.nestedScroll
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.example.myphotogallery_1.R
import com.example.myphotogallery_1.data.model.Photo
import com.example.myphotogallery_1.ui.components.PhotoItem
import com.example.myphotogallery_1.ui.state.PhotoUiState

/**
 * Renders the main gallery screen
 * This screen displays a grid of photos from the Pexels API and a search bar at the top
 * 
 * @param photoState Current UI state for photos from the ViewModel
 * @param searchQuery Current search query text from the ViewModel
 * @param onPhotoClick Callback, photo is clicked
 * @param onSearchQueryChange Callback, the search query changes
 * @param onRefresh Callback, the user requests a data refresh
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GalleryScreen(
    photoState: PhotoUiState,
    searchQuery: String,
    onPhotoClick: (Photo) -> Unit,
    onSearchQueryChange: (String) -> Unit,
    onRefresh: () -> Unit
) {
    val scrollBehavior = TopAppBarDefaults.enterAlwaysScrollBehavior()
    
    // Screen layout structure
    Scaffold(
        modifier = Modifier
            .fillMaxSize()
            .nestedScroll(scrollBehavior.nestedScrollConnection),
        topBar = {
            // App bar
            TopAppBar(
                title = { Text(text = stringResource(R.string.app_name)) },
                scrollBehavior = scrollBehavior,
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer,
                    titleContentColor = MaterialTheme.colorScheme.onPrimaryContainer
                )
            )
        }
    ) { paddingValues ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(paddingValues)
        ) {
            // Search field
            SearchBar(
                query = searchQuery,
                onQueryChange = onSearchQueryChange,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp)
            )
            
            // Main content based on state
            when (photoState) {
                is PhotoUiState.Loading -> {
                    LoadingView()
                }
                is PhotoUiState.Success -> {
                    PhotoGrid(
                        photos = photoState.photos,
                        onPhotoClick = onPhotoClick
                    )
                }
                is PhotoUiState.Empty -> {
                    EmptyView()
                }
                is PhotoUiState.Error -> {
                    ErrorView(
                        message = photoState.message,
                        onRetry = onRefresh
                    )
                }
            }
        }
    }
}

//-------------------------------------------------------------------------------------------

/**
 * Search bar composable for the gallery screen
 * 
 * This composable provides a text input field with search and clear icons
 * for entering and clearing search queries. It maintains its own internal state
 * but delegates changes to the parent via the onQueryChange callback.
 *
 * @param query The current search query text
 * @param onQueryChange Callback when the query text changes, with the new text as parameter
 * @param modifier Optional Modifier to apply to the component for customizing layout
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
private fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    // Local UI state
    var searchQuery by remember { mutableStateOf(query) }
    
    OutlinedTextField(
        value = searchQuery,
        onValueChange = { newQuery ->
            searchQuery = newQuery
            onQueryChange(newQuery)  // Delegate to ViewModel
        },
        modifier = modifier,
        placeholder = { Text("Search photos...") },
        leadingIcon = {
            Icon(
                imageVector = Icons.Default.Search,
                contentDescription = "Search"
            )
        },
        trailingIcon = {
            if (searchQuery.isNotEmpty()) {
                IconButton(onClick = {
                    searchQuery = ""
                    onQueryChange("")  //  Delegate to ViewModel
                }) {
                    Icon(
                        imageVector = Icons.Default.Clear,
                        contentDescription = "Clear search"
                    )
                }
            }
        },
        singleLine = true,
        shape = MaterialTheme.shapes.medium
    )
}

/**
 * Photo grid display composable
 * Displays a grid of photos using a LazyVerticalGrid
 *
 * @param photos List of photos
 * @param onPhotoClick Callback, photo is clicked
 * @param modifier Optional Modifier to apply to the component for customizing layout
 */
@Composable
private fun PhotoGrid(
    photos: List<Photo>,
    onPhotoClick: (Photo) -> Unit,
    modifier: Modifier = Modifier
) {
    LazyVerticalGrid(
        columns = GridCells.Adaptive(minSize = 160.dp),
        contentPadding = PaddingValues(8.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
        modifier = modifier.fillMaxSize()
    ) {
        items(
            items = photos,
            key = { it.id }
        ) { photo ->
            // MVVM Component: VIEW - Item rendering
            PhotoItem(
                photo = photo,
                onClick = onPhotoClick
            )
        }
    }
}

//-------------------------------------------------------------------------------------------

/**
 * Loading view composable
 * Displays a centered circular progress indicator
 * to indicate that data is being loaded
 *
 */
@Composable
private fun LoadingView() {
    Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        CircularProgressIndicator(
            color = MaterialTheme.colorScheme.primary
        )
    }
}

//-------------------------------------------------------------------------------------------

/**
 * Empty view composable.
 * Displays a message when no photos are found,
 * typically shown after a search with no results.
 */
@Composable
private fun EmptyView() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "No photos found",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center
        )
    }
}

//-------------------------------------------------------------------------------------------

/**
 * Error view composable.
 * Displays an error message and a retry button
 * when an error occurs during data loading.
 *
 * @param message The error message
 * @param onRetry Callback, the retry button is clicked
 */
@Composable
private fun ErrorView(
    message: String,
    onRetry: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Error: $message",
            style = MaterialTheme.typography.bodyLarge,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(bottom = 16.dp)
        )
        
        androidx.compose.material3.Button(
            onClick = onRetry  // VIEW-VIEWMODEL - Delegate retry action
        ) {
            Text("Retry")
        }
    }
} 