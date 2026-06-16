#!/usr/bin/env python3
"""harvest.py — deterministic evidence collector for outfit.

Gathers raw material about a project so the agent does not burn context
re-listing it. It DECIDES NOTHING: no classification, no domain inference.
Output is a markdown evidence dossier on stdout.

Usage: python3 scripts/harvest.py [root]   # root defaults to "."
"""
import os
import subprocess
import sys
from pathlib import Path

NOISE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
    ".next", ".turbo", "target", ".idea", ".vscode", "coverage", ".pytest_cache",
    ".mypy_cache", ".ruff_cache", "vendor", ".cache",
}
MAX_ENTRIES = 400  # cap tree size so harvest stays bounded


def build_tree(root, max_depth=3):
    """Return a newline-joined indented tree, skipping noise dirs, depth-bounded."""
    root = Path(root)
    lines = []
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in NOISE_DIRS)
        rel = Path(dirpath).relative_to(root)
        depth = 0 if str(rel) == "." else len(rel.parts)
        if depth > max_depth:
            dirnames[:] = []
            continue
        indent = "  " * depth
        if str(rel) != ".":
            lines.append(f"{indent}{rel.parts[-1]}/")
        for name in sorted(filenames):
            count += 1
            if count > MAX_ENTRIES:
                lines.append(f"{indent}  … (truncated at {MAX_ENTRIES} files)")
                return "\n".join(lines)
            lines.append(f"{indent}  {name}")
    return "\n".join(lines)


KEY_FILES = [
    "CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md", "README.rst",
    "package.json", "pyproject.toml", "setup.py", "requirements.txt",
    "go.mod", "Cargo.toml", "Gemfile", "composer.json", "pom.xml",
    "build.gradle", "Makefile", "docker-compose.yml", "Dockerfile",
    "tsconfig.json", ".tool-versions",
]


def read_key_files(root, max_bytes=4000):
    """Return [(name, content)] for present key files, each byte-bounded."""
    root = Path(root)
    out = []
    for name in KEY_FILES:
        p = root / name
        if not p.is_file():
            continue
        raw = p.read_bytes()[:max_bytes]
        text = raw.decode("utf-8", errors="replace")
        if p.stat().st_size > max_bytes:
            text += "\n… (truncated)"
        out.append((name, text))
    return out
