# API — Pradeep Maurya

HTTP API behind the portfolio: contact delivery and health.

Canonical: https://www.pradeepmaury.in/docs/api.html

---

Machine-readable: [openapi.json](https://www.pradeepmaury.in/openapi.json) · catalog: [/.well-known/api-catalog](https://www.pradeepmaury.in/.well-known/api-catalog)

## POST /api/contact

Delivers the contact form. Accepts JSON or form-encoded bodies.

| Field | Type | Notes |
| --- | --- | --- |
| name | string | required, max 120 |
| email | string | required, max 254 — used as the reply-to address |
| company | string | optional, max 160 |
| message | string | required, max 5000 |
| website | string | honeypot — leave empty |

```sh
curl -X POST https://www.pradeepmaury.in/api/contact \
  -H 'Content-Type: application/json' \
  -d '{"name":"Jane","email":"jane@example.com","message":"Hello"}'
```

Returns `{"ok":true}` on success. `400` with an error code on validation failure, `502` if the mail provider rejects it, `503` if sending is not configured.

## GET /api/health

Liveness and configuration status — the `status` relation in the API catalog.

```json
{"status":"ok","contact":"ready","time":"…"}
```

## Error codes

- `company_too_long` — Company exceeds 160 characters.
- `email_invalid` — Email is not a valid address.
- `email_required` — Email was empty.
- `email_too_long` — Email exceeds 254 characters.
- `message_required` — Message was empty.
- `message_too_long` — Message exceeds 5000 characters.
- `name_required` — Name was empty.
- `name_too_long` — Name exceeds 120 characters.
