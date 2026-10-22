#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepares a hero backdrop photo.

    python assets/img/_hero_bg.py <source> [--name hero-bg]
                                           [--ratio 16:9|native]
                                           [--widths 1280,1920]
                                           [--brightness 0.78] [--blur 0]

Writes one WebP per width, which the page picks between with srcset:

    <name>-<w>.webp   for every width except the largest
    <name>.webp       the largest

Backdrops sit behind the heading and under a shade gradient, so they are
darkened here as well as in CSS — a bright photo makes white type
unreadable, and baking part of that in keeps the CSS filter light enough
not to cost a repaint on every frame.

--blur is for sources that have to be upscaled: a little softening reads
as depth of field rather than as a low-resolution image.

Current users:
    hero-bg     index.html   16:9 source, no upscale
    skills-bg   skills.html  471x626 source, upscaled, so --blur 1.2
"""
import argparse
import pathlib

from PIL import Image, ImageEnhance, ImageFilter

HERE = pathlib.Path(__file__).parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--name", default="hero-bg")
    ap.add_argument("--ratio", default="16:9",
                    help='"16:9" to centre-crop, or "native" to keep the source shape')
    ap.add_argument("--widths", default="1280,1920")
    ap.add_argument("--brightness", type=float, default=0.78)
    ap.add_argument("--saturation", type=float, default=0.85)
    ap.add_argument("--blur", type=float, default=0.0)
    ap.add_argument("--quality", type=int, default=82)
    args = ap.parse_args()

    src = pathlib.Path(args.source)
    if not src.exists():
        raise SystemExit(f"no such file: {src}")

    im = Image.open(src).convert("RGB")
    print(f"source {src.name}  {im.size[0]}x{im.size[1]}")

    if args.ratio != "native":
        a, b = (float(x) for x in args.ratio.split(":"))
        target = a / b
        w, h = im.size
        if w / h > target:
            nw = int(h * target)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        elif w / h < target:
            nh = int(w / target)
            im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))

    ratio = im.size[0] / im.size[1]
    im = ImageEnhance.Brightness(im).enhance(args.brightness)
    im = ImageEnhance.Color(im).enhance(args.saturation)

    widths = sorted(int(x) for x in args.widths.split(","))
    for width in widths:
        out = im.resize((width, round(width / ratio)), Image.LANCZOS)
        if args.blur:
            out = out.filter(ImageFilter.GaussianBlur(args.blur))
        name = f"{args.name}.webp" if width == widths[-1] else f"{args.name}-{width}.webp"
        path = HERE / name
        out.save(path, "WEBP", quality=args.quality, method=6)
        up = width / im.size[0]
        print(f"  {name:22} {out.size[0]}x{out.size[1]}  "
              f"{path.stat().st_size:>7,} bytes  scale {up:.2f}x")


if __name__ == "__main__":
    main()
