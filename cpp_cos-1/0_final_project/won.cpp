
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *  won Instance Functions Definitions  *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

	   Contains the won instance functions definitions

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#include "exit_game.h"
#include "won.h"

/*---------------------------------------------
 |                                            |
 |Diplays won instance image, text and button |
 |                                            |
 ---------------------------------------------*/
void display_won_instance(RenderWindow &game_window, Sprite &img, Button &btn, Text &gain_state, Text &p_text) {

	// Clear the screen (fill it with black color)
	game_window.clear();
	// Displays the img and opens the window
	game_window.draw(img);
	btn.render(game_window);
	game_window.draw(gain_state);
	game_window.draw(p_text);
	game_window.display();

}

////////////////////////////////////////////////////////////////


/*---------------------------
 |                          |
 | Renders the instance won |
 |                          |
 ---------------------------*/
int render_won_instance(RenderWindow &game_window, Image &img, Font &font, Ether &player, int player_state, int amount_gain) {

	/*-------------
	 |  Variables  |
	 --------------*/
	string state_gain;

	// Checks the player state gaining points after the player won a match against a monster
	// and alocates the amount of points gained to the player correpomding state
	switch (player_state){
	case HEALTH:
		state_gain = "health";
		player.health += amount_gain;
		break;
	case ARMOR:
		state_gain = "armor";
		player.armor += amount_gain;
		break;
	case STRENGTH:
		state_gain = "strength";
		player.strength += amount_gain;
		break;
	default:
		break;
	}

	// Renders button
	// Scale button to rezised window, if resized
	float x = game_window.getSize().x / (2.0f * game_window.getSize().x / O_WIN_WD),
		y = (game_window.getSize().y) / (1.08 * game_window.getSize().y / O_WIN_HT);
	// button
	Button btn(x, y, 100.0f, 30.0f,
		       font, "Continue", Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34));
	// Renders back ground image
	Texture texture;
	texture.loadFromImage(img);
	Sprite img_background(texture);
	// Original loaded size of the img
	Vector2f targetsize(O_WIN_WD, O_WIN_HT);
	// Sets the image as same size of the window
	img_background.setScale(
		targetsize.x / img_background.getLocalBounds().width,
		targetsize.y / img_background.getLocalBounds().height);

	// Renders text player state
	string player_text = "Ether    Health: " + to_string(player.health) + "  Armor: " + to_string(player.armor) + "  Strengh: " + to_string(player.strength);
	Text p_state_text;
	// Sets the font text style
	p_state_text.setFont(font);
	p_state_text.setCharacterSize(16);
	p_state_text.setFillColor(Color::Cyan);
	p_state_text.setString(player_text);
	// Position the text in window
	p_state_text.setPosition(850.0f, 665.0f);

	// Renders text player state
	string gain_text = "Ether gained " + to_string(amount_gain) + " " + state_gain + "!";
	Text gain_state;
	// Sets the font text style
	gain_state.setFont(font);
	gain_state.setCharacterSize(20);
	gain_state.setFillColor(Color::Magenta);
	gain_state.setString(gain_text);
	// Position the text in window
	gain_state.setPosition(925.0f, 560.0f);


	//-- sound variables
	Music amb, voice;
	// Ambience
	// Checks if the file was opened successfully
	if (!amb.openFromFile("ambiences/amb4.wav")) { // If not displays an error message and exits program
		err_load_file(game_window, font, "ambiences/amb4.wav");
	}
	amb.setLoop(true);
	amb.setVolume(10);
	// Narrator
	voice.openFromFile("voices/voice1.wav");
	// Checks if the file was opened successfully
	if (!voice.openFromFile("voices/Slide 4.wav")) { // If not displays an error message and exits program
		err_load_file(game_window, font, "voices/Slide 4.wav");
	}

	/*---------------------
	 | Function processes |
	 ---------------------*/

	 // Displays the img and opens the window
	display_won_instance(game_window, img_background, btn, gain_state, p_state_text);
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
					display_won_instance(game_window, img_background, btn, gain_state, p_state_text);
					break;
				}
				break;
				// Left mouse button Released
			case Event::MouseButtonReleased:
				if (event.key.code == Mouse::Left) { // Released mouse left button
					if (btn.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, true)) { // Button clicked
						amb.stop();
						voice.stop();
						return -1;
					}
				}
				break;
				// Hover
			case Event::MouseMoved:
				btn.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, false);
				display_won_instance(game_window, img_background, btn, gain_state, p_state_text);
				break;
				//-- Window events
				// window closed
			case Event::Closed:
				exit(0); // Exits game
				break;
				// Resized window
			case Event::Resized:
				display_won_instance(game_window, img_background, btn, gain_state, p_state_text);
				break;
			default:
				// event not listed
				break;
			} // switch type of event
		} // While event
	} // while game_window is open
} // render_1btn_instances()
