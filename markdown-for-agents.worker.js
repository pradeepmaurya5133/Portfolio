/**
 * Markdown for Agents — edge content negotiation.
 *
 * If you host behind Cloudflare, you do NOT need this: turn on
 * Rules -> Settings -> "Markdown for Agents" in the dashboard and Cloudflare
 * converts HTML to markdown for you. This Worker is for everything else —
 * Cloudflare Workers Sites, Netlify Edge Functions, Vercel Middleware — where
 * you want the same behaviour from the pre-built .md twins that build.py
 * generates.
 *
 * Behaviour: a request whose Accept header prefers text/markdown is served the
 * matching .md file; everything else gets the HTML untouched. Vary: Accept is
 * set on both so caches don't replay a markdown body to a browser.
 */

const MD_TYPE = "text/markdown; charset=utf-8";

/** Does this client actually prefer markdown over HTML? */
function wantsMarkdown(accept) {
  if (!accept) return false;

  // Parse "type;q=value" pairs and compare the two q-values. A bare
  // `Accept: text/markdown` wins; `*/*` or an HTML-first browser string
  // does not, which is what keeps HTML the default.
  let md = -1;
  let html = -1;
  for (const part of accept.split(",")) {
    const [raw, ...params] = part.trim().split(";");
    const type = raw.trim().toLowerCase();
    let q = 1;
    for (const p of params) {
      const m = /^\s*q=([0-9.]+)\s*$/i.exec(p);
      if (m) q = parseFloat(m[1]);
    }
    if (type === "text/markdown" || type === "text/x-markdown") md = Math.max(md, q);
    if (type === "text/html") html = Math.max(html, q);
  }
  return md > 0 && md >= html;
}

/** /about.html -> /about.md, / -> /index.md */
function markdownPath(pathname) {
  if (pathname.endsWith("/")) return pathname + "index.md";
  if (pathname.endsWith(".html")) return pathname.slice(0, -5) + ".md";
  return null;
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const mdPath = markdownPath(url.pathname);

    if (mdPath && wantsMarkdown(request.headers.get("Accept"))) {
      const mdURL = new URL(url);
      mdURL.pathname = mdPath;
      const md = await fetch(new Request(mdURL, request));

      if (md.ok) {
        const headers = new Headers(md.headers);
        headers.set("Content-Type", MD_TYPE);
        headers.set("Vary", "Accept");
        headers.set("Link", `<${url.pathname}>; rel="canonical"`);
        return new Response(md.body, { status: 200, headers });
      }
      // No twin for this page — fall through to the HTML.
    }

    const res = await fetch(request);
    const headers = new Headers(res.headers);
    headers.append("Vary", "Accept");
    return new Response(res.body, {
      status: res.status,
      statusText: res.statusText,
      headers,
    });
  },
};
