#!/usr/bin/env python3
"""Normalize the legacy "My Links" block in every README.md.

Replaces the entire legacy block with a canonical left-aligned HTML group
containing the AngryOwlAI, Code Chronicles, and social badges.

Run with --dry-run to preview a unified diff without writing any files.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

SKIP_DIR_PARTS = {".git", "node_modules"}

CANONICAL_BLOCK = """My Links:

<p align="left">
<a href="https://github.com/AngryOwlAI/"><img width="25" height="25" src="https://github.com/user-attachments/assets/ef169f03-2a25-4737-95e8-9b6a85491c9c" alt="AngryOwlAI logo"><img height="30" src="https://img.shields.io/badge/AngryOwlAI-0D1117?style=for-the-badge" alt="AngryOwlAI GitHub organization"></a>
<a href="https://www.alexomegapy.com"><img width="27" height="27" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53" alt="Code Chronicles logo"></a><a href="https://www.alexomegapy.com"><img height="30" src="https://img.shields.io/badge/Code%20Chronicles%20%7C%20Omegapy-0D1117?style=for-the-badge" alt="Code Chronicles | Omegapy"></a>
<a href="https://medium.com/@alex.omegapy"><img height="30" src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium"></a>
<a href="https://x.com/AlexOmegapy"><img height="30" src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X"></a>
<a href="https://www.youtube.com/@AngryOwl-AI"><img height="30" src="https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="YouTube"></a>
<a href="https://www.facebook.com/profile.php?id=100089638857137"><img height="30" src="https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook"></a>
<a href="https://linkedin.com/in/alex-ricciardi"><img height="30" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"></a>
<a href="https://www.threads.net/@alexomegapy?hl=en"><img height="30" src="https://img.shields.io/badge/Threads-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads"></a>
<a href="https://dev.to/alex_ricciardi"><img height="30" src="https://img.shields.io/badge/DEV.to-0A0A0A?style=for-the-badge&logo=devdotto&logoColor=white" alt="DEV.to"></a>
</p>
"""

# Match from the "My Links:" header line through the dev.to anchor line.
# The dev.to attachment id (3dee9933-...) is the final element in the canonical
# block, so anchoring on it ensures the regex captures the entire block.
BLOCK_PATTERN = re.compile(
    r"^My Links:[^\n]*\n"
    r"(?:[^\n]*\n)*?"
    r"[^\n]*3dee9933-d8c9-4a38-b32e-b7a3c55e7e97[^\n]*\n",
    re.MULTILINE,
)


def repair(text: str) -> tuple[str, int]:
    """Return (new_text, replacement_count)."""
    new_text, count = BLOCK_PATTERN.subn(CANONICAL_BLOCK, text)
    return new_text, count


def iter_readmes(root: Path):
    for path in root.rglob("README.md"):
        if set(path.parts) & SKIP_DIR_PARTS:
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Directory to scan (default: cwd).")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print diffs; do not write any files.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    total_files = 0
    changed_files = 0
    total_replacements = 0

    for path in iter_readmes(root):
        total_files += 1
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip (non-utf8): {path}", file=sys.stderr)
            continue

        new_text, count = repair(original)
        if count == 0 or new_text == original:
            continue

        changed_files += 1
        total_replacements += count
        rel = path.relative_to(root)

        if args.dry_run:
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                new_text.splitlines(keepends=True),
                fromfile=f"a/{rel}",
                tofile=f"b/{rel}",
                n=1,
            )
            sys.stdout.writelines(diff)
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"patched  {rel}")

    verb = "would patch" if args.dry_run else "patched"
    print(
        f"\nScanned {total_files} README.md files; "
        f"{verb} {changed_files} files ({total_replacements} blocks).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
