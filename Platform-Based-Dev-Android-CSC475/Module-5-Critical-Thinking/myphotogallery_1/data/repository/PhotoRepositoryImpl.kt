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

/* Part of MVVM Architecture: MODEL */

package com.example.myphotogallery_1.data.repository

import com.example.myphotogallery_1.data.api.PexelsApiService
import com.example.myphotogallery_1.data.model.PhotosResponse
import com.example.myphotogallery_1.data.network.NetworkModule
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

/**
 * Implementation of the PhotoRepository interface
 * 
 * This class is responsible for fetching photo data from the Pexels API
 * and converting the responses into Flows that emit Result objects.
 *
 * @property apiService The API service used to make network requests to Pexels
 */
class PhotoRepositoryImpl(
    private val apiService: PexelsApiService = NetworkModule.pexelsApiService
) : PhotoRepository {
    
    /**
     * Get curated photos from the API.
     *
     * @param page The page number to fetch (pagination)
     * @param perPage The number of photos to fetch per page
     * @return A Flow, result containing either the successful PhotosResponse or an exception
     */
    override fun getCuratedPhotos(page: Int, perPage: Int): Flow<Result<PhotosResponse>> = flow {
        try {
            val response = apiService.getCuratedPhotos(
                authKey = NetworkModule.API_KEY,
                page = page,
                perPage = perPage
            )
            emit(Result.success(response))
        } catch (e: Exception) {
            emit(Result.failure(e))
        }
    }

    //-------------------------------------------------------------------------------------------
    
    /**
     * Search for photos using a query.
     * 
     * Searches the Pexels API for photos matching the provided query string.
     * The results are wrapped in a Flow of Result to handle success and failure cases.
     *
     * @param query The search term to look for in the Pexels database
     * @param page The page number to fetch (pagination)
     * @param perPage The number of photos to fetch per page
     * @return A Floe, result containing either the successful PhotosResponse or an exception
     */
    override fun searchPhotos(query: String, page: Int, perPage: Int): Flow<Result<PhotosResponse>> = flow {
        try {
            val response = apiService.searchPhotos(
                authKey = NetworkModule.API_KEY,
                query = query,
                page = page,
                perPage = perPage
            )
            emit(Result.success(response))
        } catch (e: Exception) {
            emit(Result.failure(e))
        }
    }

    //-------------------------------------------------------------------------------------------
} 