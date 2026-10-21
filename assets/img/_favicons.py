#!/usr/bin/env python3
"""Renders the favicon set from the PM monogram.

    python assets/img/_favicons.py

Produces:
    ../../favicon.ico              16 + 32 + 48, for /favicon.ico requests
    apple-touch-icon.png           180x180, iOS home screen
    icon-192.png, icon-512.png     Android / PWA install
    favicon.svg                    vector, for browsers that prefer it

The mark is drawn in a headless Chrome so it uses the site's own Archivo
webfont — an SVG favicon is rendered outside the page, so its font-family
never resolves and the text would otherwise fall back to Arial. Rasterising
here bakes the real typeface in.

Chrome is found automatically on Windows/macOS/Linux; override with the CHROME
environment variable if it lives somewhere unusual.
"""
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

from PIL import Image

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
FONT = HERE.parent / "fonts" / "archivo-3.woff2"   # latin subset

ACCENT = "#e22356"
INK = "#141414"

# Sizes baked into favicon.ico. 48 is what Windows uses for shortcuts.
ICO_SIZES = [16, 32, 48]
MASTER = 512


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "google-chrome", "chromium", "chromium-browser",
    ]
    for c in candidates:
        if os.path.sep in c:
            if pathlib.Path(c).exists():
                return c
        elif shutil.which(c):
            return shutil.which(c)
    return None


def markup(size):
    """Accent-filled tile with a white monogram.

    The site logo is dark with an accent hairline, but at 16px a hairline
    disappears and dark-on-dark browser chrome swallows the tile. A solid
    accent fill is what actually reads in a tab strip.
    """
    radius = round(size * 0.22)
    font_px = round(size * 0.46)
    return f"""<!doctype html><meta charset="utf-8">
<style>
  @font-face {{
    font-family: "Archivo Variable";
    src: url("file:///{FONT.as_posix()}") format("woff2-variations");
    font-weight: 100 900;
    font-stretch: 62% 125%;
  }}
  html, body {{ margin: 0; background: transparent; }}
  .tile {{
    width: {size}px; height: {size}px;
    border-radius: {radius}px;
    background: {ACCENT};
    display: grid; place-items: center;
    font-family: "Archivo Variable", Arial, sans-serif;
    font-weight: 800; font-stretch: 112%;
    font-size: {font_px}px; letter-spacing: {-font_px * 0.06:.2f}px;
    color: #fff; line-height: 1;
  }}
  .tile span {{ transform: translateY(2%); }}
</style>
<div class="tile"><span>PM</span></div>
"""


def render(chrome, size, out_png):
    with tempfile.TemporaryDirectory() as tmp:
        html = pathlib.Path(tmp) / "icon.html"
        html.write_text(markup(size), encoding="utf-8")
        subprocess.run([
            chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--default-background-color=00000000",
            f"--window-size={size},{size}",
            "--virtual-time-budget=4000",
            f"--user-data-dir={tmp}/profile",
            f"--screenshot={out_png}",
            html.as_uri(),
        ], capture_output=True)
    return pathlib.Path(out_png).exists()


def svg():
    """Vector twin of the raster tile. Text is kept as text — the monogram is
    only two letters, and any browser preferring the SVG renders it large
    enough that an Arial fallback is acceptable."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" role="img" aria-label="PM monogram">
<rect width="64" height="64" rx="14" fill="{ACCENT}"/>
<text x="32" y="41.5" text-anchor="middle" fill="#fff"
      font-family="Archivo, Helvetica, Arial, sans-serif"
      font-size="29" font-weight="800" letter-spacing="-1.6">PM</text>
</svg>
'''


def main():
    chrome = find_chrome()
    if not chrome:
        sys.exit("Chrome/Edge not found — set the CHROME environment variable.")
    print(f"renderer: {chrome}")

    master = HERE / "_icon-master.png"
    if not render(chrome, MASTER, master):
        sys.exit("render failed")

    src = Image.open(master).convert("RGBA")

    outputs = {
        "apple-touch-icon.png": 180,   # iOS ignores transparency, fill is opaque anyway
        "icon-192.png": 192,
        "icon-512.png": 512,
    }
    for name, size in outputs.items():
        img = src.resize((size, size), Image.LANCZOS)
        img.save(HERE / name, optimize=True)
        print(f"  assets/img/{name:<22} {size}x{size}  "
              f"{(HERE / name).stat().st_size / 1024:.1f} KB")

    ico = ROOT / "favicon.ico"
    src.save(ico, format="ICO", sizes=[(s, s) for s in ICO_SIZES])
    print(f"  favicon.ico{'':<22} {ICO_SIZES}  {ico.stat().st_size / 1024:.1f} KB")

    (HERE / "favicon.svg").write_text(svg(), encoding="utf-8")
    print(f"  assets/img/favicon.svg")

    master.unlink()


if __name__ == "__main__":
    main()
