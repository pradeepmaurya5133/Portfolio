#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Builds every page of the portfolio from shared partials + the resume data.

    python build.py

Edit the DATA blocks below and re-run — the header, menu, footer, cursor and
meta tags stay identical across all pages.
"""
import datetime
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).parent

# Absolute base URL used by sitemap.xml and robots.txt. Sitemaps require
# absolute URLs, so point this at your real domain before deploying.
# No trailing slash.
SITE_URL = "https://pradeepmaurya.com"

# ============================================================
#  PERSONAL DATA  (sourced from Pradeep_Maurya_Resume.docx)
# ============================================================
ME = {
    "name": "Pradeep Maurya",
    "first": "Pradeep",
    "role": "Full Stack Developer",
    "role_long": "Full Stack Developer | Software Engineer",
    "email": "pradeepmaurya2002@gmail.com",
    "phone": "+91 95199 65133",
    "phone_href": "+919519965133",
    "city": "Dehradun",
    "region": "Shree Enclave Panditwari, Dehradun, India",
    "linkedin": "https://linkedin.com/in/pradeep-maurya-b82b5820b/",
    "github": "https://github.com/pradeepmaurya5133/",
    "year": "2026",
    "tagline": "Full Stack Developer crafting responsive interfaces, REST APIs and the tests that keep them honest.",
    "summary": ("Computer Science graduate with hands-on experience in web development, software testing and "
                "data analysis. Working knowledge of HTML, CSS, JavaScript, React, Next.js, Node.js, Python, "
                "TypeScript, Tailwind CSS, Git/GitHub, REST APIs and AI API integration. Focused on building "
                "responsive interfaces, improving application usability and debugging web applications."),
}

def article(word):
    """'a' or 'an' for the first word of `word`."""
    return "an" if word[:1].lower() in "aeiou" else "a"


NAV = [
    ("01", "Home", "{root}index.html"),
    ("02", "Work", "{root}work.html"),
    ("03", "About", "{root}about.html"),
    ("04", "Skills", "{root}skills.html"),
    ("05", "Experience", "{root}about.html#experience"),
    ("06", "Résumé", "{root}resume.html"),
    ("07", "Contact", "{root}contact.html"),
]

SOCIALS = [
    ("GitHub", ME["github"]),
    ("LinkedIn", ME["linkedin"]),
    ("Email", "mailto:" + ME["email"]),
]

TECH_STRIP = [
    "HTML", "CSS", "JavaScript", "TypeScript", "React", "Next.js", "Node.js", "Express",
    "Python", "Django", "PostgreSQL", "Prisma", "Tailwind", "Bootstrap", "Redux",
    "Git", "GitHub", "Postman", "Power BI", "Excel",
]

PROJECTS = [
    {
        "slug": "consentx",
        "name": "ConsentX",
        "full": "ConsentX.io",
        "meta": "Full-Stack / UI Engineering",
        "tags": ["fullstack", "frontend", "testing"],
        "tag_labels": "Full-Stack · Responsive UI · Testing",
        "year": "2026",
        "role": "Full Stack Developer",
        "org": "iLeads Auxiliary Services (SS IntelligenceX)",
        "stack": "React, Next.js, TypeScript, Tailwind CSS, Node.js, REST APIs",
        "scope": "Website development, responsive UI, user-facing functionality, testing, usability",
        "link": "https://consentx.io",
        "summary": "A consent management platform where privacy choices have to be captured, stored and proven.",
        "lead": ("Contributed to full-stack development and ongoing enhancement of ConsentX.io — a consent "
                 "management platform — covering responsive UI, user-facing functionality, testing and "
                 "usability improvements."),
        "body": [
            ("Working on a live product, the brief was rarely \"build this screen.\" It was closer to \"this flow "
             "confuses people and the numbers show it.\" Most of my work sat in that gap: taking an existing "
             "interface, finding where it broke down on real viewports and real data, and rebuilding it so the "
             "consent journey reads clearly from first load to confirmation."),
            ("Beyond the frontend, I picked up backend tasks and application functionality, debugged issues "
             "reported from production, and tested each change manually and through the API before it shipped."),
        ],
        "notes": [
            ("Responsive first", "Consent interfaces get opened on whatever device is nearest. Every layout was "
                                 "rebuilt to hold up from a narrow phone through to a wide desktop without a "
                                 "separate mobile path to maintain."),
            ("Tested before shipped", "Each change went through manual web testing plus API checks in Postman, "
                                      "so regressions were caught before review rather than after release."),
        ],
    },
    {
        "slug": "regulatorybridge",
        "name": "RegulatoryBridge",
        "full": "RegulatoryBridge.com",
        "meta": "Web Development / QA",
        "tags": ["fullstack", "frontend", "testing"],
        "tag_labels": "Web Development · Responsive Design · Performance",
        "year": "2026",
        "role": "Full Stack Developer",
        "org": "iLeads Auxiliary Services (SS IntelligenceX)",
        "stack": "React, Next.js, TypeScript, Tailwind CSS, Node.js, REST APIs",
        "scope": "Website development, responsive design, feature refinement, debugging, testing, performance",
        "link": "https://regulatorybridge.com",
        "summary": "A regulatory compliance platform — dense information that still has to be quick to read.",
        "lead": ("Contributed to website development and improvements for RegulatoryBridge.com, covering "
                 "responsive design, feature refinement, debugging, testing and performance-focused updates."),
        "body": [
            ("Compliance products carry a lot of information per screen, which makes them easy to build badly. "
             "The work here was mostly about restraint: tightening layouts so dense tables and long-form "
             "requirements stay scannable, and refining existing features rather than stacking new ones on top."),
            ("Alongside that I handled debugging and testing passes, and performance-focused updates where pages "
             "were doing more work than the content justified."),
        ],
        "notes": [
            ("Refine over rebuild", "Most tickets were improvements to shipped features. Changing a live product "
                                    "without disrupting the people already using it is its own constraint."),
            ("Performance as a feature", "On an information-dense platform, how fast a page becomes readable "
                                         "matters as much as what it says."),
        ],
    },
    {
        "slug": "bakery",
        "name": "Bakery",
        "full": "Bakery — E-commerce Web Application",
        "meta": "Full-Stack / E-commerce",
        "tags": ["fullstack", "frontend", "backend"],
        "tag_labels": "Next.js · Express.js · PostgreSQL · Prisma · JWT",
        "year": "2025",
        "role": "Full-stack developer (personal project)",
        "org": "Self-directed",
        "stack": "Next.js, Express.js, PostgreSQL, Prisma, Redux Toolkit, JWT",
        "scope": "Full-stack build: storefront, cart, secure user management, REST APIs",
        "link": "",
        "summary": "A complete bakery shop — storefront, cart and secure accounts, built end to end.",
        "lead": ("Built a full-stack bakery shop application using Next.js, Express.js, PostgreSQL, Prisma, "
                 "Redux Toolkit and JWT authentication, with secure user management and REST APIs."),
        "body": [
            ("This is the project where the whole stack was mine. Next.js on the front, Express and PostgreSQL "
             "behind it, Prisma handling the schema and queries, Redux Toolkit holding client state, and JWT "
             "for authentication — so every decision, from the data model up to the cart interaction, had to "
             "actually connect to the next one."),
            ("Building it end to end is what made the API boundary real. Designing the REST endpoints and then "
             "being the one to consume them teaches you quickly which responses are convenient and which only "
             "looked tidy on paper."),
        ],
        "notes": [
            ("Secure by default", "JWT authentication with protected routes and server-side validation, so "
                                  "account and order data is never guarded by the UI alone."),
            ("One schema, one source of truth", "Prisma over PostgreSQL kept the data model explicit and "
                                                "migrations reviewable instead of improvised."),
        ],
    },
    {
        "slug": "xamlysis",
        "name": "Xamlysis",
        "full": "Xamlysis — Online Exam Portal",
        "meta": "Web App / QA",
        "tags": ["fullstack", "backend", "testing"],
        "tag_labels": "Authentication · Exam Creation · Stability",
        "year": "2025",
        "role": "Developer / QA support",
        "org": "Project work",
        "stack": "JavaScript, Node.js, REST APIs, manual & API testing",
        "scope": "Core features including authentication and exam creation, plus testing and stability work",
        "link": "",
        "summary": "An online examination portal — the kind of app where a bug has a deadline attached.",
        "lead": ("Worked on an online examination portal, supporting core features such as authentication and "
                 "exam creation, alongside testing and stability improvements."),
        "body": [
            ("Exam software has an unusual failure cost: a defect does not merely annoy someone, it interrupts "
             "a timed assessment that cannot simply be retaken. That shaped how I worked on it — authentication "
             "and exam creation were built with the unhappy paths treated as first-class, not as edge cases to "
             "handle later."),
            ("A large share of my contribution was testing and stability: exercising flows the way a stressed "
             "user would, reproducing intermittent issues, and closing them properly rather than papering over "
             "the symptom."),
        ],
        "notes": [
            ("Auth before features", "Role-correct access to exam creation and exam taking was the foundation "
                                     "everything else sat on."),
            ("Stability as the deliverable", "On a portal under time pressure, \"it reliably works\" is the "
                                             "feature users actually notice."),
        ],
    },
    {
        "slug": "movie-scraper",
        "name": "Movie Scraper",
        "full": "Movie Data Scraping Web Application",
        "meta": "Python / Data Pipeline",
        "tags": ["backend", "data"],
        "tag_labels": "Django · Data Validation · Multi-source",
        "year": "2025",
        "role": "Developer",
        "org": "Self-directed",
        "stack": "Python, Django, data validation",
        "scope": "Django application with validation and checks for reliable multi-source data flow",
        "link": "",
        "summary": "A Django app that pulls movie data from several sources and refuses to trust any of them.",
        "lead": ("Developed a Django-based application with data validation and checks to support reliable data "
                 "flow from multiple sources."),
        "body": [
            ("Scraping is the easy half. The moment data arrives from more than one source, the interesting "
             "problem becomes disagreement: missing fields, different formats for the same value, and records "
             "that are confidently wrong. The application is built around that — validation and checks sit "
             "between collection and storage, so bad records are caught at the boundary."),
            ("Working on it changed how I think about ingestion generally. A pipeline without validation is not "
             "a pipeline, it is a way to move someone else's errors into your own database."),
        ],
        "notes": [
            ("Validate at the boundary", "Checks run before anything is stored, which keeps the database "
                                         "trustworthy instead of requiring cleanup passes later."),
            ("Multiple sources, one shape", "Normalising differing source formats into a single schema is what "
                                            "makes the collected data actually usable."),
        ],
    },
]

CAPABILITIES = [
    ("01", "Frontend Development",
     "Responsive interfaces in React, Next.js and TypeScript, styled with Tailwind CSS or Bootstrap. "
     "Layouts that hold together from a narrow phone to a wide desktop, without a separate mobile codebase."),
    ("02", "Backend &amp; APIs",
     "Node.js and Express services, Python and Django applications, and REST APIs designed to be consumed — "
     "including AI API integration where a product needs it."),
    ("03", "Full-Stack Product Work",
     "End-to-end features across the stack: PostgreSQL and Prisma for data, Redux Toolkit for client state, "
     "JWT for secure user management — one coherent path from schema to screen."),
    ("04", "Testing &amp; QA",
     "Manual web testing, API testing in Postman and systematic debugging. Finding the defect before a user "
     "does is cheaper than every alternative."),
    ("05", "Data &amp; Reporting",
     "Data management and analysis with MS Excel and Power BI, plus validation checks that keep a data flow "
     "reliable across multiple sources."),
]

TOOLS = ["Visual Studio Code", "PyCharm", "Git", "GitHub", "Postman", "npm",
         "Prisma", "Redux Toolkit", "MS Excel", "Power BI"]
PLATFORMS = ["Web", "Responsive Mobile", "REST APIs", "Node.js", "Django", "PostgreSQL"]

SKILL_GROUPS = [
    ("01", "Frontend", ["HTML", "CSS", "JavaScript", "React", "Next.js", "TypeScript",
                        "Tailwind CSS", "Bootstrap"]),
    ("02", "Backend &amp; APIs", ["Node.js", "Express.js", "Python", "Django", "REST APIs",
                                  "AI API integration"]),
    ("03", "Databases &amp; State", ["PostgreSQL", "Prisma", "Redux Toolkit"]),
    ("04", "Testing &amp; Tools", ["Manual Testing", "API Testing (Postman)", "Web Testing",
                                   "Visual Studio Code", "PyCharm"]),
    ("05", "Data &amp; Collaboration", ["MS Excel", "Power BI", "Git", "GitHub"]),
    ("06", "Professional", ["Communication", "Teamwork", "Analytical thinking",
                            "Attention to detail", "Adaptability"]),
]

EXPERIENCE = [
    {
        "num": "01",
        "role": "Full Stack Developer",
        "org": "iLeads Auxiliary Services Private Limited",
        "when": "Aug 2026 — Present",
        "points": [
            "Contribute to frontend and backend web development tasks, including responsive UI improvements and application functionality.",
            "Support development, debugging, testing and refinement of web experiences using modern web technologies.",
            "Work on product and project deliverables associated with SS IntelligenceX Private Limited.",
            "Project work: ConsentX.io and RegulatoryBridge.com.",
        ],
    },
    {
        "num": "02",
        "role": "Software / QA and Data Support",
        "org": "Tecxpert Software Pvt. Ltd.",
        "when": "Sep 2025 — July 2026",
        "points": [
            "Supported software testing, quality assurance, data management, reporting and process-improvement activities.",
            "Helped coordinate tasks and resolve issues while maintaining focus on accuracy and delivery quality.",
        ],
    },
    {
        "num": "03",
        "role": "Data Entry &amp; Document Verification Operator — SBI Credit Card",
        "org": "Alexis Global Pvt. Ltd.",
        "when": "Jan 2025 — Jun 2025",
        "points": [
            "Entered and maintained customer application records with attention to accuracy and confidentiality.",
            "Verified customer documents against process requirements and coordinated resolution of discrepancies.",
        ],
    },
]

CREDENTIALS = [
    ("Front-End Development", "HTML, CSS, Bootstrap, JavaScript, React", "Certification", ""),
    ("Python Full-Stack Development", "Python, Django, full-stack web", "DUCAT IT Training Institute, Noida", ""),
    ("Full-Stack Development", "Full-stack web development", "Coding Seekho, Pune (Online)", ""),
    ("B.Tech — Computer Science", "Computer Science &amp; Engineering", "Institution to be added", ""),
]

STATS = [
    ("Years in tech", "02"),
    ("Projects shipped", "05"),
    ("Technologies used", "27"),
    ("Certifications", "03"),
]

# Real screenshots live as .jpg (see assets/img/_frame_screenshot.py); the rest
# fall back to the generated .svg placeholder of the same name.
SCREENSHOTS = {"consentx", "regulatorybridge", "xamlysis"}


def cover(slug):
    """Cover filename for a project slug."""
    return f"{slug}.jpg" if slug in SCREENSHOTS else f"{slug}.svg"


ARROW = ('<svg class="arrow-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
         'stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M4 12l8-8M5.5 4H12v6.5"/></svg>')
ARROW_BACK = ('<svg class="arrow-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M12 4l-8 8M10.5 12H4V5.5"/></svg>')
ARROW_DOWN = ('<svg class="arrow-icon" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="square" aria-hidden="true" focusable="false"><path d="M8 3v10M3.5 8.5L8 13l4.5-4.5"/></svg>')


# ============================================================
#  PARTIALS
# ============================================================
def external(url):
    """Attributes for links that leave the site."""
    if url.startswith("mailto") or url.startswith("tel"):
        return ""
    return ' target="_blank" rel="noopener"'


def head(title, description, root, extra_css=""):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{ME['name']}">
<meta name="theme-color" content="#141414">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{ME['name']}">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{root}assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<link rel="icon" href="{root}favicon.ico" sizes="32x32">
<link rel="icon" href="{root}assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{root}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{root}site.webmanifest">
<link rel="stylesheet" href="{root}assets/css/main.css">
<link rel="stylesheet" href="{root}assets/css/pages.css">{extra_css}
</head>'''


def preloader():
    return f'''<div class="preloader" aria-hidden="true">
<div class="preloader__top mono">
<span>PM — Portfolio</span>
<span>Loading assets</span>
</div>
<div class="preloader__count display"><span data-count>000</span></div>
<div class="preloader__bar"><span></span></div>
</div>
<a class="skip sr-only" href="#main">Skip to content</a>'''


def header(active, root):
    links = ""
    for num, label, href in NAV:
        url = href.format(root=root)
        cls = "nav__link is-active" if label == active else "nav__link"
        links += (f'<a href="{url}" class="{cls}" data-cursor="hover">'
                  f'<span class="nav__index mono">{num}</span>'
                  f'<span class="nav__roll" data-text="{label}"><span>{label}</span></span></a>')

    menu_links = ""
    for num, label, href in NAV:
        url = href.format(root=root)
        menu_links += (f'<a href="{url}" class="menu__link display">'
                       f'<span class="mono accent">{num}</span> {label} </a>')

    menu_foot = "".join(
        f'<a href="{url}"{external(url)} data-cursor="hover"> {name} {ARROW}</a>'
        for name, url in SOCIALS
    )

    return f'''<header class="header wrap" data-header>
<a href="{root}index.html" class="logo" aria-label="{ME['name']} — home" data-cursor="hover">
<span class="logo__mark" aria-hidden="true">P<i>/</i>M</span>
<span class="logo__name label">{ME['name']}</span>
</a>
<span class="header__spacer" aria-hidden="true"></span>
<nav class="nav" aria-label="Main">{links}</nav>
<button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="menu" data-menu-toggle>
<span></span><span></span>
</button>
</header>
<div class="menu" id="menu" data-menu hidden>
<nav class="menu__nav wrap" aria-label="Mobile">{menu_links}</nav>
<div class="menu__foot wrap mono">{menu_foot}</div>
</div>'''


def footer(root):
    return f'''<footer class="footer">
<section class="cta wrap" aria-labelledby="cta-title">
<p class="label muted cta__kicker"><span class="dot"></span> Open to new opportunities</p>
<h2 id="cta-title" class="cta__title display" data-split>
<span class="line-mask"><span>Let's build</span></span>
<span class="line-mask"><span>something <span class="accent">great</span></span></span>
</h2>
<div class="cta__row">
<p class="cta__copy muted">A frontend that needs rebuilding, an API that needs writing, or a product that needs someone to test it properly. If you think I can help, let's talk.</p>
<div class="cta__actions">
<a href="mailto:{ME['email']}" class="cta__email u-link">{ME['email']}</a>
<a href="{root}contact.html" class="btn" data-cursor="hover">Start a conversation <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
</div>
</section>
<div class="footer__base wrap mono">
<span>Built by {ME['name']} — {ME['year']}</span>
<span class="footer__legal">
<a class="u-link" href="{root}privacy.html">Privacy</a>
<a class="u-link" href="{root}terms.html">Terms</a>
<button class="u-link" data-to-top type="button">Back to top</button>
</span>
</div>
</footer>'''


def chrome_end(root):
    return f'''<div class="cursor" aria-hidden="true" data-cursor-el>
<span class="cursor__dot"></span>
<span class="cursor__ring">
<span class="cursor__bubble"><span class="cursor__label label" data-cursor-label></span></span>
<svg class="cursor__orbit" viewBox="0 0 120 120" aria-hidden="true">
<defs><path id="orbit-path" d="M60,60 m-44,0 a44,44 0 1,1 88,0 a44,44 0 1,1 -88,0"/></defs>
<text><textPath href="#orbit-path" class="cursor__orbit-text" data-cursor-name></textPath></text>
</svg>
</span>
</div>
<div class="grain" aria-hidden="true"></div>
<script src="{root}assets/vendor/gsap.min.js"></script>
<script src="{root}assets/vendor/ScrollTrigger.min.js"></script>
<script src="{root}assets/vendor/SplitText.min.js"></script>
<script src="{root}assets/vendor/lenis.min.js"></script>
<script src="{root}assets/js/app.js"></script>
</body>
</html>'''


def marquee(items, direction="forward", duration="70", outline=False, no_pause=True):
    group = "".join(
        f'<span class="marquee__item"> {i} <span class="marquee__sep" aria-hidden="true"></span></span>'
        for i in items * 2
    )
    cls = "marquee marquee--outline" if outline else "marquee"
    pause = " data-no-pause" if no_pause else ""
    return f'''<div class="{cls}" data-marquee="{direction}" data-duration="{duration}"{pause} aria-label="{', '.join(items)}">
<div class="marquee__track" data-marquee-track aria-hidden="true">
<div class="marquee__group">{group}</div>
<div class="marquee__group">{group}</div>
</div>
</div>'''


def credentials_table(root):
    rows = ('<div class="rec__row rec__row--head label" role="row">'
            '<span role="columnheader">Credential</span>'
            '<span role="columnheader">Focus</span>'
            '<span role="columnheader">Year</span>'
            '<span role="columnheader">Issuer</span>'
            '<span role="columnheader" class="sr-only">Link</span></div>')
    for title, focus, issuer, year in CREDENTIALS:
        rows += (f'<div class="rec__row" role="row" data-award-row>'
                 f'<span role="cell" class="rec__title">{title}</span>'
                 f'<span role="cell">{focus}</span>'
                 f'<span role="cell" class="mono">{year or "—"}</span>'
                 f'<span role="cell">{issuer}</span>'
                 f'<span role="cell" class="rec__arrow" aria-hidden="true"></span></div>')
    return f'''<section class="rec section wrap" aria-labelledby="rec-title">
<div class="section-head">
<h2 id="rec-title" class="section-title" data-split>
<span class="line-mask"><span>Credentials<sup>({len(CREDENTIALS):02d})</sup></span></span>
</h2>
<p class="label muted rec__kicker"><span class="dot"></span> Certifications &amp; education</p>
</div>
<div class="rec__table" role="table" aria-label="Certifications and education">{rows}</div>
</section>'''


def capabilities_block():
    tools = "".join(f'<li class="label">{t}</li>' for t in TOOLS)
    platforms = "".join(f'<li class="label">{p}</li>' for p in PLATFORMS)
    caps = ""
    for num, title, desc in CAPABILITIES:
        caps += (f'<li class="cap" data-reveal><span class="cap__num mono">{num}</span>'
                 f'<div class="cap__body"><h3 class="cap__title">{title}</h3>'
                 f'<p class="cap__desc muted">{desc}</p></div></li>')
    return f'''<section class="caps section wrap" aria-labelledby="caps-title">
<div class="caps__aside"><div class="caps__sticky">
<h2 id="caps-title" class="section-title" data-split>
<span class="line-mask"><span>How can</span></span>
<span class="line-mask"><span class="accent">I help?</span></span>
</h2>
<div class="tagsets">
<div class="tagset"><p class="label muted tagset__label">Tools</p>
<ul class="tagset__list" aria-label="Tools">{tools}</ul></div>
<div class="tagset"><p class="label muted tagset__label">Platforms</p>
<ul class="tagset__list" aria-label="Platforms">{platforms}</ul></div>
</div>
</div></div>
<ol class="caps__list">{caps}</ol>
</section>'''


# ============================================================
#  PAGES
# ============================================================
def page_index():
    root = ""
    strip_items = "".join(
        f'<li class="logos__item"><span class="logos__word">{t}</span></li>' for t in TECH_STRIP
    )
    stats = ""
    for i, (label, value) in enumerate(STATS):
        stats += (f'<div class="stat" data-reveal style="--d:{i*0.08:.2f}s">'
                  f'<dt class="label muted">{label}</dt>'
                  f'<dd class="stat__value display" data-counter="{value}">{value}</dd>'
                  f'<span class="stat__index mono">[{i+1:02d}]</span></div>')

    rows, previews = "", ""
    for i, p in enumerate(PROJECTS):
        d = i * 0.05
        rows += (f'<li class="row" data-index-row data-reveal style="--d:{d:.2f}s">'
                 f'<a href="work/{p["slug"]}.html" class="row__link" data-cursor="view" '
                 f'data-cursor-label="Open" data-cursor-name="{p["name"]}">'
                 f'<span class="row__num mono">{i+1:02d}</span>'
                 f'<span class="row__title">{p["name"]}</span>'
                 f'<span class="row__meta label">{p["meta"]}</span>'
                 f'<span class="row__arrow" aria-hidden="true">{ARROW}</span>'
                 f'<span class="row__thumb" aria-hidden="true">'
                 f'<img src="assets/img/{cover(p["slug"])}" alt="" loading="lazy" decoding="async" '
                 f'width="2560" height="1600"></span></a></li>')
        clip = "" if i == 0 else ' style="clip-path: inset(0 0 100% 0)"'
        previews += (f'<div class="preview__item" data-preview-item{clip}>'
                     f'<img src="assets/img/{cover(p["slug"])}" alt="" loading="lazy" decoding="async" '
                     f'width="2560" height="1600"></div>')

    rotate = '["web apps","interfaces","REST APIs","dashboards","platforms","e-commerce","exam portals"]'

    return head(
        f"{ME['name']} — {ME['role']}",
        ME["tagline"], root
    ) + f'''
<body data-preloader>
{preloader()}
{header("Home", root)}
<main id="main">

<section class="hero" data-hero aria-label="Introduction">
<div class="hero__bg" aria-hidden="true">
<canvas data-hero-bg data-flow="1"></canvas>
<div class="hero__shade"></div>
<div class="hero__scan"></div>
</div>
<div class="hero__content wrap">
<h1 class="hero__title display" data-hero-title>
<span class="sr-only">I build web apps, interfaces, REST APIs, dashboards, platforms that perform.</span>
<span class="hero__line" aria-hidden="true">
<span data-hero-line>I build</span>
<span class="accent hero__rotate" data-rotate='{rotate}'>web apps</span>
</span>
<span class="hero__line hero__line--pill" aria-hidden="true">
<a href="about.html" class="pill" data-pill data-cursor="view" data-cursor-label="About me" tabindex="-1">
<img src="assets/img/portrait-pill.jpg" alt="" loading="eager" fetchpriority="high" width="720" height="304">
</a>
<span data-hero-line>that perform<span class="accent">.</span></span>
</span>
</h1>
<div class="hero__bottom">
<p class="hero__intro" data-hero-fade>{ME['role']} in {ME['city']}, India — building responsive frontends in React and Next.js, Node and Django backends, and the tests that keep them honest.</p>
<a href="resume.html" class="reel-btn label" data-hero-fade data-cursor="hover">
<span class="reel-btn__text">View résumé</span>
<span class="reel-btn__icon" aria-hidden="true">
<svg viewBox="0 0 14 16" width="13" height="15"><path d="M1.5 1.6L12.5 8L1.5 14.4Z" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>
</span>
</a>
</div>
</div>
</section>

<section class="logos" aria-labelledby="logos-title">
<div class="logos__head wrap">
<p id="logos-title" class="label muted"><span class="dot"></span> Working with</p>
<span class="mono muted">Stack</span>
</div>
<div class="logos__strip" data-marquee="forward" data-duration="65" data-shuffle>
<div class="logos__track" data-marquee-track>
<ul class="logos__group">{strip_items}</ul>
<ul class="logos__group" aria-hidden="true">{strip_items}</ul>
</div>
</div>
</section>

<section class="statement section wrap" aria-label="Approach">
<div class="statement__grid">
<p class="statement__text" data-scrub-words>Two years of turning requirements into working web software. Responsive interfaces in React and Next.js, REST APIs in Node and Django, and the manual and API testing that catches what slips past review. From first commit to production debugging.</p>
</div>
<dl class="stats">{stats}</dl>
</section>

<section class="work section" id="work" aria-labelledby="work-title">
<div class="wrap section-head">
<h2 id="work-title" class="section-title" data-split>
<span class="line-mask"><span>Selected work<sup>({len(PROJECTS):02d})</sup></span></span>
</h2>
<a href="work.html" class="label u-link" data-cursor="hover">All projects {ARROW}</a>
</div>
<ol class="index wrap" data-index>{rows}</ol>
<div class="preview" data-index-preview aria-hidden="true">{previews}</div>
</section>

<section class="bth section wrap" id="spotlight" aria-labelledby="bth-title">
<div class="bth__bg" aria-hidden="true"><canvas data-flow="0.6"></canvas></div>
<div class="bth__grid">
<div class="bth__copy">
<div class="bth__brand">
<img src="assets/img/mark.svg" alt="" width="64" height="64" class="bth__mark">
<span class="mono muted">Current role</span>
</div>
<h2 id="bth-title" class="bth__title display" data-split>
<span class="line-mask"><span>Privacy</span></span>
<span class="line-mask"><span>at <span class="accent">scale</span>.</span></span>
</h2>
<p class="bth__lead" data-reveal>Full-stack work on ConsentX.io and RegulatoryBridge.com.</p>
<p class="bth__text muted" data-reveal>
At iLeads Auxiliary Services I contribute to frontend and backend development across two live platforms built with SS IntelligenceX — a consent management platform and a regulatory compliance platform. Responsive UI improvements, application functionality, debugging, testing and performance work on products people use in production.
</p>
<div class="bth__ctas" data-reveal>
<a href="work/consentx.html" class="btn" data-cursor="hover">See ConsentX <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="work/regulatorybridge.html" class="label u-link" data-cursor="hover">RegulatoryBridge {ARROW}</a>
</div>
</div>
<div class="bth__media" data-reveal>
<figure class="bth__main">
<img src="assets/img/{cover("consentx")}" alt="ConsentX platform interface" loading="lazy" decoding="async" width="2560" height="1600">
<figcaption class="mono">In production</figcaption>
</figure>
</div>
</div>
<div class="bth__foot">
<dl class="bth__stats">
<div class="bth__stat" data-reveal style="--d:0s"><dt class="label muted">Platforms in production</dt><dd class="display" data-counter="02">02</dd></div>
<div class="bth__stat" data-reveal style="--d:0.06s"><dt class="label muted">Delivery areas</dt><dd class="display" data-counter="04">04</dd></div>
<div class="bth__stat" data-reveal style="--d:0.12s"><dt class="label muted">Live since</dt><dd class="display" data-counter="2026">2026</dd></div>
</dl>
<blockquote class="bth__quote" data-reveal>
<p>&ldquo;Ship it, then try to break it on purpose. The bug you find yourself is the one that never reaches a user.&rdquo;</p>
<footer class="mono muted">{ME['name']} // {ME['role']} @ iLeads</footer>
</blockquote>
</div>
</section>

<div class="theme-light">
{capabilities_block()}
{marquee(["Frontend", "Backend", "Testing", "Data", "Debugging"], "reverse", "70")}
{credentials_table(root)}
</div>

</main>
{footer(root)}
{chrome_end(root)}'''


def page_work():
    root = ""
    filters = [("all", "All"), ("fullstack", "Full-Stack"), ("frontend", "Frontend"),
               ("backend", "Backend"), ("testing", "Testing &amp; QA"), ("data", "Data")]
    chips = "".join(
        f'<button class="chip label" data-filter="{key}" aria-pressed="{str(key == "all").lower()}" '
        f'data-cursor="hover">{label}</button>' for key, label in filters
    )
    cards = ""
    for i, p in enumerate(PROJECTS):
        cards += (f'<a class="card" href="work/{p["slug"]}.html" data-tags="{"|".join(p["tags"])}" '
                  f'data-reveal style="--d:{i*0.06:.2f}s" data-cursor="view" data-cursor-label="Open" '
                  f'data-cursor-name="{p["name"]}">'
                  f'<span class="card__media"><img src="assets/img/{cover(p["slug"])}" alt="{p["name"]} cover" '
                  f'loading="lazy" decoding="async" width="2560" height="1600"></span>'
                  f'<span class="card__meta"><span class="mono muted">{i+1:02d}</span>'
                  f'<span class="card__title">{p["name"]}</span>'
                  f'<span class="label muted">{p["year"]}</span></span>'
                  f'<span class="label muted card__tags">{p["tag_labels"]}</span></a>')

    return head(f"Work — {ME['name']}",
                f"Selected web development projects by {ME['name']}: consent and compliance platforms, "
                f"e-commerce, an exam portal and a Django data pipeline.", root) + f'''
<body>
{header("Work", root)}
<main id="main">
<section class="wh wrap">
<div class="wh__bg" aria-hidden="true">
<canvas data-plexus="1" data-plexus-ray="150"></canvas>
<div class="wh__shade"></div>
<div class="wh__scan"></div>
</div>
<p class="label muted wh__kicker"><span class="dot"></span> Selected projects</p>
<h1 class="wh__title display" data-split>
<span class="line-mask"><span>Work<span class="accent">.</span></span></span>
</h1>
<p class="cb__lead" data-reveal style="margin-top:28px">Platforms in production, full-stack side projects and the testing work that sits underneath them. {len(PROJECTS)} projects.</p>
<div class="filters" data-filters role="group" aria-label="Filter projects">{chips}</div>
</section>
<section class="grid wrap">{cards}</section>
</main>
{footer(root)}
{chrome_end(root)}'''


def page_about():
    root = ""
    exp = ""
    for e in EXPERIENCE:
        points = "".join(f'<li>{pt}</li>' for pt in e["points"])
        exp += (f'<li class="exp__item" data-reveal>'
                f'<span class="exp__num mono">{e["num"]}</span>'
                f'<div><h3 class="exp__role">{e["role"]}</h3>'
                f'<p class="exp__org">{e["org"]}</p>'
                f'<p class="exp__when mono">{e["when"]}</p></div>'
                f'<ul class="exp__points">{points}</ul></li>')

    tldr = [
        ("Career", "2 years across web development, QA and data support"),
        ("Based in", "Dehradun, Uttarakhand, India"),
        ("Education", "B.Tech — Computer Science"),
        ("Skillset", "React, Next.js, TypeScript, Tailwind, Node.js, Express, Python, Django, PostgreSQL, Prisma, Redux Toolkit, REST APIs"),
        ("Testing", "Manual testing, API testing with Postman, web testing, debugging"),
        ("Data", "MS Excel, Power BI, data validation and reporting"),
        ("Currently", "Full Stack Developer at iLeads Auxiliary Services"),
    ]
    tldr_rows = "".join(
        f'<div class="tldr__row" data-reveal><dt class="label muted">{k}</dt><dd>{v}</dd></div>'
        for k, v in tldr
    )

    return head(f"About — {ME['name']}",
                f"{ME['name']} is {article(ME['role'])} {ME['role']} based in {ME['city']}, India, working across "
                f"frontend, backend, testing and data.", root) + f'''
<body>
{header("About", root)}
<main id="main">

<section class="ph" data-project-hero aria-labelledby="ph-title">
<div class="ph__top wrap label" data-ph-fade>
<a href="index.html" class="u-link" data-cursor="hover">{ARROW_BACK} Home</a>
<span class="muted">About</span>
</div>
<h1 id="ph-title" class="ph__title display">
<span class="sr-only">About {ME['name']}</span>
<span aria-hidden="true" class="ph__word" data-fit>
<span data-ph-left>PRAD</span><span data-ph-right>EEP</span>
</span>
</h1>
<p class="ph__caption mono muted" data-ph-fade>
<span>Shree Enclave, Panditwari</span>
<span>Dehradun // Uttarakhand // India</span>
</p>
<div class="ph__media" data-ph-media>
<img src="assets/img/portrait.jpg" alt="Portrait of {ME['name']}" loading="eager" fetchpriority="high" width="900" height="900">
</div>
<div class="ph__bottom wrap">
<p class="ph__summary" data-ph-fade>{ME['tagline']}</p>
<p class="ph__tag label" data-ph-fade>{ME['role_long']} — {ME['city']}, India</p>
</div>
<div class="ph__foot wrap" data-ph-fade>
<span class="mono muted">© {ME['name']}</span>
<span class="ph__scroll label">Scroll <span class="ph__sq" aria-hidden="true">{ARROW_DOWN}</span></span>
</div>
</section>

<section class="bio wrap">
<p class="label muted bio__kicker"><span class="dot"></span> Profile</p>
<div class="bio__text">
<p class="lead" data-reveal>I'm a Computer Science graduate based in Dehradun, working as {article(ME['role'])} {ME['role']} at iLeads Auxiliary Services on two live platforms — ConsentX.io and RegulatoryBridge.com.</p>
<p class="lead" data-reveal>My work spans the full stack: responsive interfaces in React and Next.js, backends in Node.js and Django, and the manual and API testing that keeps both honest. Before this I spent a year in QA and data support, which is where the testing habit came from.</p>
<p data-reveal>{ME['summary']}</p>
<blockquote class="mission" data-reveal>
<span class="accent">&ldquo;</span>I'd rather ship a smaller feature that holds up than a bigger one that needs a hotfix on Monday. Build it, test it properly, then put it in front of people.<span class="accent">&rdquo;</span>
</blockquote>
<p class="currently" data-reveal><span class="dot dot--round pulse" aria-hidden="true"></span> Open to new opportunities — <a class="u-link" href="contact.html">get in touch</a></p>
</div>
</section>

<section class="tldr section wrap" aria-labelledby="tldr-title">
<div class="section-head">
<h2 id="tldr-title" class="section-title" data-split>
<span class="line-mask"><span>TL;DR<span class="accent">.</span></span></span>
</h2>
</div>
<dl class="tldr__list">{tldr_rows}</dl>
</section>

{marquee(["Build", "Test", "Debug", "Ship"], "forward", "60")}

<section class="exp section wrap" id="experience" aria-labelledby="exp-title">
<div class="exp__head">
<div>
<p class="label muted exp__kicker"><span class="dot"></span> Work experience</p>
<h2 id="exp-title" class="exp__title display" data-split>
<span class="line-mask"><span>Where I've</span></span>
<span class="line-mask"><span><span class="accent">worked</span>.</span></span>
</h2>
</div>
<div class="exp__copy">
<p class="exp__text" data-reveal>Three roles in two years, moving from data verification through QA into full-stack web development. Each one left something behind: accuracy, a testing instinct, and now the code itself.</p>
<a href="resume.html" class="label u-link" data-cursor="hover" data-reveal>Full résumé {ARROW}</a>
</div>
</div>
<ol class="exp__list">{exp}</ol>
</section>

<div class="theme-light">
{credentials_table(root)}
</div>

</main>
{footer(root)}
{chrome_end(root)}'''


def page_skills():
    root = ""
    groups = ""
    for num, name, items in SKILL_GROUPS:
        lis = "".join(f'<li class="label">{i}</li>' for i in items)
        groups += (f'<div class="sk__group" data-reveal>'
                   f'<div><span class="sk__num mono">{num}</span>'
                   f'<h2 class="sk__name">{name}</h2></div>'
                   f'<ul class="sk__items">{lis}</ul></div>')

    return head(f"Skills — {ME['name']}",
                "Technical skills: frontend, backend and APIs, databases and state, testing and tools, "
                "data and collaboration.", root) + f'''
<body>
{header("Skills", root)}
<main id="main">
<section class="wh wrap">
<div class="wh__bg" aria-hidden="true">
<canvas data-streams="1"></canvas>
<div class="wh__shade wh__shade--center"></div>
<div class="wh__scan"></div>
</div>
<p class="label muted wh__kicker"><span class="dot"></span> Technical skills</p>
<h1 class="wh__title display" data-split>
<span class="line-mask"><span>Skills<span class="accent">.</span></span></span>
</h1>
<p class="cb__lead" data-reveal style="margin-top:28px">What I work with day to day, grouped by where it sits in the stack. Everything listed here I've used on shipped work or a complete project — not a tutorial list.</p>
</section>
<section class="sk wrap">{groups}</section>
{marquee(["React", "Next.js", "Node.js", "Django", "PostgreSQL", "Postman"], "reverse", "65")}
<div class="theme-light">
{capabilities_block()}
</div>
</main>
{footer(root)}
{chrome_end(root)}'''


def page_resume():
    root = ""
    exp = ""
    for e in EXPERIENCE:
        points = "".join(f'<li>{pt}</li>' for pt in e["points"])
        exp += (f'<div class="res__line" data-reveal>'
                f'<dt><strong>{e["role"]}</strong><br><span class="mono muted">{e["when"]}</span></dt>'
                f'<dd><p style="margin-bottom:12px">{e["org"]}</p>'
                f'<ul class="res__list">{points}</ul></dd></div>')

    proj = ""
    for p in PROJECTS:
        proj += (f'<div class="res__line" data-reveal>'
                 f'<dt><strong>{p["full"]}</strong><br><span class="mono muted">{p["year"]}</span></dt>'
                 f'<dd><p style="margin-bottom:10px">{p["lead"]}</p>'
                 f'<p class="mono muted">{p["stack"]}</p></dd></div>')

    skills = ""
    for num, name, items in SKILL_GROUPS:
        skills += (f'<div class="res__line" data-reveal>'
                   f'<dt class="label muted">{name}</dt><dd>{", ".join(items)}</dd></div>')

    creds = ""
    for title, focus, issuer, year in CREDENTIALS:
        creds += (f'<div class="res__line" data-reveal>'
                  f'<dt><strong>{title}</strong></dt>'
                  f'<dd>{focus}<br><span class="mono muted">{issuer}</span></dd></div>')

    return head(f"Résumé — {ME['name']}",
                f"Résumé of {ME['name']}, {ME['role']} — experience, projects, skills and certifications.",
                root) + f'''
<body>
{header("Résumé", root)}
<main id="main">
<section class="wh wrap">
<p class="label muted wh__kicker"><span class="dot"></span> Curriculum vitae</p>
<h1 class="wh__title display" data-split>
<span class="line-mask"><span>Résumé<span class="accent">.</span></span></span>
</h1>
</section>
<section class="res wrap">
<div class="res__grid">
<aside class="res__aside">
<div>
<p class="label muted" style="margin-bottom:12px">Name</p>
<p style="font-size:1.3rem;font-weight:600">{ME['name']}</p>
<p class="muted">{ME['role_long']}</p>
</div>
<div>
<p class="label muted" style="margin-bottom:12px">Contact</p>
<p><a class="u-link" href="mailto:{ME['email']}">{ME['email']}</a></p>
<p><a class="u-link" href="tel:{ME['phone_href']}">{ME['phone']}</a></p>
<p class="muted">{ME['region']}</p>
</div>
<div>
<p class="label muted" style="margin-bottom:12px">Links</p>
<p><a class="u-link" href="{ME['linkedin']}" target="_blank" rel="noopener">LinkedIn {ARROW}</a></p>
<p><a class="u-link" href="{ME['github']}" target="_blank" rel="noopener">GitHub {ARROW}</a></p>
</div>
<a class="btn" href="assets/Pradeep_Maurya_Resume.docx" download data-cursor="hover">
Download résumé <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</aside>

<div>
<div class="res__block">
<h2 class="res__h">Professional summary</h2>
<p class="muted" style="font-size:1.1rem;line-height:1.6">{ME['summary']}</p>
</div>

<div class="res__block">
<h2 class="res__h">Work experience</h2>
<dl>{exp}</dl>
</div>

<div class="res__block">
<h2 class="res__h">Projects</h2>
<dl>{proj}</dl>
</div>

<div class="res__block">
<h2 class="res__h">Technical skills</h2>
<dl>{skills}</dl>
</div>

<div class="res__block">
<h2 class="res__h">Certifications &amp; education</h2>
<dl>{creds}</dl>
</div>
</div>
</div>
</section>
</main>
{footer(root)}
{chrome_end(root)}'''


def page_contact():
    root = ""
    socials = "".join(
        f'<a href="{url}"{external(url)} data-cursor="hover">'
        f'<span>{name}</span><span class="mono muted">{ARROW}</span></a>'
        for name, url in SOCIALS
    )
    return head(f"Contact — {ME['name']}",
                f"Get in touch with {ME['name']} — {ME['email']}", root) + f'''
<body>
{header("Contact", root)}
<main id="main">
<section class="ch wrap">
<p class="label muted ch__kicker"><span class="dot"></span> Open to new opportunities</p>
<h1 class="ch__title display" data-split>
<span class="line-mask"><span>Let's</span></span>
<span class="line-mask"><span>talk<span class="accent">.</span></span></span>
</h1>
</section>

<section class="cb wrap">
<div class="cb__main">
<p class="cb__lead" data-reveal>Feel free to reach me if you believe we can build something great together, or if you just want to talk (:</p>
<form class="form" data-contact-form action="#" method="post" novalidate>
<div class="field">
<label class="label muted" for="f-name">Your name</label>
<input id="f-name" name="name" type="text" placeholder="Jane Doe" required autocomplete="name">
</div>
<div class="field">
<label class="label muted" for="f-email">Email</label>
<input id="f-email" name="email" type="email" placeholder="jane@company.com" required autocomplete="email">
</div>
<div class="field">
<label class="label muted" for="f-company">Company <span class="muted">(optional)</span></label>
<input id="f-company" name="company" type="text" placeholder="Company name" autocomplete="organization">
</div>
<div class="field">
<label class="label muted" for="f-message">Message</label>
<textarea id="f-message" name="message" rows="4" placeholder="What are you building?" required></textarea>
</div>
<p class="mono" data-form-status></p>
<div class="form__foot">
<button class="btn" type="submit" data-cursor="hover">Send message <span class="arrow" aria-hidden="true">{ARROW}</span></button>
<p class="form__consent muted">By sending this you agree to your details being used to reply. See the <a class="u-link" href="privacy.html">privacy note</a>.</p>
</div>
</form>
</div>

<aside class="cb__aside">
<div>
<p class="label muted" style="margin-bottom:14px">Email</p>
<a class="cb__email u-link" href="mailto:{ME['email']}" data-cursor="hover">{ME['email']}</a>
</div>
<div>
<p class="label muted" style="margin-bottom:14px">Phone</p>
<a class="cb__email u-link" href="tel:{ME['phone_href']}" data-cursor="hover">{ME['phone']}</a>
</div>
<div>
<p class="label muted" style="margin-bottom:14px">Based in</p>
<p>{ME['region']}</p>
<p class="cb__time mono muted">Local time <span data-clock>--:--:--</span> IST</p>
</div>
<div>
<p class="label muted" style="margin-bottom:14px">Elsewhere</p>
<div class="cb__socials">{socials}</div>
</div>
</aside>
</section>
</main>
{footer(root)}
{chrome_end(root)}'''


def page_project(p, index):
    root = "../"
    nxt = PROJECTS[(index + 1) % len(PROJECTS)]
    half = max(1, len(p["name"]) // 2)
    left, right = p["name"][:half].upper(), p["name"][half:].upper()

    facts = [
        ("Role", p["role"]),
        ("Context", p["org"]),
        ("Year", p["year"]),
        ("Stack", p["stack"]),
        ("Scope", p["scope"]),
    ]
    if p["link"]:
        facts.append(("Live", f'<a class="u-link" href="{p["link"]}" target="_blank" rel="noopener">'
                              f'{p["link"].replace("https://", "")} {ARROW}</a>'))
    fact_rows = "".join(
        f'<div class="fact"><dt class="label muted">{k}</dt><dd>{v}</dd></div>' for k, v in facts
    )

    body = "".join(f'<p>{par}</p>' for par in p["body"])
    notes = "".join(
        f'<div class="g-text"><h3 class="g-text__h">{h}</h3><p class="muted">{t}</p></div>'
        for h, t in p["notes"]
    )

    return head(f"{p['name']} — {ME['name']}", p["summary"], root) + f'''
<body>
{header("Work", root)}
<main id="main">

<section class="ph" data-project-hero aria-labelledby="ph-title">
<div class="ph__top wrap label" data-ph-fade>
<a href="{root}work.html" class="u-link" data-cursor="hover">{ARROW_BACK} All work</a>
<span class="muted">{index + 1:02d} / {len(PROJECTS):02d}</span>
</div>
<h1 id="ph-title" class="ph__title display">
<span class="sr-only">{p['full']}</span>
<span aria-hidden="true" class="ph__word" data-fit>
<span data-ph-left>{left}</span><span data-ph-right>{right}</span>
</span>
</h1>
<p class="ph__caption mono muted" data-ph-fade>
<span>{p['meta']}</span>
<span>{p['year']} // {p['org']}</span>
</p>
<div class="ph__media" data-ph-media>
<img src="{root}assets/img/{cover(p['slug'])}" alt="{p['name']} interface" loading="eager" fetchpriority="high" width="2560" height="1600">
</div>
<div class="ph__bottom wrap">
<p class="ph__summary" data-ph-fade>{p['summary']}</p>
<p class="ph__tag label" data-ph-fade>{p['tag_labels']}</p>
</div>
<div class="ph__foot wrap" data-ph-fade>
<span class="mono muted">© {ME['name']}</span>
<span class="ph__scroll label">Scroll <span class="ph__sq" aria-hidden="true">{ARROW_DOWN}</span></span>
</div>
</section>

<section class="info section wrap" aria-label="Project overview">
<p class="label muted info__kicker"><span class="dot"></span> Overview</p>
<div class="info__grid">
<div class="info__text">
<p class="lead" data-reveal>{p['lead']}</p>
{body}
</div>
<dl class="facts" data-reveal>{fact_rows}</dl>
</div>
</section>

<section class="gallery contained wrap" aria-label="Project gallery">
<figure class="g-item" data-reveal>
<img src="{root}assets/img/{cover(p['slug'])}" alt="{p['name']} — main interface" loading="lazy" decoding="async" width="2560" height="1600">
<figcaption class="mono muted">{p['name']} — interface overview</figcaption>
</figure>
{notes}
<div class="g-row g-row--pair">
<figure class="g-item" data-reveal>
<img src="{root}assets/img/{cover(p['slug'])}" alt="{p['name']} — detail" loading="lazy" decoding="async" width="2560" height="1600">
<figcaption class="mono muted">Responsive layout</figcaption>
</figure>
<figure class="g-item" data-reveal style="--d:0.08s">
<img src="{root}assets/img/{cover(nxt['slug'])}" alt="Related work" loading="lazy" decoding="async" width="2560" height="1600">
<figcaption class="mono muted">Related work — {nxt['name']}</figcaption>
</figure>
</div>
</section>

<section class="credits section wrap" aria-labelledby="credits-title">
<div class="section-head">
<h2 id="credits-title" class="section-title" data-split>
<span class="line-mask"><span>Details<span class="accent">.</span></span></span>
</h2>
</div>
<ul class="credits__list">
<li data-reveal><span class="label muted">Role</span><span>{p['role']}</span></li>
<li data-reveal><span class="label muted">Context</span><span>{p['org']}</span></li>
<li data-reveal><span class="label muted">Year</span><span>{p['year']}</span></li>
<li data-reveal><span class="label muted">Stack</span><span>{p['stack']}</span></li>
</ul>
<p class="credits__copy muted" data-reveal>Artwork on this page is a representative mock-up, not a screenshot of client software.</p>
</section>

<a class="next" href="{root}work/{nxt['slug']}.html" data-cursor="view" data-cursor-label="Open" data-cursor-name="{nxt['name']}">
<div class="next__media"><img src="{root}assets/img/{cover(nxt['slug'])}" alt="" loading="lazy" decoding="async" width="2560" height="1600"></div>
<div class="next__content wrap">
<span class="label muted">Next project</span>
<span class="next__title display"><span data-fit>{nxt['name']}</span></span>
<span class="label">{nxt['meta']} {ARROW}</span>
</div>
</a>

</main>
{footer(root)}
{chrome_end(root)}'''


def page_doc(title, slug, blocks):
    root = ""
    body = ""
    for kind, text in blocks:
        if kind == "h2":
            body += f'<h2>{text}</h2>'
        elif kind == "ul":
            body += '<ul>' + "".join(f'<li>{i}</li>' for i in text) + '</ul>'
        else:
            body += f'<p>{text}</p>'
    return head(f"{title} — {ME['name']}", f"{title} for {ME['name']}'s portfolio.", root) + f'''
<body>
{header("", root)}
<main id="main">
<section class="doc wrap">
<h1 data-split><span class="line-mask"><span>{title}<span class="accent">.</span></span></span></h1>
{body}
</section>
</main>
{footer(root)}
{chrome_end(root)}'''


def page_404():
    root = ""
    return head(f"Not found — {ME['name']}", "That page doesn't exist.", root) + f'''
<body>
{header("", root)}
<main id="main">
<section class="nf wrap">
<p class="label muted" style="margin-bottom:24px">Error</p>
<p class="nf__code display accent">404</p>
<p class="cb__lead" style="margin:32px auto 40px">That page doesn't exist — it may have been renamed or never existed at all.</p>
<p><a class="btn" href="index.html" data-cursor="hover">Back home <span class="arrow" aria-hidden="true">{ARROW}</span></a></p>
</section>
</main>
{footer(root)}
{chrome_end(root)}'''


# ============================================================
#  WRITE
# ============================================================
PRIVACY = [
    ("p", "This site is a personal portfolio. It does not run analytics, advertising or third-party trackers, "
          "and it sets no cookies."),
    ("h2", "What is collected"),
    ("p", "Nothing automatically. If you use the contact form, the details you type — name, email, optional "
          "company and your message — are used solely to reply to you."),
    ("h2", "How the contact form works"),
    ("p", "Unless a form endpoint is configured, the form opens your own email client with the message "
          "pre-filled. In that case nothing is transmitted to this site at all; you send the email yourself."),
    ("h2", "Fonts and assets"),
    ("p", "All fonts, scripts and images are served from this site. No requests are made to external services "
          "while you browse."),
    ("h2", "Contact"),
    ("p", f'Questions about this note: <a class="u-link" href="mailto:{ME["email"]}">{ME["email"]}</a>.'),
]

TERMS = [
    ("p", "A short, plain note about using this site."),
    ("h2", "Content"),
    ("p", "The text, layout and artwork here are the work of " + ME["name"] +
          ", published to present professional experience. Project artwork is representative mock-up, not "
          "screenshots of client software, and no confidential client material is reproduced."),
    ("h2", "Use"),
    ("ul", ["You may read, link to and share these pages freely.",
            "Please do not republish the content as your own.",
            "Company and product names are referenced for identification only."]),
    ("h2", "Accuracy"),
    ("p", "Details are kept current to the best of my knowledge. The résumé page is the authoritative version."),
    ("h2", "Third-party libraries"),
    ("p", "Animation is handled by GSAP and Lenis, bundled locally under their respective licences."),
]


# ============================================================
#  SITEMAP / ROBOTS
# ============================================================
# Google ignores <changefreq> and treats <priority> as little more than a hint,
# but both are part of the protocol and harmless. Priority is kept to express
# the page hierarchy; changefreq is skipped since it would be pure noise.
PRIORITY = {
    "index.html": "1.0",
    "work.html": "0.9",
    "about.html": "0.9",
    "resume.html": "0.8",
    "skills.html": "0.8",
    "contact.html": "0.8",
    "privacy.html": "0.3",
    "terms.html": "0.3",
}
# 404 is not a destination — listing it invites crawlers to index an error page.
SITEMAP_EXCLUDE = {"404.html"}


def site_url(path):
    """Absolute URL for a built page. index.html maps to the bare root, so `/`
    and `/index.html` don't compete with each other as duplicates."""
    base = SITE_URL.rstrip("/")
    return base + "/" if path == "index.html" else f"{base}/{path}"


def sitemap(paths, today):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for path in paths:
        if path in SITEMAP_EXCLUDE:
            continue
        lines += [
            "  <url>",
            f"    <loc>{site_url(path)}</loc>",
            f"    <lastmod>{today}</lastmod>",
            f"    <priority>{PRIORITY.get(path, '0.7')}</priority>",   # 0.7 = project pages
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def robots():
    return "\n".join([
        "User-agent: *",
        "Allow: /",
        "",
        f"Sitemap: {SITE_URL.rstrip('/')}/sitemap.xml",
    ]) + "\n"


def webmanifest():
    """Install metadata for Android/Chrome. Icon paths are resolved relative to
    the manifest, which sits at the site root."""
    return json.dumps({
        "name": f"{ME['name']} — {ME['role']}",
        "short_name": ME["first"],
        "description": ME["tagline"],
        # Relative to the manifest, so it still works if the site is ever
        # served from a subfolder rather than the domain root.
        "start_url": "./",
        "display": "standalone",
        "background_color": "#141414",
        "theme_color": "#141414",
        "icons": [
            {"src": "assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"},
        ],
    }, indent=2, ensure_ascii=False) + "\n"


def main():
    pages = {
        "index.html": page_index(),
        "work.html": page_work(),
        "about.html": page_about(),
        "skills.html": page_skills(),
        "resume.html": page_resume(),
        "contact.html": page_contact(),
        "privacy.html": page_doc("Privacy", "privacy", PRIVACY),
        "terms.html": page_doc("Terms", "terms", TERMS),
        "404.html": page_404(),
    }
    for i, p in enumerate(PROJECTS):
        pages[f"work/{p['slug']}.html"] = page_project(p, i)

    (ROOT / "work").mkdir(exist_ok=True)
    for path, html in pages.items():
        target = ROOT / path
        target.write_text(html, encoding="utf-8")
        print(f"  {path:<34} {len(html):>7,} bytes")
    today = datetime.date.today().isoformat()
    extras = {
        "sitemap.xml": sitemap(pages.keys(), today),
        "robots.txt": robots(),
        "site.webmanifest": webmanifest(),
    }
    for path, text in extras.items():
        (ROOT / path).write_text(text, encoding="utf-8")
        print(f"  {path:<34} {len(text):>7,} bytes")

    listed = len(pages) - len(SITEMAP_EXCLUDE & set(pages))
    print(f"\n{len(pages)} pages written to {ROOT}")
    print(f"{listed} URLs in sitemap.xml  ·  base {SITE_URL}")


if __name__ == "__main__":
    main()
