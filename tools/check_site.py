#!/usr/bin/env python3
"""Check the static Pages output and optional sign-in integration."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist"
INDEXNOW_KEY = "e0d0a3ba087443e3a3e0ab8fed29896b"


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def main() -> int:
    if not SITE.is_dir():
        fail("dist/ is missing; run python3 build.py first")

    required = ("login.html", "assets/login.css", "assets/login.js")
    for rel in required:
        if not (SITE / rel).is_file():
            fail(f"missing {rel}")
        print(f"PASS {rel} exists")

    login = (SITE / "login.html").read_text(encoding="utf-8")
    if '<link rel="stylesheet" href="/assets/login.css">' not in login:
        fail("login.html must load external /assets/login.css")
    if '<script type="module" src="/assets/login.js"></script>' not in login:
        fail("login.html must load external /assets/login.js")
    if re.search(r"<style\b|<script\b[^>]*>[^<]", login, re.IGNORECASE):
        fail("login.html contains inline CSS or JavaScript")
    print("PASS login page uses external CSS and JavaScript")

    pages = sorted(SITE.rglob("*.html"))
    if not pages:
        fail("no HTML pages found in dist/")
    nav_pages = [page for page in pages if page.name != "login.html"]
    missing_nav = [
        page.relative_to(SITE).as_posix()
        for page in nav_pages
        if 'href="/login.html">Log in</a>' not in page.read_text(encoding="utf-8")
    ]
    if missing_nav:
        fail("Log in navigation missing from: " + ", ".join(missing_nav))
    print(f"PASS Log in navigation present on all {len(nav_pages)} content pages")

    privacy = SITE / "privacy" / "index.html"
    if not privacy.is_file():
        fail("privacy/index.html is missing")
    privacy_text = privacy.read_text(encoding="utf-8")
    for disclosure in ("Optional account sign-in", "email only when the provider supplies one that is verified", "Cloudflare KV"):
        if disclosure not in privacy_text:
            fail(f"privacy disclosure missing: {disclosure}")
    print("PASS privacy page discloses sign-in and stored account data")

    for rel in ("functions", "wrangler.jsonc"):
        if (SITE / rel).exists():
            fail(f"private runtime file leaked into static output: {rel}")
    print("PASS auth source and Wrangler config excluded from static output")

    key_file = SITE / f"{INDEXNOW_KEY}.txt"
    if not key_file.is_file():
        fail(f"missing {INDEXNOW_KEY}.txt")
    body = key_file.read_bytes()
    if body not in {INDEXNOW_KEY.encode("ascii"), f"{INDEXNOW_KEY}\n".encode("ascii")}:
        fail("IndexNow key file must contain only the key")
    print(f"PASS {INDEXNOW_KEY}.txt is plain text")
    print(f"All checks passed ({len(pages)} HTML pages).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
