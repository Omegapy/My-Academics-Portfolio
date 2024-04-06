
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *    Instances Functions Declaration   *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

       Contains the none fight instance functions decalartions

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef INSTANCES_H
#define INSTANCES_H

    #ifdef _MSC_VER
        #pragma once
    #endif  // _MSC_VER

#include "button.h"
#include "exit_game.h"
#include "ewindow.h"

/*----------------------------------------
 |                                       |
 |  Displays 1 button instances          |
 |  Place and Monster                    |
 |  Utilized by render_1btn_instances()  |
 |                                       |
 ----------------------------------------*/
void display_1btn_instances(RenderWindow &game_window, Sprite &img, Button &btn, Text &p_state_text);

/*----------------------------------------
 |                                       |
 |  Renders 1 button instances           |
 |  Place and Monster                    |
 |                                       |
 ----------------------------------------*/
int render_1btn_instances(RenderWindow &game_window, Image &img, Font &font, int type, Ether &player, int num_ambience, int num_voice, int amb_volume);

/*--------------------------------------------------
 |                                                 |
 |  Displays 2 buttons instances                   |
 |  Quest and Direction (left or right) instances  |
 |  Utilized by render_2btn_instances()            |
 |                                                 |
 --------------------------------------------------*/
void display_2btn_instances(RenderWindow &game_window, Sprite &img, Button &btn1, Button &btn2, Text p_state_text);


/*--------------------------------------------------
 |                                                 |
 |  Renders 2 buttons instances                    |
 |  Quest and Direction (left or right) instances  |
 |                                                 |
 --------------------------------------------------*/
int render_2btn_instances(RenderWindow &game_window, Image &img, Font &font, int type, Ether &player, int num_ambience, int num_voice, int amb_volume);

#endif