# Xamlysis — Pradeep Maurya

An online examination portal — the kind of app where a bug has a deadline attached.

Canonical: https://www.pradeepmaury.in/work/xamlysis.html

---

Worked on an online examination portal, supporting core features such as authentication and exam creation, alongside testing and stability improvements.

Exam software has an unusual failure cost: a defect does not merely annoy someone, it interrupts a timed assessment that cannot simply be retaken. That shaped how I worked on it — authentication and exam creation were built with the unhappy paths treated as first-class, not as edge cases to handle later.

A large share of my contribution was testing and stability: exercising flows the way a stressed user would, reproducing intermittent issues, and closing them properly rather than papering over the symptom.

## Details

- Role: Developer / QA support
- Context: Project work
- Year: 2025
- Stack: JavaScript, Node.js, REST APIs, manual & API testing
- Scope: Core features including authentication and exam creation, plus testing and stability work

### Auth before features

Role-correct access to exam creation and exam taking was the foundation everything else sat on.

### Stability as the deliverable

On a portal under time pressure, "it reliably works" is the feature users actually notice.
