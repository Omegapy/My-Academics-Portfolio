
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                * Fight Intance Functions Declaration  *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

	   Contains the fight instance functions.
		

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef FIGHT_H
#define FIGHT_H

	#ifdef _MSC_VER
		#pragma once
	#endif 

#include "exit_game.h"
#include "button.h"
#include "Monster.h"
#include "ewindow.h"

/*----------------------------------------
 |                                       |
 |  Displays the fight instance          |
 |  Utilized by render_fight_instances() |
 |                                       |
 ----------------------------------------*/
void display_fight_instances(RenderWindow &game_window, Sprite &img, Button &btn, Text &p_state_text, Text &m_state_text, Text &f_state_text);

/*-----------------------
 |                      |
 |  Rolls the dices     |
    Utilized by fight() |
 |                      |
 -----------------------*/
vector<int> attack(bool attacks);


/*--------------------------------
 |                               |
 |  Computes the dices ouputes,  |
    helth and monster outcomes   |
 |                               |
 --------------------------------*/
vector<int> fight(Ether &player, Monster &monster, bool player_attacks, bool monster_attacks);

/*-------------------------------
 |                              |
 |  Renders the Fight instance  |
 |                              |
 -------------------------------*/
int render_fight_instance(RenderWindow &game_window, Image &img, Font &font, Ether &player, Monster &monster, int num_ambience, int num_voice, int amb_volume);

#endif
