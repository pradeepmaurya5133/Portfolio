/**
 * GET /api/health — liveness probe.
 *
 * Referenced as the `status` relation in /.well-known/api-catalog (RFC 9727),
 * so an agent can check the API is up before trying to use it.
 */
export default function handler(req, res) {
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.setHeader("Allow", "GET, HEAD");
    return res.status(405).json({ status: "error", error: "method_not_allowed" });
  }

  res.setHeader("Cache-Control", "no-store");
  return res.status(200).json({
    status: "ok",
    // Whether the contact endpoint can actually send mail. Reported so a
    // monitor sees a misconfigured deploy instead of a false green.
    contact: process.env.RESEND_API_KEY ? "ready" : "unconfigured",
    time: new Date().toISOString(),
  });
}
