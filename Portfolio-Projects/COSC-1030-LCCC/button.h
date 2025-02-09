

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |  Ether's Quest                 *        Button class Declaration      *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*


The button class creates a button object to be displayed on a window.

	Accessor:

		void render() :
		Renders Button in the window

	Mutator:

		bool update():
		updated the color of the button if the button hovered or is pressed by the left button of the mouse.
		It returns true if the button was pressed.

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef BUTTON_H
#define BUTTON_H

	#ifdef _MSC_VER
		#pragma once
	#endif  // _MSC_VER

//#include <iostream> // For debugging purposes
//****** Headers lib. files, must be declared first
//****** Countains Global Variables INST_TYPE and INST_RESULTS, Ether struct, win_original_width, win_original_heigth
#include "hether.h"

// I had to add the SMFL Lib. in this file for it to work properly, even if this file was added in the headers for ether file 
// it may be an MS Visual Studio IDE issue.
// Multimedia Library Graphic
#include <SFML/Graphics.hpp> // https://www.sfml-dev.org
using namespace std;
using namespace sf; // SFML


	/*/////////////////////////
	--------------------------
	|          Class         |
	--------------------------
	////////////////////////*/

class Button {

		/*////////////////////////
		--------------------------
		|       Variables        |
		--------------------------
		////////////////////////*/

	// Variables
	string b_text;

	// Button box
	RectangleShape b_shape;
	RectangleShape b_shape_shadow; // shadow box
	Font font;
	Text text;

	// Position and size
	float x = 0.f, y = 0.f,
		  width = 0,f, height =0.f;
	
	// Window size
	float win_size_width = O_WIN_WD,
		  win_size_height = O_WIN_HT;

	// Colors
	Color idle_color = Color::White,
		hover_color = Color(176, 190, 197),
		click_color = Color(97, 97, 97),
		shadow = Color(207, 216, 220);


public:

		/*////////////////////////
		--------------------------
		|      Constructors      |
		--------------------------
		////////////////////////*/

	/*------------------
	 |                 |
	 |     Default     |
	 |                 |
	 ------------------*/

	Button();

	/*------------------
	 |                 |
	 |  Constructor-1  |
	 |                 |
	 ------------------*/
	Button(int x, int y, float width, float height, Font &font, string b_text);

	/*------------------
	 |                 |
	 |  Constructor-2  |
	 |                 |
	 ------------------*/
	Button(int x, int y, float width, float height,
		Font &font, string b_text,
		Color(idle_color), Color(hover_color), Color(click_color));

	/*------------------
	 |                 |
	 |  Constructor-3  |
	 |                 |
	 ------------------*/
	Button(int x, int y, float width, float height,
		Font &font, string b_text,
		Color(idle_color), Color(hover_color), Color(click_color),
		float wind_size_width, float wind_size_height);

		/*////////////////////////
		--------------------------
		|       Accessors        |
		--------------------------
		////////////////////////*/

	/*------------------------------
	 |                             |
	 |  Renders text box in window |
	 |                             |
	 ------------------------------*/
	void render(RenderWindow &window);

		/*////////////////////////
		--------------------------
		|        Mutators        |
		--------------------------
		////////////////////////*/

	/*-------------------------
	 |                        |
	 |  Update button's state | 
	 |  from mouse events     |
	 |                        |
	 -------------------------*/
	bool update(RenderWindow &window, int x, int y, bool left_pressed, bool left_click_released);

	/*----------------------------
	 |                           |
	 |  Changes the button text  |
	 |                           |
	 ----------------------------*/
	void set_text(string b_test);

}; // Button Class
#endif
