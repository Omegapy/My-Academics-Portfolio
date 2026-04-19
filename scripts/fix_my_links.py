#!/usr/bin/env python3
"""Repair malformed anchor tags in the "My Links" blocks of every README.md.

The original markup uses `<i><a href="..."><img ...></i>` (or the `<span>` variant),
which never closes the `<a>` tag. GitHub's sanitizer then renders the badges and
labels incorrectly. This script rewrites those fragments to proper HTML:
    <a href="..." ...><img ...></a>

Run with --dry-run to preview a unified diff without writing any files.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path

SKIP_DIR_PARTS = {".git", "node_modules"}
SKIP_PATH_SUBSTR = (".claude/worktrees",)

PATTERN = re.compile(
    r"<(?P<tag>i|span)>\s*"
    r"<a\s+href=\"(?P<href>[^\"]+)\"(?P<attrs>[^>]*)>\s*"
    r"<img(?P<img>[^>]+)>\s*"
    r"</(?P=tag)>",
    flags=re.DOTALL | re.IGNORECASE,
)


def repair(text: str) -> tuple[str, int]:
    """Return (new_text, replacement_count)."""

    def _sub(m: re.Match[str]) -> str:
        href = m.group("href")
        attrs = m.group("attrs") or ""
        img = m.group("img")
        return f'<a href="{href}"{attrs}><img{img}></a>'

    new_text, count = PATTERN.subn(_sub, text)
    return new_text, count


def iter_readmes(root: Path):
    for path in root.rglob("README.md"):
        parts = set(path.parts)
        if parts & SKIP_DIR_PARTS:
            continue
        sp = str(path)
        if any(s in sp for s in SKIP_PATH_SUBSTR) and root.resolve() not in path.resolve().parents:
            # allow the current worktree itself (the script runs inside it),
            # but skip OTHER worktrees nested under .claude/worktrees/*.
            if ".claude/worktrees/" in sp and not sp.startswith(str(root.resolve())):
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
        if count == 0:
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
                n=2,
            )
            sys.stdout.writelines(diff)
        else:
            path.write_text(new_text, encoding="utf-8")
            print(f"patched {count:>2}x  {rel}")

    verb = "would patch" if args.dry_run else "patched"
    print(
        f"\nScanned {total_files} README.md files; "
        f"{verb} {changed_files} files ({total_replacements} replacements).",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
