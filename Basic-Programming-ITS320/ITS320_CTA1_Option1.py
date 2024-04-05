#-------------------------------------------
# Program Name: ITS320_CTA1_Option1
# Author: Alejandro (Alex) Ricciardi
# Date: 02/15/2024
#-------------------------------------------
# Pseudocode:
# 1. Define a banner string for a decorative header.
# 2. Define three different representations of the same mouse using ASCII art
#    a. A multi-line string representation.
#    b. A single string using newline characters string.
#    c. An array of strings, each representing a line of the mouse.
# 3. Print the banner
# 4. Print each mouse representation using three different methods:
#    - Method-1, using a multi-line string
#    - Method-2, using new-line characters strings
#    - Method-3, using a string array
#-------------------------------------------
# Program Inputs: None
# Program Outputs:
# 1. A decorative banner.
# 2. Three ASCII art representations of the same mouse.
#-------------------------------------------

#---- Global Variables
#-- string literal

banner = '''
        *********************
        *   An ASCII Mouse  *
        *********************        
'''
# the line '(\-' or '\\-' will trigger a python SyntaxWarning
# in a multiline string when using the function print(multiline string)
# replacing '\' with the symbols '%c' and print(mouse_multiline % 92)
# removes the warnings, 92 is the character '\' ASCII
mouse_multiline = '''
             (%c-.
             / _`> 
     _)     / _)=
    (      / _/
     `-.__(___)_  
'''

mouse_newline = "            (\\-.\n            / _`>\n    _)     / _)=\n   (      / _/\n    `-.__(___)_"

mouse_lines = [
    "            (\\-.",
    "            / _`>",
    "    _)     / _)=",
    "   (      / _/",
    "    `-.__(___)_ "
]

#---- Main function
def main():  
    print(banner)
    print("\nMethod-1, using a multi-line string:")
    print(mouse_multiline % 92) # 92 is the character '\' ASCII
    print("Method-2, using new-line characters:\n")
    print(mouse_newline)
    print("\nMethod-3, using string array:\n")
    for line in mouse_lines:
        print(line)

if __name__ == '__main__': main()
