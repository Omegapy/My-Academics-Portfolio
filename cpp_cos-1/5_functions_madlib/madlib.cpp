/*

Functions Madlib

This is make - up work and is worth up to 40 points.It is NOT required.
Points will be earned entirely at the instructor's determination of program quality.

Write a program that gets words or phrases(as strings) from the user.
You will use the variables this data is stored in to insert and replace words or phrases in the lyrics of a song or parts of a poem.
The song or poem is of your own choice.It should be school friendly, if you need me to explain that, email / message me.

You should get at least two, but no more than five, of each of the following from the user :

nouns(things)
verbs(actions)
adjectives(description words)

You will need a function to get each of these different types of words. (That brings our total function count so far to 4; these three plus main.)

You will need to use a function to display the lyrics of the song as well as the name of the artist you most prefer to have sing it.
There can be lyrical differences between different artists.Include a URL to the lyrics as a comment in this function. (This brings our function count to 5.)
(Places like genius.com, azlyrics.com, songlyrics.com are best for this.
	Wikipedia is a 100 % no go.I will hit you with the Wikipedia penalty if you use it.
	Yes, even including a link to Wikipedia as a comment will invoke that penalty.)
	Pass the data you have gotten from the user to another function that displays your madlib.
	Examples of the output are below. (This brings our function count to 6. This is the minimum number of functions you need to get credit.)
	Separate the original lyrics from the madlib using a line of symbols of your choice. (*&# _ - etc.)

	Song / Poem Requirements :

School friendly.
Songs must be at least 1 verse plus the chorus.
Poems should be somewhat recognizable even after the minimum of 6 items have be injected. "Somewhat" is being left to your determination.
Do not use a haiku.
Do not expect any rhyme scheme from whatever you pick to be preserved.

*** Please read ***
This programm will only run on Window OS
Song :
"Come Fly With Me"
Frank Sinatra Lyrics
I had it the sound track just for fun

lyrics from azlyrics.com
https ://www.azlyrics.com/lyrics/franksinatra/comeflywithme.html

*/

#include <iostream>
#include <string>
#include <vector>
// Console Input & Output.Header file, Window OS only
#include <conio.h> // getch()
// To play the sound Track
#include <Windows.h>
#include "MMSystem.h"
#pragma comment(lib, "winmm.lib")

using namespace std;

// -- Global vector

vector <vector<string>> original_lyrics = {

	{
		"Come fly with me, let's fly, let's fly away",
		"If you can use some exotic booze",
		"There's a bar in far Bombay",
		"Come fly with me, let's fly, let's fly away"
	},
	{
		"Come fly with me, let's float down to Peru",
		"In llama land there's a one-man band",
		"And he'll toot his flute for you",
		"Come fly with me, let's take off in the blue"
	},
	{
		"Once I get you up there where the air is rarefied",
		"We'll just glide, starry-eyed",
		"Once I get you up there I'll be holding you so near",
		"You may hear angels cheer 'cause we're together"
	},
	{
		"Weather - wise it's such a lovely day",
		"Just say the words and we'll beat the birds",
		"Down to Acapulco Bay",
		"It's perfect for a flying honeymoon, they say",
		"Come fly with me, let's fly, let's fly away"
	},
	{
		"Once I get you up there where the air is rarefied",
		"We'll just glide, starry-eyed",
		"Once I get you up there I'll be holding you so near",
		"You may hear angels cheer 'cause we're together"
	},
	{
		"Weather - wise it's such a lovely day",
		"Just say the words and we'll beat the birds",
		"Down to Acapulco Bay",
		"It's perfect for a flying honeymoon, they say",
		"Come fly with me, let's fly, let's fly away"
	}
};

vector <vector<string>> original_lyrics_flag = {

	{
		"Come *fly with me, let's *fly, let's *fly away",
		"If you can use some exotic booze",
		"There's a bar in far Bombay",
		"Come *fly with me, let's *fly, let's *fly away"
	},
	{
		"Come *fly with me, let's float down to Peru",
		"In llama land there's a one-man band",
		"And he'll toot his flute for you",
		"Come *fly with me, let's take off in the blue"
	},
	{
		"Once I *get you up there where the air is rarefied",
		"We'll just glide, starry-eyed",
		"Once I get you up there I'll be holding you so near",
		"You may hear &angels cheer 'cause we're &together"
	},
	{
		"Weather - wise it's such a +lovely #day",
		"Just say the words and we'll beat the birds",
		"Down to Acapulco Bay",
		"It's perfect for a +flying #honeymoon, they say",
		"Come *fly with me, let's *fly, let's *fly away"
	},
	{
		"Once I *get you up there where the air is rarefied",
		"We'll just glide, starry-eyed",
		"Once I get you up there I'll be holding you so near",
		"You may hear &angels cheer 'cause we're &together"
	},
	{
		"Weather - wise it's such a +lovely #day",
		"Just say the words and we'll beat the birds",
		"Down to Acapulco Bay",
		"It's perfect for a +flying #honeymoon, they say",
		"Come *fly with me, let's *fly, let's *fly away"
	}
};

// ----------------------------------------------------------------- Functions declaration

/*
	Waits for a key to be pressed, 
	and exits program.
*/
void press_key_to_exit();

/*
	Asks user to input plural noun words. Accepts user string inputs,
	and returns string vector of the inputed strings.

*/
vector<string> get_plural_nouns();

/*
	Asks user to input singular noun words. Accepts user string inputs,
	and returns string vector of the inputed strings.
*/
vector<string> get_singular_nouns();

/*
	Asks user to input verbs words. Accepts user string inputs,
	and returns string vector of the inputed strings.
*/
vector<string> get_lib_verbs();

/*
	Asks user to input adjective words. Accepts user string inputs,
	and returns string vector of the inputed strings.
*/
vector<string> get_lib_adjectives();

/*
	Creates the madlib lyric,
	acceptes the user inputs madlib words
	and returns the modify lyrics.
*/
vector <vector<string>> create_madlib(vector<string> lib_p_nouns, vector<string> lib_s_nouns, vector<string> lib_verbs, vector<string> lib_adjectives);

void display_madlib(vector <vector<string>> mod_madlib_lyrics);

// ------------------------------------------------------------------ Program
int main() {

	//--- Vectors
	// Stores the user's input madlib words
	vector<string> plural_nouns, singular_nouns, lib_verbs, lib_adjectives;
	// stores the Modify lyrics
	vector <vector<string>> mod_madlib;

	//-- Banner
	cout << "\n                              \033[1m**************\n                              *   Madlib   *\n                              **************\033[m\n\n";
	cout << "     This program gets words to creat a Madlib from a song.\n\n";
	
	// Plays song in a loop
	PlaySound(TEXT("come_fly_with_me.wav"), NULL, SND_FILENAME | SND_LOOP | SND_ASYNC);
	
	// User inputs
	plural_nouns = get_plural_nouns();
	singular_nouns = get_singular_nouns();
	lib_verbs = get_lib_verbs();
	lib_adjectives = get_lib_adjectives();
	// Creats the madlib lyrics
	mod_madlib = create_madlib(plural_nouns, singular_nouns, lib_verbs, lib_adjectives);
	// Display both the orginal and madlib lyrics
	display_madlib(mod_madlib);

	press_key_to_exit();
	
	return 0;
}


//------------------------------------------------------------------------------- Functions

void press_key_to_exit() {

	/*
		Waits for a key to be pressed,
		and exits program.
	*/

	// -- Local variables
	// Press key to exit variable
	char ch;
	cout << "\n\n  -- Press any key to exit -- ";
	ch = _getch();

}

vector<string> get_plural_nouns() {

	/*
		Asks user to input plural noun words.
		Accepts user string inputs,
		and returns string vector of the inputed strings.
	*/

	//-- Local variable
	string user_input;

	//--- Local vector
	vector<string> input_plural_nouns;

	for (int i = 0; i < 2; i++) { // Itinerates trough the number of words need to be inputed
		if (i < 1) { // Ask user to input the first word
			cout << "     Please enter a plural noun: ";
			getline(cin, user_input);
			input_plural_nouns.push_back(user_input);
		}
		else {
			cout << "     Please enter another plural noun: ";
			getline(cin, user_input);
			input_plural_nouns.push_back(user_input);
		}
	}
	cout << "\n";
	return input_plural_nouns;
}

vector<string> get_singular_nouns() {

	/*
		Asks user to input singular noun words.
		Accepts user string inputs,
		and returns string vector of the inputed strings.
	*/

	//-- Local variable
	string user_input;

	//--- Local vector
	vector<string> input_singular_nouns;

	for (int i = 0; i < 2; i++) { // Itinerates trough the number of words need to be inputed
		if (i < 1) { // Ask user to input the first word
			cout << "     Please enter a singular noun: ";
			getline(cin, user_input);
			input_singular_nouns.push_back(user_input);
		}
		else {
			cout << "     Please enter another singular noun: ";
			getline(cin, user_input);
			input_singular_nouns.push_back(user_input);
		}
	}
	cout << "\n";
	return input_singular_nouns;
}
vector<string> get_lib_verbs() {

	/*
		Asks user to input verbs words.
		takes user string inputs,
		and returns string vector of the inputed strings.
	*/

	//-- Local variable
	string user_input;

	//--- Local vector
	vector<string> input_verbs;

	for (int i = 0; i < 2; i++) { // Itinerates through the number of words need to be inputed
		if (i < 1) { // Ask user to input the first word
			cout << "     Please and enter a verb: ";
			getline(cin, user_input);
			input_verbs.push_back(user_input);
		}
		else {
			cout << "     Please and enter another verb: ";
			getline(cin, user_input);
			input_verbs.push_back(user_input);
		}
	}
	cout << "\n";
	return input_verbs;
}
vector<string> get_lib_adjectives() {

	/*
		Asks user to input adjective words.
		Accepts user string inputs,
		and returns string vector of the inputed strings.
	*/

	//-- Local variable
	string user_input;

	//--- Local vector
	vector<string> input_adjectives;

	for (int i = 0; i < 2; i++) { // Itinerates through the number of words need to be inputed
		if (i < 1) { // Ask user to input the first word
			cout << "     Please and enter an adjective: ";
			getline(cin, user_input);
			input_adjectives.push_back(user_input);
		}
		else {
			cout << "     Please and enter another adjective: ";
			getline(cin, user_input);
			input_adjectives.push_back(user_input);
		}
	}
	cout << "\n";
	return input_adjectives;
}

vector <vector<string>> create_madlib(vector<string> lib_p_nouns, vector<string> lib_s_nouns, vector<string> lib_verbs, vector<string> lib_adjectives) {

	/*
		Creates the madlib lyric,
		takes the user inputs madlib words
		and returns the modify lyrics.
	*/

	//-- Local variables
	string mod_sentence, // stores a modify sentence
		lyrics_sentence; // stores a lyrics sentence

	//-- Local vector
	vector<string> mod_verse; // stores the modify verse
	vector<vector<string>> madlib_lyrics; // stores the modify lyrics

	for (int i = 0; i < original_lyrics_flag.size(); i++) { // Itinerates through the song lyrics verses
		for (int j = 0; j < original_lyrics_flag[i].size(); j++) { // Itinerates through the song lyrics sentences
			lyrics_sentence = original_lyrics_flag[i][j];
			for (int k = 0; k < lyrics_sentence.size(); k++) { // Itinerates through the song lyrics sentences characters
				//--- normal letter
				if ((original_lyrics_flag[i][j][k] != '*') && // is not a flag character for a verb word
					(original_lyrics_flag[i][j][k] != '&') && // is not a flag character for a plural noun word 
					(original_lyrics_flag[i][j][k] != '#') && // is not a flag character for a singular noun word 
					(original_lyrics_flag[i][j][k] != '+')) { // is not a flag character for a adjective word 
					// add character to sentence
					mod_sentence += original_lyrics_flag[i][j][k];
				}
				//--- verb flag
				else if (original_lyrics_flag[i][j][k] == '*') {
					// checks if the verb to be replaced is 'fly'
					if (original_lyrics_flag[i][j][k + 1] == 'f') {
						// add madlib first madlib verb to sentence
						mod_sentence += "\x1B[93m" + lib_verbs[0] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 3; // slices 'fly' from sentence
					}
					else {
						// add madlib second madlib verb to sentence
						mod_sentence += "\x1B[93m" + lib_verbs[1] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 3; // slices 'get' from sentence
					}
				}
				//-- Plural nouns
				else if (original_lyrics_flag[i][j][k] == '&') {
					// checks if the plural noun to be replaced is 'angels'
					if (original_lyrics_flag[i][j][k + 1] == 'a') {
						// add madlib first madlib plural noun to sentence
						mod_sentence += "\x1B[93m" + lib_p_nouns[0] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 6; // slices 'angels' from sentence
					}
					else {
						// add madlib second madlib plural noun to sentence
						mod_sentence += "\x1B[93m" + lib_p_nouns[1] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 8; // slices 'together' from sentence
					}
				}
				//-- Singular nouns
				else if (original_lyrics_flag[i][j][k] == '#') {
					// checks if the singular noun to be replaced is 'day'
					if (original_lyrics_flag[i][j][k + 1] == 'd') {
						// add madlib first madlib singular noun to sentence
						mod_sentence += "\x1B[93m" + lib_s_nouns[0] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 6; // slices 'day' from sentence
					}
					else {
						// add madlib second madlib singular noun to sentence
						mod_sentence += "\x1B[93m" + lib_s_nouns[1] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 9; // slices 'honeymoon' from sentence
					}
				}
				//-- Adjectives
				else if (original_lyrics_flag[i][j][k] == '+') {
					// checks if the adjective to be replaced is 'lovely' 
					if (original_lyrics_flag[i][j][k + 1] == 'l') {
						// add madlib first madlib adjective to sentence
						mod_sentence += "\x1B[93m" + lib_adjectives[0] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 6; // slices 'lovely' from sentence
					}
					else {
						// add madlib second madlib adjective to sentence
						mod_sentence += "\x1B[93m" + lib_adjectives[1] + "\033[m"; // \x1B[93m changes the font cololor to yellow
						k += 6; // slices 'flying' from sentence, I know is not realy an adjective but it works
					}
				}
			}
			mod_verse.push_back(mod_sentence); // Intiliazes temporary verse
			mod_sentence = ""; // Intiliazes temporary lyrics sentence
		}
		madlib_lyrics.push_back(mod_verse); // Add temporary verse to madlyb lyrics
		mod_verse.clear(); // Intiliazes temporary lyrics verse
	}
	return madlib_lyrics;
}

void display_madlib(vector <vector<string>> mod_madlib_lyrics) {

	/*
		Displays the original and madlib lyrics
		takes the the modify madlib lyrics.
	*/

	cout << "\n\n                    --------------------------\n\n";

	cout << "    Come Fly With Me\n" << "    Frank Sinatra\n\n";

	// display the original lyrics
	for (int i = 0; i < original_lyrics.size(); i++) { // Itinerates through the song lyrics verses
		cout << "\n";
		for (int j = 0; j < original_lyrics[i].size(); j++) { // Itinerates through the song lyrics sentences
			cout << "     " << original_lyrics[i][j] << "\n";
		}
	}
	cout << "\n\n                        **********************\n\n";
	// display the modify lyrics
	for (int i = 0; i < mod_madlib_lyrics.size(); i++) { // Itinerates through the song lyrics verses
		cout << "\n";
		for (int j = 0; j < mod_madlib_lyrics[i].size(); j++) { // Itinerates through the song lyrics sentences
			cout << "     " << mod_madlib_lyrics[i][j] << "\n";
		}
	}
}
