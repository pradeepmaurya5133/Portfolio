# Bakery — Pradeep Maurya

A complete bakery shop — storefront, cart and secure accounts, built end to end.

Canonical: https://www.pradeepmaury.in/work/bakery.html

---

Built a full-stack bakery shop application using Next.js, Express.js, PostgreSQL, Prisma, Redux Toolkit and JWT authentication, with secure user management and REST APIs.

This is the project where the whole stack was mine. Next.js on the front, Express and PostgreSQL behind it, Prisma handling the schema and queries, Redux Toolkit holding client state, and JWT for authentication — so every decision, from the data model up to the cart interaction, had to actually connect to the next one.

Building it end to end is what made the API boundary real. Designing the REST endpoints and then being the one to consume them teaches you quickly which responses are convenient and which only looked tidy on paper.

## Details

- Role: Full-stack developer (personal project)
- Context: Self-directed
- Year: 2025
- Stack: Next.js, Express.js, PostgreSQL, Prisma, Redux Toolkit, JWT
- Scope: Full-stack build: storefront, cart, secure user management, REST APIs

### Secure by default

JWT authentication with protected routes and server-side validation, so account and order data is never guarded by the UI alone.

### One schema, one source of truth

Prisma over PostgreSQL kept the data model explicit and migrations reviewable instead of improvised.
