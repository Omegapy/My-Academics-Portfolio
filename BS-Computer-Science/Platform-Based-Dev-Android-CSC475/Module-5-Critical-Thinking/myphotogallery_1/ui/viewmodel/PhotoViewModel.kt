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

/* Part of MVVM Architecture: VIEWMODEL */

package com.example.myphotogallery_1.ui.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.myphotogallery_1.data.repository.PhotoRepository
import com.example.myphotogallery_1.data.repository.PhotoRepositoryImpl
import com.example.myphotogallery_1.ui.state.PhotoUiState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collectLatest
import kotlinx.coroutines.launch

/**
 * ViewModel, photo-related operations and state
 * manages the data flow between the repository (Model layer) and
 * the UI components (View layer)
 *
 * @property repository The repository interface used to fetch photo data
 */
class PhotoViewModel(
    private val repository: PhotoRepository = PhotoRepositoryImpl()
) : ViewModel() {
    
    /**
     * Internal mutable state for photo data
     */
    private val _photoState = MutableStateFlow<PhotoUiState>(PhotoUiState.Loading)
    
    /**
     * Publicly exposed immutable state for photo data
     * UI components observe this to update their display
     */
    val photoState: StateFlow<PhotoUiState> = _photoState.asStateFlow()
    
    /**
     * Internal mutable state for search query
     */
    private val _searchQuery = MutableStateFlow("")
    
    /**
     * Publicly exposed immutable state for  search query
     * UI components observe this to update their display
     */
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()
    
    /**
     * Initialize the ViewModel by loading curated photos
     */
    init {
        // Load initial curated photos
        loadCuratedPhotos()
    }

    //-------------------------------------------------------------------------------------------

    /**
     * Load curated photos from the repository
     * fetches a collection of curated (high-quality) photos
     */
    fun loadCuratedPhotos() {
        _photoState.value = PhotoUiState.Loading
        
        viewModelScope.launch {
            repository.getCuratedPhotos().collectLatest { result ->
                _photoState.value = when {
                    result.isSuccess -> {
                        val photos = result.getOrNull()?.photos ?: emptyList()
                        if (photos.isEmpty()) PhotoUiState.Empty else PhotoUiState.Success(photos)
                    }
                    result.isFailure -> {
                        val message = result.exceptionOrNull()?.message ?: "Unknown error"
                        PhotoUiState.Error(message)
                    }
                    else -> PhotoUiState.Empty
                }
            }
        }
    }

    //-------------------------------------------------------------------------------------------
    
    /**
     * Update the search query and search for photos
     * updates the current search query and fetches photos
     * matching the query from the Pexels API via the repository.
     *
     * @param query The search string to look for in the Pexels database
     */
    fun search(query: String) {
        _searchQuery.value = query
        
        if (query.isBlank()) {
            loadCuratedPhotos()
            return
        }
        
        _photoState.value = PhotoUiState.Loading
        
        viewModelScope.launch {
            repository.searchPhotos(query).collectLatest { result ->
                _photoState.value = when {
                    result.isSuccess -> {
                        val photos = result.getOrNull()?.photos ?: emptyList()
                        if (photos.isEmpty()) PhotoUiState.Empty else PhotoUiState.Success(photos)
                    }
                    result.isFailure -> {
                        val message = result.exceptionOrNull()?.message ?: "Unknown error"
                        PhotoUiState.Error(message)
                    }
                    else -> PhotoUiState.Empty
                }
            }
        }
    }

    //-------------------------------------------------------------------------------------------
    
    /**
     * Refresh the current data
     * - If there's an active search query, it repeats the search
     * - If there's no search query, it reloads the curated photos
     * 
     * This is useful for pull-to-refresh functionality or when
     * the user wants to manually update the data.
     * 
     * MVVM Component: VIEWMODEL - User action handler
     * Role: Processes user request to refresh data
     */
    fun refresh() {
        if (_searchQuery.value.isBlank()) {
            loadCuratedPhotos()
        } else {
            search(_searchQuery.value)
        }
    }
} 