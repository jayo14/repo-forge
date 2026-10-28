#!/usr/bin/env python3
"""Scan, print the tree of, and zip a generated project.

Usage: package_repo.py <project_dir> <output.zip> [--scan]
"""
import os
import re
import sys
import zipfile

EXCLUDE_DIRS = {"node_modules", ".venv", "venv", "__pycache__", ".git", "dist",
                "build", ".next", ".turbo", "target", ".pytest_cache",
                ".ruff_cache", ".mypy_cache", "coverage"}
PLACEHOLDERS = [
    re.compile(r"\bTODO\b"),
    re.compile(r"rest of (the )?(code|file|implementation)", re.I),
    re.compile(r"\.\.\.\s*(existing|remaining|more) code", re.I),
    re.compile(r"your code here", re.I),
    re.compile(r"implement (this|me)\b", re.I),
]
TEXT_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".json", ".toml", ".md", ".yml",
            ".yaml", ".go", ".rs", ".cs", ".java", ".kt", ".sh", ".css", ".html",
            ".sql", ".env", ".example", ".txt", ".cfg", ".ini"}


def walk(root):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS)
        for name in sorted(files):
            yield os.path.join(dirpath, name)


def scan(root):
    problems = []
    for path in walk(root):
        if os.path.splitext(path)[1].lower() not in TEXT_EXT:
            continue
        if os.path.getsize(path) == 0 and os.path.basename(path) not in (
                "__init__.py", ".gitkeep"):
            problems.append((path, 0, "empty file"))
            continue
        try:
            with open(path, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    for pat in PLACEHOLDERS:
                        if pat.search(line):
                            problems.append((path, i, line.strip()[:80]))
        except UnicodeDecodeError:
            pass
    return problems


def print_tree(root):
    print(os.path.basename(os.path.abspath(root)) + "/")
    seen = set()
    for path in walk(root):
        rel = os.path.relpath(path, root)
        parts = rel.split(os.sep)
        for i in range(len(parts) - 1):
            d = os.sep.join(parts[: i + 1])
            if d not in seen:
                seen.add(d)
                print("  " * (i + 1) + parts[i] + "/")
        print("  " * len(parts) + parts[-1])


def make_zip(root, out):
    base = os.path.basename(os.path.abspath(root))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for path in walk(root):
            z.write(path, os.path.join(base, os.path.relpath(path, root)))
            count += 1
    print(f"\nZipped {count} files -> {out}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    root, out = args
    if not os.path.isdir(root):
        sys.exit(f"Not a directory: {root}")
    if "--scan" in sys.argv:
        problems = scan(root)
        if problems:
            print("Placeholder/empty-file problems found:")
            for p, ln, txt in problems:
                print(f"  {os.path.relpath(p, root)}:{ln}: {txt}")
            sys.exit(1)
        print("Scan clean: no placeholders or empty files.")
    print_tree(root)
    make_zip(root, out)


if __name__ == "__main__":
    main()
