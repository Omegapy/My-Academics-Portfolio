# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

"""Process the second half of the Module 8 split input files."""

from __future__ import annotations

from pathlib import Path

import bigdata_sum


# ======
# Constants
# ======

SCRIPT_DIR = Path(__file__).resolve().parent
HALF_DIR = SCRIPT_DIR / "generated" / "half"


# ======
# Main Script
# ======


# ---- main()
def main() -> int:
    """Run the second-half summation worker.

    Args:
        None.

    Returns:
        Process exit code.
    """
    return bigdata_sum.main(
        default_method="half_parallel_part_01", # Default benchmark method name
        default_input_a=HALF_DIR / "file1_part_01.txt", # Default first input file path
        default_input_b=HALF_DIR / "file2_part_01.txt", # Default second input file path
        default_output=HALF_DIR / "total_part_01.txt", # Default output file path
    )


# ---- end main()


if __name__ == "__main__":
    raise SystemExit(main())
