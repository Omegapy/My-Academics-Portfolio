
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------******************************************----------------------------------
  |                                *                                        *                                 |
  |   Ether's Quest                * Exit game window Functions Definitions *                                 |
  |                                *                                        *                                 |
  ---------------------------------******************************************---------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

	   Contains the Exit Game window Functions Definitions

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "exit_game.h"

/*-----------------------------------------------
 |                                              |
 |  Displays exit game window text and button.  |
 |                                              |
 -----------------------------------------------*/
void display_exit_window(RenderWindow &exit_window, Button &btn1, Button btn2, Text &disp_text) {

	exit_window.clear();
	exit_window.draw(disp_text);
	btn1.render(exit_window);
	btn2.render(exit_window);
	exit_window.display();
}

////////////////////////////////////////////////////////////////

/*--------------------------------------------------
 |                                                 |
 |  Renders the exit game window, text and button. |
 |                                                 |
 --------------------------------------------------*/
int exit_game(Font &font) {

	/*-------------
	 |  Variables  |
	 --------------*/

	// text object 
	Text disp_text;
	disp_text.setFont(font);

	// Sets the font text style
	disp_text.setCharacterSize(18);
	disp_text.setString("Do you want to exit the game?");
	// Position the text in window
	disp_text.setPosition(70.0f, 20.0f);

	// Window and button
	RenderWindow window(VideoMode(400, 150), "Exit Game", Style::Titlebar | Style::Close);

	// Button Class
	Button btn1(100, 75, 75.0f, 30.0f,
		font, "Yes", Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34), 
		400, 150);
	Button btn2(200, 75, 75.0f, 30.0f,
		font, "No", Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34),
		400, 150);

	/*---------------------
	 | Function processes |
	 ---------------------*/


	// Displays the img and opens the window
	display_exit_window(window, btn1, btn2, disp_text);

	// Game window instance open
	while (window.isOpen()) { // Run while the game window is open

		Event event;

		while (window.pollEvent(event)) { // Checks events in the window

			switch (event.type) { // Checks events type
			//--Keyword events
			// Escape exit game
			case Event::KeyReleased:
				switch (event.key.code) {
				case Keyboard::Escape:
					return -1;
					break;
				}
				break;
			//-- Mouse events
			// Mouse left button pressed
			case Event::MouseButtonPressed:
				if (event.key.code == Mouse::Left) {

					btn1.update(window, Mouse::getPosition(window).x, Mouse::getPosition(window).y, true, false);
					btn2.update(window, Mouse::getPosition(window).x, Mouse::getPosition(window).y, true, false);
					// renders window
					display_exit_window(window, btn1, btn2, disp_text);
					break;
				}
				break;
				// Mouse left button released
			case Event::MouseButtonReleased:
				if (event.key.code == Mouse::Left) {
					if (btn1.update(window, Mouse::getPosition(window).x, Mouse::getPosition(window).y, false, true)) {
						exit(0); // Exits the game
					}
					else if (btn2.update(window, Mouse::getPosition(window).x, Mouse::getPosition(window).y, false, true)) {
						return -1; // Returns to the game
					}
				}
				break;
			// Hover
			case Event::MouseMoved:
				btn1.update(window, Mouse::getPosition(window).x, Mouse::getPosition(window).y, false, false);
				btn2.update(window, Mouse::getPosition(window).x, Mouse::getPosition(window).y, false, false);
				display_exit_window(window, btn1, btn2, disp_text);
				break;
				//-- Window events
				// close window exit game
			case Event::Closed:
				return -1;
				break;
				// Resized window
			case Event::Resized:
				// renders window
				display_exit_window(window, btn1, btn2, disp_text);
				break;
			default:
				// event not listed
				break;
			} // switch type of event
		} // While event
	} // while game_window is open
}// exit_game()
