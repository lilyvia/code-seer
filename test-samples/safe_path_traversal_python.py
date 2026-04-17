import os
from pathlib import Path


# Safe: Validate path is within base directory
def safe_open(base_dir, usr_path):
    base = Path(base_dir).resolve()
    dest = (base / usr_path).resolve()
    if base != dest and base not in dest.parents:
        raise ValueError("Path traversal detected")
    return open(dest, 'r', encoding='utf-8')


# Safe: Use os.path.realpath for validation
def safe_read(base_dir, usr_path):
    full = os.path.realpath(os.path.join(base_dir, usr_path))
    base = os.path.realpath(base_dir)
    if not full.startswith(base + os.sep):
        raise ValueError("Invalid path")
    with open(full, 'r') as f:
        return f.read()
