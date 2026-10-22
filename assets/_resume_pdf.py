#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Renders resume.html to assets/Pradeep_Maurya_Resume.pdf.

    python assets/_resume_pdf.py

Headless Chrome prints the page using assets/css/print.css — the exact
stylesheet a visitor's own "Print / Save as PDF" button uses, so the
committed file and the browser export cannot drift apart.

Run this after any change to the resume content in build.py or to
print.css, then re-run build.py. The download button on resume.html only
renders when this file exists, so a stale or missing PDF is never
advertised.

Needs Google Chrome (or Chromium/Edge) installed; no Python packages.
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "resume.html"
OUT = ROOT / "assets" / "Pradeep_Maurya_Resume.pdf"

CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def find_chrome():
    for name in ("chrome", "google-chrome", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    for path in CANDIDATES:
        if pathlib.Path(path).exists():
            return path
    return None


def main():
    if not PAGE.exists():
        sys.exit("resume.html is missing — run `python build.py` first.")

    chrome = find_chrome()
    if not chrome:
        sys.exit("Chrome/Chromium/Edge not found. Install one, or use the "
                 "Print / Save as PDF button on the page instead.")

    with tempfile.TemporaryDirectory() as profile:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-default-browser-check",
            f"--user-data-dir={profile}",
            # Chrome's own page headers/footers would stamp a URL and a date
            # across a document meant to read as a resume.
            "--no-pdf-header-footer",
            # the animation JS has nothing to do in a print render, but the
            # fonts and stylesheets do need a moment to arrive
            "--virtual-time-budget=6000",
            f"--print-to-pdf={OUT}",
            PAGE.as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)

    if not OUT.exists() or OUT.stat().st_size == 0:
        sys.exit("Chrome did not produce a PDF.\n" + (proc.stderr or "")[-2000:])

    print(f"{OUT.relative_to(ROOT)}  {OUT.stat().st_size:,} bytes")
    print("Now re-run `python build.py` so the download button renders.")


if __name__ == "__main__":
    main()
