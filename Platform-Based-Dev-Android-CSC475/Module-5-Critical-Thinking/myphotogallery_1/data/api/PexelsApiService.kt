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

package com.example.myphotogallery_1.data.api

import com.example.myphotogallery_1.data.model.PhotosResponse
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Query

/**
 * Retrofit for making API requests to the Pexels API
 */
interface PexelsApiService {
    
    /**
     * Get curated photos from Pexels
     * 
     * @param authKey API key
     * @param page Page number to fetch (default is 1)
     * @param perPage Number of items per page (default is 15)
     * @return PhotosResponse, list of photos and pagination info
     */
    @GET("v1/curated")
    suspend fun getCuratedPhotos(
        @Header("Authorization") authKey: String,
        @Query("page") page: Int = 1,
        @Query("per_page") perPage: Int = 15
    ): PhotosResponse
    
    /**
     * Search for photos on Pexels
     * 
     * @param authKey API key
     * @param query Search query
     * @param page Page number to fetch (default is 1)
     * @param perPage Number of items per page (default is 15)
     * @return PhotosResponse, list of photos and pagination info
     */
    @GET("v1/search")
    suspend fun searchPhotos(
        @Header("Authorization") authKey: String,
        @Query("query") query: String,
        @Query("page") page: Int = 1,
        @Query("per_page") perPage: Int = 15
    ): PhotosResponse
} 