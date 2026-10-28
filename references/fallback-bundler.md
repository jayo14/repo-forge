# Fallback bundler (Path B only)

Use when the environment cannot create or zip files (plain chat, any AI). After printing all files, output a single Python script that writes the whole project. Python is the default because it runs on macOS, Linux and Windows. Embed each file as a raw triple-quoted string so no escaping is needed. If a file contains triple quotes, use the `FILES` entry with a list of lines instead.

Template:

```python
#!/usr/bin/env python3
"""Recreate <project-name> and zip it. Run: python setup_project.py"""
import os, zipfile

ROOT = "<project-name>"

FILES = {
    "README.md": r'''...full contents...''',
    "src/main.py": r'''...full contents...''',
    # one entry per file in the tree, nothing omitted
}

for rel, content in FILES.items():
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)

with zipfile.ZipFile(f"{ROOT}.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for dirpath, _, names in os.walk(ROOT):
        for n in names:
            full = os.path.join(dirpath, n)
            z.write(full, os.path.relpath(full, os.path.dirname(ROOT) or "."))

print(f"Created {ROOT}/ and {ROOT}.zip")
```

If the project is large, split into `setup_part1.py`, `setup_part2.py`, each writing a subset of files into the same root, and say which order to run them in. The bundler duplicates every file, so for big projects tell the user they can use either the labeled files or the bundler, not both.
