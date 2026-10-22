# Movie Scraper — Pradeep Maurya

A Django app that pulls movie data from several sources and refuses to trust any of them.

Canonical: https://www.pradeepmaury.in/work/movie-scraper.html

---

Developed a Django-based application with data validation and checks to support reliable data flow from multiple sources.

Scraping is the easy half. The moment data arrives from more than one source, the interesting problem becomes disagreement: missing fields, different formats for the same value, and records that are confidently wrong. The application is built around that — validation and checks sit between collection and storage, so bad records are caught at the boundary.

Working on it changed how I think about ingestion generally. A pipeline without validation is not a pipeline, it is a way to move someone else's errors into your own database.

## Details

- Role: Developer
- Context: Self-directed
- Year: 2025
- Stack: Python, Django, data validation
- Scope: Django application with validation and checks for reliable multi-source data flow

### Validate at the boundary

Checks run before anything is stored, which keeps the database trustworthy instead of requiring cleanup passes later.

### Multiple sources, one shape

Normalising differing source formats into a single schema is what makes the collected data actually usable.
