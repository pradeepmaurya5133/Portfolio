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
import re
import urllib.parse

ROOT = pathlib.Path(__file__).parent

# Absolute base URL used by sitemap.xml, canonicals, llms.txt and robots.txt.
# No trailing slash.
#
# This must be the host that actually SERVES the site, not the one that
# redirects to it. Vercel currently 308s the apex to www, so www is canonical;
# pointing canonicals at the apex would aim every one of them at a redirect.
# To prefer the shorter apex instead, switch the primary domain in
# Vercel → Project → Settings → Domains, then drop the "www." here.
SITE_URL = "https://www.pradeepmaury.in"

# ============================================================
#  PERSONAL DATA  (sourced from Pradeep_Maurya_Resume.docx)
# ============================================================
ME = {
    "name": "Pradeep Maurya",
    "first": "Pradeep",
    "role": "Full Stack Developer",
    "role_long": "Full Stack Developer & Software Engineer",
    "email": "pradeepmaurya2002@gmail.com",
    "phone": "+91 95199 65133",
    "phone_href": "+919519965133",
    "city": "Dehradun",
    "region": "Shree Enclave Panditwari, Dehradun, India",
    "linkedin": "https://linkedin.com/in/pradeep-maurya-b82b5820b/",
    "github": "https://github.com/pradeepmaurya5133/",
    "year": "2026",
    "tagline": ("I build modern, responsive, and scalable web applications that turn ideas into powerful digital experiences. From intuitive user interfaces to robust backend systems, I focus on clean code, practical problem-solving, and reliable software solutions."),
    "headline": "Building Modern Web Experiences & Scalable Software Solutions",
    "tech_line": "React.js · Next.js · Node.js · TypeScript · Python",
    "meta_description": ("Pradeep Maurya is a Full Stack Developer and Software Engineer specializing in modern web applications, frontend development, backend APIs, and custom software solutions."),
    "summary": ("I am Pradeep Maurya, a Full Stack Developer and Software Engineer passionate about building modern, scalable, and user-friendly web applications. I work across the development lifecycle, from creating responsive frontend interfaces to developing backend services, integrating APIs, and building practical software solutions."),
    "about": [
        "I am Pradeep Maurya, a Full Stack Developer and Software Engineer passionate about building modern, scalable, and user-friendly web applications.",
        "I work across the development lifecycle, from creating responsive frontend interfaces to developing backend services, integrating APIs, and building practical software solutions.",
        "My technical toolkit includes HTML, CSS, JavaScript, TypeScript, React.js, Next.js, Node.js, and Python. I enjoy solving real-world problems, learning modern technologies, and turning complex requirements into reliable digital products.",
        "I am open to freelance projects, professional collaborations, and opportunities to contribute to impactful software products.",
    ],
}

def article(word):
    """'a' or 'an' for the first word of `word`."""
    return "an" if word[:1].lower() in "aeiou" else "a"


NAV = [
    ("01", "Home", "{root}index.html"),
    ("02", "Work", "{root}work.html"),
    ("03", "About", "{root}about.html"),
    ("04", "Skills", "{root}skills.html"),
    ("05", "Experience", "{root}experience.html"),
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
        "role": "Web Developer",
        "org": "SS IntelligenceX Private Limited",
        "stack": "React, Next.js, TypeScript, Tailwind CSS, Node.js, REST APIs",
        "scope": "Website development, responsive UI, user-facing functionality, testing, usability",
        "link": "https://consentx.io",
        "summary": "A consent-focused digital solution designed to support consent management and privacy-related workflows.",
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
        "role": "Web Developer",
        "org": "SS IntelligenceX Private Limited",
        "stack": "React, Next.js, TypeScript, Tailwind CSS, Node.js, REST APIs",
        "scope": "Website development, responsive design, feature refinement, debugging, testing, performance",
        "link": "https://regulatorybridge.com",
        "summary": "A regulatory-focused digital solution designed to organize compliance-related information and simplify regulatory workflows.",
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
    {
        "slug": "portfolio",
        "name": "Portfolio",
        "full": "Personal Portfolio Website",
        "meta": "Static Site / Serverless",
        "tags": ["fullstack", "frontend", "backend"],
        "tag_labels": "Python Generator · Vanilla JS · GSAP · Vercel",
        "year": "2026",
        "role": "Designer and developer",
        "org": "Self-directed",
        "stack": ("Python (static site generator), HTML, CSS, vanilla JavaScript, "
                  "GSAP, Lenis, Vercel serverless functions"),
        "scope": "Design, build, content pipeline, contact API and deployment",
        "link": SITE_URL,
        "summary": ("A personal portfolio showcasing my technical expertise, selected projects, "
                    "professional experience, and freelance development services."),
        "lead": ("A personal portfolio showcasing my technical expertise, selected projects, "
                 "professional experience, and freelance development services."),
        "body": [
            ("Every page is generated by a Python build script from a single data source, so the "
             "same facts drive the HTML, the sitemap, the structured data and the machine-readable "
             "versions of each page. Editing one entry updates the site everywhere it appears."),
            ("The front end is vanilla JavaScript with GSAP and Lenis — no framework — and the "
             "contact form is backed by a serverless function on Vercel with validation, spam "
             "filtering and a graceful fallback when mail delivery is unavailable."),
        ],
        "notes": [
            ("One source of truth", "Content lives in structured data rather than in markup, so a "
             "change to a project or a job title propagates to every page, feed and metadata file "
             "in a single build."),
            ("Built to be read by machines too", "Alongside the HTML, each page is published as "
             "markdown, with an OpenAPI description for the contact API and discovery metadata "
             "for automated clients."),
        ],
    },
]

CAPABILITIES = [
    ("01", "Web Development",
     "Responsive, accessible, and high-performance websites designed around business goals "
     "and user needs."),
    ("02", "Full Stack Development",
     "End-to-end web applications featuring modern frontend interfaces, backend services, "
     "API integration, and database connectivity."),
    ("03", "Custom Software Development",
     "Practical software solutions that help businesses simplify workflows, improve "
     "productivity, and solve real-world challenges."),
    ("04", "API Integration &amp; Backend Development",
     "Reliable backend services, REST API integration, and maintainable application "
     "architectures."),
    ("05", "Website Maintenance &amp; Optimization",
     "Website improvements, bug fixes, performance optimization, and ongoing technical "
     "support."),
]

TOOLS = ["Visual Studio Code", "PyCharm", "Git", "GitHub", "Postman", "npm",
         "Prisma", "Redux Toolkit", "MS Excel", "Power BI"]
PLATFORMS = ["Web", "Responsive Mobile", "REST APIs", "Node.js", "Django", "PostgreSQL"]

SKILL_GROUPS = [
    ("01", "Frontend Development", ["HTML5", "CSS3", "JavaScript", "TypeScript",
                                    "React.js", "Next.js", "Tailwind CSS", "Bootstrap"]),
    ("02", "Backend Development", ["Node.js", "Express.js", "Python", "Django", "REST APIs",
                                   "AI API integration"]),
    ("03", "Tools &amp; Development Workflow", ["Git", "GitHub", "VS Code", "API testing",
                                                "Debugging", "Deployment", "npm"]),
    ("04", "Databases &amp; State", ["PostgreSQL", "Prisma", "Redux Toolkit"]),
    ("05", "Testing &amp; QA", ["Manual Testing", "API Testing (Postman)", "Web Testing",
                                "PyCharm"]),
    ("06", "Data &amp; Reporting", ["MS Excel", "Power BI"]),
]

# Development philosophy. Replaced the earlier "Why work with me" list, which
# covered the same ground in weaker language.
PHILOSOPHY = [
    ("01", "Build With Purpose",
     "Understand the problem before selecting a technical solution."),
    ("02", "Keep Code Maintainable",
     "Prefer readable, reusable, and well-structured implementations."),
    ("03", "Focus on User Experience",
     "Build interfaces that are intuitive, accessible, and responsive."),
    ("04", "Learn Continuously",
     "Explore modern development practices and improve through practical "
     "implementation."),
    ("05", "Collaborate Effectively",
     "Value clear communication, constructive feedback, and shared goals."),
]

# Framed for prospective freelance clients — a short list, deliberately not a
# second copy of the homepage Services cards.
HELP_WITH = [
    "Responsive website development",
    "Full-stack web applications",
    "Backend services and API integration",
    "Custom software solutions",
    "Website maintenance and improvements",
]

ABOUT_STORY = [
    ("My interest in software development comes from the ability to turn ideas into working "
     "digital products. I enjoy understanding how applications work, exploring new technologies, "
     "and building solutions that are both useful and maintainable."),
    ("My development work spans frontend interfaces, backend functionality, API integration, and "
     "web application development. I focus on writing clean code, creating responsive user "
     "experiences, and continuously improving my technical knowledge."),
    ("I believe that good software is more than code. It requires thoughtful problem-solving, "
     "clear communication, attention to detail, and an understanding of the people who use it."),
]

ABOUT_PERSONAL = ("I enjoy exploring new development approaches, solving technical challenges, "
                  "and improving the way software is built. I value consistency, curiosity, and "
                  "a willingness to learn from every project.")

# Condensed for About — the full breakdown lives on the Work page.
ABOUT_EXPERTISE = [
    ("01", "Frontend", ["HTML5", "CSS3", "JavaScript", "TypeScript", "React.js", "Next.js"]),
    ("02", "Backend", ["Node.js", "Python", "REST API development", "API integration"]),
    ("03", "Software Development", ["Responsive interfaces", "Reusable components", "Debugging",
                                    "Application architecture", "Maintainable code"]),
    ("04", "Tools", ["Git", "GitHub", "VS Code", "Postman", "npm", "Vercel"]),
]

ABOUT_EXPERIENCE_BLURB = (
    "I contribute to web development initiatives involving modern frontend technologies, "
    "application functionality, and digital product development. My work includes developing "
    "user interfaces, implementing features, integrating APIs, and improving application "
    "usability and maintainability.")

# Three shown on About; the rest live on the Work page.
ABOUT_PROJECT_SLUGS = ["consentx", "regulatorybridge", "portfolio"]

EXPERIENCE = [
    {
        "num": "01",
        "role": "Web Developer",
        "org": "SS IntelligenceX Private Limited",
        "managed_by": "iLeads Auxiliary Services Pvt. Ltd.",
        "product": "IntelligenceX.org",
        "when": "Aug 2026 — Present",
        "points": [
            "Develop and maintain responsive web interfaces using modern frontend technologies.",
            "Implement reusable UI components and application functionality.",
            "Contribute to development initiatives associated with ConsentX and RegulatoryBridge.",
            "Integrate APIs and support communication between frontend and backend services.",
            "Troubleshoot technical issues and improve code maintainability.",
            "Contribute to ongoing product improvements and application development.",
        ],
        "tech": ["HTML5", "CSS3", "JavaScript", "TypeScript", "React.js",
                 "Next.js", "Node.js", "Python"],
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
        "tech": ["Manual Testing", "API Testing", "MS Excel", "Power BI"],
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

# ============================================================
#  WORK PAGE — technical expertise
# ============================================================
# Two tiers, kept separate on purpose. The brief for this page was explicit
# that unverified technologies must not read as experience.
#
#   "using"    — evidenced by the résumé or by code in this repository.
#   "learning" — shown as a learning interest only, and rendered in a visibly
#                different style with a screen-reader label. EDIT THIS LIST:
#                it is the one place on the site not derived from evidence.
#
# Deliberately omitted entirely: Java, PHP, C, C++, C#, Go, Rust, Ruby, Swift,
# Kotlin, Dart, Vue, Angular, Svelte, Laravel, Spring Boot, .NET, AWS, Azure,
# GCP, Nginx, Apache. Listing ~20 untouched technologies would pad the page
# without telling a recruiter anything true.
TECH_STACK = [
    ("01", "Languages &amp; Web Technologies",
     ["JavaScript", "TypeScript", "Python", "SQL", "HTML5", "CSS3"],
     ["Bash / Shell"]),
    ("02", "Frontend Development",
     ["React.js", "Next.js", "Tailwind CSS", "Bootstrap", "Redux Toolkit",
      "Responsive Web Design", "UI Component Development"],
     ["Sass / SCSS", "Accessibility (WCAG)", "Frontend Performance"]),
    ("03", "Backend Development",
     ["Node.js", "Express.js", "Python", "Django", "REST API Development",
      "Authentication &amp; Authorization (JWT)", "Serverless Functions"],
     ["FastAPI", "GraphQL"]),
    ("04", "Databases &amp; Data Management",
     ["PostgreSQL", "Prisma (ORM)", "SQL", "Data Modeling", "Data Validation"],
     ["MongoDB", "SQLite", "Redis"]),
    ("05", "Software Engineering",
     ["Object-Oriented Programming", "Clean Code Principles", "Version Control",
      "API Design", "Debugging", "Code Review", "Documentation"],
     ["Data Structures &amp; Algorithms", "Design Patterns", "SOLID Principles",
      "System Design Fundamentals"]),
    ("06", "Tools, DevOps &amp; Deployment",
     ["Git", "GitHub", "VS Code", "PyCharm", "Postman", "npm", "Vercel",
      "Command Line"],
     ["Docker", "CI/CD (GitHub Actions)", "Linux"]),
    ("07", "AI-Powered Development &amp; Integrations",
     ["AI / LLM API Integration", "AI-Assisted Development"],
     ["Chatbot Integration", "Workflow Automation"]),
]

# Step 7 of the brief — capabilities, not technologies.
FULLSTACK_HIGHLIGHTS = [
    "End-to-End Web Application Development", "Frontend and Backend Integration",
    "REST API Development and Consumption", "Authentication and Authorization",
    "Database Integration", "Form Validation and Error Handling",
    "Application State Management", "Responsive Design",
    "Debugging and Testing", "Performance Optimization",
    "Secure Development Practices", "Maintainable Code and Reusable Components",
]

APPROACH = [
    ("01", "Understand", "Understand requirements and define scope."),
    ("02", "Plan", "Plan the application structure and technical approach."),
    ("03", "Build", "Build the user interface and backend functionality."),
    ("04", "Integrate", "Integrate APIs and databases where needed."),
    ("05", "Test", "Test, debug, and improve performance."),
    ("06", "Deploy", "Prepare the application for deployment and maintenance."),
]

# ============================================================
#  SKILLS PAGE
# ============================================================
# Twelve technologies given visual priority — the ones evidenced across the
# résumé and this repository.
CORE_STACK = [
    "HTML5", "CSS3", "JavaScript", "TypeScript", "React.js", "Next.js",
    "Node.js", "Python", "REST APIs", "Git", "GitHub", "VS Code",
]

# (num, category, blurb, verified[], secondary[])
#
#   verified  — evidenced by the résumé or by code in this repository.
#   secondary — collapsed behind a <details>, labelled "familiar / exploring",
#               and styled differently. NOT claimed as experience.
#
# ⚠ The `secondary` lists are the only content on this site not derived from
# evidence. Prune them to what is actually true before publishing.
SKILLS_MATRIX = [
    ("A", "Programming Languages &amp; Web Technologies",
     "The languages I write day to day, and the wider set I have had some exposure to.",
     ["JavaScript (ES6+)", "TypeScript", "Python", "SQL", "HTML5", "CSS3"],
     ["Bash / Shell", "Java", "PHP", "C", "C++", "C#", "Go", "Rust", "Ruby",
      "Swift", "Kotlin", "Dart"]),

    ("B", "Frontend Development",
     "Building responsive, component-driven interfaces that hold up on real devices.",
     ["Semantic HTML5", "CSS3", "Responsive Web Design", "Flexbox &amp; CSS Grid",
      "DOM Manipulation", "React.js", "Next.js", "Component Architecture",
      "Reusable UI Components", "State Management (Redux Toolkit)",
      "Form Handling &amp; Validation", "API Integration", "Tailwind CSS", "Bootstrap",
      "SEO-Friendly Markup"],
     ["Sass / SCSS", "Material UI", "Accessibility (WCAG)", "Web Performance Optimization",
      "Vue.js", "Angular", "Svelte"]),

    ("C", "Backend Development",
     "Server-side logic, application structure and the plumbing behind the interface.",
     ["Node.js", "Express.js", "Python", "Django", "Server-Side Development",
      "Business Logic", "Error Handling", "Request Validation",
      "Authentication &amp; Authorization", "Serverless Functions"],
     ["Middleware Design", "File Upload Handling", "Background Jobs",
      "Backend Performance Optimization", "Flask", "FastAPI"]),

    ("D", "API Development &amp; Integration",
     "Designing endpoints that are pleasant to consume, and consuming other people's well.",
     ["REST API Development", "REST API Consumption", "HTTP Methods &amp; Status Codes",
      "JSON Data Exchange", "Request Validation", "Authentication &amp; Authorization",
      "Error Handling", "API Documentation (OpenAPI)", "Third-Party API Integration",
      "API Testing (Postman)"],
     ["Pagination &amp; Filtering", "Webhooks", "GraphQL Fundamentals"]),

    ("E", "Databases &amp; Data Management",
     "Relational data modelling, migrations and keeping stored data trustworthy.",
     ["PostgreSQL", "SQL", "Prisma (ORM)", "Schema Design", "CRUD Operations",
      "Relationships &amp; Indexing", "Data Validation", "Database Migrations"],
     ["Query Optimization", "MySQL", "SQLite", "MongoDB", "Redis", "Firebase",
      "Supabase", "Microsoft SQL Server"]),

    ("F", "Full Stack Engineering",
     "I approach full-stack development as an integrated process, connecting user "
     "interfaces, server-side logic, APIs, and data storage to deliver cohesive "
     "digital products.",
     ["End-to-End Application Development", "Frontend &amp; Backend Integration",
      "Client-Server Architecture", "Authentication Workflows", "Database Connectivity",
      "Application State Management", "Form Validation", "Error &amp; Loading States",
      "Reusable Modules", "Environment Configuration", "Debugging",
      "Maintainable Architecture"],
     ["File &amp; Media Handling", "Performance Optimization"]),

    ("G", "Software Engineering Fundamentals",
     "The principles underneath the frameworks — some practised daily, some studied.",
     ["Object-Oriented Programming", "Clean Code", "Modular Architecture",
      "Separation of Concerns", "Code Reuse", "Error Handling", "Debugging",
      "Technical Documentation", "Code Review", "Problem-Solving"],
     ["Data Structures &amp; Algorithms", "SOLID Principles", "Design Patterns",
      "System Design Fundamentals", "Agile Development"]),

    ("H", "Testing &amp; Quality Assurance",
     "A year in QA before development — testing is a habit here, not an afterthought.",
     ["Manual Testing", "API Testing", "Regression Testing",
      "Form &amp; Input Validation", "Browser Compatibility Testing",
      "Responsive Testing", "Debugging &amp; Error Diagnosis"],
     ["Unit Testing", "Integration Testing", "End-to-End Testing", "Jest", "Vitest",
      "React Testing Library", "Playwright", "Cypress", "Pytest"]),

    ("I", "Git &amp; Development Workflow",
     "Version control and the day-to-day mechanics of working on a codebase.",
     ["Git", "GitHub", "Version Control", "Branching &amp; Merging", "Pull Requests",
      "Conflict Resolution", "Code Reviews", "README Documentation",
      "Package Management (npm)"],
     ["Issue Tracking", "pnpm", "Collaborative Workflows"]),

    ("J", "DevOps, Deployment &amp; Cloud",
     "Getting an application out of localhost and keeping it running.",
     ["Local Development Environments", "Environment Variables",
      "Build &amp; Deployment Workflows", "Vercel", "Command-Line Tools",
      "Serverless Deployment"],
     ["Docker", "GitHub Actions", "CI/CD Fundamentals", "Linux Fundamentals",
      "Netlify", "Application Logging", "Basic Monitoring", "Nginx", "Apache",
      "AWS", "Microsoft Azure", "Google Cloud Platform"]),

    ("K", "Web Security",
     "Development-level security practice — not a security certification or "
     "penetration-testing background.",
     ["Input Validation", "Secure Authentication Practices",
      "Authorization &amp; Access Control", "Environment Secret Management", "HTTPS",
      "CORS", "SQL Injection Prevention (parameterised queries / ORM)"],
     ["Password Handling Fundamentals", "XSS Awareness", "CSRF Awareness",
      "Dependency Updates", "OWASP Fundamentals"]),

    ("L", "Performance &amp; Accessibility",
     "Making pages fast to read and usable by everyone who lands on them.",
     ["Responsive Layouts", "Semantic HTML", "Keyboard Accessibility",
      "Image Optimization", "Lazy Loading", "Efficient API Requests",
      "Mobile-First Design", "Readable Typography"],
     ["Accessible Navigation", "Code Splitting", "Rendering Optimization",
      "Browser Performance Tools", "Core Web Vitals"]),

    ("M", "AI &amp; Automation",
     "Two different things, kept separate: integrating AI into applications, and "
     "using AI tooling while building them.",
     ["AI / LLM API Integration", "AI-Assisted Development", "AI-Assisted Debugging"],
     ["Prompt Engineering", "Chatbot Development", "Workflow Automation",
      "OpenAI API", "Anthropic API"]),

    ("N", "Freelance Development &amp; Client Collaboration",
     "As a freelance developer, I aim to understand each client's goals, recommend "
     "practical technical solutions, communicate clearly throughout development, and "
     "deliver maintainable websites and applications aligned with the agreed scope.",
     ["Requirement Gathering", "Client Communication", "Project Scoping",
      "Technical Recommendations", "Project Planning", "Progress Updates",
      "Feedback Implementation", "Testing &amp; Bug Fixing", "Documentation",
      "Website Maintenance"],
     ["Task Estimation", "Milestone Planning", "Deployment Coordination",
      "Technical Handover", "Post-Launch Improvements"]),
]

DEV_APPROACH = [
    ("01", "Understand the Problem",
     "Clarify requirements, users, constraints, and desired outcomes."),
    ("02", "Choose the Right Technology",
     "Select tools and frameworks according to project requirements rather than "
     "trends alone."),
    ("03", "Build With Quality",
     "Write maintainable code and develop responsive, accessible interfaces."),
    ("04", "Test and Improve",
     "Validate key workflows, fix issues, and refine application performance."),
    ("05", "Deliver and Maintain",
     "Support deployment, documentation, and agreed post-launch improvements."),
]

# Independent and freelance-oriented work. Deliberately separate from
# EXPERIENCE, which is employment only — the brief was explicit that
# independent projects must not read as paid client engagements. No client
# names, counts, earnings or durations are claimed, because none are verified.
FREELANCE = {
    "title": "Freelance Web Development &amp; Independent Projects",
    "kind": "Independent / self-directed",
    "description": (
        "I also focus on building practical digital solutions through independent development "
        "and freelance-oriented work. This includes developing portfolio websites, exploring "
        "full-stack application architecture, improving responsive interfaces, and working on "
        "projects that combine frontend technologies with backend functionality."),
    # Each of these is demonstrated by a project in PROJECTS.
    "areas": [
        "Responsive website development",
        "Frontend implementation",
        "Full-stack web applications",
        "API integration",
        "Website optimization and maintenance",
        "Custom software development",
        "Technical problem-solving",
    ],
    "note": ("The projects below are self-directed builds rather than paid client engagements. "
             "I am open to freelance work."),
}

# Condensed technical summary for the Experience page.
EXPERIENCE_SKILLS = [
    ("01", "Frontend", ["HTML5", "CSS3", "JavaScript", "TypeScript", "React.js", "Next.js"]),
    ("02", "Backend", ["Node.js", "Python", "REST APIs", "API integration"]),
    ("03", "Engineering", ["Responsive development", "Reusable components", "Debugging",
                           "Application maintenance", "Code organization"]),
    ("04", "Tools", ["Git", "GitHub", "VS Code", "PyCharm", "Postman", "npm", "Vercel"]),
]

# (title, focus, issuer, year, kind). `kind` is "education" or
# "certification" so the resume can use the two conventional headings.
# An empty issuer or year renders as nothing rather than as a placeholder —
# TODO: add the B.Tech institution and the award years once confirmed.
CREDENTIALS = [
    ("Front-End Development", "HTML, CSS, Bootstrap, JavaScript, React", "", "", "certification"),
    ("Python Full-Stack Development", "Python, Django, full-stack web", "DUCAT IT Training Institute, Noida", "", "certification"),
    ("Full-Stack Development", "Full-stack web development", "Coding Seekho, Pune (Online)", "", "certification"),
    ("B.Tech", "Computer Science &amp; Engineering", "", "", "education"),
]

# ============================================================
#  RESUME PAGE
# ============================================================
# The resume reads as a document, so it gets its own summary and its own
# skill headings — conventional resume labels an ATS parser recognises,
# rather than the site's section names. Everything here is drawn from the
# resume, from EXPERIENCE/PROJECTS above, or from code in this repository.
RESUME_TAGLINE = ("Building responsive web applications, reliable backend services, "
                  "and practical digital solutions.")

RESUME_SUMMARY = [
    ("I am a Full Stack Developer and Software Engineer focused on developing modern web "
     "applications and practical digital solutions. My technical toolkit includes JavaScript, "
     "TypeScript, React.js, Next.js, Node.js, and Python, with an interest in building "
     "responsive user interfaces, integrating APIs, and developing maintainable application "
     "functionality."),
    ("I contribute to web development initiatives associated with IntelligenceX.org, including "
     "ConsentX and RegulatoryBridge. I am interested in opportunities involving full-stack "
     "development, software engineering, and freelance projects where I can contribute to "
     "useful, reliable digital products."),
]

# Plain comma-separated rows — they stay readable in print and parse cleanly
# in an ATS. Every entry also appears in SKILL_GROUPS or in the verified tier
# of TECH_STACK; nothing is listed here that is not listed there.
RESUME_SKILLS = [
    ("Languages &amp; Web Technologies",
     ["JavaScript", "TypeScript", "Python", "SQL", "HTML5", "CSS3"]),
    ("Frontend Development",
     ["React.js", "Next.js", "Tailwind CSS", "Bootstrap", "Redux Toolkit",
      "Responsive web design", "Reusable UI components"]),
    ("Backend Development",
     ["Node.js", "Express.js", "Python", "Django", "REST API development",
      "API integration"]),
    ("Databases",
     ["PostgreSQL", "Prisma"]),
    ("Testing &amp; QA",
     ["Manual testing", "API testing (Postman)", "Web testing"]),
    ("Tools &amp; Workflow",
     ["Git", "GitHub", "VS Code", "PyCharm", "Postman", "npm", "Vercel"]),
    ("Data &amp; Reporting",
     ["MS Excel", "Power BI"]),
]

# A resume lists a few representative projects, not the whole portfolio.
RESUME_PROJECT_SLUGS = ["consentx", "regulatorybridge", "portfolio"]

# Capabilities exercised in independent work. Kept apart from EXPERIENCE,
# which is employment only.
RESUME_FREELANCE = (
    "Develop and explore web solutions through independent projects, portfolio development, "
    "and freelance-oriented work, with a focus on responsive interfaces, practical application "
    "functionality, and maintainable code.")

RESUME_FREELANCE_AREAS = [
    "Website development",
    "Full-stack application development",
    "API integration",
    "Responsive UI implementation",
    "Website maintenance",
    "Debugging and performance improvements",
    "Project planning and client communication",
]

# Downloadables that must exist on disk for the buttons to be honest.
# Regenerate the PDF with: python assets/_resume_pdf.py
RESUME_PDF = "assets/Pradeep_Maurya_Resume.pdf"
RESUME_DOCX = "assets/Pradeep_Maurya_Resume.docx"

STATS = [
    ("Years in tech", "02"),
    ("Projects shipped", "05"),
    ("Technologies used", "27"),
    ("Certifications", "03"),
]

# Real screenshots live as .jpg (see assets/img/_frame_screenshot.py); the rest
# fall back to the generated .svg placeholder of the same name.
SCREENSHOTS = {"consentx", "regulatorybridge", "xamlysis", "portfolio"}


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


def head(title, description, root, path="index.html", extra_css=""):
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
<link rel="canonical" href="{site_url(path)}">
{md_alternate(path)}{head_links(root)}<link rel="stylesheet" href="{root}assets/css/main.css">
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
<span class="line-mask"><span>Ready to Build</span></span>
<span class="line-mask"><span>Something <span class="accent">Great</span>?</span></span>
</h2>
<div class="cta__row">
<p class="cta__copy muted">Let's discuss your project and make it happen.</p>
<div class="cta__actions">
<a href="mailto:{ME['email']}" class="cta__email u-link">{ME['email']}</a>
<a href="{root}contact.html#f-name" class="btn" data-cursor="hover">Hire Me Now <span class="arrow" aria-hidden="true">{ARROW}</span></a>
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
<script src="{root}assets/js/webmcp.js" defer></script>
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
    for title, focus, issuer, year, _kind in CREDENTIALS:
        rows += (f'<div class="rec__row" role="row" data-award-row>'
                 f'<span role="cell" class="rec__title">{title}</span>'
                 f'<span role="cell">{focus}</span>'
                 f'<span role="cell" class="mono">{year or "—"}</span>'
                 f'<span role="cell">{issuer or "—"}</span>'
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
<span class="line-mask"><span>Services<span class="accent">.</span></span></span>
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

    rotate = ('["web experiences","software solutions","digital products",'
              '"web applications","user interfaces"]')

    return head(
        f"{ME['name']} | {ME['role_long']}",
        ME["meta_description"], root, "index.html"
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
<span class="sr-only">{ME['headline']}</span>
<span class="hero__line" aria-hidden="true">
<span data-hero-line>Building modern</span>
<span class="accent hero__rotate" data-rotate='{rotate}'>web experiences</span>
</span>
<span class="hero__line hero__line--pill" aria-hidden="true">
<a href="about.html" class="pill" data-pill data-cursor="view" data-cursor-label="About me" tabindex="-1">
<img src="assets/img/portrait-pill.jpg" alt="" loading="eager" fetchpriority="high" width="720" height="304">
</a>
<span data-hero-line>&amp; scalable software<span class="accent">.</span></span>
</span>
</h1>
<div class="hero__bottom">
<div>
<p class="hero__intro" data-hero-fade>{ME['tagline']}</p>
<p class="label muted" data-hero-fade style="margin-top:18px">{ME['tech_line']}</p>
</div>
<div class="bth__ctas" data-hero-fade style="margin-top:0">
<a href="contact.html#f-name" class="btn" data-cursor="hover">Hire Me <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="work.html" class="btn" data-cursor="hover">View My Projects <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="contact.html" class="label u-link" data-cursor="hover">Contact Me {ARROW}</a>
</div>
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
<p class="bth__lead" data-reveal>Full stack development on ConsentX and RegulatoryBridge.</p>
<p class="bth__text muted" data-reveal>
As a Web Developer at SS IntelligenceX Private Limited, managed by iLeads Auxiliary Services Pvt. Ltd., I work on two live platforms under the IntelligenceX.org product: a consent management solution and a regulatory compliance solution. My work covers responsive web interfaces, reusable UI components, API integration and full stack application development.
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
<footer class="mono muted">{ME['name']} // Web Developer @ SS IntelligenceX</footer>
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
        # Live link shown only where a real URL exists — no invented repos.
        live = (f'<span class="label accent card__live">Live {ARROW}</span>'
                if p["link"] else "")
        cards += (f'<a class="card" href="work/{p["slug"]}.html" data-tags="{"|".join(p["tags"])}" '
                  f'data-reveal style="--d:{i*0.06:.2f}s" data-cursor="view" data-cursor-label="Open" '
                  f'data-cursor-name="{p["name"]}">'
                  f'<span class="card__media"><img src="assets/img/{cover(p["slug"])}" '
                  f'alt="{p["name"]} — {p["meta"]} project cover" '
                  f'loading="lazy" decoding="async" width="2560" height="1600"></span>'
                  f'<span class="card__meta"><span class="mono muted">{i+1:02d}</span>'
                  f'<span class="card__title">{p["name"]}</span>'
                  f'<span class="label muted">{p["year"]}</span></span>'
                  f'<span class="label muted card__tags">{p["tag_labels"]}{live}</span></a>')

    # Technical expertise — reuses .sk__group / .sk__items from the Skills page.
    # Learning-interest items get .is-learning plus a screen-reader prefix, so
    # the distinction survives for someone not seeing the styling.
    stack = ""
    for num, name, using, learning in TECH_STACK:
        items = "".join(f'<li class="label">{t}</li>' for t in using)
        items += "".join(
            f'<li class="label is-learning">'
            f'<span class="sr-only">Learning: </span>{t}</li>' for t in learning)
        stack += (f'<div class="sk__group" data-reveal>'
                  f'<div><span class="sk__num mono">{num}</span>'
                  f'<h3 class="sk__name">{name}</h3></div>'
                  f'<ul class="sk__items">{items}</ul></div>')

    highlights = "".join(f'<li class="label">{h}</li>' for h in FULLSTACK_HIGHLIGHTS)

    approach = "".join(
        f'<li class="cap" data-reveal><span class="cap__num mono">{n}</span>'
        f'<div class="cap__body"><h3 class="cap__title">{t}</h3>'
        f'<p class="cap__desc muted">{d}</p></div></li>'
        for n, t, d in APPROACH
    )

    return head(f"Work &amp; Technical Expertise — {ME['name']}",
                "Full stack development capabilities, programming languages, frameworks, "
                f"databases, tools and selected projects by {ME['name']}.",
                root, "work.html") + f'''
<body>
{header("Work", root)}
<main id="main">

<section class="wh wrap">
<div class="wh__bg" aria-hidden="true">
<canvas data-plexus="1" data-plexus-ray="150"></canvas>
<div class="wh__shade"></div>
<div class="wh__scan"></div>
</div>
<p class="label muted wh__kicker"><span class="dot"></span> My work &amp; technical expertise</p>
<h1 class="wh__title wh__title--long display" data-split>
<span class="line-mask"><span>Building Digital Products.</span></span>
<span class="line-mask"><span>Engineering <span class="accent">Solutions</span>.</span></span>
</h1>
<p class="cb__lead" data-reveal style="margin-top:28px">I'm {ME['name']}, a Full Stack Developer
and Software Engineer passionate about building modern web applications, scalable backend systems,
and practical software solutions. Explore my technical expertise, development capabilities, and
selected projects across the software development lifecycle.</p>
<div class="bth__ctas" data-reveal>
<a href="#projects" class="btn" data-cursor="hover">Explore My Projects <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="contact.html#f-name" class="btn" data-cursor="hover">Let's Work Together <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
<div class="filters" data-filters role="group" aria-label="Filter projects">{chips}</div>
</section>

<section class="grid wrap" id="projects" aria-label="Selected projects">{cards}</section>

<section class="sk wrap" id="expertise" aria-labelledby="expertise-title">
<div class="section-head">
<h2 id="expertise-title" class="section-title" data-split>
<span class="line-mask"><span>Technical expertise<span class="accent">.</span></span></span>
</h2>
<p class="label muted">Solid = working with · Outlined = learning</p>
</div>
{stack}
</section>

<section class="section wrap" id="full-stack" aria-labelledby="fs-title">
<div class="section-head">
<h2 id="fs-title" class="section-title" data-split>
<span class="line-mask"><span>Full stack engineering<span class="accent">.</span></span></span>
</h2>
</div>
<p class="cb__lead" data-reveal style="margin-bottom:40px">I build web applications by connecting
modern user interfaces with backend services, APIs, and data storage. My approach focuses on
maintainable architecture, responsive experiences, reliable functionality, and practical solutions
to real-world requirements.</p>
<ul class="sk__items" data-reveal>{highlights}</ul>
</section>

<div class="theme-light">
<section class="caps section wrap" id="approach" aria-labelledby="approach-title">
<div class="caps__aside"><div class="caps__sticky">
<h2 id="approach-title" class="section-title" data-split>
<span class="line-mask"><span>How I</span></span>
<span class="line-mask"><span class="accent">work.</span></span>
</h2>
<p class="muted" style="max-width:360px">A consistent path from requirement to deployment, whatever
the size of the project.</p>
</div></div>
<ol class="caps__list">{approach}</ol>
</section>
</div>

<section class="section wrap" id="hire" aria-labelledby="hire-title">
<h2 id="hire-title" class="section-title" data-split>
<span class="line-mask"><span>Have a Project</span></span>
<span class="line-mask"><span>in <span class="accent">Mind</span>?</span></span>
</h2>
<p class="cb__lead" data-reveal style="margin-top:28px">Whether you need a responsive website, a
full-stack web application, an API integration, or a custom software solution, let's discuss your
requirements and find the right technical approach.</p>
<div class="bth__ctas" data-reveal>
<a href="contact.html#f-name" class="btn" data-cursor="hover">Contact Me <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="{ME['github']}" target="_blank" rel="noopener" class="btn" data-cursor="hover">View My GitHub <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
</section>

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
                f'<div><h3 class="exp__role">{strip_tags(e["role"])}</h3>'
                f'<p class="exp__org">{e["org"]}</p>'
                + (f'<p class="exp__when mono">Managed by {e["managed_by"]}</p>'
                   if e.get("managed_by") else "")
                + (f'<p class="exp__when mono">Product: {e["product"]}</p>'
                   if e.get("product") else "")
                + f'<p class="exp__when mono">{e["when"]}</p></div>'
                f'<ul class="exp__points">{points}</ul></li>')

    tldr = [
        ("Role", "Web Developer at SS IntelligenceX Private Limited"),
        ("Based in", "Dehradun, Uttarakhand, India"),
        ("Education", "B.Tech — Computer Science"),
        ("Focus", "Full stack web development, APIs and practical software solutions"),
        ("Open to", "Freelance projects, collaborations and full-time opportunities"),
    ]
    tldr_rows = "".join(
        f'<div class="tldr__row" data-reveal><dt class="label muted">{k}</dt><dd>{v}</dd></div>'
        for k, v in tldr
    )

    story = "".join(f'<p data-reveal>{para}</p>' for para in ABOUT_STORY[1:])

    expertise = ""
    for num, name, items in ABOUT_EXPERTISE:
        lis = "".join(f'<li class="label">{i}</li>' for i in items)
        expertise += (f'<div class="sk__group" data-reveal>'
                      f'<div><span class="sk__num mono">{num}</span>'
                      f'<h3 class="sk__name">{name}</h3></div>'
                      f'<ul class="sk__items">{lis}</ul></div>')

    picks = [x for x in PROJECTS if x["slug"] in ABOUT_PROJECT_SLUGS]
    cards = ""
    for i, pr in enumerate(picks):
        live = (f'<span class="label accent card__live">Live {ARROW}</span>'
                if pr["link"] else "")
        cards += (f'<a class="card" href="work/{pr["slug"]}.html" data-reveal '
                  f'style="--d:{i*0.06:.2f}s" data-cursor="view" data-cursor-label="Open" '
                  f'data-cursor-name="{pr["name"]}">'
                  f'<span class="card__media"><img src="assets/img/{cover(pr["slug"])}" '
                  f'alt="{pr["name"]} — {pr["meta"]} project cover" loading="lazy" '
                  f'decoding="async" width="2560" height="1600"></span>'
                  f'<span class="card__meta"><span class="mono muted">{i+1:02d}</span>'
                  f'<span class="card__title">{pr["name"]}</span>'
                  f'<span class="label muted">{pr["year"]}</span></span>'
                  f'<span class="label muted card__tags">{pr["summary"]}{live}</span></a>')

    philosophy = "".join(
        f'<li class="cap" data-reveal><span class="cap__num mono">{n}</span>'
        f'<div class="cap__body"><h3 class="cap__title">{t}</h3>'
        f'<p class="cap__desc muted">{d}</p></div></li>'
        for n, t, d in PHILOSOPHY
    )

    help_items = "".join(f'<li class="label">{h}</li>' for h in HELP_WITH)

    return head(f"About {ME['name']} | {ME['role_long']}",
                f"Learn about {ME['name']}, a Full Stack Developer and Software Engineer focused "
                "on modern web applications, frontend development, backend services, and practical "
                "software solutions.", root, "about.html") + f'''
<body>
{header("About", root)}
<main id="main">

<section class="ph" data-project-hero aria-labelledby="ph-title">
<div class="ph__top wrap label" data-ph-fade>
<a href="index.html" class="u-link" data-cursor="hover">{ARROW_BACK} Home</a>
<span class="muted">A little about me</span>
</div>
<h1 id="ph-title" class="ph__title display">
<span class="sr-only">Turning Ideas Into Digital Experiences</span>
<span aria-hidden="true" class="ph__word" data-fit>
<span data-ph-left>PRAD</span><span data-ph-right>EEP</span>
</span>
</h1>
<p class="ph__caption mono muted" data-ph-fade>
<span>Shree Enclave, Panditwari</span>
<span>Dehradun // Uttarakhand // India</span>
</p>
<div class="ph__media" data-ph-media>
<img src="assets/img/portrait.jpg" alt="Portrait of {ME['name']}, Full Stack Developer" loading="eager" fetchpriority="high" width="900" height="900">
</div>
<div class="ph__bottom wrap">
<p class="ph__summary" data-ph-fade>Turning Ideas Into Digital Experiences</p>
<p class="ph__tag label" data-ph-fade>Full Stack Developer | Software Engineer | Freelance Developer</p>
<div class="bth__ctas" data-ph-fade style="margin-top:4px;justify-content:center">
<a href="work.html" class="btn" data-cursor="hover">Explore My Work <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="contact.html#f-name" class="btn" data-cursor="hover">Contact Me <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
</div>
<div class="ph__foot wrap" data-ph-fade>
<span class="mono muted">© {ME['name']}</span>
<span class="ph__scroll label">Scroll <span class="ph__sq" aria-hidden="true">{ARROW_DOWN}</span></span>
</div>
</section>

<section class="bio wrap" id="story" aria-labelledby="story-title">
<p class="label muted bio__kicker"><span class="dot"></span> <span id="story-title">My journey in software development</span></p>
<div class="bio__text">
<p class="lead" data-reveal>{ABOUT_STORY[0]}</p>
{story}
<blockquote class="mission" data-reveal>
<span class="accent">&ldquo;</span>{ABOUT_PERSONAL}<span class="accent">&rdquo;</span>
</blockquote>
<p class="currently" data-reveal><span class="dot dot--round pulse" aria-hidden="true"></span> Open to freelance projects and new opportunities — <a class="u-link" href="contact.html">get in touch</a></p>
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
<p class="label muted exp__kicker"><span class="dot"></span> Professional experience</p>
<h2 id="exp-title" class="exp__title display" data-split>
<span class="line-mask"><span>Where I've</span></span>
<span class="line-mask"><span><span class="accent">worked</span>.</span></span>
</h2>
</div>
<div class="exp__copy">
<p class="exp__text" data-reveal>{ABOUT_EXPERIENCE_BLURB}</p>
<a href="experience.html" class="label u-link" data-cursor="hover" data-reveal>View Full Experience {ARROW}</a>
<a href="resume.html" class="label u-link" data-cursor="hover" data-reveal>Full résumé {ARROW}</a>
</div>
</div>
<ol class="exp__list">{exp}</ol>
</section>

<section class="sk wrap" id="expertise" aria-labelledby="skills-title">
<div class="section-head">
<h2 id="skills-title" class="section-title" data-split>
<span class="line-mask"><span>Technical expertise<span class="accent">.</span></span></span>
</h2>
<a href="work.html#expertise" class="label u-link" data-cursor="hover">Full skills overview {ARROW}</a>
</div>
{expertise}
</section>

<section class="grid wrap" id="projects" aria-label="Selected projects">{cards}</section>
<section class="wrap" style="padding-bottom:clamp(64px,8vw,120px)">
<a href="work.html" class="btn" data-reveal data-cursor="hover">View All Projects <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</section>

<div class="theme-light">
<section class="caps section wrap" id="philosophy" aria-labelledby="phil-title">
<div class="caps__aside"><div class="caps__sticky">
<h2 id="phil-title" class="section-title" data-split>
<span class="line-mask"><span>Development</span></span>
<span class="line-mask"><span class="accent">philosophy.</span></span>
</h2>
<p class="muted" style="max-width:360px">How I approach building software, whatever the project.</p>
</div></div>
<ol class="caps__list">{philosophy}</ol>
</section>
</div>

<section class="sk wrap" id="help" aria-labelledby="help-title">
<div class="section-head">
<h2 id="help-title" class="section-title" data-split>
<span class="line-mask"><span>What I can help with<span class="accent">.</span></span></span>
</h2>
</div>
<p class="cb__lead" data-reveal style="margin-bottom:32px">I am open to discussing projects where thoughtful engineering and practical problem-solving can help turn an idea into a working digital product.</p>
<ul class="sk__items" data-reveal>{help_items}</ul>
</section>

{credentials_table(root)}

<section class="section wrap" id="connect" aria-labelledby="connect-title">
<h2 id="connect-title" class="section-title" data-split>
<span class="line-mask"><span>Let's Build</span></span>
<span class="line-mask"><span>Something <span class="accent">Meaningful</span>.</span></span>
</h2>
<p class="cb__lead" data-reveal style="margin-top:28px">Have a project idea, a development challenge, or an opportunity to collaborate? I'd be happy to connect and discuss how we can bring your ideas to life.</p>
<div class="bth__ctas" data-reveal>
<a href="contact.html#f-name" class="btn" data-cursor="hover">Get in Touch <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="work.html" class="btn" data-cursor="hover">Explore My Work <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
</section>

</main>
{footer(root)}
{chrome_end(root)}'''



def page_skills():
    root = ""

    core = "".join(f'<li class="label">{t}</li>' for t in CORE_STACK)

    # Verified skills sit in the open; secondary ones collapse into a native
    # <details>, which is keyboard-accessible and needs no JavaScript. The
    # summary states the count so the group is honest even while closed.
    groups = ""
    for num, name, blurb, verified, secondary in SKILLS_MATRIX:
        pills = "".join(f'<li class="label">{t}</li>' for t in verified)
        more = ""
        if secondary:
            extra = "".join(
                f'<li class="label is-learning">'
                f'<span class="sr-only">Familiar or exploring: </span>{t}</li>'
                for t in secondary)
            more = (f'<details class="sk__more">'
                    f'<summary class="label muted">'
                    f'+ {len(secondary)} familiar / exploring</summary>'
                    f'<ul class="sk__items">{extra}</ul></details>')
        groups += (f'<div class="sk__group" data-reveal>'
                   f'<div><span class="sk__num mono">{num}</span>'
                   f'<h3 class="sk__name">{name}</h3>'
                   f'<p class="sk__blurb muted">{blurb}</p></div>'
                   f'<div><ul class="sk__items">{pills}</ul>{more}</div></div>')

    approach = "".join(
        f'<li class="cap" data-reveal><span class="cap__num mono">{n}</span>'
        f'<div class="cap__body"><h3 class="cap__title">{t}</h3>'
        f'<p class="cap__desc muted">{d}</p></div></li>'
        for n, t, d in DEV_APPROACH
    )

    picks = [x for x in PROJECTS if x["slug"] in ABOUT_PROJECT_SLUGS]
    cards = ""
    for i, pr in enumerate(picks):
        live = (f'<span class="label accent card__live">Live {ARROW}</span>'
                if pr["link"] else "")
        cards += (f'<a class="card" href="work/{pr["slug"]}.html" data-reveal '
                  f'style="--d:{i*0.06:.2f}s" data-cursor="view" data-cursor-label="Open" '
                  f'data-cursor-name="{pr["name"]}">'
                  f'<span class="card__media"><img src="assets/img/{cover(pr["slug"])}" '
                  f'alt="{pr["name"]} — {pr["meta"]} project cover" loading="lazy" '
                  f'decoding="async" width="2560" height="1600"></span>'
                  f'<span class="card__meta"><span class="mono muted">{i+1:02d}</span>'
                  f'<span class="card__title">{pr["name"]}</span>'
                  f'<span class="label muted">{pr["year"]}</span></span>'
                  f'<span class="label muted card__tags">{pr["stack"]}{live}</span></a>')

    return head(f"{ME['name']} | Full Stack Developer Skills &amp; Expertise",
                f"Explore {ME['name']}'s full-stack development skills, including frontend "
                "technologies, backend development, APIs, databases, software engineering, "
                "and freelance web development.", root, "skills.html") + f'''
<body>
{header("Skills", root)}
<main id="main">

<section class="wh wrap">
<p class="label muted wh__kicker"><span class="dot"></span> Technical expertise</p>
<h1 class="wh__title wh__title--long display" data-split>
<span class="line-mask"><span>The Skills Behind</span></span>
<span class="line-mask"><span>Every <span class="accent">Digital Solution</span>.</span></span>
</h1>
<p class="ph__tag label" data-reveal style="margin-top:22px;display:inline-block">Full Stack Developer · Software Engineer · Freelance Developer</p>
<p class="cb__lead" data-reveal style="margin-top:24px">My technical toolkit spans modern web
technologies, frontend engineering, backend development, API integration, and software delivery.
I focus on building responsive interfaces, reliable application functionality, and maintainable
digital solutions that address real-world needs.</p>
<div class="bth__ctas" data-reveal>
<a href="#stack" class="btn" data-cursor="hover">Explore My Expertise <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="work.html" class="btn" data-cursor="hover">View My Work <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="contact.html#f-name" class="btn" data-cursor="hover">Hire Me <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
</section>

<section class="sk wrap" id="stack" aria-labelledby="stack-title">
<div class="section-head">
<h2 id="stack-title" class="section-title" data-split>
<span class="line-mask"><span>My core technology stack<span class="accent">.</span></span></span>
</h2>
</div>
<p class="cb__lead" data-reveal style="margin-bottom:32px">The technologies I reach for first,
across the stack and the toolchain.</p>
<ul class="sk__items sk__items--core" data-reveal>{core}</ul>
</section>

<section class="sk wrap" id="expertise" aria-labelledby="matrix-title">
<div class="section-head">
<h2 id="matrix-title" class="section-title" data-split>
<span class="line-mask"><span>Complete skill set<span class="accent">.</span></span></span>
</h2>
<p class="label muted">Solid = working with · Collapsed = familiar / exploring</p>
</div>
{groups}
</section>

<div class="theme-light">
<section class="caps section wrap" id="approach" aria-labelledby="approach-title">
<div class="caps__aside"><div class="caps__sticky">
<h2 id="approach-title" class="section-title" data-split>
<span class="line-mask"><span>How I approach</span></span>
<span class="line-mask"><span class="accent">development.</span></span>
</h2>
<p class="muted" style="max-width:360px">The same five steps, whether it is a landing page or a
full application.</p>
</div></div>
<ol class="caps__list">{approach}</ol>
</section>
</div>

<section class="sk wrap" id="proof" aria-labelledby="proof-title">
<div class="section-head">
<h2 id="proof-title" class="section-title" data-split>
<span class="line-mask"><span>Skills in practice<span class="accent">.</span></span></span>
</h2>
<a href="work.html" class="label u-link" data-cursor="hover">All projects {ARROW}</a>
</div>
<p class="cb__lead" data-reveal style="margin-bottom:32px">Where these technologies actually meet
— frontend, backend, APIs and data in one running product.</p>
</section>
<section class="grid wrap" aria-label="Selected projects">{cards}</section>

</main>
{footer(root)}
{chrome_end(root)}'''



def page_resume():
    """The resume, in two presentation modes.

    Screen: the site's own layout — sticky contact aside, revealed blocks.
    Print:  assets/css/print.css collapses it to a single-column document,
            drops the chrome and the animation transforms, and swaps the
            display hero for .res__printhead. Section order is the
            conventional one (summary, skills, experience, projects,
            education, certifications) in the DOM, so print, PDF export and
            an ATS parser all read it in that order.
    """
    root = ""

    skills = "".join(
        f'<div class="res__line" data-reveal>'
        f'<dt class="res__dt">{heading}</dt>'
        f'<dd>{", ".join(items)}</dd></div>'
        for heading, items in RESUME_SKILLS
    )

    exp = ""
    for e in EXPERIENCE:
        points = "".join(f'<li>{pt}</li>' for pt in e["points"])
        meta = [e["org"]]
        if e.get("managed_by"):
            meta.append(f'Managed by {e["managed_by"]}')
        if e.get("product"):
            meta.append(f'Product: {e["product"]}')
        tech = ""
        if e.get("tech"):
            tech = (f'<p class="res__tech mono muted">'
                    f'Technologies: {", ".join(e["tech"])}</p>')
        exp += (f'<div class="res__line" data-reveal>'
                f'<dt class="res__dt"><strong class="res__role">{strip_tags(e["role"])}</strong>'
                f'<span class="res__when mono">{e["when"]}</span></dt>'
                f'<dd><p class="res__org">{" · ".join(meta)}</p>'
                f'<ul class="res__list">{points}</ul>{tech}</dd></div>')

    areas = "".join(f'<li>{a}</li>' for a in RESUME_FREELANCE_AREAS)

    picks = [x for x in PROJECTS if x["slug"] in RESUME_PROJECT_SLUGS]
    proj = ""
    for p in picks:
        live = ""
        if p["link"]:
            label = p["link"].replace("https://", "").rstrip("/")
            live = (f'<p class="res__link"><a class="u-link" href="{p["link"]}"'
                    f'{external(p["link"])}>{label} {ARROW}</a></p>')
        proj += (f'<div class="res__line" data-reveal>'
                 f'<dt class="res__dt"><strong class="res__role">{p["full"]}</strong>'
                 f'<span class="res__when mono">{p["year"]}</span></dt>'
                 f'<dd><p class="res__lead">{p["summary"]}</p>'
                 f'<p class="res__tech mono muted">Stack: {p["stack"]}</p>'
                 f'<p class="res__tech mono muted">Contribution: {p["scope"]}</p>'
                 f'{live}'
                 f'<p class="res__more"><a class="u-link" '
                 f'href="work/{p["slug"]}.html" data-cursor="hover">Case study {ARROW}</a>'
                 f'</p></dd></div>')

    def creds(kind):
        out = ""
        for title, focus, issuer, year, k in CREDENTIALS:
            if k != kind:
                continue
            detail = " · ".join(x for x in (issuer, year) if x)
            out += (f'<div class="res__line" data-reveal>'
                    f'<dt class="res__dt"><strong class="res__role">{title}</strong></dt>'
                    f'<dd><p>{focus}</p>'
                    + (f'<p class="res__tech mono muted">{detail}</p>' if detail else "")
                    + '</dd></div>')
        return out

    education = creds("education")
    certs = creds("certification")

    # Only rendered if the file is actually on disk — the brief was explicit
    # that a download must not be advertised unless it exists.
    pdf = (f'<a class="btn btn--solid" href="{RESUME_PDF}" download '
           f'data-cursor="hover">Download Resume PDF '
           f'<span class="arrow" aria-hidden="true">{ARROW}</span></a>'
           if (ROOT / RESUME_PDF).exists() else "")
    docx = (f'<p><a class="u-link" href="{RESUME_DOCX}" download>'
            f'Word version (.docx) {ARROW}</a></p>'
            if (ROOT / RESUME_DOCX).exists() else "")

    contact_line = " · ".join([
        ME["email"], ME["phone"], ME["region"],
        SITE_URL.replace("https://", ""),
        ME["linkedin"].replace("https://", "").rstrip("/"),
        ME["github"].replace("https://", "").rstrip("/"),
    ])

    return head(f"{ME['name']} | Full Stack Developer Resume",
                f"View {ME['name']}'s resume, technical skills, professional experience, "
                "and projects in full-stack development and software engineering.",
                root, "resume.html",
                extra_css=f'\n<link rel="stylesheet" href="{root}assets/css/print.css" media="print">'
                ) + f'''
<body>
{header("Résumé", root)}
<main id="main">

<section class="wh wrap res__head">
<p class="label muted wh__kicker"><span class="dot"></span> Résumé</p>
<h1 class="wh__title display" data-split>
<span class="line-mask"><span>{ME['first']}</span></span>
<span class="line-mask"><span>{ME['name'].split()[-1]}<span class="accent">.</span></span></span>
</h1>
<p class="ph__tag label" data-reveal style="margin-top:22px;display:inline-block">Full Stack Developer | Software Engineer</p>
<p class="cb__lead" data-reveal style="margin-top:24px">{RESUME_TAGLINE}</p>
<div class="bth__ctas" data-reveal>
{pdf}
<button type="button" class="btn" data-print data-cursor="hover">Print / Save as PDF <span class="arrow" aria-hidden="true">{ARROW}</span></button>
<a href="contact.html#f-name" class="btn" data-cursor="hover">Contact Me <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
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
<p><a class="u-link" href="index.html" data-cursor="hover">Portfolio {ARROW}</a></p>
<p><a class="u-link" href="{ME['github']}" target="_blank" rel="noopener">GitHub {ARROW}</a></p>
<p><a class="u-link" href="{ME['linkedin']}" target="_blank" rel="noopener">LinkedIn {ARROW}</a></p>
</div>
<div>
<p class="label muted" style="margin-bottom:12px">On this site</p>
<p><a class="u-link" href="experience.html" data-cursor="hover">Experience {ARROW}</a></p>
<p><a class="u-link" href="skills.html" data-cursor="hover">Skills {ARROW}</a></p>
<p><a class="u-link" href="work.html" data-cursor="hover">Work {ARROW}</a></p>
<p><a class="u-link" href="about.html" data-cursor="hover">About {ARROW}</a></p>
</div>
<div>
<p class="label muted" style="margin-bottom:12px">Download</p>
{docx}
<p><button type="button" class="u-link res__printlink" data-print>Print / Save as PDF {ARROW}</button></p>
</div>
</aside>

<div class="res__doc">

<header class="res__printhead" aria-hidden="true">
<p class="res__printname">{ME['name']}</p>
<p class="res__printrole">Full Stack Developer | Software Engineer</p>
<p class="res__printtag">{RESUME_TAGLINE}</p>
<p class="res__printmeta">{contact_line}</p>
</header>

<div class="res__block" id="summary">
<h2 class="res__h">Summary</h2>
{"".join(f'<p class="res__p">{p}</p>' for p in RESUME_SUMMARY)}
</div>

<div class="res__block" id="skills">
<h2 class="res__h">Technical Skills</h2>
<dl>{skills}</dl>
</div>

<div class="res__block" id="experience">
<h2 class="res__h">Professional Experience</h2>
<dl>{exp}</dl>
</div>

<div class="res__block" id="freelance">
<h2 class="res__h">Freelance &amp; Independent Development</h2>
<p class="res__p">{RESUME_FREELANCE}</p>
<ul class="res__list res__list--inline">{areas}</ul>
<p class="res__note muted">{FREELANCE['note']}</p>
</div>

<div class="res__block" id="projects">
<h2 class="res__h">Projects</h2>
<dl>{proj}</dl>
<p class="res__more res__more--all"><a class="u-link" href="work.html" data-cursor="hover">All projects {ARROW}</a></p>
</div>

<div class="res__block" id="education">
<h2 class="res__h">Education</h2>
<dl>{education}</dl>
</div>

<div class="res__block" id="certifications">
<h2 class="res__h">Certifications</h2>
<dl>{certs}</dl>
</div>

</div>
</div>
</section>
</main>
{footer(root)}
{chrome_end(root)}'''



def page_contact():
    """Contact page.

    The form posts to /api/contact (see api/contact.js). Delivery needs
    RESEND_API_KEY in the Vercel environment; without it the endpoint
    answers 503 and the front end falls back to the visitor's own mail
    client rather than claiming a message was sent.
    """
    root = ""

    socials = "".join(
        f'<a href="{url}"{external(url)} data-cursor="hover">'
        f'<span>{name}</span><span class="mono muted">{ARROW}</span></a>'
        for name, url in SOCIALS
    )
    # The portfolio itself is a verified link, and it belongs with the others.
    socials += (f'<a href="index.html" data-cursor="hover">'
                f'<span>Portfolio</span>'
                f'<span class="mono muted">{ARROW}</span></a>')

    topics = "".join(
        f'<li class="cap" data-reveal><span class="cap__num mono">{n}</span>'
        f'<div class="cap__body"><h3 class="cap__title">{t}</h3>'
        f'<p class="cap__desc muted">{d}</p></div></li>'
        for n, t, d in CONTACT_TOPICS
    )
    options = "".join(f'<option value="{t}"></option>' for _, t, _ in CONTACT_TOPICS)

    return head(f"Contact {ME['name']} | {ME['role']}",
                f"Get in touch with {ME['name']}, {article(ME['role'])} {ME['role']} — "
                "full-time opportunities, freelance development, web application "
                "projects and technical collaboration.",
                root, "contact.html") + f'''
<body>
{header("Contact", root)}
<main id="main">

<section class="ch wrap">
<div class="ch__bg" aria-hidden="true"><canvas data-flow="0.45"></canvas></div>
<p class="label muted ch__kicker"><span class="dot"></span> Get in touch</p>
<h1 class="ch__title display" data-split>
<span class="line-mask"><span>Let's Build</span></span>
<span class="line-mask"><span>Something <span class="accent">Great</span>.</span></span>
</h1>
<p class="cb__lead ch__lead" data-reveal>{CONTACT_INTRO}</p>
</section>

<section class="cb wrap">
<div class="cb__main">
<p class="cb__lead" data-reveal>{CONTACT_AUDIENCE}</p>

<form class="form" data-contact-form action="/api/contact" method="post" novalidate
      aria-labelledby="form-title"
      toolname="send_message"
      tooldescription="Send a message to {ME['name']}. Delivers a real email, so confirm the wording with the user first.">
<h2 id="form-title" class="sr-only">Send a message</h2>

<div class="field">
<label class="label muted" for="f-name">Your name <span class="field__req" aria-hidden="true">*</span></label>
<input toolparamdescription="Sender&#39;s full name." id="f-name" name="name" type="text"
       placeholder="Jane Doe" required maxlength="120" autocomplete="name"
       aria-describedby="e-name">
<p class="field__error" id="e-name" data-error-for="name" aria-live="polite"></p>
</div>

<div class="field">
<label class="label muted" for="f-email">Email <span class="field__req" aria-hidden="true">*</span></label>
<input toolparamdescription="Sender&#39;s email address, used as the reply-to." id="f-email"
       name="email" type="email" placeholder="jane@company.com" required maxlength="254"
       autocomplete="email" inputmode="email" aria-describedby="e-email">
<p class="field__error" id="e-email" data-error-for="email" aria-live="polite"></p>
</div>

<div class="field">
<label class="label muted" for="f-subject">Subject <span class="muted">(optional)</span></label>
<input toolparamdescription="Optional subject or enquiry type." id="f-subject" name="subject"
       type="text" list="enquiry-types" maxlength="160" autocomplete="off"
       placeholder="Freelance project, full-time role, collaboration…"
       aria-describedby="e-subject f-subject-hint">
<datalist id="enquiry-types">{options}</datalist>
<p class="field__hint muted" id="f-subject-hint">Pick a suggestion or write your own.</p>
<p class="field__error" id="e-subject" data-error-for="subject" aria-live="polite"></p>
</div>

<div class="field">
<label class="label muted" for="f-message">Message <span class="field__req" aria-hidden="true">*</span></label>
<textarea toolparamdescription="The message body." id="f-message" name="message" rows="4"
          placeholder="What are you building?" required maxlength="5000"
          aria-describedby="e-message"></textarea>
<p class="field__error" id="e-message" data-error-for="message" aria-live="polite"></p>
</div>

<div class="form__trap" aria-hidden="true">
<label for="f-website">Website</label>
<input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off">
</div>

<p class="form__status mono" data-form-status role="status" aria-live="polite"></p>

<div class="form__foot">
<button class="btn btn--solid" type="submit" data-cursor="hover" data-submit>
<span data-submit-label>Send Message</span>
<span class="arrow" aria-hidden="true">{ARROW}</span>
</button>
<p class="form__consent muted">Your name, email and message are used only to reply to you. See the <a class="u-link" href="privacy.html">privacy note</a>.</p>
</div>
</form>
</div>

<aside class="cb__aside" aria-labelledby="reach-title">
<h2 id="reach-title" class="sr-only">Contact details</h2>
<div>
<p class="label muted cb__label">Email</p>
<a class="cb__email u-link" href="mailto:{ME['email']}" data-contact-email data-cursor="hover">{ME['email']}</a>
</div>
<div>
<p class="label muted cb__label">Phone</p>
<a class="cb__email u-link" href="tel:{ME['phone_href']}" data-cursor="hover">{ME['phone']}</a>
</div>
<div>
<p class="label muted cb__label">Based in</p>
<p>{ME['region']}</p>
<p class="cb__time mono muted">Local time <span data-clock>--:--:--</span> IST</p>
</div>
<div>
<p class="label muted cb__label">Elsewhere</p>
<div class="cb__socials">{socials}</div>
</div>
</aside>
</section>

<div class="theme-light">
<section class="caps section wrap" id="topics" aria-labelledby="topics-title">
<div class="caps__aside"><div class="caps__sticky">
<p class="label muted"><span class="dot"></span> Enquiries</p>
<h2 id="topics-title" class="section-title" data-split>
<span class="line-mask"><span>What can we</span></span>
<span class="line-mask"><span class="accent">discuss?</span></span>
</h2>
<p class="muted" style="max-width:360px">Pick whichever is closest — the subject field above
takes the same list.</p>
</div></div>
<ol class="caps__list">{topics}</ol>
</section>
</div>

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

    return head(f"{p['name']} — {ME['name']}", p["summary"], root, f"work/{p['slug']}.html") + f'''
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
    return head(f"{title} — {ME['name']}", f"{title} for {ME['name']}'s portfolio.", root, f"{slug}.html") + f'''
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


def page_api_docs():
    """Human-readable docs — the `service-doc` the API catalog points at."""
    root = "../"
    base = SITE_URL.rstrip("/")
    errors = "".join(
        f'<li data-reveal><span class="label muted">{code}</span>'
        f'<span>{text}</span></li>'
        for code, text in sorted(API_ERRORS.items())
    )
    return head("API — " + ME["name"],
                f"HTTP API behind {ME['name']}'s portfolio: contact delivery "
                f"and a health endpoint.", root, "docs/api.html") + f'''
<body>
{header("", root)}
<main id="main">
<section class="wh wrap">
<p class="label muted wh__kicker"><span class="dot"></span> Developer reference</p>
<h1 class="wh__title display" data-split>
<span class="line-mask"><span>API<span class="accent">.</span></span></span>
</h1>
<p class="cb__lead" data-reveal style="margin-top:28px">A small HTTP API behind this
portfolio. Machine-readable description:
<a class="u-link" href="{root}openapi.json">openapi.json</a> ·
catalog: <a class="u-link" href="{root}.well-known/api-catalog">/.well-known/api-catalog</a></p>
</section>

<section class="res wrap" style="padding-top:0">
<div class="res__block">
<h2 class="res__h">POST /api/contact</h2>
<p class="muted" style="margin-bottom:24px">Delivers the contact form. Accepts
JSON or form-encoded bodies.</p>
<dl>
<div class="res__line" data-reveal><dt class="label muted">name</dt>
<dd>string, required, max 120</dd></div>
<div class="res__line" data-reveal><dt class="label muted">email</dt>
<dd>string, required, max 254 — used as the reply-to address</dd></div>
<div class="res__line" data-reveal><dt class="label muted">subject</dt>
<dd>string, optional, max 160 — used as the subject of the delivered mail</dd></div>
<div class="res__line" data-reveal><dt class="label muted">company</dt>
<dd>string, optional, max 160</dd></div>
<div class="res__line" data-reveal><dt class="label muted">message</dt>
<dd>string, required, max 5000</dd></div>
<div class="res__line" data-reveal><dt class="label muted">website</dt>
<dd>honeypot — leave empty. A non-empty value is treated as a bot and
discarded, with a 200 so the bot learns nothing.</dd></div>
</dl>
<pre class="api__code" data-reveal><code>curl -X POST {base}/api/contact \\
  -H 'Content-Type: application/json' \\
  -d '{{"name":"Jane","email":"jane@example.com","message":"Hello"}}'</code></pre>
<p class="muted">Returns <code>{{"ok":true}}</code> on success.
<code>400</code> with an error code on validation failure, <code>502</code> if
the mail provider rejects it, <code>503</code> if sending is not configured.</p>
</div>

<div class="res__block">
<h2 class="res__h">GET /api/health</h2>
<p class="muted" style="margin-bottom:24px">Liveness and configuration status —
the <code>status</code> relation in the API catalog.</p>
<pre class="api__code" data-reveal><code>{{"status":"ok","contact":"ready","time":"…"}}</code></pre>
<p class="muted"><code>contact</code> reports <code>unconfigured</code> when the
mail key is missing, so a monitor sees a misconfigured deploy rather than a
false green.</p>
</div>

<div class="res__block">
<h2 class="res__h">Error codes</h2>
<ul class="credits__list">{errors}</ul>
</div>
</section>
</main>
{footer(root)}
{chrome_end(root)}'''


def page_experience():
    """Dedicated career page. about.html keeps its own #experience summary —
    the brief required that anchor to keep working."""
    root = ""

    roles = ""
    for e in EXPERIENCE:
        points = "".join(f'<li>{pt}</li>' for pt in e["points"])
        tech = ""
        if e.get("tech"):
            chips = "".join(f'<li class="label">{t}</li>' for t in e["tech"])
            tech = f'<ul class="sk__items exp__tech">{chips}</ul>'
        roles += (f'<li class="exp__item" data-reveal>'
                  f'<span class="exp__num mono">{e["num"]}</span>'
                  f'<div><h3 class="exp__role">{strip_tags(e["role"])}</h3>'
                  f'<p class="exp__org">{e["org"]}</p>'
                  + (f'<p class="exp__when mono">Managed by {e["managed_by"]}</p>'
                     if e.get("managed_by") else "")
                  + (f'<p class="exp__when mono">Product: {e["product"]}</p>'
                     if e.get("product") else "")
                  + f'<p class="exp__when mono">{e["when"]}</p></div>'
                  f'<div><ul class="exp__points">{points}</ul>{tech}</div></li>')

    areas = "".join(f'<li class="label">{a}</li>' for a in FREELANCE["areas"])

    skills = ""
    for num, name, items in EXPERIENCE_SKILLS:
        lis = "".join(f'<li class="label">{i}</li>' for i in items)
        skills += (f'<div class="sk__group" data-reveal>'
                   f'<div><span class="sk__num mono">{num}</span>'
                   f'<h3 class="sk__name">{name}</h3></div>'
                   f'<ul class="sk__items">{lis}</ul></div>')

    picks = [x for x in PROJECTS if x["slug"] in ABOUT_PROJECT_SLUGS]
    cards = ""
    for i, pr in enumerate(picks):
        live = (f'<span class="label accent card__live">Live {ARROW}</span>'
                if pr["link"] else "")
        cards += (f'<a class="card" href="work/{pr["slug"]}.html" data-reveal '
                  f'style="--d:{i*0.06:.2f}s" data-cursor="view" data-cursor-label="Open" '
                  f'data-cursor-name="{pr["name"]}">'
                  f'<span class="card__media"><img src="assets/img/{cover(pr["slug"])}" '
                  f'alt="{pr["name"]} — {pr["meta"]} project cover" loading="lazy" '
                  f'decoding="async" width="2560" height="1600"></span>'
                  f'<span class="card__meta"><span class="mono muted">{i+1:02d}</span>'
                  f'<span class="card__title">{pr["name"]}</span>'
                  f'<span class="label muted">{pr["year"]}</span></span>'
                  f'<span class="label muted card__tags">{pr["summary"]}{live}</span></a>')

    return head(f"Professional Experience | {ME['name']}",
                f"Explore {ME['name']}'s professional experience in web development, full-stack "
                "engineering, software projects, and modern application development.",
                root, "experience.html") + f'''
<body>
{header("Experience", root)}
<main id="main">

<section class="wh wrap">
<p class="label muted wh__kicker"><span class="dot"></span> Career</p>
<h1 class="wh__title wh__title--long display" data-split>
<span class="line-mask"><span>Professional</span></span>
<span class="line-mask"><span><span class="accent">Experience</span>.</span></span>
</h1>
<p class="ph__tag label" data-reveal style="margin-top:22px;display:inline-block">Building digital experiences, developing web applications, and solving real-world problems through software engineering.</p>
<p class="cb__lead" data-reveal style="margin-top:24px">I'm {ME['name']}, a Full Stack Developer
and Software Engineer focused on modern web development, application functionality, and practical
digital solutions. My experience combines professional product development, technical
problem-solving, and a commitment to continuous learning.</p>
<div class="bth__ctas" data-reveal>
<a href="resume.html" class="btn" data-cursor="hover">View Résumé <span class="arrow" aria-hidden="true">{ARROW}</span></a>
<a href="contact.html#f-name" class="btn" data-cursor="hover">Contact Me <span class="arrow" aria-hidden="true">{ARROW}</span></a>
</div>
</section>

<section class="exp section wrap" id="timeline" aria-labelledby="timeline-title">
<div class="exp__head">
<div>
<p class="label muted exp__kicker"><span class="dot"></span> Career timeline</p>
<h2 id="timeline-title" class="exp__title display" data-split>
<span class="line-mask"><span>Where I've</span></span>
<span class="line-mask"><span><span class="accent">worked</span>.</span></span>
</h2>
</div>
<div class="exp__copy">
<p class="exp__text" data-reveal>Contribute to web development and digital product initiatives,
focusing on responsive interfaces, application functionality, reusable components, and integration
between frontend interfaces and backend services.</p>
</div>
</div>
<ol class="exp__list">{roles}</ol>
</section>

<section class="exp section wrap" id="freelance" aria-labelledby="freelance-title">
<div class="exp__head">
<div>
<p class="label muted exp__kicker"><span class="dot"></span> {FREELANCE['kind']}</p>
<h2 id="freelance-title" class="exp__title display" data-split>
<span class="line-mask"><span>Freelance &amp;</span></span>
<span class="line-mask"><span><span class="accent">independent</span>.</span></span>
</h2>
</div>
<div class="exp__copy">
<p class="exp__text" data-reveal>{FREELANCE['description']}</p>
<p class="muted" data-reveal style="font-size:.95rem">{FREELANCE['note']}</p>
</div>
</div>
<ul class="sk__items" data-reveal>{areas}</ul>
</section>

<section class="sk wrap" id="projects" aria-labelledby="proj-title">
<div class="section-head">
<h2 id="proj-title" class="section-title" data-split>
<span class="line-mask"><span>Selected project experience<span class="accent">.</span></span></span>
</h2>
<a href="work.html" class="label u-link" data-cursor="hover">All projects {ARROW}</a>
</div>
</section>
<section class="grid wrap" aria-label="Selected projects">{cards}</section>

<section class="sk wrap" id="skills" aria-labelledby="skills-title">
<div class="section-head">
<h2 id="skills-title" class="section-title" data-split>
<span class="line-mask"><span>Skills used in my work<span class="accent">.</span></span></span>
</h2>
<a href="skills.html" class="label u-link" data-cursor="hover">Full skill set {ARROW}</a>
</div>
{skills}
</section>

</main>
{footer(root)}
{chrome_end(root)}'''


def page_404():
    root = ""
    return head(f"Not found — {ME['name']}", "That page doesn't exist.", root, "404.html") + f'''
<body>
{header("", root)}
<main id="main">
<section class="nf wrap">
<p class="label muted" style="margin-bottom:24px">Error</p>
<h1 class="nf__code display accent">404</h1>
<p class="cb__lead" style="margin:32px auto 40px">That page doesn't exist — it may have been renamed or never existed at all.</p>
<p><a class="btn" href="index.html" data-cursor="hover">Back home <span class="arrow" aria-hidden="true">{ARROW}</span></a></p>
</section>
</main>
{footer(root)}
{chrome_end(root)}'''


# ============================================================
#  WRITE
# ============================================================
# ============================================================
#  CONTACT PAGE
# ============================================================
CONTACT_INTRO = ("Have a project in mind, an opportunity to discuss, or an idea worth "
                 "exploring? I'd be glad to hear from you. Share a few details below, "
                 "and let's start a conversation.")

CONTACT_AUDIENCE = ("Recruiters, clients, founders and fellow developers are all welcome — "
                    "whether it's a role to fill, a product to build, or a question about "
                    "something on this site.")

# The form's enquiry-type suggestions are generated from the first column, so
# the datalist and this list can never drift apart.
CONTACT_TOPICS = [
    ("01", "Full-time opportunities",
     "Full-stack, frontend or backend engineering roles."),
    ("02", "Freelance development",
     "Websites and web applications, taken from brief to deployment."),
    ("03", "Web application development",
     "React, Next.js and Node.js products with real functionality behind them."),
    ("04", "Technical collaboration",
     "Side projects, open source, or a second pair of hands on a build."),
    ("05", "Other professional enquiries",
     "Anything else worth a conversation."),
]

PRIVACY = [
    ("p", "This site is a personal portfolio. It does not run analytics, advertising or third-party trackers, "
          "and it sets no cookies."),
    ("h2", "What is collected"),
    ("p", "Nothing automatically. If you use the contact form, the details you type — name, email, an "
          "optional subject and your message — are used solely to reply to you."),
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
#  API  (serverless functions in api/, described for discovery)
# ============================================================
API_ERRORS = {
    "name_required": "Name was empty.",
    "email_required": "Email was empty.",
    "message_required": "Message was empty.",
    "email_invalid": "Email is not a valid address.",
    "name_too_long": "Name exceeds 120 characters.",
    "email_too_long": "Email exceeds 254 characters.",
    "subject_too_long": "Subject exceeds 160 characters.",
    "company_too_long": "Company exceeds 160 characters.",
    "message_too_long": "Message exceeds 5000 characters.",
}


def openapi_json():
    base = SITE_URL.rstrip("/")
    return json.dumps({
        "openapi": "3.1.0",
        "info": {
            "title": f"{ME['name']} — Portfolio API",
            "summary": "Contact delivery and health for pradeepmaury.in.",
            "description": (
                "A small API behind the portfolio. `/api/contact` delivers the "
                "contact form; `/api/health` reports whether it can send mail."
            ),
            "version": "1.0.0",
            "contact": {"name": ME["name"], "email": ME["email"], "url": base},
        },
        "servers": [{"url": base, "description": "Production"}],
        "paths": {
            "/api/contact": {
                "post": {
                    "operationId": "sendContactMessage",
                    "summary": "Send a message via the contact form",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/ContactRequest"}
                            },
                            "application/x-www-form-urlencoded": {
                                "schema": {"$ref": "#/components/schemas/ContactRequest"}
                            },
                        },
                    },
                    "responses": {
                        "200": {
                            "description": "Accepted for delivery",
                            "content": {"application/json": {
                                "schema": {"$ref": "#/components/schemas/Ok"}}},
                        },
                        "400": {
                            "description": "Validation failed",
                            "content": {"application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}}},
                        },
                        "405": {"description": "Method not allowed"},
                        "502": {"description": "Upstream mail provider failed"},
                        "503": {"description": "Mail sending is not configured"},
                    },
                }
            },
            "/api/health": {
                "get": {
                    "operationId": "getHealth",
                    "summary": "Liveness and configuration status",
                    "responses": {
                        "200": {
                            "description": "Service is up",
                            "content": {"application/json": {
                                "schema": {"$ref": "#/components/schemas/Health"}}},
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "ContactRequest": {
                    "type": "object",
                    "required": ["name", "email", "message"],
                    "properties": {
                        "name": {"type": "string", "maxLength": 120},
                        "email": {"type": "string", "format": "email", "maxLength": 254},
                        "subject": {"type": "string", "maxLength": 160,
                                    "description": "Optional subject or enquiry type."},
                        "company": {"type": "string", "maxLength": 160},
                        "message": {"type": "string", "maxLength": 5000},
                        "website": {
                            "type": "string",
                            "description":
                                "Honeypot. Leave empty — a non-empty value is "
                                "treated as a bot and silently discarded.",
                        },
                    },
                },
                "Ok": {
                    "type": "object",
                    "properties": {"ok": {"type": "boolean", "const": True}},
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "ok": {"type": "boolean", "const": False},
                        "error": {"type": "string", "enum": sorted(API_ERRORS)},
                    },
                },
                "Health": {
                    "type": "object",
                    "properties": {
                        "status": {"type": "string", "enum": ["ok"]},
                        "contact": {"type": "string", "enum": ["ready", "unconfigured"]},
                        "time": {"type": "string", "format": "date-time"},
                    },
                },
            }
        },
    }, indent=2, ensure_ascii=False) + "\n"


def poppy_json():
    """Personal Agent Protocol discovery — personalagentprotocol.org

    A website-only declaration: `web: {}` with no `auth` block. The spec allows
    this explicitly, and it's the only honest shape here — declaring `agent` or
    `apis` obliges you to publish an `auth.issuer` with matching RFC 8414
    metadata, and there is no authorization server behind this site. The API
    that does exist (POST /api/contact, GET /api/health) is deliberately
    public, so it has no issuer to name.

    `domain` is the registrable domain: the spec matches it against the
    requested hostname ignoring a leading "www", so this covers both
    pradeepmaury.in and www.pradeepmaury.in.
    """
    host = SITE_URL.split("://", 1)[1].rstrip("/")
    return json.dumps({
        "protocol_version": "0.1",
        "organization": {
            "name": ME["name"],
            "domain": host.removeprefix("www."),
            "description": (
                f"Portfolio of {ME['name']}, {ME['role']} in {ME['city']}, India."
            ),
            "contact": ME["email"],
        },
        "web": {},
    }, indent=2, ensure_ascii=False) + "\n"


def ai_catalog():
    """ARD manifest — agenticresourcediscovery.org

    Every entry points at something this site actually serves. Notably absent:
    an MCP server entry. The WebMCP tools in assets/js/webmcp.js run in the
    visitor's browser; there is no hosted MCP endpoint for a registry to call,
    and claiming one would send agents to a URL that doesn't answer.
    """
    base = SITE_URL.rstrip("/")
    # URNs identify the registrable domain, not the serving host, so no "www".
    urn_domain = base.split("://", 1)[1].removeprefix("www.")

    def entry(namespace, name, display, media_type, path, description, queries):
        return {
            "id": f"urn:air:{urn_domain}:{namespace}:{name}",
            "displayName": display,
            "description": description,
            "type": media_type,
            "url": f"{base}{path}",
            "representativeQueries": queries,
        }

    return json.dumps({
        # TODO: confirm against the published spec — see README.
        "specVersion": "0.1",
        "host": {
            "name": ME["name"],
            "url": base + "/",
            "description": (
                f"Portfolio of {ME['name']}, {ME['role']} in {ME['city']}, India. "
                "Projects, résumé and a small contact API."
            ),
            "contact": ME["email"],
        },
        "entries": [
            entry("api", "openapi", "Portfolio API (OpenAPI 3.1)",
                  "application/openapi+json", "/openapi.json",
                  "Machine-readable description of POST /api/contact and "
                  "GET /api/health.",
                  ["How do I send Pradeep Maurya a message programmatically?",
                   "What API endpoints does this site expose?",
                   "Is there an OpenAPI schema for pradeepmaury.in?"]),

            entry("api", "catalog", "API Catalog (RFC 9727)",
                  "application/linkset+json", "/.well-known/api-catalog",
                  "Linkset naming the site's API, its description, docs and "
                  "health endpoint.",
                  ["Where is the API catalog for this domain?",
                   "What services does pradeepmaury.in provide?",
                   "How do I check if this site's API is up?"]),

            entry("content", "llms", "LLM content index",
                  "text/markdown", "/llms.txt",
                  "Curated llmstxt.org index linking every page's markdown "
                  "version.",
                  ["What is on Pradeep Maurya's portfolio?",
                   "Give me an index of this site for an LLM.",
                   "Which pages does pradeepmaury.in have?"]),

            entry("content", "llms-full", "Full site content",
                  "text/markdown", "/llms-full.txt",
                  "Every page of the site inlined as markdown in a single "
                  "document (~5.5k tokens).",
                  ["Summarise Pradeep Maurya's entire portfolio.",
                   "Give me the full text of this website.",
                   "What is Pradeep Maurya's experience and skill set?"]),

            entry("data", "profile", "Structured profile and project data",
                  "application/json", "/agent-data.json",
                  "Projects, skills, work history and contact details as JSON.",
                  ["What projects has Pradeep Maurya built?",
                   "What technologies does Pradeep Maurya work with?",
                   "Who is Pradeep Maurya and where is he based?",
                   "What is Pradeep Maurya's work history?"]),

            entry("content", "sitemap", "Sitemap",
                  "application/xml", "/sitemap.xml",
                  "Every indexable URL on the site.",
                  ["List all pages on pradeepmaury.in.",
                   "Where is the sitemap for this domain?"]),
        ],
    }, indent=2, ensure_ascii=False) + "\n"


def agent_data():
    """Structured site data for the WebMCP tools in assets/js/webmcp.js.

    Fetched lazily the first time a tool runs, so it costs nothing on a normal
    page view. Same source as the HTML, so it can't drift.
    """
    base = SITE_URL.rstrip("/")
    return json.dumps({
        "profile": {
            "name": ME["name"],
            "role": ME["role"],
            "location": ME["region"],
            "email": ME["email"],
            "phone": ME["phone"],
            "github": ME["github"],
            "linkedin": ME["linkedin"],
            "summary": ME["summary"],
        },
        "projects": [{
            "name": p["name"],
            "slug": p["slug"],
            "year": p["year"],
            "category": p["meta"],
            "summary": p["summary"],
            "stack": p["stack"],
            "role": p["role"],
            "url": f"{base}/work/{p['slug']}.html",
            "live": p["link"] or None,
        } for p in PROJECTS],
        "skills": [
            {"group": strip_tags(name), "items": items}
            for _, name, items in SKILL_GROUPS
        ],
        "experience": [{
            "role": strip_tags(e["role"]),
            "org": e["org"],
            "period": e["when"],
            "highlights": [strip_tags(pt) for pt in e["points"]],
        } for e in EXPERIENCE],
        "pages": [
            {"title": t, "url": f"{base}/{h}", "markdown": f"{base}{md_href(h)}"}
            for t, h in [
                ("Home", "index.html"), ("Work", "work.html"),
                ("About", "about.html"), ("Skills", "skills.html"),
                ("Resume", "resume.html"), ("Contact", "contact.html"),
                ("API", "docs/api.html"),
            ]
        ],
    }, indent=2, ensure_ascii=False) + "\n"


def api_catalog():
    """RFC 9727 catalog as an RFC 9264 linkset."""
    base = SITE_URL.rstrip("/")
    return json.dumps({
        "linkset": [{
            "anchor": f"{base}/api",
            "service-desc": [
                {"href": f"{base}/openapi.json", "type": "application/openapi+json"}
            ],
            "service-doc": [
                {"href": f"{base}/docs/api.html", "type": "text/html"}
            ],
            "status": [
                {"href": f"{base}/api/health", "type": "application/json"}
            ],
            "author": [{"href": f"{base}/about.html"}],
        }]
    }, indent=2) + "\n"


# ============================================================
#  LINK RELATIONS  (RFC 8288)
# ============================================================
# Emitted twice from one definition: as <link> elements in every page head,
# and as a single RFC 8288 Link: response header via the server configs below.
#
# Every relation here is in the IANA Link Relations registry and is true of
# this site. api-catalog and service-desc are included now that api/ actually
# exists — before it did, they would have pointed agents at a 404.
SITE_RELS = [
    # (rel, href, extra params) — params are kept as a dict so the HTML
    # attribute form and the RFC 8288 header form can't drift apart.
    ("author", "/about.html", {}),
    ("me", ME["github"], {}),
    ("me", ME["linkedin"], {}),
    ("me", "mailto:" + ME["email"], {}),
    ("privacy-policy", "/privacy.html", {}),
    ("terms-of-service", "/terms.html", {}),
    ("api-catalog", "/.well-known/api-catalog", {"type": "application/linkset+json"}),
    ("service-desc", "/openapi.json", {"type": "application/openapi+json"}),
    ("service-doc", "/docs/api.html", {"type": "text/html"}),
]


def link_header():
    """One Link header carrying every link-value, comma-separated.

    RFC 8288 §3 allows multiple link-values in a single field, which is safer
    across servers than repeating the header name.
    """
    values = []
    for rel, href, params in SITE_RELS:
        value = f'<{href}>; rel="{rel}"'
        for key, val in params.items():
            value += f'; {key}="{val}"'
        values.append(value)
    return ", ".join(values)


def md_alternate(path):
    """<link rel=alternate> for the markdown twin, or nothing if there isn't one."""
    href = md_href(path)
    if not href:
        return ""
    return (f'<link rel="alternate" type="text/markdown" href="{href}" '
            f'title="Markdown for agents">\n')


def head_links(root):
    """The same relations as <link> elements, for hosts that can't set headers
    (GitHub Pages) and for agents that only parse HTML."""
    out = ""
    for rel, href, params in SITE_RELS:
        # Site-local targets go through {root} so project pages resolve too.
        target = root + href.lstrip("/") if href.startswith("/") else href
        attrs = "".join(f' {k}="{v}"' for k, v in params.items())
        out += f'<link rel="{rel}" href="{target}"{attrs}>\n'
    return out


# An error page has no agent-readable form, so it gets no markdown twin —
# and must not advertise one either.
NO_MARKDOWN = {"404.html"}


def md_href(path):
    """Root-relative URL of a page's markdown twin, or None if it has none."""
    if path in NO_MARKDOWN:
        return None
    return "/" + path[:-len(".html")] + ".md"


def headers_file(md_paths):
    """Netlify / Cloudflare Pages `_headers`."""
    out = [
        "# RFC 8288 Link relations for agent discovery.",
        "# Netlify and Cloudflare Pages read this file; see README for Apache,",
        "# nginx and Vercel equivalents.",
        "/*",
        f"  Link: {link_header()}",
        "",
        "# Markdown twins, so an agent can find the text-only form of a page.",
    ]
    for path in md_paths:
        rule = f'  Link: <{md_href(path)}>; rel="alternate"; type="text/markdown"'
        # The homepage is reached as "/", which does not match an
        # "/index.html" rule — emit both or the home page, the one scanners
        # actually test, silently misses its alternate link.
        if path == "index.html":
            out += ["/", rule]
        out += ["/" + path, rule]
    out += [
        "",
        "/*.md",
        "  Content-Type: text/markdown; charset=utf-8",
        "",
        "# llmstxt.org files are markdown-formatted but .txt by convention.",
        "# charset is explicit — the content has em dashes and accents.",
        "/llms.txt",
        "  Content-Type: text/plain; charset=utf-8",
        "/llms-full.txt",
        "  Content-Type: text/plain; charset=utf-8",
        "",
        "# RFC 9727 / RFC 9264 discovery documents.",
        "/.well-known/api-catalog",
        "  Content-Type: application/linkset+json",
        "/.well-known/ai-catalog.json",
        "  Content-Type: application/json",
        "  Access-Control-Allow-Origin: *",
        "/.well-known/poppy.json",
        "  Content-Type: application/json",
        "  Access-Control-Allow-Origin: *",
        "/agent-data.json",
        "  Access-Control-Allow-Origin: *",
        "/openapi.json",
        "  Content-Type: application/openapi+json",
    ]
    return "\n".join(out) + "\n"


def vercel_json(md_paths):
    """Vercel reads neither `_headers` (Netlify/CF Pages) nor `.htaccess`
    (Apache) — without this file the site ships no Link headers at all.

    Each page gets ONE complete Link value rather than relying on Vercel
    merging a site-wide rule with a per-page one, since same-key headers from
    overlapping rules override rather than append.
    """
    rules = [{
        "source": "/(.*)",
        "headers": [
            {"key": "Link", "value": link_header()},
            {"key": "Vary", "value": "Accept"},
        ],
    }]
    for path in md_paths:
        combined = f'{link_header()}, <{md_href(path)}>; rel="alternate"; type="text/markdown"'
        sources = ["/"] if path == "index.html" else []
        sources.append("/" + path)
        for source in sources:
            rules.append({
                "source": source,
                "headers": [
                    {"key": "Link", "value": combined},
                    {"key": "Vary", "value": "Accept"},
                ],
            })
    rules += [
        {"source": "/(.*).md",
         "headers": [{"key": "Content-Type", "value": "text/markdown; charset=utf-8"}]},
        {"source": "/llms.txt",
         "headers": [{"key": "Content-Type", "value": "text/plain; charset=utf-8"}]},
        {"source": "/llms-full.txt",
         "headers": [{"key": "Content-Type", "value": "text/plain; charset=utf-8"}]},
        {"source": "/.well-known/api-catalog",
         "headers": [{"key": "Content-Type", "value": "application/linkset+json"}]},
        {"source": "/.well-known/poppy.json",
         "headers": [
             {"key": "Content-Type", "value": "application/json"},
             {"key": "Access-Control-Allow-Origin", "value": "*"},
         ]},
        {"source": "/.well-known/ai-catalog.json",
         "headers": [
             {"key": "Content-Type", "value": "application/json"},
             {"key": "Access-Control-Allow-Origin", "value": "*"},
         ]},
        {"source": "/agent-data.json",
         "headers": [{"key": "Access-Control-Allow-Origin", "value": "*"}]},
        {"source": "/openapi.json",
         "headers": [{"key": "Content-Type", "value": "application/openapi+json"}]},
    ]

    # Accept-based rewrites, one explicit entry per page.
    #
    # A single wildcard like "/:path*.html" -> "/:path*.md" reads tidier, but
    # path-to-regexp's segment modifiers make that pattern ambiguous against
    # nested paths such as /work/bakery.html, and Vercel's router can't be
    # tested locally. There are only 13 pages and this file is generated, so
    # spelling them out costs nothing and removes the guesswork.
    #
    # Vercel's `has` matches a regex against the header, so it can't compare
    # q-values the way the Worker does — a client sending
    # `text/markdown;q=0.1` would still get markdown. Browsers never send
    # text/markdown at all, so HTML stays the default where it matters.
    md_accept = [{"type": "header", "key": "accept", "value": "(.*)text/markdown(.*)"}]
    rewrites = [{"source": "/", "has": md_accept, "destination": "/index.md"}]
    for path in md_paths:
        rewrites.append({
            "source": "/" + path,
            "has": md_accept,
            "destination": md_href(path),
        })

    return json.dumps({
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "headers": rules,
        "rewrites": rewrites,
    }, indent=2) + "\n"


def htaccess_file():
    """Apache: the Link header, plus Accept-based content negotiation so
    `Accept: text/markdown` gets the .md twin while browsers still get HTML."""
    value = link_header().replace('"', '\\"')
    return "\n".join([
        "# RFC 8288 Link relations for agent discovery.",
        "<IfModule mod_headers.c>",
        f'  Header always set Link "{value}"',
        "</IfModule>",
        "",
        "# Markdown for agents: serve page.md when the client asks for",
        "# markdown and that twin exists. HTML stays the default.",
        "AddType text/markdown .md",
        "",
        "# llms.txt / llms-full.txt carry em dashes and accents — be explicit",
        "# about UTF-8 so they aren't decoded as latin-1.",
        "AddDefaultCharset UTF-8",
        '<FilesMatch "^llms(-full)?\\.txt$">',
        "  ForceType 'text/plain; charset=utf-8'",
        "</FilesMatch>",
        "<IfModule mod_rewrite.c>",
        "  RewriteEngine On",
        "",
        "  # /path.html -> /path.md",
        "  RewriteCond %{HTTP:Accept} text/markdown [NC]",
        "  RewriteCond %{DOCUMENT_ROOT}/$1.md -f",
        "  RewriteRule ^(.+)\\.html$ /$1.md [L]",
        "",
        "  # bare directory root -> /index.md",
        "  RewriteCond %{HTTP:Accept} text/markdown [NC]",
        "  RewriteCond %{DOCUMENT_ROOT}/index.md -f",
        "  RewriteRule ^$ /index.md [L]",
        "</IfModule>",
        "",
        "<IfModule mod_headers.c>",
        "  # Caches must key on Accept, or a markdown response could be",
        "  # replayed to a browser.",
        '  <FilesMatch "\\.(html|md)$">',
        "    Header append Vary Accept",
        "  </FilesMatch>",
        "</IfModule>",
    ]) + "\n"


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
    "experience.html": "0.8",
    "resume.html": "0.8",
    "skills.html": "0.8",
    "contact.html": "0.8",
    "docs/api.html": "0.4",
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


# Content Signals (contentsignals.org, draft-romm-aipref-contentsignals).
# A preference expressed in robots.txt, not an enforcement mechanism — it
# tells well-behaved crawlers what you want, and nothing more.
#
#   search    appearing in search results and the links/snippets around them
#   ai-input  using the page to ground an AI answer (RAG, assistants)
#   ai-train  using the page as training data for a model
#
# Chosen for a portfolio whose whole job is being found:
#   search=yes    — the obvious one
#   ai-input=yes  — this site ships llms.txt and serves markdown on
#                   `Accept: text/markdown` precisely so assistants can read
#                   it. Saying no here would contradict all of that, and an
#                   assistant answering "full stack developers in Dehradun"
#                   is exactly the discovery this site exists for.
#   ai-train=no   — no reciprocal benefit, so withheld.
CONTENT_SIGNALS = {
    "search": "yes",
    "ai-input": "yes",
    "ai-train": "no",
}


def robots():
    signals = ", ".join(f"{k}={v}" for k, v in CONTENT_SIGNALS.items())
    return "\n".join([
        "# Content Signals express how this site's operator prefers its",
        "# content to be used. They are preferences, not access controls.",
        "# See https://contentsignals.org/",
        "#",
        "# search=yes    indexing and search results are welcome",
        "# ai-input=yes  grounding AI answers in this content is welcome",
        "# ai-train=no   training models on this content is not permitted",
        "#",
        f"# Questions or licensing requests: {ME['email']}",
        "",
        "User-agent: *",
        f"Content-Signal: {signals}",
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


# ============================================================
#  MARKDOWN FOR AGENTS
# ============================================================
# Built from the same data as the HTML rather than converted from it — the
# conversion route drags in nav, footer and decorative markup, which is
# exactly the noise an agent is trying to avoid.


def _md_head(title, path, description):
    return [f"# {title}", "", description, "",
            f"Canonical: {site_url(path)}", "", "---", ""]


def _md_projects(slugs=None, heading="Selected work"):
    """All projects, or just `slugs` (in PROJECTS order) when given."""
    picks = PROJECTS if slugs is None else [p for p in PROJECTS if p["slug"] in slugs]
    out = [f"## {heading}", ""]
    for i, p in enumerate(picks, 1):
        out.append(f"{i}. **{p['name']}** — {p['meta']} ({p['year']})")
        out.append(f"   {p['summary']}")
        out.append(f"   Stack: {p['stack']}")
        if p["link"]:
            out.append(f"   Live: {p['link']}")
        out.append(f"   Detail: {site_url('work/' + p['slug'] + '.html')}")
        out.append("")
    return out


def _md_experience():
    out = ["## Experience", ""]
    for e in EXPERIENCE:
        line = f"### {strip_tags(e['role'])} — {e['org']}"
        if e.get("managed_by"):
            line += f" (managed by {e['managed_by']})"
        out += [line, f"*{e['when']}*", ""]
        out += [f"- {strip_tags(pt)}" for pt in e["points"]]
        if e.get("tech"):
            out += ["", f"Technologies: {', '.join(e['tech'])}"]
        out += [""]
    return out


def _md_skills():
    out = ["## Technical skills", ""]
    for _, name, items in SKILL_GROUPS:
        out.append(f"- **{strip_tags(name)}**: {', '.join(items)}")
    return out + [""]


def _md_credentials():
    out = ["## Certifications & education", ""]
    for title, focus, issuer, year, _kind in CREDENTIALS:
        detail = ", ".join(x for x in (issuer, year) if x)
        out.append(f"- **{strip_tags(title)}** — {strip_tags(focus)}"
                   + (f" ({detail})" if detail else ""))
    return out + [""]


def _md_contact():
    out = ["## Contact", "",
           f"- Email: {ME['email']}",
           f"- Phone: {ME['phone']}",
           f"- Location: {ME['region']}"]
    for name, url in SOCIALS:
        if not url.startswith("mailto"):
            out.append(f"- {name}: {url}")
    return out + [""]


def _md_doc(blocks):
    out = []
    for kind, text in blocks:
        if kind == "h2":
            out += [f"## {strip_tags(text)}", ""]
        elif kind == "ul":
            out += [f"- {strip_tags(i)}" for i in text] + [""]
        else:
            out += [strip_tags(text), ""]
    return out


def markdown_page(path):
    """Markdown twin of a built page, or None if that page has no useful
    text-only form (404)."""
    name = f"{ME['name']}"
    if path == "index.html":
        body = _md_head(f"{name} — {ME['role']}", path, ME["tagline"])
        body += ["## About", "", ME["summary"], ""]
        body += ["## At a glance", ""]
        body += [f"- {label}: {value}" for label, value in STATS] + [""]
        body += _md_projects()
        body += ["## How I can help", ""]
        body += [f"- **{strip_tags(t)}**: {strip_tags(d)}" for _, t, d in CAPABILITIES] + [""]
        body += _md_credentials() + _md_contact()
        return "\n".join(body)

    if path == "work.html":
        return "\n".join(_md_head(f"Work — {name}", path,
                                  f"Projects by {name}.") + _md_projects())

    if path == "about.html":
        body = _md_head(f"About — {name}", path, ME["tagline"])
        body += [ME["summary"], "", f"Based in {ME['region']}.", ""]
        body += _md_experience() + _md_credentials() + _md_contact()
        return "\n".join(body)

    if path == "skills.html":
        return "\n".join(_md_head(f"Skills — {name}", path,
                                  "What I work with, grouped by stack layer.")
                         + _md_skills())

    if path == "resume.html":
        body = _md_head(f"{name} | Full Stack Developer Resume", path,
                        "Full Stack Developer | Software Engineer — " + RESUME_TAGLINE)
        body += ["## Summary", ""] + [p for pair in
                                      ((p, "") for p in RESUME_SUMMARY) for p in pair]
        body += ["## Technical Skills", ""]
        body += [f"- **{strip_tags(h)}**: {', '.join(i)}" for h, i in RESUME_SKILLS]
        body.append("")
        body += _md_experience()
        body += ["## Freelance & Independent Development", "", RESUME_FREELANCE, "",
                 FREELANCE["note"], ""]
        body += [f"- {a}" for a in RESUME_FREELANCE_AREAS] + [""]
        body += _md_projects(RESUME_PROJECT_SLUGS, "Projects")
        body += _md_credentials() + _md_contact()
        return "\n".join(body)

    if path == "contact.html":
        body = _md_head(f"Contact {name} | {ME['role']}", path, CONTACT_INTRO)
        body += _md_contact()
        body += ["## What can we discuss?", ""]
        body += [f"- **{t}** — {d}" for _, t, d in CONTACT_TOPICS]
        body += ["",
                 "Send a message with `POST /api/contact` "
                 "(fields: name, email, subject, message) or email the address above.",
                 ""]
        return "\n".join(body)

    if path in ("privacy.html", "terms.html"):
        label = "Privacy" if path == "privacy.html" else "Terms"
        blocks = PRIVACY if path == "privacy.html" else TERMS
        return "\n".join(_md_head(f"{label} — {name}", path,
                                  f"{label} for {name}'s portfolio.") + _md_doc(blocks))

    if path == "experience.html":
        body = _md_head(f"Professional Experience — {name}", path,
                        "Career timeline, freelance work, projects and skills.")
        body += _md_experience()
        body += [f"## {strip_tags(FREELANCE['title'])}", "",
                 f"*{FREELANCE['kind']}*", "", FREELANCE["description"], "",
                 FREELANCE["note"], ""]
        body += [f"- {a}" for a in FREELANCE["areas"]] + [""]
        body += _md_projects()
        body += ["## Skills used", ""]
        body += [f"- **{strip_tags(n)}**: {', '.join(i)}" for _, n, i in EXPERIENCE_SKILLS]
        body.append("")
        return "\n".join(body)

    if path == "docs/api.html":
        base = SITE_URL.rstrip("/")
        body = _md_head(f"API — {name}", path,
                        "HTTP API behind the portfolio: contact delivery and health.")
        body += [
            f"Machine-readable: [openapi.json]({base}/openapi.json) · "
            f"catalog: [/.well-known/api-catalog]({base}/.well-known/api-catalog)",
            "",
            "## POST /api/contact", "",
            "Delivers the contact form. Accepts JSON or form-encoded bodies.", "",
            "| Field | Type | Notes |",
            "| --- | --- | --- |",
            "| name | string | required, max 120 |",
            "| email | string | required, max 254 — used as the reply-to address |",
            "| subject | string | optional, max 160 — becomes the mail subject |",
            "| company | string | optional, max 160 |",
            "| message | string | required, max 5000 |",
            "| website | string | honeypot — leave empty |",
            "",
            "```sh",
            f"curl -X POST {base}/api/contact \\",
            "  -H 'Content-Type: application/json' \\",
            '  -d \'{"name":"Jane","email":"jane@example.com","message":"Hello"}\'',
            "```",
            "",
            "Returns `{\"ok\":true}` on success. `400` with an error code on "
            "validation failure, `502` if the mail provider rejects it, `503` "
            "if sending is not configured.", "",
            "## GET /api/health", "",
            "Liveness and configuration status — the `status` relation in the "
            "API catalog.", "",
            "```json",
            '{"status":"ok","contact":"ready","time":"…"}',
            "```", "",
            "## Error codes", "",
        ]
        body += [f"- `{code}` — {text}" for code, text in sorted(API_ERRORS.items())]
        body.append("")
        return "\n".join(body)

    if path.startswith("work/"):
        slug = path[len("work/"):-len(".html")]
        p = next(x for x in PROJECTS if x["slug"] == slug)
        body = _md_head(f"{p['name']} — {name}", path, p["summary"])
        body += [p["lead"], ""] + [par + "\n" for par in p["body"]]
        body += ["## Details", "",
                 f"- Role: {p['role']}",
                 f"- Context: {p['org']}",
                 f"- Year: {p['year']}",
                 f"- Stack: {p['stack']}",
                 f"- Scope: {p['scope']}"]
        if p["link"]:
            body.append(f"- Live: {p['link']}")
        body.append("")
        for h, t in p["notes"]:
            body += [f"### {strip_tags(h)}", "", strip_tags(t), ""]
        return "\n".join(body)

    return None   # 404 has no agent-readable form


# ============================================================
#  llms.txt  (llmstxt.org)
# ============================================================
# A curated index for language models: H1, a blockquote summary, then H2
# sections of links. Everything it points at is the markdown twin, not the
# HTML, so a model following a link gets clean text with no second hop.
# Anything under "## Optional" may be skipped when context is tight.


def _md_link(label, path, note):
    # Build from md_href, not site_url — site_url("index.html") is the bare
    # root, and trimming ".html" off that mangles the domain.
    return f"- [{label}]({SITE_URL.rstrip('/')}{md_href(path)}): {note}"


def llms_txt():
    out = [
        f"# {ME['name']}",
        "",
        # The tagline already opens with the role, so don't restate it.
        f"> {ME['tagline']} Based in {ME['city']}, India.",
        "",
        "Portfolio site. Every page has a markdown twin at the same path with a",
        "`.md` extension — the links below point straight at those. The site also",
        "returns markdown to any request sending `Accept: text/markdown`.",
        "",
        "## Core",
        "",
        _md_link("Home", "index.html",
                 "overview — stats, selected work, capabilities, credentials"),
        _md_link("About", "about.html",
                 "background, full work history, certifications and education"),
        _md_link("Résumé", "resume.html",
                 "complete CV — summary, experience, projects, skills, credentials"),
        _md_link("Skills", "skills.html",
                 "technical skills grouped by where they sit in the stack"),
        _md_link("Contact", "contact.html", "email, phone, location, profiles"),
        "",
        "## Projects",
        "",
    ]
    for p in PROJECTS:
        note = f"{p['summary']} Stack: {p['stack']}. ({p['year']})"
        out.append(_md_link(p["name"], f"work/{p['slug']}.html", note))
    out += [
        "",
        "## Optional",
        "",
        _md_link("Work index", "work.html", "the project list on its own"),
        _md_link("Privacy", "privacy.html", "what the site does and doesn't collect"),
        _md_link("Terms", "terms.html", "terms of use"),
        "",
    ]
    return "\n".join(out)


def llms_full_txt(md_pages):
    """Every markdown twin inlined, so a model can take the whole site in one
    fetch instead of crawling the index."""
    order = ["index.md", "about.md", "resume.md", "skills.md", "work.md"]
    order += [f"work/{p['slug']}.md" for p in PROJECTS]
    order += ["contact.md", "privacy.md", "terms.md"]

    out = [f"# {ME['name']} — complete site content", "",
           f"> {ME['tagline']}", "",
           f"Generated {datetime.date.today().isoformat()} from {SITE_URL}.",
           "Each section below is one page of the site.", ""]
    for path in order:
        if path in md_pages:
            out += ["---", "", md_pages[path].rstrip(), ""]
    return "\n".join(out) + "\n"


def strip_tags(text):
    """Data blocks carry a few HTML entities and inline tags for the web
    output; markdown wants them plain."""
    text = re.sub(r"<[^>]+>", "", text)
    return (text.replace("&amp;", "&").replace("&mdash;", "—")
                .replace("&ldquo;", "“").replace("&rdquo;", "”")
                .replace("&nbsp;", " "))


def main():
    pages = {
        "index.html": page_index(),
        "work.html": page_work(),
        "about.html": page_about(),
        "skills.html": page_skills(),
        "resume.html": page_resume(),
        "contact.html": page_contact(),
        "experience.html": page_experience(),
        "privacy.html": page_doc("Privacy", "privacy", PRIVACY),
        "terms.html": page_doc("Terms", "terms", TERMS),
        "docs/api.html": page_api_docs(),
        "404.html": page_404(),
    }
    for i, p in enumerate(PROJECTS):
        pages[f"work/{p['slug']}.html"] = page_project(p, i)

    (ROOT / "work").mkdir(exist_ok=True)
    (ROOT / "docs").mkdir(exist_ok=True)
    (ROOT / ".well-known").mkdir(exist_ok=True)
    md_pages = {}
    for path in pages:
        md = markdown_page(path)
        if md:
            md_pages[path[:-len(".html")] + ".md"] = md.rstrip() + "\n"

    for path, html in pages.items():
        target = ROOT / path
        target.write_text(html, encoding="utf-8")
        print(f"  {path:<34} {len(html):>7,} bytes")
    for path, text in md_pages.items():
        (ROOT / path).write_text(text, encoding="utf-8")
    md_html = [k[:-len(".md")] + ".html" for k in md_pages]
    print(f"  {len(md_pages)} markdown twins (*.md) for agent requests")

    today = datetime.date.today().isoformat()
    extras = {
        "sitemap.xml": sitemap(pages.keys(), today),
        "robots.txt": robots(),
        "site.webmanifest": webmanifest(),
        "openapi.json": openapi_json(),
        "agent-data.json": agent_data(),
        ".well-known/ai-catalog.json": ai_catalog(),
        ".well-known/poppy.json": poppy_json(),
        ".well-known/api-catalog": api_catalog(),
        "llms.txt": llms_txt(),
        "llms-full.txt": llms_full_txt(md_pages),
        "_headers": headers_file(sorted(md_html)),
        "vercel.json": vercel_json(sorted(md_html)),
        ".htaccess": htaccess_file(),
    }
    for path, text in extras.items():
        (ROOT / path).write_text(text, encoding="utf-8")
        print(f"  {path:<34} {len(text):>7,} bytes")

    listed = len(pages) - len(SITEMAP_EXCLUDE & set(pages))
    print(f"\n{len(pages)} pages written to {ROOT}")
    print(f"{listed} URLs in sitemap.xml  ·  base {SITE_URL}")


if __name__ == "__main__":
    main()
