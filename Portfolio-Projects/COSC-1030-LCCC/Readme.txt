-----------------------------------------------------------------------------------------------------------------------------

                                                       Ether’s Quest

-----------------------------------------------------------------------------------------------------------------------------

Small story-based D&D game, c++ window desktop application 64bit.

-----------------------------------------------------------------------------------------------------------------------------

Ether’s Quest is the final project for my c++ Computer Science – 1 (COSC 1030) at Laramie County. Community College.
https://www.lccc.wy.edu
https://lccc.wy.edu/pathways/sciTechEngMath/computerScienceProgram/index.aspx

-----------------------------------------------------------------------------------------------------------------------------

COSC 1030 – Computer Science 1
Professor: David Durbin
Fall Semester - 2022
Student: Alejandro (Alex) Ricciardi

-----------------------------------------------------------------------------------------------------------------------------

Requirement:

    MS Windows 10, 64 bit
    c++ 11 or later
    SFML (Simple and Fast Multimedia Library) 
    https://www.sfml-dev.org/
    I used MS Visual Studio IDE to create my program.

-----------------------------------------------------------------------------------------------------------------------------

Class Final Project Prerequisites:

“Your final project is to create an interactive, text-based Choose Your Own Adventure style game based on a movie, 
book or game of your choice. You may use your own idea if you don't want to base it on an existing property.
 If you aren't sure what I mean by Choose Your Own Adventure, see the "Cat Break" image file in this week's module. 
 (Credit to the author, Fox, for the Choose Your Own Adventure.).”

This project goes substantially beyond the Class Final Project Prerequisites; the project is a small c++ window desktop application.

-----------------------------------------------------------------------------------------------------------------------------

Project description:

Ether’s Quest is a small story-based “D&D game” based on the Innistrad universe. 
Where Ether journeys to save his younger sister Clarabella. 
Clarabella was abducted by the evil vampire lord, Salt, 
to be offered in sacrifice to the demon Iretrat. In exchange for Clarabella’s soul, 
Iretrat will reanimate Pantra, Salt’s lost love, using Clarabella’s blood. 
The sacrifice must be performed on the first day of the Hunter’s moon, 
at the Skirsdag high temple located in Stensia. 
Ether’s journey to save Clarabella will start at his home in Gavony; 
he will travel through the region of Nephalia , Kessig, and Stensia, 
where he will encounter many dangers. Provided that he survives the journey; 
at Skirsdag high temple, he will have to battle 
and defeat both lord Salt and the demon Iretrat to save Clarabella and complete his quest.

-----------------------------------------------------------------------------------------------------------------------------

Project Credits:

Lore: 
Magic The Gathering Innistrat,
https://magic.wizards.com/en/story/innistrad-plane

Images:
- Background images from PNG Slides 1 through 36, except PNG Slides 11 and 28,
Magic The Gathering Innistrat, https://magic.wizards.com/en/story/innistrad-plane
- Background images from PNG Slides 11 and 28, Matteo Ricciardi
- PNG Slides, Alejandro Ricciardi

Narrators Voices:
Micheala Ricciardi
Isaac Larme

Ambiences sounds:
Pixabay, https://pixabay.com/sound-effects/

Story:
Alejandro Ricciardi

-----------------------------------------------------------------------------------------------------------------------------

SFML
(Simple and Fast Multimedia Library)

Installing SFML library on MS Visual Studio guide:
 https://www.youtube.com/watch?v=YfMQyOw1zik&t=175s
Download SFML: https://www.sfml-dev.org/download/sfml/2.5.1/

-----------------------------------------------------------------------------------------------------------------------------

Project Map:

Folders:
        - img           contains the project .PNG slides files
        - ambiences     contains the project .wav ambiences sounds files
        - voices        contains the project .wav narration voices files
        - fonts         contains the project font file
        - SFML-2.5.1    contains the library SFML folders and files
        - demo          contains game footage pics and game run through video

Files:
       - <name>.dll (Dynamic Link Library) utilized to run and debugging SFML library
       - ether_quest.pdf project slides
       - flow_chart_ether_quest.pdf game flowchart
       - Ether's Quest.exe only works if you have MS Visual Studio installed on your PC, 
         the file has some .dll files dependencies associated with MS visual Studio.


-----------------------------------------------------------------------------------------------------------------------------

c++ Headers and .cpp files

- main.ccp
main instance

- hether.h
Contains the library headers
Contains Global Variables enumerators 
       INST_TYPE
       INST_RESULTS
       PLAYER_STATE
       ORIGINAL_WINDOW_SIZE
	Contains the struct Ether

- button.h button.cpp
The button class creates a button object to be displayed on a window.
	Accessor:
		void render() :
		Renders Button in the window
	Mutator:
		bool update():
		updated the color of the button if the button hovered or is pressed by the left button of the mouse.
		It returns true if the button was pressed.

- monster.h monster.cpp
The Monster class create objects with the states:
string name, int health, int armor, and int strength

- instances.h instances.cpp 
Contains the none fight instance functions 

- fight.h fight.cpp
Contains the fight instance functions.

- won.h won.cpp
Contains the won instance functions

- exit_game.h exit_game.cpp
Contains the Exit Game window Functions

- ewindow.h ewindow.cpp
Handles file load errors

        


