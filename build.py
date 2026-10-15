#!/usr/bin/env python3
"""Copy the checked-in static How to Fish site into the Pages build directory."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "dist"
SOURCE_ONLY = {
    ".git",
    ".github",
    ".wrangler",
    "build.py",
    "dist",
    "functions",
    "README.md",
    "tools",
    "wrangler.jsonc",
}


def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for source in ROOT.iterdir():
        if source.name in SOURCE_ONLY or source.name.startswith("."):
            continue
        target = OUTPUT_DIR / source.name
        if source.is_dir():
            if source.name == "assets" or (source / "index.html").is_file():
                shutil.copytree(source, target, dirs_exist_ok=True)
        elif source.is_file() and (source.suffix == ".html" or source.name in {"robots.txt", "sitemap.xml", "_headers", "_redirects", "llms.txt"}):
            shutil.copy2(source, target)
    assert not any((OUTPUT_DIR / name).exists() for name in (".dev.vars", ".env", "functions", "wrangler.jsonc"))
    print(f"Built static site in {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    build()
