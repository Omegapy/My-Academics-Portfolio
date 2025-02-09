/*
Program Name: Rotating Cube - WebGL
Author: Alejandro (Alex) Ricciardi
Date: 10/06/2024

Program Description: 
    This program is version 3 of 
    - the Module-5 Portfolio Milestone: https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Module-5-Portfolio-Milestone
    - and Portfolio Milestone version 2: https://github.com/Omegapy/My-Academics-Portfolio/tree/main/Graphics-and-Visualization-CSC405/Portfolio-Project/Portfolio-Milestone

    This program displays a 3D rotating cube in WebGL.
    It implements an interactive viewer that can be toggled between orthographic and perspective projections.
    It also implements an interactive Blinn-Phong lighting that can be toggled between on and off state.
    The program implements the Painter's Algorithm for hidden surface removal.
    Users can rotate the cube along the X, Y, and Z axes, stop the rotation, 
    and reset all parameters using buttons. Additionally, users can resize the cube using a slider.

    The program also implements the Painter's Algorithm for Hidden Surface Removal (HSR). 
    The Painter's Algorithm sorts the cube’s faces to simulate depth 
    without relying on the WebGL z-buffer to remove hidden surfaces.
*/

"use strict";

/**
 * Main function - runs the cube rendering and projection logic.
 * It initializes the WebGL context, creates the 3D cube, and provides event handlers for interactions.
 * Implements the Painter's Algorithm for hidden surface removal.
 */
var rotatingCube = function() {

    // ================================================================================
    /*-------------------- 
    |   Initialization   |
    ---------------------*/

    var canvas; // Reference to the HTML canvas element
    var gl;     // WebGL context for rendering
    
    var numPositions = 36;  // Number of positions (vertices) for the cube (6 faces * 2 triangles per face * 3 vertices per triangle)

    var cubeSize = 1.5; // Default size of the cube (can be changed by the slider)

    var vertices = []; // Array to store the cube's vertices
    var faces = [];    // Array to store the cube's faces with their associated data (indices, color, normal)

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
        size: 1.5
    };

    // Optimized parameters for perspective projection
    const perspectiveParams = {
        depth: 20,
        radius: 10,
        theta: 0,
        phi: 0,
        size: 1.5
    };
    
    var near, far;    // Near and far clipping planes for the projection
    var radius;       // Radius for spherical camera position
    var theta;        // Camera angle (vertical)
    var phi;          // Camera angle (horizontal)

    var left, right, top, bottom;  // View volume boundaries for orthographic projection

    //--- Rotation variables ---
    
    var angleX = 0, angleY = 0, angleZ = 0; // Angles for rotating the cube
    var currentAxis = initialValues.currentAxis; // Current rotation axis
    var stopRotation = initialValues.stopRotation; // Flag to stop rotation

    //--- View variables ---

    var modelViewMatrix, projectionMatrix; // Matrices for the model-view and projection transformations
    var modelViewMatrixLoc, projectionMatrixLoc, normalMatrixLoc; // Locations of these matrices in the shader
    var eye;   // Camera position in the scene
    const at = vec3(0.0, 0.0, 0.0); // Look-at point (origin)
    const up = vec3(0.0, 1.0, 0.0); // Up vector for the camera

    // Buffer variables
    var vBufferId, cBufferId, nBufferId; // Buffer IDs for position, color, and normal data
    var aPositionLoc, aColorLoc, aNormalLoc; // Attribute locations

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
            vec4(-cubeSize, -cubeSize,  cubeSize, 1.0),  // Vertex 0: Front bottom left
            vec4(-cubeSize,  cubeSize,  cubeSize, 1.0),  // Vertex 1: Front top left
            vec4(cubeSize, cubeSize,  cubeSize, 1.0),    // Vertex 2: Front top right
            vec4(cubeSize, -cubeSize,  cubeSize, 1.0),   // Vertex 3: Front bottom right
            vec4(-cubeSize, -cubeSize,  -cubeSize, 1.0), // Vertex 4: Back bottom left
            vec4(-cubeSize, cubeSize,  -cubeSize, 1.0),  // Vertex 5: Back top left
            vec4(cubeSize, cubeSize,  -cubeSize, 1.0),   // Vertex 6: Back top right
            vec4(cubeSize, -cubeSize,  -cubeSize, 1.0)   // Vertex 7: Back bottom right
        ];
    }

    generateVertices(); // Generate the initial vertices based on the default cube size

    // ----------------------------------------------------------------------------

    // Predefined colors for each face of the cube
    var faceColors = [
        vec4(1.0, 0.0, 0.0, 1.0),  // Face 0: Red
        vec4(0.0, 1.0, 0.0, 1.0),  // Face 1: Green
        vec4(0.0, 0.0, 1.0, 1.0),  // Face 2: Blue
        vec4(1.0, 1.0, 0.0, 1.0),  // Face 3: Yellow
        vec4(1.0, 0.0, 1.0, 1.0),  // Face 4: Magenta
        vec4(0.0, 1.0, 1.0, 1.0)   // Face 5: Cyan
    ];

    // Indices for each face (quad defined by four vertex indices)
    var faceIndices = [
        [1, 0, 3, 2], // Face 0: Front
        [2, 3, 7, 6], // Face 1: Right
        [3, 0, 4, 7], // Face 2: Bottom
        [6, 5, 1, 2], // Face 3: Top
        [4, 5, 6, 7], // Face 4: Back
        [5, 4, 0, 1]  // Face 5: Left
    ];

    // ----------------------------------------------------------------------------

    /**
     * Builds the faces array, storing face data including vertex indices, color, normal, and positions.
     * This function is called whenever the cube's size changes.
     */
    function buildFaces() {
        // Empty the faces array to be filed by the new faces data to be rendered
        faces = []; 
        for (var i = 0; i < faceIndices.length; i++) {
            var indices = faceIndices[i];

            // Compute the face normal
            var t1 = subtract(vertices[indices[1]], vertices[indices[0]]);
            var t2 = subtract(vertices[indices[2]], vertices[indices[1]]);
            var normal = normalize(cross(t1, t2));
            normal = vec3(normal);

            // Store face data
            var face = {
                indices: indices,
                color: faceColors[i],
                normal: normal,
                depth: 0,
                positions: [
                    vertices[indices[0]],
                    vertices[indices[1]],
                    vertices[indices[2]],
                    vertices[indices[3]]
                ]
            };
            faces.push(face);
        }
    }

    buildFaces(); // Build the initial faces

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

        var program = initShaders(gl, "vertex-shader", "fragment-shader"); // Initialize shaders
        gl.useProgram(program); // Use the shader program

        // Get attribute locations
        aPositionLoc = gl.getAttribLocation(program, "aPosition");
        aColorLoc = gl.getAttribLocation(program, "aColor");
        aNormalLoc = gl.getAttribLocation(program, "aNormal");

        // Enable the attributes
        gl.enableVertexAttribArray(aPositionLoc);
        gl.enableVertexAttribArray(aColorLoc);
        gl.enableVertexAttribArray(aNormalLoc);

        // Create buffers
        vBufferId = gl.createBuffer();
        cBufferId = gl.createBuffer();
        nBufferId = gl.createBuffer();

        // Get uniform locations in the shader
        modelViewMatrixLoc = gl.getUniformLocation(program, "uModelViewMatrix");
        projectionMatrixLoc = gl.getUniformLocation(program, "uProjectionMatrix");
        normalMatrixLoc = gl.getUniformLocation(program, "uNormalMatrix");
        uUseLightingLoc = gl.getUniformLocation(program, "uUseLighting");

        // Set the initial lighting state (on)
        gl.uniform1i(uUseLightingLoc, useLighting);

        // Light Properties
        var lightPosition = vec4(2.0, 2.0, 2.0, 1.0);  // Light position in world space
        var materialShininess = 100.0;  // Shininess factor for specular highlights

        // Pass light properties as uniforms to the shader
        gl.uniform4fv(gl.getUniformLocation(program, "uLightPosition"), flatten(lightPosition));
        gl.uniform1f(gl.getUniformLocation(program, "uShininess"), materialShininess);

        // Initialize projection parameters (set the projection to orthographic initially)
        setParametersForProjection(currentProjection);

        //---- Event listeners ---- 

        // Depth Slider
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

        // Radius Slider
        document.getElementById("radiusSlider").onchange = function(event) {
            radius = parseFloat(event.target.value); // Update radius based on the slider value
        };

        // Theta Slider
        document.getElementById("thetaSlider").onchange = function(event) {
            theta = parseFloat(event.target.value) * Math.PI / 180.0; // Convert degrees to radians
        };

        // Phi Slider
        document.getElementById("phiSlider").onchange = function(event) {
            phi = parseFloat(event.target.value) * Math.PI / 180.0; // Convert degrees to radians
        };

        // Size Slider
        document.getElementById("sizeSlider").onchange = function(event) {
            cubeSize = parseFloat(event.target.value); // Update the cube size
            generateVertices(); // Regenerate vertices based on new size
            buildFaces(); // Rebuild the faces with the new size
        };

        // Rotation Buttons
        document.getElementById("rotateXBtn").onclick = function() {
            currentAxis = 'x'; // Rotate around the x-axis
            stopRotation = false; // Allow rotation
        };
        document.getElementById("rotateYBtn").onclick = function() {
            currentAxis = 'y'; // Rotate around the y-axis
            stopRotation = false; // Allow rotation
        };
        document.getElementById("rotateZBtn").onclick = function() {
            currentAxis = 'z'; // Rotate around the x-axis
            stopRotation = false; // Allow rotation
        };
        document.getElementById("stopBtn").onclick = function() {
            stopRotation = true; // Stop the rotation
        };

        // Reset Button
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
            buildFaces();

            // Reset lighting
            useLighting = true;
            gl.uniform1i(uUseLightingLoc, useLighting);
            document.getElementById("toggleLightingBtn").textContent = "Turn Off Lighting";
        };

        // Toggle Projection Button
        document.getElementById("toggleProjectionBtn").onclick = function() {
            if (currentProjection === "orthographic") {
                currentProjection = "perspective";
            } else {
                currentProjection = "orthographic";
            }
            setParametersForProjection(currentProjection);
        };

        // Toggle Lighting Button
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
     * Implements the Painter's Algorithm by sorting faces based on depth and rendering them back-to-front.
     */
    var render = function() {
        gl.clear(gl.COLOR_BUFFER_BIT); // Clear the screen

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
            } else if (currentAxis === 'y') {
                angleY += 1;
            } else if (currentAxis === 'z') {
                angleZ += 1;
            }
        }

        // Apply rotations to the model-view matrix
        modelViewMatrix = mult(modelViewMatrix, rotateX(angleX));
        modelViewMatrix = mult(modelViewMatrix, rotateY(angleY));
        modelViewMatrix = mult(modelViewMatrix, rotateZ(angleZ));

        // Compute the normal matrix for lighting calculations
        var normalMatrix = normalMatrixFromMV(modelViewMatrix);

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

        // Send the projection matrix to the shader
        gl.uniformMatrix4fv(projectionMatrixLoc, false, flatten(projectionMatrix));

        //--------------------------------------------------------------------------

        /*-----------------------------------------------
        |                                              |
        |      Painter's Algorithm Implementation      |
        |                                              |
        |----------------------------------------------*/

        //------ Compute depth for each face
        for (var i = 0; i < faces.length; i++) {
            var face = faces[i];
            var depthSum = 0;

            // Iterate over each vertex of the face
            for (var j = 0; j < face.positions.length; j++) {
                // Apply the model-view matrix to transform the vertex to camera space
                var transformedVertex = mult(modelViewMatrix, face.positions[j]);
                // Sum up the Z-coordinates (depth) of the transformed vertices
                depthSum += transformedVertex[2]; // Z-coordinate in camera space
            }
            
            // Store the average Z-depth of the face (used for sorting)
            face.depth = depthSum / 4; // Average depth of the face (since each face has 4 vertices)
        }

        //------- Sort faces based on depth (from farthest to nearest)
        faces.sort(function(a, b) {
            // Sort faces by depth to implement back-to-front rendering (Painter's Algorithm)
            return a.depth - b.depth; // Faces with higher Z-values (farther) are rendered first
        });

//------- Render faces in sorted order (back-to-front)
for (var i = 0; i < faces.length; i++) {
    var face = faces[i];

    // Prepare arrays for storing the vertex positions, colors, and normals of the face
    var facePositions = [];
    var faceColors = [];
    var faceNormals = [];

    // Form two triangles for each face from the four vertex indices (quad -> 2 triangles)
    var indices = face.indices;
    // Create 6 indices (two triangles) from the 4 vertices of the face
    var idx = [indices[0], indices[1], indices[2], indices[0], indices[2], indices[3]];

    // Loop through the indices and populate the positions, colors, and normals arrays
    for (var j = 0; j < idx.length; j++) {
        facePositions.push(vertices[idx[j]]); // Add the vertex positions
        faceColors.push(face.color);          // Assign the color of the face
        faceNormals.push(face.normal);        // Assign the face's normal vector for lighting
    }

    // Bind and fill the position buffer with vertex data for the current face
    gl.bindBuffer(gl.ARRAY_BUFFER, vBufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(facePositions), gl.STATIC_DRAW);
    gl.vertexAttribPointer(aPositionLoc, 4, gl.FLOAT, false, 0, 0); // Set attribute pointer

    // Bind and fill the color buffer with color data for the current face
    gl.bindBuffer(gl.ARRAY_BUFFER, cBufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(faceColors), gl.STATIC_DRAW);
    gl.vertexAttribPointer(aColorLoc, 4, gl.FLOAT, false, 0, 0); // Set attribute pointer

    // Bind and fill the normal buffer with normal vectors for the current face
    gl.bindBuffer(gl.ARRAY_BUFFER, nBufferId);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(faceNormals), gl.STATIC_DRAW);
    gl.vertexAttribPointer(aNormalLoc, 3, gl.FLOAT, false, 0, 0); // Set attribute pointer

    // Send the model-view matrix and the normal matrix to the vertex shader
    gl.uniformMatrix4fv(modelViewMatrixLoc, false, flatten(modelViewMatrix));
    gl.uniformMatrix3fv(normalMatrixLoc, false, flatten(normalMatrix));

    // Render the face as 2 triangles (6 vertices total) using the drawArrays function
    gl.drawArrays(gl.TRIANGLES, 0, 6);
}

        //--------------------------------------------------------------------

        // Request the next frame for continuous rendering
        requestAnimationFrame(render);
    }

    // ----------------------------------------------------------------------------

    /**
     * Computes the normal matrix from the model-view matrix.
     * The normal matrix is the inverse transpose of the upper-left 3x3 part of the model-view matrix.
     *
     * @param {mat4} mvMatrix - The model-view matrix.
     * @returns {mat3} - The normal matrix.
     */
    function normalMatrixFromMV(mvMatrix) {
        var upperLeft3x3 = [
            vec3(mvMatrix[0][0], mvMatrix[0][1], mvMatrix[0][2]),
            vec3(mvMatrix[1][0], mvMatrix[1][1], mvMatrix[1][2]),
            vec3(mvMatrix[2][0], mvMatrix[2][1], mvMatrix[2][2])
        ];
        var normalMatrix = inverse3(upperLeft3x3);
        normalMatrix = transpose(normalMatrix);
        return normalMatrix;
    }

    // ----------------------------------------------------------------------------

}();


