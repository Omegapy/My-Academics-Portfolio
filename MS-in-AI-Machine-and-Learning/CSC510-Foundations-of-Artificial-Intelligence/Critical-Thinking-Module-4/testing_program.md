# Testing Instructions

## Hospital Medication-Delivery Robot Using A* Search

This document explains how to test `hospital_robot_astar.py` using the command line.   
The program terminal interface displays a hospital map; it asks you to choose a starting
location (s0) and destination (sg), and then it displays the optimal route found by A* search.

The program requires Python 3.11 or newer. It uses only the Python standard library, so no
third-party packages need to be installed.

## Method 1: Run with a Python Virtual Environment

A virtual environment keeps a project's Python setup separate from the rest of the
computer. The repository's virtual environment is named `.venv`.

### macOS or Linux

From the repository folder, activate the environment:

```bash
source .venv/bin/activate
```

Confirm the Python version:

```bash
python --version
```

The version must be Python 3.11 or newer. Then launch the program:

```bash
python hospital_robot_astar.py
```

When finished, leave the virtual environment with:

```bash
deactivate
```

### Windows PowerShell

From the repository folder, activate the environment:

```powershell
.venv\Scripts\Activate.ps1
```

Then check the version and launch the program:

```powershell
python --version
python CTA_Module-4\hospital_robot_astar.py
```

When finished, run `deactivate`.

### If `.venv` Does Not Exist

Creating a virtual environment is optional. To create one on macOS or Linux, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, run:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
```

No `pip install` command is needed because the program has no third-party dependencies.

## Method 2: Run Without a Virtual Environment

You can run the program directly when Python 3.11 or newer is already installed.

### macOS or Linux

From the repository folder, run:

```bash
python3 --version
python3 hospital_robot_astar.py
```

### Windows PowerShell

From the repository folder, run:

```powershell
py -3 --version
py -3 hospital_robot_astar.py
```

## Test 1: Use the Terminal Interface to Test the Default Route

| What the program displays                                      | What you should enter                                |
| -------------------------------------------------------------- | ---------------------------------------------------- |
| Press Enter to choose a starting location and destination...   | Press Enter.                                         |
| Choose the starting location (number/code; Enter = P):         | Press Enter to select `P`, the Pharmacy.             |
| Choose the destination (number/code; Enter = E):               | Press Enter to select `E`, the Emergency Department. |
| Any later message beginning with `Press Enter to...`           | Press Enter to continue.                             |

The program will display a route map, route directions, a table of moves, and a result
summary. 

```text
Starting location:                    P - (row 1, column 1) - Pharmacy
Destination:                          E - (row 11, column 29) - Emergency Department
Route found:                          Yes
Number of moves:                      38
Total travel cost (g at goal):        44.0 cost units
```

The last message should be:

```text
Finished: A* found a route to the destination.
```

## Test 2: Use the Interface to Test Input 

Launch the program again and press Enter at the first pause. Then do these steps:

1. Enter `Z` for the starting location. The program should reject it with:

   ```text
   I did not recognize that choice. Enter a menu number or location code.
   ```

2. Enter `P` for the starting location. The program should accept it.
3. Enter `P` again for the destination. The program should reject it with:

   ```text
   Choose a destination different from the starting location.
   ```

4. Enter `E` for the destination.
5. Press Enter at each later pause so the program can calculate and display the route.

This test passes when both invalid choices are rejected, the program asks again instead of
stopping, and the valid `P`-to-`E` route finishes successfully.

## Test 3: Use the Interface to Test a Different Route

Launch the program again. Choose a different pair of locations by entering either the menu
number or the one-letter code. For example:

```text
Choose the starting location (number/code; Enter = P): L
Choose the destination (number/code; Enter = E): N
```

Press Enter at each pause. This test passes when the route map marks the selected start with
`A`, marks the destination with `G`, shows the route with `*`, and reports `Route found: Yes`.

## Built-In Verification

The script also provides an automatic map and algorithm check. 

```bash
python hospital_robot_astar.py --verify-map --no-color --no-pause
```

The script will output the result of the verification:

```text
All internal verification checks passed.
```

