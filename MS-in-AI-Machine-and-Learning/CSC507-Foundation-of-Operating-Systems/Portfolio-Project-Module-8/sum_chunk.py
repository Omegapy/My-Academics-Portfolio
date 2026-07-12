# Author: Alexander Ricciardi 
# Date: 2026-07-05
# Course: CSC507 
# Professor: Dr. Joseph Issa 
# Term: Spring C 2026
# 
# ----------------------------------------

"""Process one numbered chunk for the ten-way Module 8 benchmark."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

import bigdata_sum


# ======
# Constants
# ======

SCRIPT_DIR = Path(__file__).resolve().parent
CHUNK_DIR = SCRIPT_DIR / "generated" / "chunks"


# ======
# Argument Helpers
# ======


# ---- normalize_chunk_index()
def normalize_chunk_index(chunk_index: str) -> str:
    """Normalize a chunk index to a two-digit suffix.

    Args:
        chunk_index: User-supplied chunk index.

    Returns:
        Two-digit chunk suffix.
    """
    return f"{int(chunk_index):02d}"


# ---- end normalize_chunk_index()


# ---- parse_wrapper_args()
def parse_wrapper_args() -> tuple[str, list[str]]:
    """Parse wrapper-specific arguments before delegating to bigdata_sum.

    Args:
        None.

    Returns:
        Tuple containing the normalized chunk suffix and remaining arguments.
    """
    parser = argparse.ArgumentParser(add_help=False) # Create an argument parser
    parser.add_argument("--chunk-index", default=os.environ.get("CHUNK_INDEX", "00")) # Add a chunk index argument that defaults to 00
    namespace, remaining_args = parser.parse_known_args() # Parse the arguments
    return normalize_chunk_index(namespace.chunk_index), remaining_args # Return the normalized chunk suffix and the remaining arguments


# ---- end parse_wrapper_args()


# ======
# Main Script
# ======


# ---- main()
def main() -> int:
    """Run the selected chunk summation worker.

    Args:
        None.

    Returns:
        Process exit code.
    """
    chunk_suffix, remaining_args = parse_wrapper_args()
    return bigdata_sum.main(
        argv=remaining_args, # Pass the remaining arguments to bigdata_sum
        default_method=f"ten_way_chunk_{chunk_suffix}", # Set the default method to ten_way_chunk_ plus the chunk suffix
        default_input_a=CHUNK_DIR / f"file1_part_{chunk_suffix}.txt", # Set the default input file path to the first part of the chunk
        default_input_b=CHUNK_DIR / f"file2_part_{chunk_suffix}.txt", # Set the default input file path to the second part of the chunk
        default_output=CHUNK_DIR / f"total_part_{chunk_suffix}.txt", # Set the default output file path to the total of the chunk
    )


# ---- end main()


if __name__ == "__main__":
    raise SystemExit(main())
