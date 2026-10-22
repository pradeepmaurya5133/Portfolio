#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepares the footer background loop.

    python assets/video/_footer_bg.py <source.mp4>

Writes two files:

    footer-bg.mp4    H.264, 1280x720, 30fps, no audio, faststart
    footer-bg.jpg    poster frame, darkened to match the video under its shade

Why these settings:

  * H.264 only. A VP9 WebM of the same clip came out just 13% smaller,
    which does not pay for a second file and a second encode.
  * 30fps, not the source's 60. Nothing in a background loop needs 60, and
    halving the frame rate is most of the size saving.
  * -movflags +faststart puts the index at the front so playback can begin
    before the whole file has arrived.
  * No audio track is produced; the footer must never make noise.

The poster matters more than usual here: the <video> is preload="none" and
only starts downloading once the footer scrolls into view, so the poster is
what visitors see until then — and all they ever see if they have asked for
reduced motion.

Needs ffmpeg. Uses the copy bundled with imageio-ffmpeg if one is not on PATH.
"""
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
MP4 = HERE / "footer-bg.mp4"
POSTER = HERE / "footer-bg.jpg"
POSTER_AT = "00:00:02"      # a couple of seconds in, past any fade-up
CRF = "33"
WIDTH = 1280
FPS = "30"


def ffmpeg():
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
    except ImportError:
        raise SystemExit("ffmpeg not found. Install it, or: pip install imageio-ffmpeg")
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(args):
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr[-2000:])


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python assets/video/_footer_bg.py <source.mp4>")
    src = pathlib.Path(sys.argv[1])
    if not src.exists():
        raise SystemExit(f"no such file: {src}")

    ff = ffmpeg()
    print(f"source {src.name}  {src.stat().st_size:,} bytes")

    run([ff, "-y", "-hide_banner", "-loglevel", "error", "-i", str(src),
         "-an", "-r", FPS, "-vf", f"scale={WIDTH}:-2",
         "-c:v", "libx264", "-preset", "slow", "-crf", CRF,
         "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-movflags", "+faststart", str(MP4)])

    # eq darkens the still to roughly match the video once the shade is over
    # it, so the swap from poster to playing frame is not a brightness jump
    run([ff, "-y", "-hide_banner", "-loglevel", "error", "-ss", POSTER_AT,
         "-i", str(src), "-frames:v", "1",
         "-vf", f"scale={WIDTH}:-2,eq=brightness=-0.06:saturation=0.9",
         "-q:v", "6", str(POSTER)])

    for f in (MP4, POSTER):
        print(f"  {f.name:18} {f.stat().st_size:>10,} bytes")


if __name__ == "__main__":
    main()
