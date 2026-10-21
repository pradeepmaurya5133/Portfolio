#!/usr/bin/env python3
"""Turns a raw browser screenshot into a project cover.

    python assets/img/_frame_screenshot.py

Crops the browser's own toolbar off the top, then sits the page on the same
dark canvas the generated covers use (radial accent wash + grid) inside a
neutral window frame. Output is 2560x1600 — the widest ratio any surface uses,
so the 16:9 index row and spotlight crop vertically into the margin rather than
clipping the page.

To add or re-cut a shot, add an entry to SHOTS. `chrome_px` is how many pixels
of browser UI to remove from the top; find it by looking at where the page
actually starts. The window is sized from the cropped image's own aspect, so
nothing is cropped horizontally.
"""
import pathlib
import sys

from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).parent
SHOTS_DIR = pathlib.Path.home() / "Pictures" / "Screenshots"

INK = (20, 20, 20)
ACCENT = (226, 35, 86)

# slug -> (source filename, pixels of browser chrome to crop off the top)
SHOTS = {
    "consentx":         ("Screenshot 2026-10-21 172520.png", 72),
    "regulatorybridge": ("Screenshot 2026-10-21 172727.png", 67),
    "xamlysis":         ("Screenshot 2026-10-21 172902.png", 23),
}

W, H = 2560, 1600
MARGIN_X = 200
BAR = 56          # height of the window's title bar
RADIUS = 16


def backdrop():
    """Dark canvas with the radial accent wash and grid the SVG covers use."""
    base = Image.new("RGB", (W, H), INK)

    # Radial wash, drawn at low res and scaled up — fast and smooth enough.
    sw, sh = 160, 100
    wash = Image.new("RGB", (sw, sh), INK)
    wp = wash.load()
    cx, cy = sw * 0.26, sh * 0.18
    far = (sw ** 2 + sh ** 2) ** 0.5
    for y in range(sh):
        for x in range(sw):
            d = (((x - cx) ** 2 + (y - cy) ** 2) ** 0.5) / far
            t = max(0.0, 1.0 - d / 0.95)
            # accent near the hotspot, cool grey mid, ink at the edges
            if t > 0.55:
                k = (t - 0.55) / 0.45
                col = (42 + (ACCENT[0] - 42) * k * 0.40,
                       42 + (ACCENT[1] - 42) * k * 0.40,
                       56 + (ACCENT[2] - 56) * k * 0.40)
            else:
                k = t / 0.55
                col = (INK[0] + (42 - INK[0]) * k,
                       INK[1] + (42 - INK[1]) * k,
                       INK[2] + (56 - INK[2]) * k)
            wp[x, y] = tuple(int(c) for c in col)
    base = Image.blend(base, wash.resize((W, H), Image.BICUBIC), 0.92)

    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    g = ImageDraw.Draw(grid)
    for x in range(96, W, 96):
        g.line([(x, 0), (x, H)], fill=(255, 255, 255, 13))
    for y in range(96, H, 96):
        g.line([(0, y), (W, y)], fill=(255, 255, 255, 13))
    return Image.alpha_composite(base.convert("RGBA"), grid)


def rounded(img, radius):
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1],
                                           radius=radius, fill=255)
    img.putalpha(mask)
    return img


def frame(slug, src_name, chrome_px):
    src = SHOTS_DIR / src_name
    if not src.exists():
        print(f"  !! missing source: {src}")
        return False

    shot = Image.open(src).convert("RGB")
    shot = shot.crop((0, chrome_px, shot.size[0], shot.size[1]))

    # Size the window from the shot's own aspect so nothing is cropped sideways.
    inner_w = W - MARGIN_X * 2
    inner_h = round(inner_w * shot.size[1] / shot.size[0])
    win_h = inner_h + BAR
    win_y = (H - win_h) // 2

    win = Image.new("RGBA", (inner_w, win_h), (27, 27, 27, 255))
    d = ImageDraw.Draw(win)
    d.rectangle([0, 0, inner_w, BAR], fill=(35, 35, 35, 255))
    for i, col in enumerate([ACCENT + (255,), (255, 255, 255, 72), (255, 255, 255, 46)]):
        cx = 28 + i * 24
        d.ellipse([cx - 7, BAR // 2 - 7, cx + 7, BAR // 2 + 7], fill=col)
    d.rounded_rectangle([104, BAR // 2 - 9, 104 + int(inner_w * 0.42), BAR // 2 + 9],
                        radius=9, fill=(255, 255, 255, 26))
    win.paste(shot.resize((inner_w, inner_h), Image.LANCZOS), (0, BAR))
    d.rounded_rectangle([0, 0, inner_w - 1, win_h - 1], radius=RADIUS,
                        outline=(255, 255, 255, 36), width=2)
    win = rounded(win, RADIUS)

    canvas = backdrop()

    # Soft drop shadow under the window.
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [MARGIN_X + 10, win_y + 24, MARGIN_X + inner_w - 10, win_y + win_h + 24],
        radius=RADIUS, fill=(0, 0, 0, 130))
    canvas = Image.alpha_composite(canvas, shadow)

    canvas.alpha_composite(win, (MARGIN_X, win_y))

    out = HERE / f"{slug}.jpg"
    canvas.convert("RGB").save(out, quality=88, optimize=True, progressive=True)
    print(f"  {slug}.jpg  {canvas.size}  window {inner_w}x{win_h} @ y={win_y}"
          f"  {out.stat().st_size / 1024:.0f} KB")
    return True


def main():
    only = sys.argv[1:] or list(SHOTS)
    print(f"sources: {SHOTS_DIR}")
    for slug in only:
        if slug not in SHOTS:
            print(f"  !! unknown slug: {slug}")
            continue
        frame(slug, *SHOTS[slug])


if __name__ == "__main__":
    main()
