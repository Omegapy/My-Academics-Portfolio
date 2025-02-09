
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *    Instances Functions Definitions   *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

	   Contains the none fight instance functions definitions

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////


#include "instances.h"


/*----------------------------------------
|                                       |
|  Displays 1 button instances          |
|  Place and Monster                    |
|  Utilized by render_1btn_instances()  |
|                                       |
----------------------------------------*/
void display_1btn_instances(RenderWindow &game_window, Sprite &img, Button &btn, Text &p_state_text) {

	// Clear the screen (fill it with black color)
	game_window.clear();
	// Displays the img and opens the window
	game_window.draw(img);
	btn.render(game_window);
	game_window.draw(p_state_text);
	game_window.display();

}

////////////////////////////////////////////////////////////////

/*----------------------------------------
 |                                       |
 |  Renders 1 button instances           |
 |  Place and Monster                    |
 |                                       |
 ----------------------------------------*/
int render_1btn_instances(RenderWindow &game_window, Image &img, Font &font, int type, Ether &player, int num_ambience, int num_voice, int amb_volume) {

	/*-------------
	 |  Variables  |
	 --------------*/

	int click = -1;
	string btn_text, player_state = " ";

	// Assignes the button text and the click return type
	if (type == MONSTER) { // Monster instance	
		click = FIGHT;
		btn_text = "Fight";
		player_state = "Ether    Health: " + to_string(player.health) + "  Armor: " + to_string(player.armor) + "  Strengh: " + to_string(player.strength);
	}
	else { // Place instance
		click = CONTINUE;
		btn_text = "Continue";
	}

	// Renders button
	// Scale button to rezised window, if resized
	float x = game_window.getSize().x / (2.0f * game_window.getSize().x / O_WIN_WD),
		  y = (game_window.getSize().y) / (1.09 * game_window.getSize().y / O_WIN_HT);
	// button
	Button btn(x, y, 100.0f, 30.0f,
		       font, btn_text, Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34));
	// Renders back ground image
	Texture texture;
	texture.loadFromImage(img);
	Sprite img_background(texture);
	// Original loaded size of the img
	Vector2f targetsize(1279.0f, 713.0f);
	// Sets the image as same size of the window
	img_background.setScale(
		targetsize.x / img_background.getLocalBounds().width,
		targetsize.y / img_background.getLocalBounds().height);

	// Renders text
	Text p_state_text;
	// Sets the font text style
	p_state_text.setFont(font);
	p_state_text.setCharacterSize(16);
	p_state_text.setFillColor(Color::Cyan);
	p_state_text.setString(player_state);
	// Position the text in window
	p_state_text.setPosition(850.0f, 665.0f);


	//-- sound variables
	string name_amb = "ambiences/amb" + to_string(num_ambience) + ".wav";
	string name_voice = "voices/Slide " + to_string(num_voice) + ".wav";
	Music amb, voice;
	// Ambience
	// Checks if the file was opened successfully
	if (!amb.openFromFile(name_amb)) { // If not displays an error message and exits program
		err_load_file(game_window, font, name_amb);
	}
	amb.setLoop(true);
	amb.setVolume(amb_volume);
	// Narrator
	voice.openFromFile(name_voice);
	// Checks if the file was opened successfully
	if (!voice.openFromFile(name_voice)) { // If not displays an error message and exits program
		err_load_file(game_window, font, name_voice);
	}

	/*---------------------
	 | Function processes |
	 ---------------------*/

	// Displays the img and opens the window
	display_1btn_instances(game_window, img_background, btn, p_state_text);
	// Plays sound
	amb.play();
	voice.play();

	// Game window instance open
	while (game_window.isOpen()) { // Run while the game window is open

		Event event;

		while (game_window.pollEvent(event)) { // Checks events in game_window

			switch (event.type) { //-- Checks events type
			//-- Keyword events
			// Escape exit game
			case Event::KeyReleased:
				switch (event.key.code) {
				case Keyboard::Escape:
					exit_game(font);
					break;
				}
				break;
			//--- Mouse events
			// Left mouse button pressed
			case Event::MouseButtonPressed:
				if (event.key.code == Mouse::Left) {

					btn.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, true, false);
					// renders window
					display_1btn_instances(game_window, img_background, btn, p_state_text);
					break;
				}
				break;
			// Left mouse button Released
			case Event::MouseButtonReleased:
				if (event.key.code == Mouse::Left) { // Released mouse left button
					if (btn.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, true)) { // Button clicked
						amb.stop();
						voice.stop();
						return click;
					}
				}
				break;
			// Hover
			case Event::MouseMoved:
				btn.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, false);
				display_1btn_instances(game_window, img_background, btn, p_state_text);
				break;
			//-- Window events
			// window closed
			case Event::Closed:
				exit(0); // Exits game
				break;
			// Resized window
			case Event::Resized:
				display_1btn_instances(game_window, img_background, btn, p_state_text);
				break;
			default:
				// event not listed
				break;
			} // switch type of event
		} // While event
	} // while game_window is open
} // render_1btn_instances()

////////////////////////////////////////////////////////////////

/*--------------------------------------------------
 |                                                 |
 |  Displays 2 buttons instances                   |
 |  Quest and Direction (left or right) instances  |
 |  Utilized by render_2btn_instances()            |
 |                                                 |
 --------------------------------------------------*/
void display_2btn_instances(RenderWindow &game_window, Sprite &img, Button &btn1, Button &btn2, Text p_state_text) {

	game_window.clear();
	game_window.draw(img);
	btn1.render(game_window);
	btn2.render(game_window);
	game_window.draw(p_state_text);
	game_window.display();
}

////////////////////////////////////////////////////////////////

/*--------------------------------------------------
 |                                                 |
 |  Renders 2 buttons instances                    |
 |  Quest and Direction (left or right) instances  |
 |                                                 |
 --------------------------------------------------*/
int render_2btn_instances(RenderWindow &game_window, Image &img, Font &font, int type, Ether &player, int num_ambience, int num_voice, int amb_volume) {

	/*-------------
	 |  Variables  |
	 --------------*/

	int btn1_click = -1, btn2_click = -1;
	string btn1_text, btn2_text;

	// Assignes the button text and the click return type
	if (type == QUEST) { // Quest instance	
		btn1_click = ACCEPT;
		btn2_click = REJECT;
		btn1_text = "Accept";
		btn2_text = "Reject";
	}
	else { // Place instance
		btn1_click = LEFT;
		btn2_click = RIGHT;
		btn1_text = "LEFT";
		btn2_text = "Right";
	}

	// Button Class
	// Scale buttons to rezised window, if resized
	float x_1 = game_window.getSize().x / (12.0f * game_window.getSize().x / O_WIN_WD),
		  x_2 = game_window.getSize().x / (4.0f * game_window.getSize().x / O_WIN_WD),
		  y = (game_window.getSize().y) / (1.09 * game_window.getSize().y / O_WIN_HT);
	// button
	Button btn1(x_1, y, 100.0f, 30.0f,
		        font, btn1_text, Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34));
	Button btn2(x_2, y, 100.0f, 30.0f,
		        font, btn2_text, Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34));

	// Image rendering variables
	Texture texture;
	texture.loadFromImage(img);
	Sprite img_background(texture);
	// Original loaded size of the img
	Vector2f targetsize(1279.0f, 713.0f);
	// Sets the image as same size of the window
	img_background.setScale(
		targetsize.x / img_background.getLocalBounds().width,
		targetsize.y / img_background.getLocalBounds().height);

	// Renders text
	string player_state = "Ether    Health: " + to_string(player.health) + "  Armor: " + to_string(player.armor) + "  Strengh: " + to_string(player.strength);
	Text p_state_text;
	// Sets the font text style
	p_state_text.setFont(font);
	p_state_text.setCharacterSize(16);
	p_state_text.setFillColor(Color::Cyan);
	p_state_text.setString(player_state);
	// Position the text in window
	p_state_text.setPosition(850.0f, 965.0f);

	//-- sound variables
	string name_amb = "ambiences/amb" + to_string(num_ambience) + ".wav";
	string name_voice = "voices/Slide " + to_string(num_voice) + ".wav";
	Music amb, voice;
	// Ambience
	// Checks if the file was opened successfully
	if (!amb.openFromFile(name_amb)) { // If not displays an error message and exits program
		err_load_file(game_window, font, name_amb);
	}
	amb.setLoop(true);
	amb.setVolume(amb_volume);
	// Narrator
	voice.openFromFile(name_voice);
	// Checks if the file was opened successfully
	if (!voice.openFromFile(name_voice)) { // If not displays an error message and exits program
		err_load_file(game_window, font, name_voice);
	}

	/*---------------------
	 | Function processes |
	 ---------------------*/

	// Displays the img and opens the window
	display_2btn_instances(game_window, img_background, btn1, btn2, p_state_text);
	// Plays sound
	amb.play();
	voice.play();

	// Game window instance open
	while (game_window.isOpen()) { // Run while the game window is open


		Event event;

		while (game_window.pollEvent(event)) { // Checks events in the err_window

			switch (event.type) { // Checks events type
			//--Keyword events
			// Escape exit game
			case Event::KeyReleased:
				switch (event.key.code) {
				case Keyboard::Escape:
					return EXIT;
					break;
				}
				break;
			//-- Mouse events
			// Mouse left button pressed
			case Event::MouseButtonPressed:
				if (event.key.code == Mouse::Left) {

					btn1.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, true, false);
					btn2.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, true, false);
					// renders window
					display_2btn_instances(game_window, img_background, btn1, btn2, p_state_text);
					break;
				}
				break;
			// Mouse left button released
			case Event::MouseButtonReleased:
				if (event.key.code == Mouse::Left) {
					if (btn1.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, true)) { // Button-1 clicked
						amb.stop();
						voice.stop();
						return btn1_click;
					}
					else if (btn2.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, true)) { // Button-2 clicked
						amb.stop();
						voice.stop();
						return btn2_click;
					}
				}
				break;
			// Hover
			case Event::MouseMoved:
				btn1.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, false);
				btn2.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, false);
				display_2btn_instances(game_window, img_background, btn1, btn2, p_state_text);
				break;
			//-- Window events
			// close window exit game
			case Event::Closed:
				exit(0); // Exits game
				break;
			// Resized window
			case Event::Resized:
				// renders window
				display_2btn_instances(game_window, img_background, btn1, btn2, p_state_text);
				break;
			default:
				// event not listed
				break;
			} // switch type of event
		} // While event
	} // while game_window is open
}// render_2btn_instances()

////////////////////////////////////////////////////////////////