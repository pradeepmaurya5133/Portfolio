#!/usr/bin/env python3
"""Cuts the two portrait crops the site needs from one source photo.

    python assets/img/_crop_portrait.py [path/to/photo.jpg]

Produces:
    portrait.jpg       900x900   — About page hero (.ph__media is a square)
    portrait-pill.jpg  720x304   — Home hero pill (1.75em / .74em = 2.365:1)

Both boxes use object-fit: cover, so cropping to the exact display ratio here
means the browser never crops again and the framing is predictable.

If you swap in a different photo, re-measure the three SUBJECT values below --
they are fractions of the image's width/height, not pixels, so they survive a
change of resolution.
"""
import pathlib
import sys

from PIL import Image

HERE = pathlib.Path(__file__).parent
DEFAULT_SRC = pathlib.Path.home() / "Downloads" / "Pradeep.jpg"

# Where the subject sits in the frame, as fractions of width/height.
FACE_X = 0.57   # centre of the face, horizontally
SQUARE_Y = 0.55  # vertical centre for the head-to-knees square
PILL_Y = 0.445   # vertical centre for the head-and-shoulders strip

SQUARE_SIDE = 980   # source pixels sampled for the square crop
PILL_WIDTH = 660    # source pixels sampled for the pill crop
PILL_RATIO = 2.365  # 1.75em / .74em, the pill's aspect ratio


def crop(im, cx, cy, cw, ch):
    """A cw x ch box centred on (cx, cy), clamped inside the frame."""
    w, h = im.size
    x = min(max(cx - cw / 2, 0), w - cw)
    y = min(max(cy - ch / 2, 0), h - ch)
    return im.crop((int(x), int(y), int(x + cw), int(y + ch)))


def main():
    src = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SRC
    if not src.exists():
        sys.exit(f"source photo not found: {src}")

    im = Image.open(src).convert("RGB")
    w, h = im.size
    print(f"source {src}  {w}x{h}")

    square = crop(im, FACE_X * w, SQUARE_Y * h, SQUARE_SIDE, SQUARE_SIDE)
    square.resize((900, 900), Image.LANCZOS).save(
        HERE / "portrait.jpg", quality=86, optimize=True, progressive=True)

    pill = crop(im, FACE_X * w, PILL_Y * h, PILL_WIDTH, int(PILL_WIDTH / PILL_RATIO))
    pill.resize((720, int(720 / PILL_RATIO)), Image.LANCZOS).save(
        HERE / "portrait-pill.jpg", quality=86, optimize=True, progressive=True)

    for name in ("portrait.jpg", "portrait-pill.jpg"):
        p = HERE / name
        print(f"  {name:<20} {Image.open(p).size}  {p.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
