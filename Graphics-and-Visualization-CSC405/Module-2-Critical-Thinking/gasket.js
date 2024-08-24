/*
 Program Name: Sierpinski Gasket Vertex 2D
    Author: Alejandro (Alex) Ricciardi
    Date: 08/25/2024
    
    Program Description: 
    The program is a very simple WebGL application that displays a 2D representation of the Sierpinski Gasket.
*/


"use strict";


/** @type {WebGLRenderingContext} */
var gl;

var positions =[];
var numPositions = 5000; // Number of points to be generated 

/**
 * Initializes the WebGL context and generates the Sierpinski Gasket points.
 * Sets the graphic pipeline.
 *
 * @function
 * @name init
 */
window.onload = function init() {
    var canvas = document.getElementById("gl-canvas"); // Sets the HTML canvas
    gl = canvas.getContext('webgl2');
    if (!gl) alert( "WebGL 2.0 isn't available" );

    // ================================================================================
    /*-----------------------
     |   Initialize Gasket  |
     -----------------------*/

    // Corners of our gasket with three positions, a triangle.
    var vertices = [
        vec2(-1, -1),
        vec2(0,  1),
        vec2( 1, -1)
    ];

    // ------------------------------------------------------------------------------

    // Add the initial position to the array of points
    var u = add(vertices[0], vertices[1]);
    var v = add(vertices[0], vertices[2]);
    var p = mult(0.25, add( u, v )); // Computed point position inside the gasket

    positions.push(p);

    // ------------------------------------------------------------------------------

    // Compute new positions to generate the gasket
    // Each new point is located midway between the last point
    // the new point is randomly picked
    for ( var i = 0; positions.length < numPositions; ++i ) {
        var j = Math.floor(3*Math.random()); // vertex index picked randomly 

        // Calculate the midpoint
        p = add(positions[i], vertices[j]); 
        p = mult(0.5, p);
        positions.push(p);
    }

    // ================================================================================
    /*----------------------
     |   Configure WebGL   |
     ----------------------*/

    // Set view point and background
    gl.viewport(0, 0, canvas.width, canvas.height); // Set the viewport size
    gl.clearColor(1.0, 1.0, 1.0, 1.0); // Set the background color to white

    // Load shaders and initialize attribute buffers
    var program = initShaders(gl, "vertex-shader", "fragment-shader");
    gl.useProgram(program);

    // Load the data into the GPU
    var bufferId = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, bufferId );
    gl.bufferData(gl.ARRAY_BUFFER, flatten(positions), gl.STATIC_DRAW);

    // Associate out shader variables with our data buffer
    var positionLoc = gl.getAttribLocation(program, "aPosition");
    gl.vertexAttribPointer(positionLoc, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(positionLoc);

    render();
};

// ================================================================================

/**
 * Clears the canvas and renders the Sierpinski Gasket points.
 * 
 * @function
 * @name render
 */
function render() {
    gl.clear( gl.COLOR_BUFFER_BIT );
    gl.drawArrays(gl.POINTS, 0, positions.length);
}
