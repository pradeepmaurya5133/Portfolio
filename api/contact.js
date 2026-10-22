/**
 * POST /api/contact — delivers the contact form.
 *
 * Accepts JSON or form-encoded bodies and sends the message on via Resend.
 * Described by /openapi.json and listed in /.well-known/api-catalog.
 *
 * Environment (Vercel → Project → Settings → Environment Variables):
 *   RESEND_API_KEY  required — https://resend.com, free tier is ample here
 *   CONTACT_TO      where mail is delivered   (default: the address below)
 *   CONTACT_FROM    verified sender in Resend (default: Resend's test sender)
 *
 * Without RESEND_API_KEY this returns 503 rather than pretending to succeed;
 * the front end then falls back to opening the visitor's mail client, so the
 * form still works while the key is missing.
 */

const DEFAULT_TO = "pradeepmaurya2002@gmail.com";
// Resend only accepts a `from` on a domain you've verified. Until
// pradeepmaury.in is verified there, its shared test sender is the fallback.
const DEFAULT_FROM = "Portfolio <onboarding@resend.dev>";

const LIMITS = { name: 120, email: 254, company: 160, message: 5000 };

function readBody(req) {
  // Vercel parses JSON and form bodies for us, but be defensive about a raw
  // string body (some clients send JSON without the right content type).
  let body = req.body;
  if (typeof body === "string") {
    try {
      body = JSON.parse(body);
    } catch {
      body = Object.fromEntries(new URLSearchParams(body));
    }
  }
  return body && typeof body === "object" ? body : {};
}

function validate(data) {
  const clean = {};
  for (const [field, max] of Object.entries(LIMITS)) {
    const value = typeof data[field] === "string" ? data[field].trim() : "";
    if (value.length > max) {
      return { error: `${field}_too_long` };
    }
    clean[field] = value;
  }

  if (!clean.name) return { error: "name_required" };
  if (!clean.email) return { error: "email_required" };
  if (!clean.message) return { error: "message_required" };

  // Deliberately loose — the only thing worth rejecting here is something
  // that clearly isn't an address. Resend does the real validation.
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clean.email)) {
    return { error: "email_invalid" };
  }

  return { data: clean };
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const body = readBody(req);

  // Honeypot: a field hidden from humans. Anything that fills it is a bot.
  // Answer 200 so the bot can't tell it was caught.
  if (typeof body.website === "string" && body.website.trim() !== "") {
    return res.status(200).json({ ok: true });
  }

  const { data, error } = validate(body);
  if (error) {
    return res.status(400).json({ ok: false, error });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    // Not the visitor's fault, and the front end has a fallback for this.
    return res.status(503).json({ ok: false, error: "email_not_configured" });
  }

  const lines = [
    `Name:    ${data.name}`,
    `Email:   ${data.email}`,
    data.company ? `Company: ${data.company}` : null,
    "",
    data.message,
  ].filter((l) => l !== null);

  try {
    const sent = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: process.env.CONTACT_FROM || DEFAULT_FROM,
        to: [process.env.CONTACT_TO || DEFAULT_TO],
        // reply_to means hitting reply in the inbox answers the sender,
        // not the no-reply address the mail was sent from.
        reply_to: data.email,
        subject: `Portfolio enquiry — ${data.name}`,
        text: lines.join("\n"),
      }),
    });

    if (!sent.ok) {
      // Log the provider's reason, but don't hand it to the client — it can
      // contain account detail that isn't the visitor's business.
      console.error("resend failed", sent.status, await sent.text());
      return res.status(502).json({ ok: false, error: "delivery_failed" });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error("contact handler threw", err);
    return res.status(502).json({ ok: false, error: "delivery_failed" });
  }
}
