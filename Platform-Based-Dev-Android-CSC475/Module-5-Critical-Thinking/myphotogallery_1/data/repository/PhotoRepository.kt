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

/* Part of MVVM Architecture: MODEL */

package com.example.myphotogallery_1.data.repository

//import com.example.myphotogallery_1.data.model.Photo
import com.example.myphotogallery_1.data.model.PhotosResponse
import kotlinx.coroutines.flow.Flow

/**
 * Repository interface for handling photo data
 */
interface PhotoRepository {
    /**
     * Get curated photos from the API
     * 
     * @param page Page number to fetch
     * @param perPage Number of items per page
     * @return Flow of Result<PhotosResponse> the API response
     */
    fun getCuratedPhotos(page: Int = 1, perPage: Int = 15): Flow<Result<PhotosResponse>>
    
    /**
     * Search for photos using a query
     * 
     * @param query Search query
     * @param page Page number to fetch
     * @param perPage Number of items per page
     * @return Flow of Result<PhotosResponse> the API response
     */
    fun searchPhotos(query: String, page: Int = 1, perPage: Int = 15): Flow<Result<PhotosResponse>>
} 