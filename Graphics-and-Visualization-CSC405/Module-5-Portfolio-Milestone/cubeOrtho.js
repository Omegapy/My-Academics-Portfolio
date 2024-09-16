/*
 Program Name: Rotating 3D Cube with Adjustable Size
 Author: Alejandro (Alex) Ricciardi
 Date: 09/08/2024
    
 Program Description: 
    This program creates a simple rotating colored 3D cube using WebGL 
    The user can rotate the cube along the X, Y, and Z axes and move it up, down, left, and right
    The user can also pause and restart the rotation while moving the cube
    Additionally, the program includes orthographic projection and sliders to adjust viewing parameters:
    Depth, Radius, Theta, Phi, and Size.
    The size slider allows the user to adjust the dimensions of the cube dynamically.
    This program visits the concepts of transformation in computer graphics, more specifically quaternion rotation, translation, scaling, and viewing transformations.
*/

"use strict";
// ================================================================================

/*----------------------
|   Global Variables   |
-----------------------*/

// Global variables
var canvas;  // Reference to the HTML canvas element where the cube will be rendered
var gl;      // WebGL context, used to draw and render graphics in the canvas

var numPositions = 36;  // Number of vertices (6 faces * 2 triangles per face * 3 vertices per triangle)
var positions = [];     // Store the cube's vertex positions
var colors = [];        // Store the cube's vertex colors for each face

// Constants for rotation axes
var xAxis = 0;   
var yAxis = 1;   
var zAxis = 2;   
var axis = 0;    // Default rotation axis (initially set to X-axis)

// Control for rotation and animation (pause/restart)
var rotationActive = true;  // Determine if the rotation is active
var animationFrameId;       // Store the requestAnimationFrame ID to control animation (pause/restart)

// Rotation and translation variables
var theta = [0, 0, 0];  // Hold rotation angles for the x, y, and z axes
var thetaLoc;           // Uniform location for the rotation angles in the vertex shader
var translation = [0.0, 0.0];  // Translation offsets for x and y axes (moves the cube)
var translationLoc;     // Uniform location for the translation in the vertex shader

// Variables for viewing parameters the view 
// near and far define the visible depth range along the Z-axis in the camera's view space.
var near = -5; // near plane - clipping planes for the projection
var far = 5; // far plane - clipping planes for the projection
// radius controls the distance from the camera to the origin along a spherical surface
var radius = 0.1;
var thetaView = 0.1;
var phi = 0.1;
// viewing volume, viewing Cube box, 
var left = -1.0; // left side of the viewing volume along the x-axis.
var right = 1.0; // right side of the viewing volume along the x-axis.
var ytop = 1.0; // top of the viewing volume along the y-axis
var bottom = -1.0; // bottom of the viewing volume along the y-axis.

var eye;  // Eye (camera) position in 3D space
var at = vec3(0.0, 0.0, 0.0);  // Look-at point - The point the camera is looking at (the center of the scene)
var up = vec3(0.0, 1.0, 0.0);  // Up vector - The up direction for the camera - y-axis

var modelViewMatrix, projectionMatrix;  // Matrices for transformations - model-view and projection transformations
var modelViewMatrixLoc, projectionMatrixLoc;  // Uniform locations for the matrices

// Variable for cube size
var cubeSize = 0.5;  // Default size of the cube (edge length)
var sizeSliderValue = 0.5;  // Value from the size slider

// ================================================================================

/*-------------------
|   Main Function   |
---------------------*/

/**
 * Initializes the WebGL context, shaders, and sets up event listeners for the cube's control
 */
window.onload = function init() {
    // Get the canvas element by its ID
    canvas = document.getElementById("gl-canvas");

    // ================================================================================
    /*-------------------- 
    |   Initialization   |
    ---------------------*/

    // Initialize the WebGL context for rendering the cube
    gl = canvas.getContext("webgl2");
    if (!gl) {
        alert("WebGL 2.0 isn't available"); // Display an error if WebGL 2.0 is not supported
    }

    // Load and compile the vertex and fragment shaders
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);  // Use the shader program

    // ================================================================================
    /*--------------------
     |   Configuration   |
     ---------------------*/

    // ------------------------------ vertices and colors ----------------------------

    // Define the cube's vertices and colors
    colorCube();

    // ----------------------------------- Viewport ---------------------------------

    // Configure WebGL viewport (visible part of the canvas)
    gl.viewport(0, 0, canvas.width, canvas.height);  // Set the viewport size to match the canvas
    gl.clearColor(0.0, 0.0, 0.0, 1.0);  // Set the background color to black
    // Enable depth testing to handle hidden surfaces behind others
    // Without it, when rotating, the faces will overlap incorrectly
    gl.enable(gl.DEPTH_TEST);  

    // ---------------------------------- Buffers --------------------------------------

    // --- Position buffer
    // Create and bind buffers for vertex positions
    var vBuffer = gl.createBuffer(); // Store the vertex positions in buffer
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW); // Data position to the GPU

    // Link the position buffer to the aPosition attribute in the vertex shader
    var positionLoc = gl.getAttribLocation(program, "aPosition"); // Store and retrieve the index location of the aPosition attribute from the compiled shader
    gl.vertexAttribPointer(positionLoc, 4, gl.FLOAT, false, 0, 0); // Define the position data format to be processed by WebGL
    gl.enableVertexAttribArray(positionLoc); // Link point location and aPosition to be used during rendering

    // --- Color buffer    
    // Create and bind buffers for vertex colors
    var cBuffer = gl.createBuffer(); // Store the colors of the vertices in buffer
    gl.bindBuffer(gl.ARRAY_BUFFER, cBuffer); 
    gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW); // Data color to the GPU

    // Link the color buffer to the aColor attribute in the vertex shader
    var colorLoc = gl.getAttribLocation(program, "aColor"); // Store and retrieve the location of the aColor attribute from the compiled shader
    gl.vertexAttribPointer(colorLoc, 4, gl.FLOAT, false, 0, 0); // Define the colors data format to be processed by WebGL
    gl.enableVertexAttribArray(colorLoc); // Link point location and color to be used during rendering

    // ---------------------------------- Get Uniform Locations  ----------------------

    // Get the uniform locations for the rotation angles, translation, and matrices in the vertex shader
    thetaLoc = gl.getUniformLocation(program, "uTheta"); // passing rotation angles to the shader
    translationLoc = gl.getUniformLocation(program, "uTranslation"); // passing translatio
    modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix"); // passing transformation matrices view
    projectionMatrixLoc = gl.getUniformLocation(program, "uProjectionMatrix"); // passing transformation matrices view projection 

    // Get the uniform location for the cube size
    var cubeSizeLoc = gl.getUniformLocation(program, "uCubeSize");

    // ---------------------------------- Event listeners ----------------------------------

    // --- Slider value update function
    function updateSliderValue(id, value) {
        document.getElementById(id).innerText = value;
    }

    // --- Sliders for viewing parameters
    document.getElementById("depthSlider").oninput = function(event) {
        var val = parseFloat(event.target.value);
        near = -val / 2; // Set the near clipping plane to half the negative value
        far = val / 2; // he far clipping plane to half the positive valu
        updateSliderValue("depthValue", val);
    };

    // --- Update the radius variable, controlling the distance of the eye (camera) from the origin
    document.getElementById("radiusSlider").oninput = function(event) {
        radius = parseFloat(event.target.value);
        updateSliderValue("radiusValue", radius);
    };

    // --- Update the spherical coordinates thetaView for positioning the camera 
    document.getElementById("thetaSlider").oninput = function(event) {
        thetaView = parseFloat(event.target.value);
        updateSliderValue("thetaValue", thetaView);
    };

    // --- Update the spherical coordinates phi for positioning the camera around the scene.
    document.getElementById("phiSlider").oninput = function(event) {
        phi = parseFloat(event.target.value);
        updateSliderValue("phiValue", phi);
    };

    // --- Slider for cube size
    document.getElementById("sizeSlider").oninput = function(event) {
        sizeSliderValue = parseFloat(event.target.value);
        cubeSize = sizeSliderValue;
        updateSliderValue("sizeValue", sizeSliderValue);

        // Recalculate the cube's positions with the new size
        positions = []; // Clear the positions array
        colorCube();    // Recalculate positions
        // Update the position buffer with new positions
        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);
    };

    // --- Rotation buttons
    // Event listeners for rotation buttons (x, y, z)
    document.getElementById("xButton").onclick = function () {
        axis = xAxis;  // Set the rotation axis to x
    };
    document.getElementById("yButton").onclick = function () {
        axis = yAxis;  // Set the rotation axis to y
    };
    document.getElementById("zButton").onclick = function () {
        axis = zAxis;  // Set the rotation axis to z
    };

    // --- Translation buttons
    // Event listeners for translation buttons (Up, Down, Left, Right)
    document.getElementById("upButton").onclick = function () {
        translation[1] += 0.1; // Move the cube up (increase y translation)
    };
    document.getElementById("downButton").onclick = function () {
        translation[1] -= 0.1; // Move the cube down (decrease y translation)
    };
    document.getElementById("rightButton").onclick = function () {
        translation[0] -= 0.1; // Move the cube right (decrease x translation)
    };
    document.getElementById("leftButton").onclick = function () {
        translation[0] += 0.1; // Move the cube left (increase x translation)
    };

    // --- Reset button
    // Event listener for reset button to reset rotation, translation, and size
    document.getElementById("resetButton").onclick = function () {
        // Reset rotation angles, translation, and viewing parameters to the original state
        theta = [0, 0, 0];    // Reset all rotation angles to 0
        translation = [0.0, 0.0]; // Reset translation to the center
        axis = xAxis;  // Reset the rotation axis to x

        // Reset viewing parameters
        near = -5;
        far = 5;
        radius = 0.1;
        thetaView = 0.1;
        phi = 0.1;

        // Reset cube size
        cubeSize = 0.5;
        sizeSliderValue = 0.5;

        // Update slider values
        document.getElementById("depthSlider").value = 10;
        updateSliderValue("depthValue", 10);
        document.getElementById("radiusSlider").value = radius;
        updateSliderValue("radiusValue", radius);
        document.getElementById("thetaSlider").value = thetaView;
        updateSliderValue("thetaValue", thetaView);
        document.getElementById("phiSlider").value = phi;
        updateSliderValue("phiValue", phi);
        document.getElementById("sizeSlider").value = cubeSize;
        updateSliderValue("sizeValue", cubeSize);

        // Recalculate the cube's positions with the default size
        positions = []; // Clear the positions array
        colorCube();    // Recalculate positions
        // Update the position buffer with new positions
        gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);
    };

    // --- Pause and restart rotation buttons
    // Event listener for Pause Rotation button
    document.getElementById("pauseButton").onclick = function () {
        rotationActive = false; // Stop rotation but allow translation
    };
    // Event listener for Restart Rotation button
    document.getElementById("restartButton").onclick = function () {
        if (!rotationActive) {
            rotationActive = true; // Restart rotation
        }
    };

    // ------------------------------------------------------------------------------

    // Start the rendering loop 
    render();
};

// ================================================================================

/**
 * Defines the vertices and colors for each face of the cube.
 * Each face is created using two triangles.
 */
function colorCube() {
    // Clear any existing positions and colors
    positions = [];
    colors = [];

    // Define the six faces of the cube, each face is made up of two triangles
    quad(1, 0, 3, 2, vec4(1.0, 0.0, 0.0, 1));  // Front face - Red
    quad(2, 3, 7, 6, vec4(0.0, 1.0, 0.0, 1.0));  // Right face - Green
    quad(3, 0, 4, 7, vec4(0.0, 0.0, 1.0, 1.0));  // Bottom face - Blue
    quad(6, 5, 1, 2, vec4(1.0, 1.0, 0.0, 1.0));  // Top face - Yellow
    quad(4, 5, 6, 7, vec4(1.0, 0.0, 1.0, 1.0));  // Back face - Magenta
    quad(5, 4, 0, 1, vec4(0.0, 1.0, 1.0, 1.0));  // Left face - Cyan
}

// ================================================================================

/**
 * Creates two triangles from a quad (4 vertices) and assigns colors to each face.
 * A quad is a quadrilateral, which is a four-sided polygon.
 * In this program, the quad represents 2 triangles making a face of the cube.
 * 
 * @param {number} a - Index of the first vertex of the quad
 * @param {number} b - Index of the second vertex of the quad
 * @param {number} c - Index of the third vertex of the quad
 * @param {number} d - Index of the fourth vertex of the quad
 * @param {Array} color - The color assigned to the face of the cube
 */
function quad(a, b, c, d, color) {
    // Vertices of the cube, each represented as vec4 (x, y, z, w)
    // These vertices define the eight corners of a cube, centered at the origin
    var hs = cubeSize / 2; // Half size of the cube

    var vertices = [
        vec4(-hs, -hs,  hs, 1.0),  // Vertex 0: Bottom-left front
        vec4(-hs,  hs,  hs, 1.0),  // Vertex 1: Top-left front
        vec4( hs,  hs,  hs, 1.0),  // Vertex 2: Top-right front
        vec4( hs, -hs,  hs, 1.0),  // Vertex 3: Bottom-right front
        vec4(-hs, -hs, -hs, 1.0),  // Vertex 4: Bottom-left back
        vec4(-hs,  hs, -hs, 1.0),  // Vertex 5: Top-left back
        vec4( hs,  hs, -hs, 1.0),  // Vertex 6: Top-right back
        vec4( hs, -hs, -hs, 1.0)   // Vertex 7: Bottom-right back
    ];

    // Indices to define the two triangles for each face
    var indices = [a, b, c, a, c, d];

    // Push the vertices and colors for each triangle into the buffers
    for (var i = 0; i < indices.length; ++i) {
        positions.push(vertices[indices[i]]);  // Add vertex position
        colors.push(color);  // Add color to the face
    }
}

// ================================================================================

/**
 * Converts degrees to radians.
 * @param {number} degrees - The angle in degrees.
 * @returns {number} The angle in radians.
 */
function radians(degrees) {
    return degrees * Math.PI / 180.0;
}

// ================================================================================

/**
 * Handles the rendering of the cube.
 * Recursive function - creates an animation 
 */
function render() {
    // Clear the canvas and the depth buffer
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // Even if rotation is paused, translation should still occur
    if (rotationActive) {
        // Increment the rotation angle for the selected axis
        theta[axis] += 2.0;
    }

    // Compute eye position in spherical coordinates
    var thetaRad = radians(thetaView);
    var phiRad = radians(phi);

    eye = vec3(
        radius * Math.sin(thetaRad) * Math.cos(phiRad),
        radius * Math.sin(thetaRad) * Math.sin(phiRad),
        radius * Math.cos(thetaRad)
    );

    // Compute model-view and projection matrices
    modelViewMatrix = lookAt(eye, at, up);
    projectionMatrix = ortho(left, right, bottom, ytop, near, far);

    // Send the updated rotation angles, translation values, cube size, and matrices to the vertex shader
    gl.uniform3fv(thetaLoc, theta);
    gl.uniform2fv(translationLoc, translation);
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
    gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));

    // Draw the cube (6 faces * 2 triangles per face * 3 vertices per triangle = 36 vertices)
    gl.drawArrays(gl.TRIANGLES, 0, numPositions);

    // Recursion case
    // Request another frame for continuous rendering (animation)
    animationFrameId = requestAnimationFrame(render);
}
