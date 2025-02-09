

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *  Fight Intance Functions Definitons  *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

	   Contains the fight instance functions.

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////


#include "fight.h"


/*----------------------------------------
 |                                       |
 |  Displays the fight instance          |
 |  Utilized by render_fight_instances() |
 |                                       |
 ----------------------------------------*/

void display_fight_instances(RenderWindow &game_window, Sprite &img, Button &btn, Text &p_state_text, Text &m_state_text, Text &f_state_text) {

	// Clear the screen (fill it with black color)
	game_window.clear();
	// Displays the img and opens the window
	game_window.draw(img);
	btn.render(game_window);
	game_window.draw(p_state_text); // Player's state txt
	game_window.draw(m_state_text); // Monster's state
	game_window.draw(f_state_text); // Hit Miss and Roller results txt
	game_window.display();

}

/*-----------------------
 |                      |
 |  Rolls the dices     |
	Utilized by fight() |
 |                      |
 -----------------------*/
vector<int> attack(bool attacks) {


	/*-------------
	 |  Variables  |
	 --------------*/
	vector<int> roll;

	/*---------------------
	 | Function processes |
	 ---------------------*/

	if (attacks) { // attacks is true then roll 2 20 dices
		roll.push_back(rand() % (20 - 1) + 1);
		roll.push_back(rand() % (20 - 1) + 1);
	}
	else { // attacks is false then roll 2 10 dices, defence
		roll.push_back(rand() % (10 - 1) + 1);
		roll.push_back(rand() % (10 - 1) + 1);
	}

	return roll;
}

////////////////////////////////////////////////////////////////

/*--------------------------------
 |                               |
 |  Computes the dices ouputes,  |
	helth and monster outcomes   |
 |                               |
 --------------------------------*/
vector<int> fight(Ether &player, Monster &monster, bool player_attacks, bool monster_attacks) {

	/*-------------
	 |  Variables  |
	 --------------*/

	int attack_results = 0;

	vector<int> monster_rolls,
		player_rolls,
		fight_results;

	/*---------------------
	 | Function processes |
	 ---------------------*/

	if (monster_attacks) { // the monster attacks

		monster_rolls = attack(monster_attacks); // monster attack rolls
		player_rolls = attack(player_attacks); // player defence rolls

		if ((monster_rolls[0] + monster_rolls[1]) > (player_rolls[0] + player_rolls[1])) { // checks result of the monster attack rolls

			attack_results = MONSTER_HITS;
			player.health = player.health - monster.get_strength() - round(player.armor / 150);

			if (player.health <= 0) { // checks if the play died

				attack_results = PLAYER_DEAD;
				player.health = 0;
			}
		}
		else { // monster attack miss

			attack_results = MONSTER_MISS;

		}
	}
	else if (player_attacks) { // Player attacks

		player_rolls = attack(player_attacks); // player attack rolls
		monster_rolls = attack(monster_attacks); // player defence rolls

		if ((player_rolls[0] + monster_rolls[1]) > (monster_rolls[0] + monster_rolls[1])) { // checks result of the player attack rolls

			attack_results = PLAYER_HITS;
			monster.set_health(monster.get_health() - player.strength - round(monster.get_armor() / 150));

			if (monster.get_health() <= 0) { // checks if the play died

				attack_results = MONSTER_DEAD;
				monster.set_health(0);
			}
		}
		else { // monster attack miss

			attack_results = PLAYER_MISS;
		}
	}

	// Stores results
	fight_results.push_back(attack_results);
	fight_results.push_back(player_rolls[0]);
	fight_results.push_back(player_rolls[1]);
	fight_results.push_back(monster_rolls[0]);
	fight_results.push_back(monster_rolls[1]);

	return fight_results;

} // fight()

////////////////////////////////////////////////////////////////

/*-------------------------------
 |                              |
 |  Renders the Fight instance  |
 |                              |
 -------------------------------*/
int render_fight_instance(RenderWindow &game_window, Image &img, Font &font, Ether &player, Monster &monster, int num_ambience, int num_voice, int amb_volume) {

	/*-------------
	 |  Variables  |
	 --------------*/

	int m_health = monster.get_health(),
		temp_m_health = monster.get_health(),
		p_health = player.health, // Store the player's health before the monster fight
		temp_p_health = player.health;

	bool monster_attacks = true,
		player_attacks = false;

	vector<int> fight_results;

	// Renders button
	// Scale button to rezised window, if resized
	float x = game_window.getSize().x / (2.0f * game_window.getSize().x / O_WIN_WD),
		  y = (game_window.getSize().y) / (1.09 * game_window.getSize().y / O_WIN_HT);
	// button
	Button btn(x, y, 100.0f, 30.0f,
		      font, "        Roll Dice", Color(158, 158, 158), Color(97, 97, 97), Color(255, 87, 34));

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

	// Renders text player
	string player_state = "Ether      Health: " + to_string(player.health)
		+ "    Armor: " + to_string(player.armor)
		+ "    Strength: " + to_string(player.strength);
	Text p_state_text;
	// Sets the font text style
	p_state_text.setFont(font);
	p_state_text.setCharacterSize(16);
	p_state_text.setFillColor(Color::Cyan);
	p_state_text.setString(player_state);
	// Position the text in window
	p_state_text.setPosition(850.0f, 665.0f);

	// Renders text monster
	string m_name_spaces;
	for (int i = monster.get_name().size(); i > 0; i--) { m_name_spaces += " "; }
	string monster_state = monster.get_name() + m_name_spaces + "Health: " + to_string(monster.get_health())
		+ "    Armor: " + to_string(monster.get_armor())
		+ "    Strength: " + to_string(monster.get_strength());
	Text m_state_text;
	// Sets the font text style
	m_state_text.setFont(font);
	m_state_text.setCharacterSize(16);
	m_state_text.setFillColor(Color::Magenta);
	m_state_text.setString(monster_state);
	// Position the text in window
	m_state_text.setPosition(850.0f, 642.0f);

	// Renders text fight
	string fight_rolls_text = " ";
	Text f_state_text;
	// Sets the font text style
	f_state_text.setFont(font);
	f_state_text.setCharacterSize(18);
	f_state_text.setFillColor(Color::Yellow);
	f_state_text.setString(fight_rolls_text);
	// Position the text in window
	f_state_text.setPosition(100.0f, 625.0f);

	//-- sound variables
	string name_amb = "ambiences/amb" + to_string(num_ambience) + ".wav";
	Music amb;
	// Ambience
	// Checks if the file was opened successfully
	if (!amb.openFromFile(name_amb)) { // If not displays an error message and exits program
		err_load_file(game_window, font, name_amb);
	}
	amb.setLoop(true);
	amb.setVolume(amb_volume);

	/*---------------------
	 | Function processes |
	 ---------------------*/

	// Displays the img and opens the window
	display_fight_instances(game_window, img_background, btn, p_state_text, m_state_text, f_state_text);
	// Plays sound
	amb.play();

	//// Game window instance open
	while (game_window.isOpen()) { // Run while the game window is open

		Event event;

		while (game_window.pollEvent(event)) { // Checks events in game_window

			switch (event.type) { // Checks events type
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
					display_fight_instances(game_window, img_background, btn, p_state_text, m_state_text, f_state_text);
					break;
				}
				break;
			// Left mouse button Released
			case Event::MouseButtonReleased: // A mouse button was release

				if (event.key.code == Mouse::Left) { // Checks if the event is left mouse click
					// if mouse left click on button
					if (btn.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, true)) {

						// Roll the dice return Miss or hit or dead (monter or player)
						fight_results = fight(player, monster, player_attacks, monster_attacks); 

						// Turn to attack loops
						if (monster_attacks) { // if Monster turn to attack
							if (fight_results[0] == MONSTER_MISS) { // if Monster miss
								fight_rolls_text = "The " + monster.get_name() + " atacked Ether and missed.\n";
							}
							else if ((fight_results[0] == MONSTER_HITS)) { // if Monster hit player
								fight_rolls_text = "The " + monster.get_name() + " attacked Ether and hit Ether for "
									+ to_string(temp_p_health - player.health) + " points.\n";
							}
							else { // Player is dead
								// Reset the player health to the value set before the fight
								player.health = p_health;
								amb.stop();
								return fight_results[0]; // exits fight()
							}
						} 
						else if (player_attacks) { // if it is the player turn to attack
							if (fight_results[0] == PLAYER_MISS) { // if player hit
								fight_rolls_text = "Ether attacked the " + monster.get_name() + " and missed.\n";
							}
							else if ((fight_results[0] == PLAYER_HITS)) { // if player miss
								fight_rolls_text = "Ether attacked the " + monster.get_name() + " and hit it for "
									+ to_string(temp_m_health - monster.get_health()) + " points.\n";
							}
							else { // Monster is dead
								// Reset the player health to the value set before the fight
								player.health = p_health;
								amb.stop();
								return fight_results[0]; // exits fight()
							}
						} // end if loops turn to attack 

						// Store the fight result to be dislayed
						fight_rolls_text += "You rolled " + to_string(fight_results[1])
							+ " and " + to_string(fight_results[2])
							+ "  for a total of: " + to_string(fight_results[1] + fight_results[2])
							+ "\nThe " + monster.get_name() + " rolled " + to_string(fight_results[3])
							+ " and " + to_string(fight_results[4])
							+ "  for a total of: " + to_string(fight_results[3] + fight_results[4]);

						f_state_text.setString(fight_rolls_text);

						// Renders text player's state
						string player_state = "Ether      Health: " + to_string(player.health)
							+ "    Armor: " + to_string(player.armor)
							+ "    Strength: " + to_string(player.strength);
						p_state_text.setString(player_state);

						// Renders text monster's state
						string monster_state = monster.get_name() + m_name_spaces + "Health: " + to_string(monster.get_health())
							+ "    Armor: " + to_string(monster.get_armor())
							+ "    Strength: " + to_string(monster.get_strength());
						m_state_text.setString(monster_state);


						display_fight_instances(game_window, img_background, btn, p_state_text, m_state_text, f_state_text);

						// Set state variable for next play
						temp_m_health = monster.get_health();
						temp_p_health = player.health;
						monster_attacks = !monster_attacks;
						player_attacks = !player_attacks;

					} // if mouse left click on button
				} // if event left mouse click
				break;
			// Hover
			case Event::MouseMoved:
				btn.update(game_window, Mouse::getPosition(game_window).x, Mouse::getPosition(game_window).y, false, false);
				display_fight_instances(game_window, img_background, btn, p_state_text, m_state_text, f_state_text);
				break;
			//-- Window events
			// window closed
			case Event::Closed:
				exit(0); // Exits game
				break;
			// Resized window
			case Event::Resized:
				display_fight_instances(game_window, img_background, btn, p_state_text, m_state_text, f_state_text);
				break;
			default:
				// event not listed
				break;
			} // switch type of event
		} // While event

	} // while game_window is open

	throw "Loop return Error: render_fight_instance()";
} // render_fight_instances()


