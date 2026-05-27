# ---------------------------------
# Author: Alexander Ricciardi 
# Date: 2026-05-20
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Spring C 2026
# ---------------------------------

"""Creates a file2.txt with 1,000 random-number lines.

Writes one random integer per line to a text file.
"""

from __future__ import annotations

import random
from pathlib import Path


# Number of random numbers to generate
LINE_COUNT = 1000  

# Maximum value for a 16-bit signed integer
MAX_BASH_RANDOM = 32767  

# Name of the output file
OUTPUT_FILE = Path("file2.txt")  


# ---- write_random_num()
def write_random_num(output_path: Path, line_count: int) -> None:
    """Write lines ofrandom integer lines to a text file.

    Args:
        output_path: Path to the text file.
        line_count: Number of random-num lines to write.

    Returns:
        None.
    """
    # Open the output file in write mode 
    with output_path.open("w", encoding="utf-8") as file_handle:
        # Write random integer per line.
        for _ in range(line_count):
            random_num = random.randint(0, MAX_BASH_RANDOM)
            file_handle.write(f"{random_num}\n")

# ----

# ---- main()
def main() -> None:
    """Run the program."""
    
    # Call the write_random_num() function that creates 
    # the text file with random numbers.
    write_random_num(OUTPUT_FILE, LINE_COUNT)
    
    # Print confirmation message.
    print(f"Created {OUTPUT_FILE} with {LINE_COUNT} lines.")

# ---- 


if __name__ == "__main__":
    main()
