#!/usr/bin/env python3
"""Content guard for nevadacitynugget.com.

The paper is written by scheduled tasks from fetched web pages and reader email, then
copied here automatically. This check fails (and GitHub emails the publisher) if any
published page picks up something that could run code or send readers elsewhere:
an unapproved script, an inline event handler, a javascript: link, a frame or form,
or a meta refresh. It also fails if index.html loses its Content-Security-Policy.

Approved inline scripts are the ones whose sha256 hashes appear in index.html's CSP.
To approve a new script on purpose, add the hash this check prints to that CSP.
"""
import base64
import hashlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSP_RE = re.compile(r'<meta http-equiv="Content-Security-Policy" content="([^"]*)"')
CHECKS = [
    (re.compile(r"<script\b[^>]*\bsrc\s*=", re.I), "external script"),
    (re.compile(r"<[a-z][^>]*\son[a-z]+\s*=", re.I), "inline event handler"),
    (re.compile(r"""\b(?:href|src|action|formaction)\s*=\s*["']?\s*javascript:""", re.I), "javascript: link"),
    (re.compile(r"<(?:iframe|frame|object|embed|form|base)\b", re.I), "frame, embed, form or base tag"),
    (re.compile(r"<meta[^>]*http-equiv\s*=\s*[\"']?refresh", re.I), "meta refresh"),
]


def sha(text):
    return "sha256-" + base64.b64encode(hashlib.sha256(text.encode("utf-8")).digest()).decode()


def main():
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    m = CSP_RE.search(home[: home.find("</head>")])
    if not m:
        print("index.html: Content-Security-Policy meta tag is missing from <head>")
        return 1
    allowed = set(re.findall(r"'(sha256-[A-Za-z0-9+/=]+)'", m.group(1)))

    problems = []
    pages = sorted(ROOT.glob("*.html")) + sorted((ROOT / "editions").glob("*.html"))
    for page in pages:
        html = page.read_text(encoding="utf-8")
        name = page.relative_to(ROOT)
        for pattern, what in CHECKS:
            for hit in pattern.finditer(html):
                line = html.count("\n", 0, hit.start()) + 1
                problems.append(f"{name}:{line}: {what}: {hit.group(0)[:80]}")
        for attrs, body in re.findall(r"<script\b([^>]*)>(.*?)</script>", html, re.S | re.I):
            if "application/ld+json" in attrs:
                continue
            if sha(body) not in allowed:
                problems.append(f"{name}: inline script not approved in index.html's CSP ('{sha(body)}')")

    for p in problems:
        print(p)
    print(f"checked {len(pages)} pages, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
