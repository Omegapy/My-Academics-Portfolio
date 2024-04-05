
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *  Errors window Functions definitions *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

  Handles file load errors


*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "ewindow.h"

/*------------------------------------
  |                                   |
  |  Renders error window and button  |
  |  Utlized by  err_load_file()      |
  |                                   |
  ------------------------------------*/
void render_err_window(RenderWindow &err_window, Button &btn, Text &disp_text) {
	err_window.clear();
	err_window.draw(disp_text);
	btn.render(err_window);
	err_window.display();
}

/*-----------------------------------------------------------
 |                                                          |
 |  Displays to the the game user a laod file error window, |
 |  if the file is not found or did not load                |
 |  successfully.                                           |
 |                                                          |
 -----------------------------------------------------------*/
void err_load_file(RenderWindow &game_window, Font &font, string file_path) {

	/*-------------
	 |  Variables  |
	 --------------*/

	// text object create
	Text disp_text;
	disp_text.setFont(font);

	// Creates a string to use as a message error
	string err_text = "A file load error occurred!\nThe file \"" + file_path + "\" was not find or did not load succefully!";

	// Sets the font text style
	disp_text.setCharacterSize(18);
	disp_text.setString(err_text);
	// Position the text in window
	disp_text.setPosition(10.0f, 20.0f);

	// Window and button
	RenderWindow err_window(VideoMode(err_text.size() * 7, 150), "File Load Error", Style::Titlebar | Style::Close);

	// button
	Button b_ok(((err_text.size() * 7) / 2)-5, 105, 60.0f, 30.0f,
		       font, "ok", Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34), err_window.getSize().x, err_window.getSize().y);

	/*---------------------
	 | Function processes |
	 ---------------------*/

	 // Renders window
	render_err_window(err_window, b_ok, disp_text);

	// Game error window instance open
	while (err_window.isOpen()) {

		Event event;

		while (err_window.pollEvent(event)) { // Checks events in the err_window

			switch (event.type) { // Checks events type
			//-- Keyword events
			case Event::KeyReleased:
				switch (event.key.code) {
				case Keyboard::Escape:
					err_window.close();
					game_window.close();
					exit(-1);
					break;
				}
				break;
			//-- Mouse events
			// Left mouse button pressed
			case Event::MouseButtonPressed:
				if (event.key.code == Mouse::Left) {
					b_ok.update(err_window, Mouse::getPosition(err_window).x, Mouse::getPosition(err_window).y, true, false);
					// Renders window
					render_err_window(err_window, b_ok, disp_text);
				}
				break;
			// Left mouse button Released
			case Event::MouseButtonReleased:
				switch (event.key.code) {
				case Mouse::Left:
					if (b_ok.update(err_window, Mouse::getPosition(err_window).x, Mouse::getPosition(err_window).y, false, true)) {
						err_window.close();
						game_window.close();
						exit(-1);
					}
					break;
				}
				break;
			//-- Window events
			// Close window exit game
			case Event::Closed:
				game_window.close();
				err_window.close();
				exit(-1);
			// Hover
			case Event::MouseMoved:
				b_ok.update(err_window, Mouse::getPosition(err_window).x, Mouse::getPosition(err_window).y, false, false);
				render_err_window(err_window, b_ok, disp_text);
				break;
			// Window resized
			case Event::Resized:
				render_err_window(err_window, b_ok, disp_text);
				break;
			default:
				// event not listed
				break;
			} // Switch event
		} // While event			
	} // While err_window is open
} // err_load_file()
