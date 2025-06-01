/*
 Program Name: Rotating 3D Cube with Toggleable Projection and Lighting
 Author: Alejandro (Alex) Ricciardi
 Date: 10/06/2024

 Program Description: 
    This program is version 2 of the Module-5 Portfolio Milestone: https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Module-5-Portfolio-Milestone
    It displays a 3D rotating cube in WebGL.
    It implements an interactive viewer that can be toggled between orthographic and perspective projections.
    It also implements an interactive Blinn-Phong lighting that can be toggled between on and off state.
    Users can rotate the cube along the X, Y, and Z axes, stop the rotation, 
    and reset all parameters using buttons. Additionally, users can resize the cube using a slider.
*/

"use strict";

/**
 * Main function - runs the cube rendering and projection logic.
 * It initializes the WebGL context, creates the 3D cube, and provides event handlers for interactions
 */
var cubeToggle = function() {

    // ================================================================================
    /*-------------------- 
    |   Initialization   |
    ---------------------*/

    var canvas; // Reference to the HTML canvas element
    var gl;     // WebGL context for rendering
    
    var numPositions = 36;  // Number of positions (vertices) for the cube (6 faces * 2 triangles per face * 3 vertices per triangle)

    var cubeSize = 1; // Default size of the cube (can be changed by the slider)

    var positionsArray = []; // Array to hold vertex positions
    var colorsArray = [];    // Array to hold vertex colors
    var normalsArray = [];   // Array to hold normal vectors for lighting

    var vertices; // Array to store the cube's vertices

    //--- Projections ---

    // Initial values for angles, projection type, and rotation axis
    const initialValues = {
        angleX: 0,
        angleY: 0,
        angleZ: 0,
        projectionType: "orthographic",  // Default projection
        currentAxis: 'y',  // Start rotating around the y-axis
        stopRotation: false  // Control whether the rotation stops
    };

    var currentProjection = initialValues.projectionType; // Stores the current projection mode

    // Optimized parameters for orthographic projection
    const orthoParams = {
        depth: 10,
        radius: 4,
        theta: 0,
        phi: 0,
        size: 1
    };

    // Optimized parameters for perspective projection
    const perspectiveParams = {
        depth: 20,
        radius: 8,
        theta: 0,
        phi: 0,
        size: 1
    };

    
    var near, far;    // Near and far clipping planes for the projection
    var radius;       // Radius for spherical camera position
    var theta;        // Camera angle (vertical)
    var phi;          // Camera angle (horizontal)

    var left, right, top, bottom;  // View volume boundaries for orthographic projection

    //--- Projections ---
    
    var angleX = 0, angleY = 0, angleZ = 0; // Angles for rotating the cube
    var currentAxis = initialValues.currentAxis; // Current rotation axis
    var stopRotation = initialValues.stopRotation; // Flag to stop rotation

    //--- Views ---

    var modelViewMatrix, projectionMatrix; // Matrices for the model-view and projection transformations
    var modelViewMatrixLoc, projectionMatrixLoc, normalMatrixLoc; // Locations of these matrices in the shader
    var eye;   // Camera position in the scene
    const at = vec3(0.0, 0.0, 0.0); // Look-at point (origin)
    const up = vec3(0.0, 1.0, 0.0); // Up vector for the camera

    var vBufferId, cBufferId, nBufferId; // Buffer IDs for position, color, and normal data

    // Lighting variables
    var useLighting = true; // Lighting is enabled by default
    var uUseLightingLoc;    // Location of the lighting uniform in the shader

    // ================================================================================
    /*--------------------
     |   Configuration   |
     ---------------------*/

    /**
     * Generates the vertices for the cube based on the current size.
     * Vertices are defined in homogeneous coordinates (vec4), where the fourth component is 1.0.
     */
    function generateVertices() {
        vertices = [
            vec4(-cubeSize, -cubeSize,  cubeSize, 1.0),  // Front bottom left
            vec4(-cubeSize,  cubeSize,  cubeSize, 1.0),  // Front top left
            vec4(cubeSize, cubeSize,  cubeSize, 1.0),    // Front top right
            vec4(cubeSize, -cubeSize,  cubeSize, 1.0),   // Front bottom right
            vec4(-cubeSize, -cubeSize,  -cubeSize, 1.0), // Back bottom left
            vec4(-cubeSize, cubeSize,  -cubeSize, 1.0),  // Back top left
            vec4(cubeSize, cubeSize,  -cubeSize, 1.0),   // Back top right
            vec4(cubeSize, -cubeSize,  -cubeSize, 1.0)   // Back bottom right
        ];
    }

    generateVertices(); // Generate the initial vertices based on the default cube size

    // ----------------------------------------------------------------------------

    // Predefined colors for each face of the cube
    var faceColors = [
        vec4(1.0, 0.0, 0.0, 1.0),  // Red
        vec4(0.0, 1.0, 0.0, 1.0),  // Green
        vec4(0.0, 0.0, 1.0, 1.0),  // Blue
        vec4(1.0, 1.0, 0.0, 1.0),  // Yellow
        vec4(1.0, 0.0, 1.0, 1.0),  // Magenta
        vec4(0.0, 1.0, 1.0, 1.0)   // Cyan
    ];

    // ----------------------------------------------------------------------------

    /**
     * Creates a quad (a face of the cube) by specifying four vertices and a color.
     * Each quad is split into two triangles, which are added to the `positionsArray`.
     * Normals and colors are also generated for each vertex.
     *
     * @param {number} a - Index of the first vertex.
     * @param {number} b - Index of the second vertex.
     * @param {number} c - Index of the third vertex.
     * @param {number} d - Index of the fourth vertex.
     * @param {vec4} color - The color to apply to this face of the cube.
     */
    function quad(a, b, c, d, color) {
        var t1 = subtract(vertices[b], vertices[a]); // Vector from a to b
        var t2 = subtract(vertices[c], vertices[b]); // Vector from b to c
        var normal = normalize(cross(t1, t2)); // Compute the normal vector for the face
        normal = vec3(normal); // Convert to vec3 format (drop the 4th component)

        // Add two triangles (6 vertices) for this face
        positionsArray.push(vertices[a]);
        colorsArray.push(color);
        normalsArray.push(normal);

        positionsArray.push(vertices[b]);
        colorsArray.push(color);
        normalsArray.push(normal);

        positionsArray.push(vertices[c]);
        colorsArray.push(color);
        normalsArray.push(normal);

        positionsArray.push(vertices[a]);
        colorsArray.push(color);
        normalsArray.push(normal);

        positionsArray.push(vertices[c]);
        colorsArray.push(color);
        normalsArray.push(normal);

        positionsArray.push(vertices[d]);
        colorsArray.push(color);
        normalsArray.push(normal);
    }

    // ----------------------------------------------------------------------------

    /**
     * Creates the cube by calling `quad` for each of the six faces.
     * Each face is assigned a different color.
     */
    function colorCube() {
        positionsArray = [];
        colorsArray = [];
        normalsArray = [];
        quad(1, 0, 3, 2, faceColors[0]); // Front face - Red
        quad(2, 3, 7, 6, faceColors[1]); // Right face - Green
        quad(3, 0, 4, 7, faceColors[2]); // Bottom face - Blue
        quad(6, 5, 1, 2, faceColors[3]); // Top face - Yellow
        quad(4, 5, 6, 7, faceColors[4]); // Back face - Magenta
        quad(5, 4, 0, 1, faceColors[5]); // Left face - Cyan
    }

    // ----------------------------------------------------------------------------

    /**
     * Initializes the WebGL context, shaders, and buffers, and sets up the cube for rendering.
     * Binds the generated cube vertices, colors, and normals to WebGL buffers.
     * Adds event listeners to sliders and buttons for user interaction.
     */
    window.onload = function init() {
        canvas = document.getElementById("gl-canvas"); // Reference to the canvas element
        gl = canvas.getContext('webgl'); // Initialize WebGL context
        if (!gl) alert("WebGL isn't available");

        gl.viewport(0, 0, canvas.width, canvas.height); // Set the viewport size to match the canvas
        gl.clearColor(0.0, 0.0, 0.0, 1.0); // Set the background color (black)
        gl.enable(gl.DEPTH_TEST); // Enable depth testing to handle overlapping geometry

        var program = initShaders(gl, "vertex-shader", "fragment-shader"); // Initialize shaders
        gl.useProgram(program); // Use the shader program

        colorCube(); // Generate the cube geometry

        // Position Buffer (binds the cube vertices to the buffer)
        vBufferId = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW); // Upload position data to the GPU

        var aPosition = gl.getAttribLocation(program, "aPosition");
        gl.vertexAttribPointer(aPosition, 4, gl.FLOAT, false, 0, 0); // Describe the layout of position data
        gl.enableVertexAttribArray(aPosition); // Enable the position attribute in the shader

        // Color Buffer (binds the colors to the buffer)
        cBufferId = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, cBufferId);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW); // Upload color data to the GPU

        var aColor = gl.getAttribLocation(program, "aColor");
        gl.vertexAttribPointer(aColor, 4, gl.FLOAT, false, 0, 0); // Describe the layout of color data
        gl.enableVertexAttribArray(aColor); // Enable the color attribute in the shader

        // Normal Buffer (binds the normal vectors for lighting to the buffer)
        nBufferId = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, nBufferId);
        gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW); // Upload normal data to the GPU

        var aNormal = gl.getAttribLocation(program, "aNormal");
        gl.vertexAttribPointer(aNormal, 3, gl.FLOAT, false, 0, 0); // Describe the layout of normal data
        gl.enableVertexAttribArray(aNormal); // Enable the normal attribute in the shader

        // Get uniform locations in the shader
        modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix");
        projectionMatrixLoc = gl.getUniformLocation(program, "uProjectionMatrix");
        normalMatrixLoc = gl.getUniformLocation(program, "uNormalMatrix");
        uUseLightingLoc = gl.getUniformLocation(program, "uUseLighting");

        // Set the initial lighting state (on)
        gl.uniform1i(uUseLightingLoc, useLighting);

        // Light Properties
        var lightPosition = vec4(2.0, 2.0, 2.0, 1.0);  // Light position in world space
        var lightAmbient = vec4(0.2, 0.2, 0.2, 1.0);   // Ambient light component
        var lightDiffuse = vec4(1.0, 1.0, 1.0, 1.0);   // Diffuse light component
        var lightSpecular = vec4(1.0, 1.0, 1.0, 1.0);  // Specular light component

        var materialShininess = 100.0;  // Shininess factor for specular highlights

        // Pass light properties as uniforms to the shader
        gl.uniform4fv(gl.getUniformLocation(program, "uLightPosition"), flatten(lightPosition));
        gl.uniform1f(gl.getUniformLocation(program, "uShininess"), materialShininess);

        // Initialize projection parameters (set the projection to orthographic initially)
        setParametersForProjection(currentProjection);

        //---- listeners ---- 

        // Event listeners for interacting with sliders and buttons
        document.getElementById("depthSlider").onchange = function(event) {
            var depth = parseFloat(event.target.value);
            if (currentProjection === "orthographic") {
                far = depth / 2;
                near = -depth / 2;
            } else {
                near = 0.1;
                far = depth;
            }
        };

        //--- Sliders

        document.getElementById("radiusSlider").onchange = function(event) {
            radius = parseFloat(event.target.value); // Update radius based on the slider value
        };

        document.getElementById("thetaSlider").onchange = function(event) {
            theta = parseFloat(event.target.value) * Math.PI / 180.0; // Convert degrees to radians
        };

        document.getElementById("phiSlider").onchange = function(event) {
            phi = parseFloat(event.target.value) * Math.PI / 180.0; // Convert degrees to radians
        };

        document.getElementById("sizeSlider").onchange = function(event) {
            cubeSize = parseFloat(event.target.value); // Update the cube size
            generateVertices(); // Regenerate vertices based on new size
            colorCube(); // Rebuild the cube with the new size

            // Update buffers with the new vertices, colors, and normals
            gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

            gl.bindBuffer(gl.ARRAY_BUFFER, cBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW);

            gl.bindBuffer(gl.ARRAY_BUFFER, nBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW);
        };

        //--- Buttons

        document.getElementById("rotateXBtn").onclick = function() {
            currentAxis = 'x'; // Rotate around the X-axis
            stopRotation = false; // Allow rotation
        };
        document.getElementById("rotateYBtn").onclick = function() {
            currentAxis = 'y'; // Rotate around the Y-axis
            stopRotation = false; // Allow rotation
        };
        document.getElementById("rotateZBtn").onclick = function() {
            currentAxis = 'z'; // Rotate around the Z-axis
            stopRotation = false; // Allow rotation
        };
        document.getElementById("stopBtn").onclick = function() {
            stopRotation = true; // Stop the rotation
        };

        //--- Reset button to restore initial values
        document.getElementById("resetBtn").onclick = function() {
            // Reset all parameters to their initial values
            angleX = initialValues.angleX;
            angleY = initialValues.angleY;
            angleZ = initialValues.angleZ;
            currentProjection = initialValues.projectionType;
            currentAxis = initialValues.currentAxis;
            stopRotation = initialValues.stopRotation;
            setParametersForProjection(currentProjection);

            generateVertices();
            colorCube();

            // Update the buffers
            gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

            gl.bindBuffer(gl.ARRAY_BUFFER, cBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW);

            gl.bindBuffer(gl.ARRAY_BUFFER, nBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW);

            // Reset lighting
            useLighting = true;
            gl.uniform1i(uUseLightingLoc, useLighting);
            document.getElementById("toggleLightingBtn").textContent = "Turn Off Lighting";
        };

        //--- Toggle the projection between orthographic and perspective
        document.getElementById("toggleProjectionBtn").onclick = function() {
            if (currentProjection === "orthographic") {
                currentProjection = "perspective";
            } else {
                currentProjection = "orthographic";
            }
            setParametersForProjection(currentProjection);

            generateVertices();
            colorCube();

            // Update buffers
            gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(positionsArray), gl.STATIC_DRAW);

            gl.bindBuffer(gl.ARRAY_BUFFER, cBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(colorsArray), gl.STATIC_DRAW);

            gl.bindBuffer(gl.ARRAY_BUFFER, nBufferId);
            gl.bufferData(gl.ARRAY_BUFFER, flatten(normalsArray), gl.STATIC_DRAW);
        };

        //--- Toggle lighting on/off
        document.getElementById("toggleLightingBtn").onclick = function() {
            useLighting = !useLighting; // Toggle the lighting state
            gl.uniform1i(uUseLightingLoc, useLighting); // Update the lighting uniform in the shader

            // Update button text
            if (useLighting) {
                this.textContent = "Turn Off Lighting";
            } else {
                this.textContent = "Turn On Lighting";
            }
        };

        render(); // Start the rendering loop
    }

    // ----------------------------------------------------------------------------

    /**
     * Sets the parameters for the current projection (either orthographic or perspective).
     * Updates the view volume and projection matrix settings based on the selected projection type.
     *
     * @param {string} projectionType - The current projection type ("orthographic" or "perspective").
     */
    function setParametersForProjection(projectionType) {
        if (projectionType === "orthographic") {
            near = -orthoParams.depth / 2;
            far = orthoParams.depth / 2;
            radius = orthoParams.radius;
            theta = orthoParams.theta * Math.PI / 180.0;
            phi = orthoParams.phi * Math.PI / 180.0;
            cubeSize = orthoParams.size;

            // Update the slider values to match orthographic projection settings
            document.getElementById("depthSlider").value = orthoParams.depth;
            document.getElementById("radiusSlider").value = orthoParams.radius;
            document.getElementById("thetaSlider").value = orthoParams.theta;
            document.getElementById("phiSlider").value = orthoParams.phi;
            document.getElementById("sizeSlider").value = orthoParams.size;

            // Update the projection display text
            document.getElementById("projectionDisplay").textContent = "Current Projection: Orthographic";
        } else {
            near = 0.1;
            far = perspectiveParams.depth;
            radius = perspectiveParams.radius;
            theta = perspectiveParams.theta * Math.PI / 180.0;
            phi = perspectiveParams.phi * Math.PI / 180.0;
            cubeSize = perspectiveParams.size;

            // Update the slider values to match perspective projection settings
            document.getElementById("depthSlider").value = perspectiveParams.depth;
            document.getElementById("radiusSlider").value = perspectiveParams.radius;
            document.getElementById("thetaSlider").value = perspectiveParams.theta;
            document.getElementById("phiSlider").value = perspectiveParams.phi;
            document.getElementById("sizeSlider").value = perspectiveParams.size;

            // Update the projection display text
            document.getElementById("projectionDisplay").textContent = "Current Projection: Perspective";
        }
    }

    // ----------------------------------------------------------------------------

    /**
     * Main render loop that continuously updates and draws the scene.
     * It updates the cube's rotation, applies the current projection, and redraws the cube.
     */
    var render = function() {
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT); // Clear the screen

        // Compute the eye (camera) position in spherical coordinates
        eye = vec3(
            radius * Math.sin(theta) * Math.cos(phi),
            radius * Math.sin(theta) * Math.sin(phi),
            radius * Math.cos(theta)
        );
        modelViewMatrix = lookAt(eye, at, up); // Compute the model-view matrix

        // Rotate the cube if rotation is not stopped
        if (!stopRotation) {
            if (currentAxis === 'x') {
                angleX += 1;
                modelViewMatrix = mult(modelViewMatrix, rotateX(angleX)); // Rotate around X-axis
            } else if (currentAxis === 'y') {
                angleY += 1;
                modelViewMatrix = mult(modelViewMatrix, rotateY(angleY)); // Rotate around Y-axis
            } else if (currentAxis === 'z') {
                angleZ += 1;
                modelViewMatrix = mult(modelViewMatrix, rotateZ(angleZ)); // Rotate around Z-axis
            }
        }

        // Compute the normal matrix for lighting calculations
        var normalMatrix = [
            vec3(modelViewMatrix[0][0], modelViewMatrix[0][1], modelViewMatrix[0][2]),
            vec3(modelViewMatrix[1][0], modelViewMatrix[1][1], modelViewMatrix[1][2]),
            vec3(modelViewMatrix[2][0], modelViewMatrix[2][1], modelViewMatrix[2][2])
        ];
        normalMatrix = inverse3(normalMatrix);
        normalMatrix = transpose(normalMatrix);

        // Set up the projection matrix
        if (currentProjection === "orthographic") {
            var aspect = canvas.width / canvas.height;
            var viewSize = 5; // Adjust the view volume size for better visibility
            left = -viewSize * aspect;
            right = viewSize * aspect;
            bottom = -viewSize;
            top = viewSize;
            projectionMatrix = ortho(left, right, bottom, top, near, far); // Orthographic projection
        } else {
            var fovy = 60.0; // Field of view for perspective projection
            var aspect = canvas.width / canvas.height;
            projectionMatrix = perspective(fovy, aspect, near, far); // Perspective projection
        }

        // Send the matrices to the shader
        gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
        gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));
        gl.uniformMatrix3fv(normalMatrixLoc, false, flatten(normalMatrix));

        // Draw the cube using the vertex data
        gl.drawArrays(gl.TRIANGLES, 0, numPositions);

        // Request the next frame for continuous rendering
        requestAnimationFrame(render);
    }

    // ----------------------------------------------------------------------------

}();

