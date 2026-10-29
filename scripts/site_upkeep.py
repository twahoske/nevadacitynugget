#!/usr/bin/env python3
"""Search-engine upkeep for nevadacitynugget.com.

Run from the repo root (the GitHub Action does this after every push to main).
It never touches index.html, which the Site Publisher owns. It:
  - points each archived edition's canonical link and og:url at its own address
    (archives are moved out of index.html, so they arrive claiming to be the homepage),
  - gives each archived edition a dated <title>,
  - copies the homepage's Content-Security-Policy and referrer tags into each archived edition,
  - points a stray duplicate (editions/YYYY-MM-DD-N.html) at the edition it duplicates,
  - rewrites sitemap.xml.
Safe to run repeatedly; it only writes files whose content changes.
"""
import datetime
import pathlib
import re

SITE = "https://nevadacitynugget.com/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(-\d+)?\.html$")


def folio_date(html):
    """The last bold date in the folio line, e.g. 'Friday, October 23, 2026'."""
    m = re.search(r'<div class="folio">(.*?)</div>', html, re.S)
    if not m:
        return None
    dates = re.findall(r"<b>([A-Z][a-z]+day, [A-Z][a-z]+ \d{1,2}, \d{4})</b>", m.group(1))
    return dates[-1] if dates else None


def set_head_tag(html, pattern, tag, after):
    """Replace the first tag matching pattern in <head>, or insert it after `after`."""
    head_end = html.find("</head>")
    head_end = head_end if head_end != -1 else len(html)
    head, rest = html[:head_end], html[head_end:]
    if re.search(pattern, head):
        head = re.sub(pattern, lambda _: tag, head, count=1)
    else:
        m = re.search(after, head)
        if not m:
            return html
        head = head[: m.end()] + "\n" + tag + head[m.end():]
    return head + rest


SECURITY_TAGS = [r'<meta name="referrer"[^>]*>', r'<meta http-equiv="Content-Security-Policy"[^>]*>']


def homepage_tags():
    """(pattern, tag) for each security <meta> tag in index.html's head; archives carry them too."""
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    head = html[: html.find("</head>")]
    return [(p, m.group(0)) for p, m in ((p, re.search(p, head)) for p in SECURITY_TAGS) if m]


def fix_edition(path, editions, tags=()):
    html = path.read_text(encoding="utf-8")
    date, dup = FILE_RE.match(path.name).groups()
    own = f"{SITE}editions/{path.name}"
    # A -N file is an earlier copy of a later edition; send search engines to the real one.
    canonical = own
    if dup:
        twin = f"{date}.html"
        no = re.search(r"Vol\. 1, No\. \d+", html)
        for other in editions:
            if not FILE_RE.match(other.name).group(2) and no and no.group(0) in other.read_text(encoding="utf-8"):
                twin = other.name
                break
        canonical = f"{SITE}editions/{twin}"

    new = set_head_tag(html, r'<link rel="canonical"[^>]*>',
                       f'<link rel="canonical" href="{canonical}">', r'<meta name="viewport"[^>]*>')
    new = re.sub(r'(<meta property="og:url" content=")[^"]*(")', rf"\g<1>{canonical}\g<2>", new, count=1)
    for pattern, tag in tags:
        new = set_head_tag(new, pattern, tag, r'<meta name="viewport"[^>]*>')
    new = new.replace('<link rel="icon" href="favicon.svg"', '<link rel="icon" href="/favicon.svg"', 1)
    day = folio_date(new)
    if day:
        new = re.sub(r"<title>Nevada City Nugget</title>",
                     f"<title>Nevada City Nugget · {day}</title>", new, count=1)
    if new != html:
        path.write_text(new, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
    return None if dup else date


def iso(day):
    return datetime.datetime.strptime(day, "%A, %B %d, %Y").date().isoformat()


def main():
    editions = sorted(p for p in (ROOT / "editions").glob("*.html") if FILE_RE.match(p.name))
    tags = homepage_tags()
    dated = [d for d in (fix_edition(p, editions, tags) for p in editions) if d]

    today = folio_date((ROOT / "index.html").read_text(encoding="utf-8"))
    urls = [(SITE, iso(today) if today else None, "daily", "1.0"),
            (f"{SITE}sources.html", None, "monthly", "0.5")]
    if (ROOT / "drinks.html").exists():
        urls.append((f"{SITE}drinks.html", None, "monthly", "0.7"))
    if (ROOT / "trails.html").exists():
        urls.append((f"{SITE}trails.html", None, "monthly", "0.7"))
    urls += [(f"{SITE}{page}", None, "yearly", "0.3")
             for page in ("standards.html", "privacy.html", "terms.html") if (ROOT / page).exists()]
    urls += [(f"{SITE}editions/{d}.html", d, "never", "0.6") for d in sorted(set(dated), reverse=True)]

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, freq, prio in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{loc}</loc>")
        if lastmod:
            lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{freq}</changefreq>")
        lines.append(f"    <priority>{prio}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    sitemap = ROOT / "sitemap.xml"
    body = "\n".join(lines) + "\n"
    if not sitemap.exists() or sitemap.read_text(encoding="utf-8") != body:
        sitemap.write_text(body, encoding="utf-8")
        print("updated sitemap.xml")


if __name__ == "__main__":
    main()
