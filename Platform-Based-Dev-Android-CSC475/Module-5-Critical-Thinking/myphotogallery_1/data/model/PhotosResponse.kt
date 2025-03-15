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

package com.example.myphotogallery_1.data.model

import com.google.gson.annotations.SerializedName

/**
 * Response model for the Pexels API photos endpoint.
 * 
 * This class encapsulates the complete response from Pexels API photo-related endpoints,
 * including pagination information and the list of photos.
 * Used for both curated photos and search results responses.
 *
 * MVVM Component: MODEL - API response data class
 * Role: Represents the structure of network responses before they're processed
 *       into domain models for the rest of the application
 * 
 * @property page The current page number in paginated results
 * @property perPage The number of photos per page in the response
 * @property photos The list of photo objects returned in this response
 * @property totalResults The total number of results available for the request
 * @property nextPage URL to fetch the next page of results, null if there are no more pages
 * @property prevPage URL to fetch the previous page of results, null if this is the first page
 */
data class PhotosResponse(
    val page: Int,
    @SerializedName("per_page")
    val perPage: Int,
    val photos: List<Photo>,
    @SerializedName("total_results")
    val totalResults: Int,
    @SerializedName("next_page")
    val nextPage: String? = null,
    @SerializedName("prev_page")
    val prevPage: String? = null
) 