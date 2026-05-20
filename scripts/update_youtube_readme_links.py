#!/usr/bin/env python3
"""Update legacy YouTube badge links in README.md files.

The script walks a target directory, finds every README.md file, and replaces
the old channel URL with the canonical @AngryOwl-AI handle URL.

Run with --dry-run to preview a unified diff without writing any files.
"""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

SKIP_DIR_PARTS = {
    ".claude",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "node_modules",
    "venv",
}

LEGACY_YOUTUBE_URL = "https://www.youtube.com/channel/UC4rMaQ7sqywMZkfS1xGh2AA"
CANONICAL_YOUTUBE_URL = "https://www.youtube.com/@AngryOwl-AI"


def iter_readmes(root: Path):
    for path in sorted(root.rglob("*")):
        if set(path.parts) & SKIP_DIR_PARTS:
            continue
        if not path.is_file() or path.name != "README.md":
            continue
        yield path


def replace_youtube_url(text: str) -> tuple[str, int]:
    count = text.count(LEGACY_YOUTUBE_URL)
    return text.replace(LEGACY_YOUTUBE_URL, CANONICAL_YOUTUBE_URL), count


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
    if not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2

    total_readmes = 0
    changed_files = 0
    total_replacements = 0

    for path in iter_readmes(root):
        total_readmes += 1
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"skip (non-utf8): {path}", file=sys.stderr)
            continue

        updated, replacements = replace_youtube_url(original)
        if replacements == 0:
            continue

        changed_files += 1
        total_replacements += replacements
        rel_path = path.relative_to(root)

        if args.dry_run:
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                updated.splitlines(keepends=True),
                fromfile=f"a/{rel_path}",
                tofile=f"b/{rel_path}",
                n=1,
            )
            sys.stdout.writelines(diff)
        else:
            path.write_text(updated, encoding="utf-8")
            print(f"patched {rel_path} ({replacements})")

    action = "would patch" if args.dry_run else "patched"
    print(
        f"Scanned {total_readmes} README.md files; "
        f"{action} {changed_files} files ({total_replacements} replacements).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
