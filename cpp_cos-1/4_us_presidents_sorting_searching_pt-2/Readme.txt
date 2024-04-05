-----------------------------------------------------------------------------------------------------------------------------	
				              c++ Computer Science – 1
-----------------------------------------------------------------------------------------------------------------------------

This repository is a collection of c++ program assignments from COSC 1030 - Computer Science-1 class at Laramie County Community College.
Related links:
https://www.lccc.wy.edu
https://lccc.wy.edu/pathways/sciTechEngMath/computerScienceProgram/index.aspx

-----------------------------------------------------------------------------------------------------------------------------

COSC 1030 – Computer Science 1
Professor: David Durbin
Fall Semester - 2022
Student: Alejandro (Alex) Ricciardi

-----------------------------------------------------------------------------------------------------------------------------

Requirement:
c++ 11 or later
I used MS Visiual Studio IDE to creat my programs

-----------------------------------------------------------------------------------------------------------------------------
					           Assignements
-----------------------------------------------------------------------------------------------------------------------------

---------------------------------------
4_us_presidents_sorting_searching_pt-2
---------------------------------------

President of the United States Information Dump

Using the link below to an external site. website, record information on past U.S. 
Presidents into a set of arrays (you may also use vectors, but they are more difficult to sort).
https://www.whitehouse.gov/about-the-white-house/presidents/

- potus_Last_Name (string): The President's last name. <- This is what you will sort by.
- potus_First_Name (string): The President's first name. <- Do NOT sort by this. 
  DO remember to include this when displaying the names. 
  If a middle initial is needed it should go here. (George H. W. Bush vs. George W. Bush)
- potus_Terms (int): The number of terms the President served.
- potus_FirstYear (int): The year the President started serving his term in office.  <- Note that this is NOT the same as the year the President was elected. 
  President Biden was elected in 2020, but his term started in 2021. (<- Most recent example.)

All of this information should be hard coded, there should be no user input up to this point.

You will need to have options for the user to do the following:

Display the list of Presidents, in order, first to most recent, in groups of 10.  i.e. Display Washington through Tyler, 
pause for user to hit a key, then display Polk through Garfield, etc. Yes, you need to list Cleveland twice.
Sort the list of names in Alphabetical order and display it in groups of 10 Presidents at a time. Again, 
display 1 through 10, wait for key press, then 11 through 20, etc. (i.e. Quincy-Adams should be sorted as a 'Q' not as an 'A'.)
Show only Presidents who served 1 term.
Show only Presidents who served 2 or more terms. (Yes, we had one 4 term President. (Yes, you should know that by now if you are from the U.S.))
Show a list of the Presidents and the year they started serving their term. Again, you need to show Cleveland twice.
You need to use functions for each of these options. At least one function for each one. That's five different functions just for the displays, 
plus those you'll need for the sorting and the searching.

Display a menu of the options that the user can choose from. Have the program clear the screen and return to the menu after each option is done.

--Don't forget an option to exit the program.

Note: 
There should be no input from the user other than their menu choices. All the Presidential data should be hard coded.

Hint: 
You can clear the screen by simply printing endl 30-50 times. Use a loop.
Input Validation: 
Do not accept options not included in the menu. (A, B, C or 1, 2, 3 etc.)
Screen Capture: 
Screen capture should show the first 20 presidents from the default display.

Note: 
Make sure the information you are displaying is accurate. 
Yes, there are Presidents I am not that fond of either, but that is no excuse for getting the information wrong.

Warning: 
The instructor just so happens to have his undergrad degree in U.S. History and will notice wild inaccuracies.

*** Please read  ***

This programm will only run on Window OS
It is important to note that:
Not all the Presidents served full terms.
Also, the US has/had 46 presidents but only 45 individuals served as Presidents
this is due to President Grover Cleveland who served 2 nonconsecutive terms, i.e., he is the 22sd and 24th President

Ter completion types:
- Full Term - the President completed a full term.
- Unfinished Term - the President did not complete a full term (passed away, assassinated, resigned).
- Partial Term - the President was the vice president and became the President after the elected President did not finish his term.

I utilized some of the information from the following website 
https://historyinpieces.com/research/presidential-inauguration-dates
