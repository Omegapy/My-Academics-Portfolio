

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*-------------------------------*****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		        Ether's Quest            *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
//////////////////////////////////////////////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

COSC 1030 � Computer Science 1
Professor: David Durbin
Student : Alejandro (Alex) Ricciardi
Due date : 12 / 13 / 2022


											Final Project
										   (Ether's Quest)

 Your final project is to create an interactive, text-based Choose Your Own Adventure style game based on a movie,
 book or game of your choice. You may use your own idea if you don't want to base it on an existing property.
 If you aren't sure what I mean by Choose Your Own Adventure, see the "Cat Break" image file in this week's module.
 (Credit to the author, Fox, for the Choose Your Own Adventure.)

 Part of the final project's grade will be on whether or not you followed your project plan.

That said, this is one of the rare opportunities for you to express your creativity, so try to have fun with this and pick something you want to do.
Pro Tip: Commenting the exact spot where you put the required elements is a great idea.  <- New!

To earn full points on the final project you will need:

multiple loops
multiple conditionals
a class and resulting objects
multiple non-Class related functions
multiple arrays or vectors
Submit your .cpp file in a zipped folder.
To conform to your initial project plan. (That's what you're turning in here!)
There are also points for me to judge the quality of your work.
You can see the full rubric on the final project page, which will open Nov. 14th. You have until the last day of class (Dec. 13th)
to finish and submit your project. I have provided a 12 hour grace period for late projects,
but at 11:59 a.m. Dec. 14th the assignment locks and you won't be able to submit after that. That 12 hours counts as 2 days late.

As the final is 200 points and 25% of your overall grade, you really don't want to skip the final.


****** Please the Readme.txt file  for more information about this project **********

This project runs on MS Window 10


*/
/////////////////////////////////////////////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*-------------------------------*****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		          Headers                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////

//****** Headers lib. files, must be declared first
//****** Contains Global Variables enumerators INST_TYPE, INST_RESULTS, PLAYER_STATE, and ORIGINAL_WINDOW_SIZE
//****** and the struct Ether
#include "hether.h"

// must be declare second, class button
#include "button.h"
// contains the load error window functions
#include "ewindow.h"
// Contains the monster class
#include "monster.h"
// contains the none fight instances functions
#include "instances.h"
// contains the fight instance functions
#include "fight.h"
// Contains the exit game functions
#include "exit_game.h"
// Contains the won instance functions
#include "won.h"


//////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /*--------------------------------****************************************----------------------------------
     |                                *                                      *                                 |
     |                                *	           Classes                *                                 |
     |                                *                                      *                                 |
     ---------------------------------****************************************----------------------------------*/
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*---------------------------------------------------------------------------------------------------------------

			Class Button
			See button.h and button.cpp

---------------------------------------------------------------------------------------------------------------*/

/*---------------------------------------------------------------------------------------------------------------

			Class Monster
			See monster.h and monster.cpp

---------------------------------------------------------------------------------------------------------------*/


//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *	        Function Declaration         *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////


/*---------------------------------
 |                                |
 |  Loads images into a vector.   |
 |  Returns a vector of images.   |
 |                                |
 ---------------------------------*/
    vector<Image> load_images(RenderWindow &game_window, Font &font);


/*------------------------------------------------------
 |                                                     |
 |  Switch that selects the intance by its categories  |
 |  And redirects the instance to be rendered          |
 |                                                     |
 ------------------------------------------------------*/
    int render_instance(RenderWindow &game_window, Image &img, Font &font, int type, Ether &player, Monster monster, int num_ambience, int num_voice, int amb_volume);


//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		          Program                *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
    //////////////////////////////////////////////////////////////////////////////////////////////////////////////

    int main() {

        /*////////////////////////
        --------------------------
        |      Main Variables    |
        --------------------------
        ////////////////////////*/

        //--- Variables
        int results;
        bool reject_quest = false;

        // Creates an object player from global struct Ether
        Ether player;


        //--- Window objects;
        RenderWindow window(VideoMode(O_WIN_WD, O_WIN_HT, 64), "window");

        //wind(window);

        //--- Loads the font
        Font font;
        if (!font.loadFromFile("font/segoeui.ttf")){ // Checks font for file load error
            throw "The font file was not loaded successfully";
        }

        //--- Loads and stores images
        vector<Image> images = load_images(window, font);


        //--- Monster objects
        Monster no_monster;
        Monster geist("Geist", 100, 100, 10);
        Monster ophra("Ophra", 150, 150, 20);
        Monster four_heads("Four Heads", 150, 150, 20);
        Monster horde("Horde", 150, 150, 23);
        Monster boar("Boar", 165, 165, 35);
        Monster moose("Moose", 175, 175, 35);
        Monster brian("Brian", 175, 175, 35);
        Monster creature("Creature", 175, 175, 38);
        Monster frog("Frog", 195, 200, 45);
        Monster dalia("Dalia", 200, 195, 45);
        Monster nightmare("Nightmare", 200, 195, 55);
        Monster zombies("Zombies", 200, 195, 53);
        Monster salt("Salt", 350, 350, 65);
        Monster iretrat("Iretrat", 400, 200, 100);


        /*////////////////////////
        --------------------------
        |   Main Game Instance   |
        --------------------------
        ////////////////////////*/

	srand(time(NULL)); // set random seed number = system clock time


	//////////////////////////////////////////////////
	/*-----------------------------------------------
	 |                                              |
	 |               Game introduction              |
	 |                                              |
	 -----------------------------------------------*/
	//////////////////////////////////////////////////

	// Ambiense/narrator sounds intro slides
	// Render intance
	render_instance(window, images[0], font, PLACE, player, no_monster, 1, 1, 3);
	render_instance(window, images[1], font, PLACE, player, no_monster, 1, 2, 3);
	render_instance(window, images[4], font, PLACE, player, no_monster, 5, 5, 10); // leaving nephalia

	//////////////////////////////////////////////////
	/*-----------------------------------------------
	 |                                              |
	 |     Naphalia First Road Monster, Geist       |
	 |                                              |
	 -----------------------------------------------*/
	//////////////////////////////////////////////////

A:  // set resurrection point geist monster-1
	// giest monster
	render_instance(window, images[5], font, MONSTER, player, no_monster, 6, 6, 10);
	results = render_instance(window, images[5], font, FIGHT, player, geist, 6, 0, 15);
	if (results == PLAYER_DEAD) { // player dead
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto A; // go to First Road Monster, Geist
	}
	// player won
	render_won_instance(window, images[3], font, player, ARMOR, 50); 
	/*-----------------------------------------------
	 |                                              |
	 |              First Road Fork                 |
	 |                                              |
	 -----------------------------------------------*/
B:  // set resurrection point fork-1
	results = render_instance(window, images[6], font, DIRECTION, player, no_monster, 7, 7, 10);
	if (results == RIGHT) { goto C; } // Kalla oupost
	/*-----------------------------------------------
	 |                                              |
	 |        Village of Napha Omagra's quest       |
	 |                                              |
	 -----------------------------------------------*/
	// Omagra's quest
	results = render_instance(window, images[7], font, QUEST, player, no_monster, 8, 8, 10);
	if (results == REJECT) { goto D; } // Reject quest, go to monster on the road, Horde
	// Accept quest fight Ophra;
	render_instance(window, images[8], font, MONSTER, player, no_monster, 9, 9, 10);
	results = render_instance(window, images[8], font, FIGHT, player, ophra, 9, 0, 15);
	if (results == PLAYER_DEAD) { // Player dead
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto B; // go to First Road Fork 
	}
	// Player won
	render_won_instance(window, images[3], font, player, STRENGTH, 25);
	goto E; // Go to Leaving Naphalia Entering Kessig
	/*-----------------------------------------------
	 |                                              |
	 |          Kalla Oupost Kayla's quest          |
	 |                                              |
	 -----------------------------------------------*/
C:  // Kayla's quest
	results = render_instance(window, images[9], font, QUEST, player, no_monster, 10, 10, 10);
	if (results == REJECT) { goto D; } // // Reject quest, go to monster on the road, Hords of undeads
	// Accept quest fight Four Heads
	render_instance(window, images[10], font, MONSTER, player, no_monster, 11, 11, 10);
	results = render_instance(window, images[10], font, FIGHT, player, four_heads, 11, 0, 15);
	if (results == PLAYER_DEAD) { // Player dead
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto B; } // go to First Road Fork 
	// Player won
	render_won_instance(window, images[3], font, player, STRENGTH, 25);
	goto E; // go to Leaving Naphalia Entering Kessig
	/*-----------------------------------------------
	 |                                              |
	 |     Monster on the road Hords of undeads     |
	 |                                              |
	 -----------------------------------------------*/
D:	reject_quest = true;
	render_instance(window, images[12], font, PLACE, player, no_monster, 12, 13, 10);
	render_instance(window, images[11], font, MONSTER, player, no_monster, 13, 12, 10);
	results = render_instance(window, images[11], font, FIGHT, player, horde, 13, 0, 15);
	if (results == PLAYER_DEAD) { // Player dead 
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto B; // go to First Road Fork 
	}
	// Player won
	render_won_instance(window, images[3], font, player, STRENGTH, 25);

	//////////////////////////////////////////////////
	/*-----------------------------------------------
	 |                                              |
	 |      Leaving Naphalia Entering Kessig        |
	 |                                              |
	 -----------------------------------------------*/
	////////////////////////////////////////////////// 

E:  // Set resurrection Leaving Naphalia Entering Kessig
	if (!reject_quest) { // Check if the player did not rejected a prior quest
		render_instance(window, images[12], font, PLACE, player, no_monster, 12, 13, 10);
		reject_quest = false; // reset player rejected a quest to false
	}
	render_instance(window, images[13], font, PLACE, player, no_monster, 7, 14, 10);
	/*-----------------------------------------------
	 |                                              |
	 |         Monster on the road boar             |
	 |                                              |
	 -----------------------------------------------*/
	render_instance(window, images[14], font, MONSTER, player, no_monster, 14, 15, 10);
	results = render_instance(window, images[14], font, FIGHT, player, boar, 14, 0, 15); 
	if (results == PLAYER_DEAD) { // player dead, 
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto E; // go to Leaving Naphalia Entering Kessig
	}
	// player won
	render_won_instance(window, images[3], font, player, ARMOR, 50);
	/*-----------------------------------------------
	 |                                              |
	 |             Second Road Fork                 |
	 |                                              |
	 -----------------------------------------------*/
F: // set resurrection point fork-2
	results = render_instance(window, images[6], font, DIRECTION, player, no_monster, 7, 7, 10);
	if (results == RIGHT) { goto G; } // Logus plains Matteo's quest 
	/*-----------------------------------------------
	 |                                              |
	 |        Redwood village Connor's quest        |
	 |                                              |
	 -----------------------------------------------*/
    // Connor's quest
	results = render_instance(window, images[15], font, QUEST, player, no_monster, 8, 16, 10);
	if (results == REJECT) { goto H; } // Reject quest, go to monster on the road, creature
	// Accept quest fight moose
	render_instance(window, images[16], font, MONSTER, player, no_monster, 15, 17, 10);
	results = render_instance(window, images[16], font, FIGHT, player, moose, 15, 0, 15);
	if (results == PLAYER_DEAD) { // Player dead
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto F; // go to Second Road Fork 
	}
	// Player won
	render_won_instance(window, images[3], font, player, HEALTH, 50);
	goto I; // Go to leaving Kessig entering Stensia
	/*-----------------------------------------------
	 |                                              |
	 |         Logus plains Matteo's quest          |
	 |                                              |
	 -----------------------------------------------*/
G:  //Matteo's quest
	results = render_instance(window, images[17], font, QUEST, player, no_monster, 16, 18, 30);
	if (results == REJECT) { goto H; } // Reject quest, go to monster on the road, creature
	// Accept quest fight Four Heads
	render_instance(window, images[18], font, MONSTER, player, no_monster, 17, 19, 30);
	results = render_instance(window, images[18], font, FIGHT, player, brian, 17, 0, 35);
	if (results == PLAYER_DEAD) { // Player dead
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto F; // go to second Road Fork 
	} 
    // Player won
	render_won_instance(window, images[3], font, player, HEALTH, 50);
	goto I; // go to Leaving Kessig entering Stensia
	/*-----------------------------------------------
	 |                                              |
	 |        Monster on the road, creature         |
	 |                                              |
	 -----------------------------------------------*/
H:	render_instance(window, images[19], font, MONSTER, player, no_monster, 18, 20, 10);
	results = render_instance(window, images[19], font, FIGHT, player, creature, 18, 0, 15);
	if (results == PLAYER_DEAD) { // Player dead 
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto F; // go to second Road Fork 
	}
	// Player won
	render_won_instance(window, images[3], font, player, HEALTH, 50);

	//////////////////////////////////////////////////
	/*-----------------------------------------------
	 |                                              |
	 |      Leaving Kessig Entering Stensia         |
	 |                                              |
	 -----------------------------------------------*/
	//////////////////////////////////////////////////

I:	// set resurrection point
	render_instance(window, images[20], font, PLACE, player, no_monster, 19, 21, 5);
	render_instance(window, images[21], font, PLACE, player, no_monster, 19, 22, 5);
	/*-----------------------------------------------
	 |                                              |
	 |         Monster on the road Amphibian        |
	 |                                              |
	 -----------------------------------------------*/
	render_instance(window, images[22], font, MONSTER, player, no_monster, 20, 23, 10);
	results = render_instance(window, images[22], font, FIGHT, player, frog, 20, 0, 15);
	if (results == PLAYER_DEAD) { // player dead 
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto I; // go to Leaving Kessig Entering Stensia
	}
	// player won
	render_won_instance(window, images[3], font, player, ARMOR, 50);
	/*-----------------------------------------------
	 |                                              |
	 |              Third Road Fork                 |
	 |                                              |
	 -----------------------------------------------*/
J:  // set resurrection point fork-3
	results = render_instance(window, images[6], font, DIRECTION, player, no_monster, 7, 7, 10);
	if (results == RIGHT) { goto K; } // go to Morna Isaac'quest
	/*-----------------------------------------------
	 |                                              |
	 |         Graful castle, Eryn's quest          |
	 |                                              |
	 -----------------------------------------------*/
	 // Eryn's quest
	results = render_instance(window, images[23], font, QUEST, player, no_monster, 21, 24, 5);
	if (results == REJECT) { goto L; } // Reject quest, go to monster on the road, egg zombies
	// Accept quest fight dalia
	render_instance(window, images[24], font, MONSTER, player, no_monster, 22, 25, 5);
	results = render_instance(window, images[24], font, FIGHT, player, dalia, 22, 0, 5);
	if (results == PLAYER_DEAD) { // Player dead
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto J; // go to Third Road Fork 
	}
	// Player won
	render_won_instance(window, images[3], font, player, STRENGTH, 55);
	goto M; // Go to Entering High Temple
	/*-----------------------------------------------
	 |                                              |
	 |             Morna Isaac's quest              |
	 |                                              |
	 -----------------------------------------------*/
K:  // Isaac's quest
	results = render_instance(window, images[25], font, QUEST, player, no_monster, 23, 26, 20);
	if (results == REJECT) { goto L; } // Reject quest, go to monster on the road, egg zombies
	// Accept quest fight Four Heads
	render_instance(window, images[26], font, MONSTER, player, no_monster, 24, 27, 20);
	results = render_instance(window, images[26], font, FIGHT, player, nightmare, 24, 0, 25);
	if (results == PLAYER_DEAD) { // Player dead
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto J; // go to Third Road Fork 
	}
	// Player won
	render_won_instance(window, images[3], font, player, STRENGTH, 55);
	goto M; // go to Entering High Temple
	/*-----------------------------------------------
	 |                                              |
	 |         Monster on the road, Zombies         |
	 |                                              |
	 -----------------------------------------------*/
L:	render_instance(window, images[27], font, MONSTER, player, no_monster, 25, 28, 7);
	results = render_instance(window, images[27], font, FIGHT, player, zombies, 25, 0, 8);
	if (results == PLAYER_DEAD) { // Player dead 
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto J; // go to third Road Fork 
	}
	// Player won
	render_won_instance(window, images[3], font, player, STRENGTH, 55);

	//////////////////////////////////////////////////
	/*-----------------------------------------------
	 |                                              |
	 |            Entering High Temple              |
	 |                                              |
	 -----------------------------------------------*/
	 //////////////////////////////////////////////////

M:  render_instance(window, images[28], font, PLACE, player, no_monster, 26, 29, 10);
	render_instance(window, images[29], font, PLACE, player, no_monster, 26, 30, 10);
	//amb26.stop(); voice1.stop();
	/*-----------------------------------------------
	 |                                              |
	 |                  Lord Salt                   |
	 |                                              |
	 -----------------------------------------------*/
	render_instance(window, images[30], font, MONSTER, player, no_monster, 27, 31, 2);
	results = render_instance(window, images[30], font, FIGHT, player, salt, 27, 0, 2);
	if (results == PLAYER_DEAD) { // Player dead 
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto M; // go to Entering High Temple
	}
	// Player won
	render_won_instance(window, images[3], font, player, HEALTH, 100);
	render_instance(window, images[31], font, PLACE, player, no_monster, 27, 32, 2);
	/*-----------------------------------------------
	 |                                              |
	 |              Demon Iretrat                   |
	 |                                              |
	 -----------------------------------------------*/
	render_instance(window, images[32], font, MONSTER, player, no_monster, 28, 33, 4);
	results = render_instance(window, images[32], font, FIGHT, player, iretrat, 28, 0, 4);;
	if (results == PLAYER_DEAD) { // Player dead 
		render_instance(window, images[2], font, PLACE, player, no_monster, 3, 3, 10);
		goto M; // go to Entering High Temple
	}
	// Player won
	render_won_instance(window, images[3], font, player, HEALTH, 100);
	render_instance(window, images[33], font, PLACE, player, no_monster, 28, 34, 4);
	/*-----------------------------------------------
	 |                                              |
	 |                Clarabella                    |
	 |                                              |
	 -----------------------------------------------*/
	render_instance(window, images[34], font, PLACE, player, no_monster, 1, 35, 3);
	render_instance(window, images[35], font, PLACE, player, no_monster, 1, 36, 3);

return 0;

} // main()

//////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*--------------------------------****************************************----------------------------------
 |                                *                                      *                                 |
 |                                *		         Functions               *                                 |
 |                                *                                      *                                 |
 ---------------------------------****************************************----------------------------------*/
 //////////////////////////////////////////////////////////////////////////////////////////////////////////////



/*------------------------------------------------------
 |                                                     |
 |  Switch that selects the intance by its categories  |
 |  And redirects the instance to be rendered          |
 |                                                     |
 ------------------------------------------------------*/
int render_instance(RenderWindow &game_window, Image &img, Font &font, int type, Ether &player, Monster monster, int num_ambience, int num_voice, int amb_volume){
	
	int inst_results =-1;

	switch (type) {
	case QUEST:
		return render_2btn_instances(game_window, img, font, type, player, num_ambience, num_voice, amb_volume);
		break;
	case DIRECTION:
		return render_2btn_instances(game_window, img, font, type, player, num_ambience, num_voice, amb_volume);
	 	break;
	case PLACE:
		return render_1btn_instances(game_window, img, font, type, player, num_ambience, num_voice, amb_volume);
		break;
	case MONSTER:
		return render_1btn_instances(game_window, img, font, type, player, num_ambience, num_voice, amb_volume);
		break;
	case FIGHT:
		return render_fight_instance(game_window, img, font, player, monster, num_ambience, num_voice, amb_volume);
		break;

	default:
		throw "ERROR: Invalid intance type";
		break;
	}
}

////////////////////////////////////////////////////////////////

 /*---------------------------------
  |                                |
  |  Loads images into a vector.   |
  |  Returns a vector of images.   |
  |                                |
  ---------------------------------*/
vector<Image> load_images(RenderWindow &game_window, Font &font) {

	/*-------------
	|  Variables  |
	--------------*/
	vector<Image> images;
	Image temp_img;
	string temp_img_name;

	for (int i = 1; i < 37; i++) {

		temp_img_name = "img/Slide" + to_string(i) + ".PNG";
		
		// Checks if the file loaded successfully
		if (!temp_img.loadFromFile(temp_img_name)) { // If not displays a message and exits program
			err_load_file(game_window, font, temp_img_name);
		}

		images.push_back(temp_img);
	}

	return images;

}// Load_images()

////////////////////////////////////////////////////////////////



