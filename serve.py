#!/usr/bin/env python3
"""Local dev server that behaves like the deployed site.

    python serve.py            # http://localhost:8000
    python serve.py 8080

`python -m http.server` serves the files but ignores `_headers` and
`.htaccess`, so locally the site has no Link headers and no markdown
negotiation — which makes it look broken to any agent-readiness scanner even
though the deployed config is fine. This applies both:

  * the `/*` and per-path blocks from `_headers`
  * `Accept: text/markdown` -> the page's .md twin, with Vary: Accept

Production still uses the real host config (`_headers` on Netlify/Cloudflare
Pages, `.htaccess` on Apache, the Worker elsewhere). This only exists so you
can see and test that behaviour before deploying.
"""
import http.server
import io
import os
import pathlib
import re
import socketserver
import sys

ROOT = pathlib.Path(__file__).parent
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


def load_headers():
    """Parse `_headers` into {path_pattern: [(name, value), ...]}."""
    rules, block = {}, None
    path = ROOT / "_headers"
    if not path.exists():
        return rules
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if not raw.startswith((" ", "\t")):
            block = raw.strip()
            rules.setdefault(block, [])
            continue
        if block:
            name, _, value = raw.strip().partition(":")
            rules[block].append((name.strip(), value.strip()))
    return rules


RULES = load_headers()


def headers_for(path):
    """Every rule whose pattern matches this request path.

    A request for "/" must also pick up "/index.html" rules — real hosts
    resolve the directory index before matching, and the home page is the one
    scanners test.
    """
    candidates = {path}
    if path.endswith("/"):
        candidates.add(path + "index.html")

    out = []
    for pattern, headers in RULES.items():
        if pattern == "/*":
            out += headers
        elif pattern.startswith("/*."):                 # e.g. /*.md
            if any(c.endswith(pattern[2:]) for c in candidates):
                out += headers
        elif pattern in candidates:
            out += headers
    # "/" and "/index.html" can both match the same rule — keep one copy
    return list(dict.fromkeys(out))


def wants_markdown(accept):
    """True only if the client prefers markdown over HTML — a browser's
    `text/html,...,*/*;q=0.8` must not trigger this."""
    if not accept:
        return False
    md = html = -1.0
    for part in accept.split(","):
        bits = part.strip().split(";")
        kind = bits[0].strip().lower()
        q = 1.0
        for p in bits[1:]:
            m = re.match(r"\s*q=([0-9.]+)\s*$", p, re.I)
            if m:
                q = float(m.group(1))
        if kind in ("text/markdown", "text/x-markdown"):
            md = max(md, q)
        elif kind == "text/html":
            html = max(html, q)
    return md > 0 and md >= html


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(ROOT), **kw)

    def send_head(self):
        """Overridden rather than do_GET so HEAD negotiates identically."""
        req = self.path.split("?")[0]
        twin = None
        if req.endswith("/"):
            twin = req + "index.md"
        elif req.endswith(".html"):
            twin = req[:-len(".html")] + ".md"

        if twin and wants_markdown(self.headers.get("Accept")):
            target = ROOT / twin.lstrip("/")
            if target.is_file():
                body = target.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Link", f'<{req}>; rel="canonical"')
                self.send_header("x-markdown-tokens", str(len(body.split())))
                self._emit_configured(req)
                self.send_header("Vary", "Accept")
                self.end_headers()
                return io.BytesIO(body)

        self._request_path = req
        return super().send_head()

    def end_headers(self):
        # super().send_head() reaches here; the markdown branch has already
        # emitted its own headers and called end_headers directly.
        if getattr(self, "_request_path", None):
            self._emit_configured(self._request_path)
            self.send_header("Vary", "Accept")
            self._request_path = None
        super().end_headers()

    def _emit_configured(self, path):
        for name, value in headers_for(path):
            # Content-Type from _headers must replace, not duplicate
            if name.lower() == "content-type":
                continue
            self.send_header(name, value)

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    if not (ROOT / "index.html").exists():
        sys.exit("No index.html — run `python build.py` first.")
    patterns = len(RULES)
    print(f"serving {ROOT}")
    print(f"  {patterns} header rule(s) from _headers")
    print(f"  Accept: text/markdown -> .md twins")
    print(f"\n  http://localhost:{PORT}\n")
    with Server(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
