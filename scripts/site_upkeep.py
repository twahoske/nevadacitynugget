#!/usr/bin/env python3
"""Search-engine upkeep for nevadacitynugget.com.

Run from the repo root (the GitHub Action does this after every push to main).
It never touches index.html, which the Site Publisher owns. It:
  - points each archived edition's canonical link and og:url at its own address
    (archives are moved out of index.html, so they arrive claiming to be the homepage),
  - gives each archived edition a title and description built from its own headlines,
    plus NewsArticle structured data,
  - makes the archives' relative links work from inside editions/,
  - points a stray duplicate (editions/YYYY-MM-DD-N.html) at the edition it duplicates,
  - writes editions/index.html, a list of every edition,
  - gives the bar guide (drinks.html) structured data for each bar it lists,
  - rewrites sitemap.xml.
Safe to run repeatedly; it only writes files whose content changes.
"""
import datetime
import html as htmllib
import json
import pathlib
import re

SITE = "https://nevadacitynugget.com/"
ROOT = pathlib.Path(__file__).resolve().parent.parent
FILE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})(-\d+)?\.html$")
LD_RE = r'<script type="application/ld\+json"[^>]*>.*?</script>'
# Standing sections whose h3s are not news headlines.
NOT_NEWS = {"The Docket", "Elected Officials", "The Back Page", "Amusements", "Civic Calendar",
            "Coming Attractions", "Meeting Watch", "Corrections", "Previously"}


def folio_date(html):
    """The last bold date in the folio line, e.g. 'Friday, October 23, 2026'."""
    m = re.search(r'<div class="folio">(.*?)</div>', html, re.S)
    if not m:
        return None
    dates = re.findall(r"<b>([A-Z][a-z]+day, [A-Z][a-z]+ \d{1,2}, \d{4})</b>", m.group(1))
    return dates[-1] if dates else None


def text(fragment):
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", "", fragment)).split())


def headlines(html):
    """[(section, headline)] for the news stories on an edition page, lead story first."""
    body = html[html.find("<body"):]
    out = []
    parts = re.split(r'<h2 class="kicker"[^>]*>(.*?)</h2>', body, flags=re.S)
    for i in range(1, len(parts) - 1, 2):
        section = text(parts[i])
        if section in NOT_NEWS:
            continue
        for article in re.findall(r"<article[^>]*>(.*?)</article>", parts[i + 1], re.S):
            h = re.search(r"<h3[^>]*>(.*?)</h3>", article, re.S)
            if h and text(h.group(1)):
                out.append((section, text(h.group(1))))
    return out


def ld_nodes():
    """The organization and website nodes from the homepage's structured data."""
    home = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', home, re.S)
    graph = json.loads(m.group(1)).get("@graph", []) if m else []
    return [n for n in graph if n.get("@type") in ("NewsMediaOrganization", "WebSite")]


def ld_script(nodes, script_id=""):
    attr = f' id="{script_id}"' if script_id else ""
    data = json.dumps({"@context": "https://schema.org", "@graph": nodes}, ensure_ascii=False,
                      separators=(",", ":")).replace("</", "<\\/")
    return f'<script type="application/ld+json"{attr}>\n{data}\n</script>'


def set_meta(html, attr, name, value):
    """Replace the content of an existing <meta attr="name"> in <head>; never adds one."""
    value = htmllib.escape(value, quote=True)
    head_end = html.find("</head>")
    return re.sub(rf'(<meta {attr}="{re.escape(name)}" content=")[^"]*(")',
                  lambda m: m.group(1) + value + m.group(2), html[:head_end], count=1) + html[head_end:]


def root_links(html):
    """Archives live in editions/, so the edition's page-relative links need a leading slash."""
    return re.sub(r'\b(href|src)="(?!https?:|/|#|mailto:|tel:|data:|javascript:)(?:\./)?([^"]*)"',
                  lambda m: f'{m.group(1)}="/{m.group(2)}"', html)


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


def fix_edition(path, editions):
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
    new = new.replace('<link rel="icon" href="favicon.svg"', '<link rel="icon" href="/favicon.svg"', 1)
    new = root_links(new)

    day = folio_date(new)
    heads = headlines(new)
    lead = heads[0][1] if heads else None
    if day:
        short = day.split(", ", 1)[1]
        title = f"{lead} · Nevada City Nugget, {short}" if lead else f"Nevada City Nugget · {day}"
        desc = f"Nevada City news for {day}: "
        for _, h in heads:
            if len(desc) + len(h) > 240:
                break
            desc += h + ". "
        desc = desc.strip() if heads else f"The Nevada City Nugget for {day}."
        new = re.sub(r"<title>.*?</title>", lambda _: f"<title>{htmllib.escape(title, quote=False)}</title>",
                     new, count=1, flags=re.S)
        new = set_head_tag(new, r'<meta name="description"[^>]*>',
                           f'<meta name="description" content="{htmllib.escape(desc, quote=True)}">',
                           r'<meta name="viewport"[^>]*>')
        for attr, name, value in (("property", "og:type", "article"), ("property", "og:title", title),
                                  ("property", "og:description", desc), ("name", "twitter:title", title),
                                  ("name", "twitter:description", desc)):
            new = set_meta(new, attr, name, value)
        article = {"@type": "NewsArticle", "@id": f"{canonical}#edition", "url": canonical,
                   "mainEntityOfPage": canonical, "headline": (lead or f"Nevada City Nugget, {day}")[:110],
                   "description": desc, "datePublished": iso(day), "dateModified": iso(day),
                   "inLanguage": "en-US", "image": [f"{SITE}og-image.png"],
                   "articleSection": list(dict.fromkeys(s for s, _ in heads)),
                   "author": {"@id": f"{SITE}#organization"}, "publisher": {"@id": f"{SITE}#organization"},
                   "isPartOf": {"@id": f"{SITE}#website"}}
        script = ld_script(ld_nodes() + [article])
        head_end = new.find("</head>")
        if re.search(LD_RE, new[:head_end], re.S):
            new = re.sub(LD_RE, lambda _: script, new[:head_end], count=1, flags=re.S) + new[head_end:]
        else:
            new = set_head_tag(new, r"(?!)", script, r'<link rel="canonical"[^>]*>')

    if new != html:
        path.write_text(new, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")
    return None if dup else (date, day, lead)


def write_if_changed(path, body):
    if not path.exists() or path.read_text(encoding="utf-8") != body:
        path.write_text(body, encoding="utf-8")
        print(f"updated {path.relative_to(ROOT)}")


def archive_page(entries):
    """editions/index.html: every edition with its lead headline, styled like the policy pages."""
    template = (ROOT / "standards.html").read_text(encoding="utf-8")
    head = template[:template.find("</head>")]
    url = f"{SITE}editions/"
    desc = "Every edition of the Nevada City Nugget, a Modern-Vintage daily paper for Nevada City, California, with each day's lead story."
    head = re.sub(r"<title>.*?</title>", "<title>The Archive · Nevada City Nugget</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">', head, count=1)
    items = []
    for date, day, lead in entries:
        name = htmllib.escape(day or date)
        what = htmllib.escape(lead or "")
        items.append(f'  <li><a class="s-name" href="/editions/{date}.html">{name}</a>'
                     f'<span class="s-what">{what}</span></li>')
    footer = template[template.find("<footer>"):]
    footer = root_links(footer)
    body = f"""</head>
<body>
<div class="wrap">

<div class="banner">The Archive</div>
<div>
  <h1>Nevada City Nugget</h1>
  <p class="motto">Every Edition, Day by Day</p>
</div>

<a class="back" href="/">◂ Back to Today's Edition</a>

<section>
  <h2 class="kicker" id="editions"><span class="label">Past Editions</span></h2>
<ul class="srclist">
{chr(10).join(items)}
</ul>
</section>

{footer}"""
    write_if_changed(ROOT / "editions" / "index.html", root_links(head) + body)


def bar_guide():
    """Structured data for each bar in drinks.html, read from the page itself so it never drifts."""
    path = ROOT / "drinks.html"
    if not path.exists():
        return
    html = path.read_text(encoding="utf-8")
    bars = []
    for li in re.findall(r"<li>(.*?)</li>", html, re.S):
        name = re.search(r'<span class="d-name">(.*?)</span>', li, re.S)
        addr = re.search(r'<span class="d-addr">(.*?)</span>', li, re.S)
        if not name:
            continue
        bar = {"@type": "BarOrPub", "name": text(name.group(1))}
        if addr:
            bar["address"] = {"@type": "PostalAddress", "streetAddress": text(addr.group(1)),
                              "addressLocality": "Nevada City", "addressRegion": "CA",
                              "postalCode": "95959", "addressCountry": "US"}
        phone = re.search(r"\(\d{3}\) \d{3}-\d{4}", li)
        if phone:
            bar["telephone"] = phone.group(0)
        # Only a link whose text is the bar's own domain counts as its website.
        for href, label in re.findall(r'<a href="(https?://[^"]+)">([^<]+)</a>', li):
            host = re.sub(r"^www\.", "", href.split("/")[2])
            if re.sub(r"^www\.", "", label.strip()) == host:
                bar["url"] = href
                break
        bars.append(bar)
    nodes = [{"@type": "ItemList", "@id": f"{SITE}drinks.html#bars", "name": "Where to get a drink in Nevada City",
              "url": f"{SITE}drinks.html", "numberOfItems": len(bars),
              "itemListElement": [{"@type": "ListItem", "position": i, "item": b} for i, b in enumerate(bars, 1)]}]
    script = ld_script(nodes, "bar-guide-ld")
    head_end = html.find("</head>")
    pattern = r'<script type="application/ld\+json" id="bar-guide-ld">.*?</script>'
    if re.search(pattern, html[:head_end], re.S):
        new = re.sub(pattern, lambda _: script, html[:head_end], count=1, flags=re.S) + html[head_end:]
    else:
        new = html[:head_end] + script + "\n" + html[head_end:]
    write_if_changed(path, new)


def iso(day):
    return datetime.datetime.strptime(day, "%A, %B %d, %Y").date().isoformat()


def main():
    editions = sorted(p for p in (ROOT / "editions").glob("*.html") if FILE_RE.match(p.name))
    entries = sorted((e for e in (fix_edition(p, editions) for p in editions) if e), reverse=True)
    dated = [date for date, _, _ in entries]
    archive_page(entries)
    bar_guide()

    today = folio_date((ROOT / "index.html").read_text(encoding="utf-8"))
    urls = [(SITE, iso(today) if today else None, "daily", "1.0"),
            (f"{SITE}sources.html", None, "monthly", "0.5")]
    if (ROOT / "drinks.html").exists():
        urls.append((f"{SITE}drinks.html", None, "monthly", "0.7"))
    urls += [(f"{SITE}{page}", None, "yearly", "0.3")
             for page in ("standards.html", "privacy.html", "terms.html") if (ROOT / page).exists()]
    urls.append((f"{SITE}editions/", dated[0] if dated else None, "daily", "0.6"))
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
    write_if_changed(ROOT / "sitemap.xml", "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
