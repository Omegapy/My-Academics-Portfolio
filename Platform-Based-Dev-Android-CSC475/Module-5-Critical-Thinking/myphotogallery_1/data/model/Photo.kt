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
 * Data model representing a photo from the Pexels API
 * This class encapsulates all the properties of a photo returned by the Pexels API.
 * It is the core data structure for photos
 *
 * @property id The unique identifier
 * @property width The width in pixels
 * @property height The height in pixels
 * @property url The Pexels URL
 * @property photographer The name of the photographer
 * @property photographerUrl The URL to the photographer's Pexels profile
 * @property photographerId The unique identifier of the photographer (stored as Long to handle large values)
 * @property avgColor The average color of the photo represented as a HEX code (e.g., "#FFFFFF")
 * @property src URLs to the photo in various resolutions
 * @property liked Indicates whether the photo has been liked by the user (API Key)
 * @property alt Alternative text description of the photo
 */
data class Photo(
    val id: Int,
    val width: Int,
    val height: Int,
    val url: String,
    val photographer: String,
    @SerializedName("photographer_url")
    val photographerUrl: String,
    @SerializedName("photographer_id")
    val photographerId: Long,
    @SerializedName("avg_color")
    val avgColor: String,
    val src: PhotoSource,
    val liked: Boolean,
    val alt: String
)

//-------------------------------------------------------------------------------------------

/**
 * Data model, different resolution sources for a photo.
 * contains URLs to the same photo in different resolutions and aspect ratios
 * 
 * @property original The original resolution
 * @property large2x A large version of the photo with width of 1880px
 * @property large A large version of the photo with width of 940px
 * @property medium A medium version of the photo with width of 700px (used in grid views)
 * @property small A small version of the photo with width of 400px
 * @property portrait A vertical crop of the photo with height of 1200px and width of 800px
 * @property landscape A horizontal crop of the photo with height of 627px and width of 940px
 * @property tiny A tiny version of the photo with width of 280px (used for thumbnails)
 */
data class PhotoSource(
    val original: String,
    val large2x: String,
    val large: String,
    val medium: String,
    val small: String,
    val portrait: String,
    val landscape: String,
    val tiny: String
) 