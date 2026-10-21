#!/usr/bin/env python3
"""Generates the portfolio's placeholder artwork as SVG.

Run again after editing PROJECTS to refresh the covers:
    python assets/img/_generate.py
Swap any file for a real screenshot of the same name (keep the aspect ratio).
"""
import os
import pathlib

HERE = pathlib.Path(__file__).parent
INK = "#141414"
ACCENT = "#e22356"

# Only the projects that still need a placeholder. ConsentX, RegulatoryBridge
# and Xamlysis use real screenshots instead — see _frame_screenshot.py.
PROJECTS = [
    # slug, display name, kicker, ui flavour
    ("bakery",        "Bakery",        "E-commerce Web Application", "shop"),
    ("movie-scraper", "Movie Scraper", "Django Data Pipeline",       "pipeline"),
]


def grid(w, h, step=96, opacity=0.05):
    out = []
    x = step
    while x < w:
        out.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="#fff" stroke-opacity="{opacity}"/>')
        x += step
    y = step
    while y < h:
        out.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="#fff" stroke-opacity="{opacity}"/>')
        y += step
    return "".join(out)


def chrome(x, y, w, h):
    """Browser-ish window frame."""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#1b1b1b" stroke="#fff" stroke-opacity=".14"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="54" rx="10" fill="#232323"/>'
        f'<circle cx="{x+28}" cy="{y+27}" r="7" fill="{ACCENT}"/>'
        f'<circle cx="{x+52}" cy="{y+27}" r="7" fill="#fff" fill-opacity=".28"/>'
        f'<circle cx="{x+76}" cy="{y+27}" r="7" fill="#fff" fill-opacity=".18"/>'
        f'<rect x="{x+104}" y="{y+18}" width="{int(w*0.42)}" height="18" rx="9" fill="#fff" fill-opacity=".1"/>'
    )


def bar(x, y, w, h, o=0.16, fill="#fff", rx=4):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{o}"/>'


def ui(flavour, x, y, w, h):
    """Abstract product mock inside the window frame."""
    p = [chrome(x, y, w, h)]
    ix, iy = x + 32, y + 86
    iw, ih = w - 64, h - 118

    if flavour == "dashboard":
        p.append(bar(ix, iy, 220, ih, 0.07))
        for i in range(6):
            p.append(bar(ix + 18, iy + 24 + i * 44, 170, 14, 0.18 if i == 1 else 0.1))
        cw = (iw - 252) / 3 - 16
        for i in range(3):
            cx = ix + 252 + i * (cw + 24)
            p.append(bar(cx, iy, cw, 150, 0.07))
            p.append(bar(cx + 20, iy + 26, 90, 12, 0.14))
            p.append(f'<text x="{cx+20}" y="{iy+108}" fill="{ACCENT if i==0 else "#fff"}" '
                     f'fill-opacity="{1 if i==0 else .75}" font-family="Archivo, Arial" font-size="54" '
                     f'font-weight="800">{["98%","12.4k","24"][i]}</text>')
        p.append(bar(ix + 252, iy + 174, iw - 252, ih - 174, 0.05))
        for i in range(9):
            bh = 40 + (i * 37) % 170
            p.append(bar(ix + 290 + i * 74, iy + ih - 34 - bh, 44, bh,
                         0.9 if i == 5 else 0.16, ACCENT if i == 5 else "#fff"))

    elif flavour == "table":
        p.append(bar(ix, iy, iw, 56, 0.09))
        for c in range(5):
            p.append(bar(ix + 24 + c * (iw - 48) / 5, iy + 20, 110, 14, 0.2))
        for r in range(7):
            ry = iy + 72 + r * 62
            p.append(bar(ix, ry, iw, 50, 0.04))
            for c in range(5):
                wdt = [260, 150, 90, 170, 60][c]
                p.append(bar(ix + 24 + c * (iw - 48) / 5, ry + 18, wdt, 14,
                             0.85 if (c == 4 and r % 3 == 0) else 0.13,
                             ACCENT if (c == 4 and r % 3 == 0) else "#fff"))

    elif flavour == "shop":
        p.append(bar(ix, iy, iw, 40, 0.08))
        cols, rows = 4, 2
        cw = (iw - (cols - 1) * 20) / cols
        chh = (ih - 72 - 20) / rows
        for r in range(rows):
            for c in range(cols):
                cx, cy = ix + c * (cw + 20), iy + 72 + r * (chh + 20)
                p.append(bar(cx, cy, cw, chh, 0.06))
                p.append(bar(cx + 14, cy + 14, cw - 28, chh * 0.56, 0.1))
                p.append(bar(cx + 14, cy + chh * 0.56 + 28, cw * 0.6, 14, 0.2))
                p.append(bar(cx + 14, cy + chh * 0.56 + 52, 70, 22, 1, ACCENT, 11))

    elif flavour == "exam":
        p.append(bar(ix, iy, iw * 0.62, 56, 0.09))
        p.append(bar(ix + 24, iy + 20, 300, 16, 0.26))
        for i in range(4):
            oy = iy + 86 + i * 86
            p.append(bar(ix, oy, iw * 0.62, 66, 0.05))
            p.append(f'<circle cx="{ix+36}" cy="{oy+33}" r="13" fill="none" '
                     f'stroke="{ACCENT if i==1 else "#fff"}" stroke-opacity="{1 if i==1 else .3}" stroke-width="3"/>')
            if i == 1:
                p.append(f'<circle cx="{ix+36}" cy="{oy+33}" r="6" fill="{ACCENT}"/>')
            p.append(bar(ix + 66, oy + 26, 340 - i * 40, 14, 0.16))
        px = ix + iw * 0.66
        p.append(bar(px, iy, iw - iw * 0.66, 200, 0.06))
        p.append(f'<text x="{px+24}" y="{iy+108}" fill="#fff" font-family="Archivo, Arial" '
                 f'font-size="58" font-weight="800">24:18</text>')
        p.append(bar(px + 24, iy + 138, iw * 0.2, 10, 0.12, "#fff", 5))
        p.append(bar(px + 24, iy + 138, iw * 0.12, 10, 1, ACCENT, 5))

    else:  # pipeline
        stages = ["SOURCE", "SCRAPE", "VALIDATE", "STORE"]
        bw = (iw - 3 * 60) / 4
        for i, s in enumerate(stages):
            bx = ix + i * (bw + 60)
            p.append(bar(bx, iy + ih / 2 - 80, bw, 160, 0.07))
            p.append(f'<rect x="{bx}" y="{iy+ih/2-80}" width="{bw}" height="160" rx="4" fill="none" '
                     f'stroke="{ACCENT if i==2 else "#fff"}" stroke-opacity="{.9 if i==2 else .18}"/>')
            p.append(f'<text x="{bx+bw/2}" y="{iy+ih/2+6}" fill="#fff" fill-opacity=".8" text-anchor="middle" '
                     f'font-family="Archivo, Arial" font-size="26" letter-spacing="3" font-weight="600">{s}</text>')
            if i < 3:
                ax = bx + bw + 12
                p.append(f'<path d="M{ax} {iy+ih/2} H{ax+36} M{ax+24} {iy+ih/2-9} L{ax+36} {iy+ih/2} '
                         f'L{ax+24} {iy+ih/2+9}" stroke="{ACCENT}" stroke-width="3" fill="none"/>')
        for i in range(5):
            p.append(bar(ix, iy + ih - 90 + i * 0, 0, 0))
    return "".join(p)


def cover(slug, name, kicker, flavour, w=2560, h=1600):
    # No large wordmark baked in: every surface that shows a cover (index row,
    # work card, hover preview) already renders the project name in HTML, and a
    # baked-in title both duplicates it and gets cropped by the 16:10 card.
    #
    # Authored at 16:10 — the widest aspect any surface uses — so the 16:9 row
    # thumb and spotlight figure crop ~80px off the top and bottom rather than
    # cropping the sides (which clipped the kicker). pad_y absorbs that crop.
    pad_y = 330
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{name} — {kicker}">
<defs>
<radialGradient id="g-{slug}" cx="26%" cy="18%" r="95%">
<stop offset="0" stop-color="{ACCENT}" stop-opacity=".40"/>
<stop offset="45%" stop-color="#2a2a38" stop-opacity=".55"/>
<stop offset="100%" stop-color="{INK}"/>
</radialGradient>
</defs>
<rect width="{w}" height="{h}" fill="{INK}"/>
<rect width="{w}" height="{h}" fill="url(#g-{slug})"/>
{grid(w, h)}
<text x="200" y="238" fill="#fff" fill-opacity=".5" font-family="Archivo, Arial" font-size="36"
      letter-spacing="9" font-weight="600">{kicker.upper()}</text>
<circle cx="{w-212}" cy="224" r="16" fill="{ACCENT}"/>
<g opacity=".97">{ui(flavour, 200, pad_y, w - 400, h - pad_y * 2)}</g>
</svg>
'''


def mark(size=128):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" role="img" aria-label="PM monogram">
<rect width="{size}" height="{size}" rx="24" fill="{INK}"/>
<rect x="4" y="4" width="{size-8}" height="{size-8}" rx="20" fill="none" stroke="{ACCENT}" stroke-width="3"/>
<text x="{size/2}" y="{size*0.645}" text-anchor="middle" fill="#fff" font-family="Archivo, Arial"
      font-size="{int(size*0.42)}" font-weight="800" letter-spacing="-2">PM</text>
</svg>
'''


def og(w=1200, h=630):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs><radialGradient id="o" cx="25%" cy="20%" r="95%">
<stop offset="0" stop-color="{ACCENT}" stop-opacity=".45"/>
<stop offset="100%" stop-color="{INK}"/></radialGradient></defs>
<rect width="{w}" height="{h}" fill="{INK}"/><rect width="{w}" height="{h}" fill="url(#o)"/>
{grid(w, h, 60, 0.05)}
<text x="72" y="108" fill="#fff" fill-opacity=".6" font-family="Archivo, Arial" font-size="20"
      letter-spacing="7" font-weight="600">PRADEEP MAURYA</text>
<text x="72" y="300" fill="#fff" font-family="Archivo, Arial" font-size="106" font-weight="700"
      letter-spacing="-5">I build web apps</text>
<text x="72" y="400" fill="{ACCENT}" font-family="Archivo, Arial" font-size="106" font-weight="700"
      letter-spacing="-5">that perform.</text>
<text x="72" y="520" fill="#fff" fill-opacity=".6" font-family="Archivo, Arial" font-size="26">
Associate Web Developer · React, Next.js, Node.js, Python</text>
</svg>
'''


def write(path, text):
    (HERE / path).write_text(text, encoding="utf-8")
    print("wrote", path, len(text), "bytes")


if __name__ == "__main__":
    for slug, name, kicker, flavour in PROJECTS:
        write(f"{slug}.svg", cover(slug, name, kicker, flavour))
    write("mark.svg", mark())
    write("og.svg", og())
    # favicon.svg is owned by _favicons.py, which also renders the .ico and
    # PNG sizes from the same mark — don't write it from here too.
    print("done")
