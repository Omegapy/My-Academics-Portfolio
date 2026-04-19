#!/usr/bin/env python3
"""Normalize the "My Links" block in every README.md.

Replaces the entire block (from the "My Links:" header through the YouTube
badge line) with a canonical layout that renders correctly on GitHub:
properly closed <a> tags, `align="left"` on the image tags, grouping of
shields-style badges between the two anchor groups, and blank-line
separators between groups.

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

<a href="https://www.alexomegapy.com" target="_blank"><img width="25" height="25" align="left" src="https://github.com/user-attachments/assets/a8e0ea66-5d8f-43b3-8fff-2c3d74d57f53"></a>
<a href="https://www.alexomegapy.com" target="_blank"><img width="150" height="23" align="left" src="https://github.com/user-attachments/assets/caa139ba-6b78-403f-902b-84450ff4d563"></a>

[![Medium](https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=whit)](https://medium.com/@alex.omegapy)
[![X](https://img.shields.io/badge/X-black.svg?logo=X&logoColor=white)](https://x.com/AlexOmegapy)
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?logo=YouTube&logoColor=white)](https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA)
[![Facebook](https://img.shields.io/badge/Facebook-%231877F2.svg?logo=Facebook&logoColor=white)](https://www.facebook.com/profile.php?id=100089638857137)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?logo=linkedin&logoColor=white)](https://linkedin.com/in/alex-ricciardi)

<a href="https://www.threads.net/@alexomegapy?hl=en" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/58c9e833-4501-42e4-b4fe-39ffafba99b2"></a>
<a href="https://dev.to/alex_ricciardi" target="_blank"><img width="53" height="20" align="left" src="https://github.com/user-attachments/assets/3dee9933-d8c9-4a38-b32e-b7a3c55e7e97"></a>
"""

# Match from the "My Links:" header line through the line containing the
# YouTube channel URL. The YouTube URL is identical in every README, so it is
# a reliable anchor for the end of the block, whether the block spans many
# lines (multi-line layout) or just two (single-line layout).
BLOCK_PATTERN = re.compile(
    r"My Links:[^\n]*\n"
    r"(?:[^\n]*\n)*?"
    r"[^\n]*UC4rMaQ7sqywMZkfS1xGh2AA[^\n]*\n"
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
