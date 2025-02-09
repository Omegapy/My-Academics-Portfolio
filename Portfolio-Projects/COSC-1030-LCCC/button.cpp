

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *       Button class definitions       *                                 |
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

	/*////////////////////////
	--------------------------
	|        Headers         |
	--------------------------
	////////////////////////*/


#include "button.h"


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
Button::Button() {
	// Empty
}


 /*------------------
  |                 |
  |  Constructor-1  |
  |                 |
  ------------------*/
Button::Button(int x, int y, float width, float height, Font &font, string b_text) {

	// Box
	b_shape.setPosition(Vector2f(x, y));
	b_shape.setSize(Vector2f(width, height));
	b_shape.setFillColor(idle_color);
	// Shadow box
	b_shape_shadow.setPosition(Vector2f(x + 2, y + 2));
	b_shape_shadow.setSize(Vector2f(width, height));
	b_shape_shadow.setFillColor(shadow);

	// Position and size
	this->x = x;
	this->y = y;
	this->width = width;
	this->height = height;

	// Text
	text.setPosition(x + width / 2.0f - (b_text.size()*9.0f)/20.f, y + height / 2.0f - 10.0f);
	this->font = font;
	text.setFont(font);
	text.setString(b_text);
	text.setFillColor(Color::Black);
	text.setCharacterSize(16);
	text.setStyle(Text::Style::Bold);

} // Constructor-1 Button()


 /*------------------
  |                 |
  |  Constructor-2  |
  |                 |
  ------------------*/
Button::Button::Button(int x, int y, float width, float height,
	Font &font, string b_text,
	Color(idle_color), Color(hover_color), Color(click_color)) {

	// Button shape
	b_shape.setPosition(Vector2f(x, y));
	b_shape.setSize(Vector2f(width, height));
	b_shape.setFillColor(idle_color);
	// Shadow
	b_shape_shadow.setPosition(Vector2f(x + 2, y + 2));
	b_shape_shadow.setSize(Vector2f(width, height));
	b_shape_shadow.setFillColor(shadow);

	// Position and size
	this->x = x;
	this->y = y;
	this->width = width;
	this->height = height;

	// Text
	text.setPosition(x + width / 2.0f - (b_text.size() * 9) / 2.0f, y + height / 2.0f - 10.0f);
	this->font = font;
	this->b_text = b_text;
	text.setFont(font);
	text.setString(b_text);
	text.setFillColor(Color::Black);
	text.setCharacterSize(16);
	text.setStyle(Text::Style::Bold);

	// Button colors
	this->idle_color = idle_color;
	this->hover_color = hover_color;
	this->click_color = click_color;
	this->shadow = shadow;


} // constructor-2 Button()

/*------------------
  |                 |
  |  Constructor-3  |
  |                 |
  ------------------*/
Button::Button::Button(int x, int y, float width, float height,
	Font &font, string b_text,
	Color(idle_color), Color(hover_color), Color(click_color), float wind_size_width, float wind_size_height) {

	// Button shape
	b_shape.setPosition(Vector2f(x, y));
	b_shape.setSize(Vector2f(width, height));
	b_shape.setFillColor(idle_color);
	// Shadow
	b_shape_shadow.setPosition(Vector2f(x + 2, y + 2));
	b_shape_shadow.setSize(Vector2f(width, height));
	b_shape_shadow.setFillColor(shadow);

	// Position and size
	this->x = x;
	this->y = y;
	this->width = width;
	this->height = height;

	this->win_size_width = wind_size_width;
	this->win_size_height = wind_size_height;

	// Text
	text.setPosition(x + width / 2.0f - (b_text.size() * 9) / 2.0f, y + height / 2.0f - 10.0f);
	this->font = font;
	this->b_text = b_text;
	text.setFont(font);
	text.setString(b_text);
	text.setFillColor(Color::Black);
	text.setCharacterSize(16);
	text.setStyle(Text::Style::Bold);

	// Button colors
	this->idle_color = idle_color;
	this->hover_color = hover_color;
	this->click_color = click_color;
	this->shadow = shadow;


} // constructor-3 Button()
 

		/*////////////////////////
		--------------------------
		|       Accessors        |
		--------------------------
		////////////////////////*/

 /*------------------------------
  |                             |
  |  Renders Button in window   |
  |                             |
  ------------------------------*/
void Button::render(RenderWindow &window) {

	window.draw(b_shape_shadow);
	window.draw(b_shape);
	window.draw(text);
}

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
bool Button::update(RenderWindow &window, int x, int y, bool left_pressed, bool left_click_released) {

	/*-------------
	 |  Variables  |
	 --------------*/

	Vector2u resized_window_size = window.getSize();
	Vector2f box = b_shape.getPosition();
	Vector2f box_size = b_shape.getSize();

	// Coumpute the scale of the window related to the original window size
	float x_s = resized_window_size.x / win_size_width;
	float y_s = resized_window_size.y / win_size_height;

	/*---------------------
	 | Function processes |
	 ---------------------*/ 

	// Troubleshoot mouse position
	/*cout << x_s << "  " << y_s << "\n";
	cout << box.x * x_s << " < " << x << " < " << box_size.x * x_s + box.x << "\n"
		<< box.y * y_s << " < " << y << " < " << box_size.y * y_s + box.y << "\n\n";*/

	 // Check mouse position and mouse left click event
	 // if Left Mouse button pressed
	if ((box.x * x_s < x ) && (x < box_size.x * x_s + box.x)
		&& (box.y * y_s < y) && (y < box.y * y_s + box_size.y)
		&& left_pressed && !left_click_released) { // Mouse on button being pressed

		b_shape.setFillColor(click_color);
		return false;

	}
	// if Left Mouse button Realease
	else if ((box.x * x_s < x) && (x < box_size.x * x_s + box.x)
		&& (box.y * y_s < y) && (y < box.y * y_s + box_size.y)
		&& !left_pressed && left_click_released) { // Mouse on button realease

		b_shape.setFillColor(idle_color);
		return true;

	} // if hover no click
	else if ((box.x * x_s < x) && (x < box_size.x * x_s + box.x)
		&& (box.y * y_s < y) && (y < box.y * y_s + box_size.y)
		&& !left_pressed && !left_click_released) { // Mouse on button not being pressed

		b_shape.setFillColor(hover_color);
		return false;

	} // Idle
	else {// Mouse Not on button 

		b_shape.setFillColor(idle_color);
		return false;
	}
	
	throw "ERROR: something went wrong with Button::update()";

} // update ()

/*----------------------------
 |                           |
 |  Changes the button text  |
 |                           |
 ----------------------------*/
void Button::set_text(string b_text) {
	this->b_text = b_text;
	text.setPosition(x + width / 2.0f - (b_text.size() * 9) / 2, y + height / 2.0f - 10.0f);
}

	

