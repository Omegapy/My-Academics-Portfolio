
//////////////////////////////////////////////////////////////////////////////////////////////////////////////
 /*--------------------------------****************************************----------------------------------
  |                                *                                      *                                 |
  |   Ether's Quest                *  won instance Functions Declaration  *                                 |
  |                                *                                      *                                 |
  ---------------------------------****************************************----------------------------------*/
  //////////////////////////////////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////////////////////////////////
/*

      Contains the won instance function declaration

*/
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

#ifndef WON_H
#define WON_H

    #ifdef _MSC_VER
        #pragma once
    #endif  // _MSC_VER

//****** Headers lib. files, must be declared first
//****** Countains Global Variables INST_TYPE and INST_RESULTS, Ether struct, win_original_width, win_original_heigth
//#include "hether.h"

#include "button.h"
#include "ewindow.h"

/*---------------------------------------------
 |                                            |
 |Diplays won instance image, text and button |
 |                                            |
 ---------------------------------------------*/
void display_won_instance(RenderWindow &game_window, Sprite &img, Button &btn, Text &gain_state, Text &p_text);

/*---------------------------
 |                          |
 | Renders the instance won |
 |                          |
 ---------------------------*/
int render_won_instance(RenderWindow &game_window, Image &img, Font &font, Ether &player, int player_state, int amount_gain);

#endif