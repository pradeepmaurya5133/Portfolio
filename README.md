# Pradeep Maurya — Portfolio

A portfolio site built to the visual language of [stefanobg.com](https://www.stefanobg.com/),
with content taken from `Pradeep_Maurya_Resume.docx`.

Static HTML/CSS/JS — no build step needed to *view* it, no framework, no CDN calls.
Everything (fonts, GSAP, Lenis) is served from `assets/`, so it works offline and
can be dropped on any static host.

## Run it

Open `index.html` directly, or serve the folder (recommended — some browsers
restrict fonts over `file://`):

```sh
python -m http.server 8000
# then visit http://localhost:8000
```

## Pages

| Page | File |
| --- | --- |
| Home | `index.html` |
| Work | `work.html` |
| About (+ experience timeline at `#experience`) | `about.html` |
| Skills | `skills.html` |
| Résumé | `resume.html` |
| Contact | `contact.html` |
| Project detail × 5 | `work/*.html` |
| Privacy / Terms / 404 | `privacy.html`, `terms.html`, `404.html` |

## Editing content

**Don't edit the `.html` files by hand** — they're generated. Edit the data blocks
at the top of `build.py` (`ME`, `NAV`, `PROJECTS`, `SKILL_GROUPS`, `EXPERIENCE`,
`CREDENTIALS`, `STATS`, `CAPABILITIES`), then:

```sh
python build.py
```

That regenerates all 14 pages with a consistent header, menu, footer and meta tags.

## Artwork

### Portrait

`assets/img/portrait.jpg` (900×900, About hero) and `assets/img/portrait-pill.jpg`
(720×304, home hero pill) are cut from one source photo. To swap the photo:

```sh
python assets/img/_crop_portrait.py path/to/new-photo.jpg
```

Both boxes use `object-fit: cover`, so the script crops to the exact display ratio
and the browser never crops again. If the new photo frames the subject differently,
adjust `FACE_X` / `SQUARE_Y` / `PILL_Y` at the top of that script — they're
fractions of the image, not pixels.

### Project covers

Three projects use real screenshots (`.jpg`), two still use generated
placeholders (`.svg`). `build.py` picks the right file per project via the
`SCREENSHOTS` set and the `cover()` helper — add a slug there when you swap one.

**Real screenshots** — take a browser screenshot, drop it in
`~/Pictures/Screenshots`, add an entry to `SHOTS` in the script, then:

```sh
python assets/img/_frame_screenshot.py            # all
python assets/img/_frame_screenshot.py consentx   # just one
```

It crops the browser's own toolbar off the top (`chrome_px` per entry — the
pixel row where the page actually starts) and sits the page in a neutral window
frame on the same dark canvas the generated covers use. Output is 2560×1600.

**Placeholders** for projects without a screenshot yet:

```sh
python assets/img/_generate.py
```

Either way the cover is **16:10**. The index row and spotlight figure crop to
16:9, so keep ~200px of breathing room top and bottom; the project-page hero
crops to a square, so expect the centre to be what shows there.

## Things you'll want to fill in

- **Education** — the résumé didn't list an institution or graduation year.
  Search `Institution to be added` in `build.py`.
- **Project screenshots** — Bakery and Movie Scraper still use generated
  placeholders; the other three use real screenshots.
- **Certification years** — not in the résumé, so they render as `—`.
  See the `CREDENTIALS` list.
- **Contact form** — with `action="#"` (the default) it opens the visitor's mail
  client with the message pre-filled, so it works on a static host with no backend.
  To post to a real endpoint instead, set the form `action` in `page_contact()`
  to e.g. a Formspree URL; `app.js` already handles the fetch, status messages
  and error states.

## What drives the motion

| Behaviour | Where |
| --- | --- |
| Smooth scrolling | Lenis |
| Work hero plexus network (3D node mesh + light rays, canvas) | `initPlexus()` in `assets/js/app.js`; markup is `.wh__bg` in `build.py`, tuned with `data-plexus` (density) and `data-plexus-ray` (ray angle) |
| Skills hero data streams (dot strands radiating from a core, canvas) | `initStreams()` in `assets/js/app.js`; markup is `.wh__bg` + `.wh__shade--center`, tuned with `data-streams` (density) |
| Preloader counter, hero character reveal, scroll reveals, counters, marquees, word-by-word scrub, hover preview, pinned project hero | GSAP + ScrollTrigger + SplitText (`assets/js/app.js`) |
| Custom cursor, grain, rotating headline, filters, live clock | `assets/js/app.js` |

If JavaScript is unavailable the page still renders: the preloader is hidden and
all reveal states default to visible.

## Licences

GSAP and Lenis are bundled under their own licences (see the headers in
`assets/vendor/`). Archivo is an open-source typeface from Google Fonts.
