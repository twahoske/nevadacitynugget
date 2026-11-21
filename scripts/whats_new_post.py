#!/usr/bin/env python3
"""What's New at the Nugget: release-notes features on Instagram (feed + Story)
and the Facebook Page, one feature per post, twice a day (Todd, Nov 16 2026).

Slots (Pacific): am 10:00 AM-12:00 PM, pm 8:00-11:30 PM. They aim for ~10 AM and
~8 PM, between the paper's other posts (front ~6 AM, Merchant ~8:30 AM, Saturday
roundup ~9 AM, Friday Geezer Gig ~1 PM, Thirsty Thursday ~3 PM, spotlight 4-7:30 PM).
The windows are wide on purpose (Nov 19 2026): GitHub's timer can run an hour or
more late, and on Nov 17-18 three slots were missed because no run landed inside the
old one-hour windows.

The queue is social/whats-new/queue.json, oldest release first. Each item posts once
and is recorded in social-cards:posted/whats-new-ID.json; each slot posts at most one
item a day (social-cards:posted/whats-new-DATE-SLOT.json). A release in
release-notes.html at or after the queue's "start" that has no queue entries is
posted straight from its bullets, with the NEW stamp drawing, so the posts keep
coming even if a thread forgets the queue. When the queue runs dry, nothing posts.
Holiday posts (social/holiday/holiday.json, Nov 21 2026) are dated: on its date, in its
slot, a holiday post goes ahead of the queue; on other days they never post.

Steps (run by .github/workflows/whats-new-post.yml):
  gate     is a slot open, and is there an item to post?
  render   draw out/feed.jpg, out/story.jpg, out/caption.txt
  publish  push the cards to the social-cards branch, post them, record the result
DRY_RUN=yes renders and posts nothing (a manual run's default). ITEM=id draws that item.
"""
import base64
import html as htmlmod
import json
import os
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import social_post as sp  # noqa: E402  (shares the card branch, Graph calls and record)

ROOT = sp.ROOT
OUT = sp.OUT
HERE = ROOT / "social" / "whats-new"
TOUR = ROOT / "social" / "grand-tour"
NOTES = ROOT / "release-notes.html"
SLOTS = {"am": (10 * 60, 12 * 60), "pm": (20 * 60, 23 * 60 + 30)}
TAGS = "#NevadaCity #NevadaCityCA #NevadaCounty #GoldCountry #LocalNews"


def vkey(v):
    return tuple(int(x) for x in re.findall(r"\d+", v))


def plain(fragment):
    t = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", htmlmod.unescape(t)).strip()


def note_sections():
    """{version: [bullet html, ...]} from release-notes.html."""
    s = NOTES.read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<section id="v([\d.]+)">(.*?)</section>', s, re.S):
        out[m.group(1)] = re.findall(r"<li>(.*?)</li>", m.group(2), re.S)
    return out


def auto_item(version, i, li):
    b = re.search(r"<b>(.*?)</b>", li, re.S)
    head = plain(b.group(1)).rstrip(".:") if b else "New at the Nugget"
    body = plain(li)
    a = re.search(r'href="([^"]+)"', li)
    link = a.group(1) if a and not a.group(1).startswith("http") else ""
    first = re.split(r"(?<=[.!?])\s", body, maxsplit=1)[0]
    return {"id": f"{version}-{i + 1}", "version": version, "art": "stamp",
            "head": head[:90], "deck": sp.clip(first, 200) if first != head else "", "body": body,
            "link": link.lstrip("/"), "auto": True}


def queue():
    q = json.loads((HERE / "queue.json").read_text(encoding="utf-8"))
    start = vkey(q.get("start", "0"))
    items = [x for x in q["items"] if not x.get("skip")]
    have = {x["version"] for x in q["items"]}
    for v, lis in note_sections().items():
        if vkey(v) >= start and v not in have:
            items += [auto_item(v, i, li) for i, li in enumerate(lis)]
    order = {x["id"]: n for n, x in enumerate(items)}
    items.sort(key=lambda x: (vkey(x["version"]), order[x["id"]]))
    for x in items:
        for k in ("head", "deck", "body"):
            x[k] = (x.get(k) or "").replace("—", ",").replace("–", "-")
    return items + tour()


def tour():
    """The Grand Tour welcome series (Todd, Nov 16 2026): one paper or Visitor Guide
    section per post, after any What's New items, so a new release always cuts in."""
    f = TOUR / "tour.json"
    if not f.exists():
        return []
    stops = [x for x in json.loads(f.read_text(encoding="utf-8"))["stops"] if not x.get("skip")]
    for n, x in enumerate(stops, 1):
        x.update(series="tour", version="", n=n, total=len(stops))
        for k in ("head", "deck", "body"):
            x[k] = (x.get(k) or "").replace("—", ",").replace("–", "-")
    return stops


HOLIDAY = ROOT / "social" / "holiday"
HAT_LINE = ("While you're on Broad Street: The Hat Store, 314 Broad, has a hat for every head "
            "and every kind of weather. (Full disclosure: it's the Nugget publisher's own shop.)")


def holiday():
    """Dated holiday posts (Todd, Nov 21 2026): Black Friday, Small Business Saturday
    and Victorian Christmas, the day before, the day of and the day after. Each one
    posts only on its own date, in its own slot, ahead of the regular queue."""
    f = HOLIDAY / "holiday.json"
    if not f.exists():
        return []
    posts = [x for x in json.loads(f.read_text(encoding="utf-8"))["posts"] if not x.get("skip")]
    for x in posts:
        x.update(series="holiday", version="")
        for k in ("head", "deck", "body"):
            x[k] = (x.get(k) or "").replace("—", ",").replace("–", "-")
    return posts


def holiday_today(now, slot):
    return next((x for x in holiday() if x["date"] == f"{now:%Y-%m-%d}" and x["slot"] == slot), None)


def holiday_caption(item):
    url = "nevadacitynugget.com/" + item["link"] if item.get("link") else "nevadacitynugget.com (link in bio)"
    lines = [item["kicker"].upper(), "", item["head"].upper(), "", item["body"], ""]
    if item.get("hat"):
        lines += [HAT_LINE, ""]
    lines += [f"Read it: {url}", "",
              "The Nevada City Nugget is a free daily paper for Nevada City, out every morning by 6.", "",
              (item.get("tags", "") + " " + TAGS).strip()]
    return "\n".join(lines).replace("—", ",")[:2100]


def tour_caption(item):
    url = "nevadacitynugget.com/" + item["link"] if item.get("link") else "nevadacitynugget.com (link in bio)"
    where = "the Nevada City Visitor Guide" if item.get("where") == "visitor" else "the paper"
    lines = [f"THE GRAND TOUR ✱ HOWDY, STRANGER! ✱ STOP {item['n']} OF {item['total']}", "",
             item["head"].upper(), "", item["body"], "", f"Find it in {where}: {url}", "",
             "New around here? Welcome. The Nevada City Nugget is a free daily paper for Nevada City, "
             "out every morning by 6. This tour shows you around, one section at a time.", "",
             TAGS]
    return "\n".join(lines).replace("—", ",")[:2100]


def caption(item):
    if item.get("series") == "holiday":
        return holiday_caption(item)
    if item.get("series") == "tour":
        return tour_caption(item)
    url = "nevadacitynugget.com/" + item["link"] if item.get("link") else "nevadacitynugget.com (link in bio)"
    lines = [f"WHAT'S NEW AT THE NUGGET ✱ v{item['version']}", "", item["head"].upper(), "",
             item["body"], "", f"See it: {url}",
             "Every change, big and small: nevadacitynugget.com/release-notes.html", "",
             "The Nevada City Nugget is free, every morning by 6. Still in beta, still adding things.", "",
             TAGS]
    return "\n".join(lines).replace("—", ",")[:2100]


CARD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Besley:ital,wght@0,400;0,700;0,800;0,900;1,400;1,600&family=Grenze+Gotisch:wght@900&display=swap">
<style>
:root{--paper:#f0ead9;--panel:#e7e0cb;--ink:#201c13;--soft:#5f5743;--rule:#9c927a;--red:#7e2a18;--gold:#b8862f;--d:"Besley",Georgia,serif}
*{box-sizing:border-box;margin:0}
html,body{width:1080px;height:__H__px;overflow:hidden}
body{background:var(--paper);background-image:radial-gradient(ellipse at 50% 30%,rgba(255,255,255,.35),transparent 60%),radial-gradient(ellipse at 50% 120%,rgba(32,28,19,.10),transparent 60%);color:var(--ink);font-family:var(--d);padding:__PAD__;display:flex}
.frame{flex:1;border:3px solid var(--ink);outline:1px solid var(--ink);outline-offset:-12px;display:flex;flex-direction:column;align-items:center;text-align:center;padding:30px 50px 28px;gap:__GAP__px;position:relative;overflow:hidden}
.name{font-family:"Grenze Gotisch",serif;font-weight:900;font-size:__NAME__px;line-height:1;margin-top:4px}
.rule{width:100%;border-top:3px double var(--ink);border-bottom:1px solid var(--ink);padding:9px 0 8px;font-weight:800;font-size:22px;letter-spacing:.3em;text-transform:uppercase}
.stamp{position:absolute;top:__STOP__px;right:46px;transform:rotate(9deg);border:4px solid var(--red);outline:1.5px solid var(--red);outline-offset:-9px;color:var(--red);padding:12px 18px 10px;font-weight:900;font-size:26px;letter-spacing:.12em;text-transform:uppercase;line-height:1.05;background:rgba(240,234,217,.85)}
.stamp small{display:block;font-size:17px;letter-spacing:.2em;font-weight:800}
.art{width:__M__px;height:__M__px;flex:none;margin-top:auto !important;border-radius:50%;background:var(--panel);box-shadow:0 0 0 5px var(--ink),0 0 0 11px var(--paper),0 0 0 14px var(--gold);display:grid;place-items:center;margin:14px 0 6px}
.art img{width:80%;height:80%}
h1{font-weight:900;font-size:__HEAD__px;line-height:1.06;text-wrap:balance;max-width:920px;letter-spacing:-.005em}
.deck{font-size:__DECK__px;line-height:1.4;font-style:italic;color:var(--soft);max-width:880px;text-wrap:pretty}
.sp{margin-top:auto}
.foot{width:100%;border-top:3px double var(--ink);padding-top:14px;display:flex;justify-content:space-between;font-weight:800;font-size:19px;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap;gap:20px}
.foot b{color:var(--red)}
</style></head><body><div class="frame">
<div class="name">The Nevada City Nugget</div>
<div class="rule">What's New at the Nugget</div>
<div class="stamp">Beta<small>v__V__</small></div>
<div class="art"><img src="__ART__" alt=""></div>
<h1>__HEAD_T__</h1>
__DECK_T__
<div class="sp"></div><div class="foot"><span>__FOOTL__</span><b>nevadacitynugget.com</b></div>
</div></body></html>"""


TOUR_CSS = """<style>
body{background:#201c13;background-image:radial-gradient(ellipse at 50% 30%,rgba(240,234,217,.08),transparent 60%),radial-gradient(ellipse at 50% 120%,rgba(0,0,0,.35),transparent 60%);color:#f0ead9}
.frame{border-color:#b8862f;outline-color:#b8862f}
.rule{border-color:#b8862f;color:#e3c27a}
.deck{color:#c9bfa6}
.foot{border-color:#b8862f}.foot b{color:#e3c27a}
.art{box-shadow:0 0 0 5px #b8862f,0 0 0 11px #201c13,0 0 0 14px #f0ead9}
.stamp{position:static;transform:rotate(-4deg);margin-top:4px;font-size:30px;border:none;outline:none;background:#b8862f;color:#201c13;padding:12px 30px 10px;
 -webkit-mask:radial-gradient(circle 9px at 0 50%,transparent 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 9px at 100% 50%,transparent 98%,#000) right/51% 100% no-repeat;
 mask:radial-gradient(circle 9px at 0 50%,transparent 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 9px at 100% 50%,transparent 98%,#000) right/51% 100% no-repeat}
.stamp small{border-top:2px dashed #201c13;margin-top:6px;padding-top:5px}
</style></head>"""


HOLIDAY_CSS = """<style>
.stamp{position:static;transform:rotate(-4deg);margin-top:4px;font-size:30px;border:none;outline:none;background:#7e2a18;color:#f0ead9;padding:12px 30px 10px;
 -webkit-mask:radial-gradient(circle 9px at 0 50%,transparent 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 9px at 100% 50%,transparent 98%,#000) right/51% 100% no-repeat;
 mask:radial-gradient(circle 9px at 0 50%,transparent 98%,#000) left/51% 100% no-repeat,radial-gradient(circle 9px at 100% 50%,transparent 98%,#000) right/51% 100% no-repeat}
.stamp small{border-top:2px dashed #f0ead9;margin-top:6px;padding-top:5px}
</style></head>"""


def card_html(kind, item):
    if item.get("series") == "holiday":
        esc = htmlmod.escape
        h = _card_html(kind, item, HOLIDAY / "art" / f"{item.get('art')}.svg")
        h = h.replace("</head>", TOUR_CSS if item.get("night") else HOLIDAY_CSS, 1)
        top, bottom = (item.get("stamp") or ["", ""])[:2]
        return (h.replace("What's New at the Nugget", esc(item["kicker"]))
                .replace('<div class="stamp">Beta<small>v</small></div>',
                         f'<div class="stamp">{esc(top)}<small>{esc(bottom)}</small></div>'))
    if item.get("series") == "tour":
        t = dict(item, version="")
        where = "Visitor Guide" if item.get("where") == "visitor" else "The Paper"
        h = _card_html(kind, t, TOUR / "art" / f"{item['id']}.svg")
        return (h.replace("</head>", TOUR_CSS, 1)
                .replace("What's New at the Nugget", "The Grand Tour ✱ Howdy, Stranger!")
                .replace('<div class="stamp">Beta<small>v</small></div>',
                         f'<div class="stamp">Stop {item["n"]} of {item["total"]}<small>{where}</small></div>'))
    return _card_html(kind, item)


def _card_html(kind, item, art=None):
    esc = htmlmod.escape
    art = art if art and art.exists() else HERE / "art" / f"{item.get('art') or 'stamp'}.svg"
    svg = art.read_bytes()
    story = kind == "story"
    deck = f'<p class="deck">{esc(item["deck"])}</p>' if item.get("deck") else ""
    footl = "Free every morning by 6"
    return (CARD.replace("__H__", "1920" if story else "1350")
            .replace("__PAD__", "200px 50px 220px" if story else "44px 50px")
            .replace("__GAP__", "30" if story else "20")
            .replace("__NAME__", "84" if story else "70")
            .replace("__STOP__", "150" if story else "126")
            .replace("__M__", "460" if story else "380")
            .replace("__HEAD__", "70" if story else "60")
            .replace("__DECK__", "34" if story else "29")
            .replace("__ART__", "data:image/svg+xml;base64," + base64.b64encode(svg).decode())
            .replace("__V__", esc(item["version"]))
            .replace("__HEAD_T__", esc(item["head"]))
            .replace("__DECK_T__", deck)
            .replace("__FOOTL__", esc(footl)))


def render(item, out=OUT):
    out.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        for kind, h in (("feed", 1350), ("story", 1920)):
            pg = b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=1)
            pg.set_content(card_html(kind, item), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(500)
            # shrink the words, then the drawing, if a long one crowds the frame
            pg.evaluate("""() => { const f = document.querySelector('.frame'), h = document.querySelector('h1');
              const dk = document.querySelector('.deck'), a = document.querySelector('.art');
              const over = () => f.scrollHeight > f.clientHeight + 1;
              let t = dk ? parseFloat(getComputedStyle(dk).fontSize) : 0, s = parseFloat(getComputedStyle(h).fontSize), m = a.offsetWidth;
              while (over() && dk && t > 24) { t -= 1; dk.style.fontSize = t + 'px'; }
              while (over() && m > 240) { m -= 10; a.style.width = a.style.height = m + 'px'; }
              while (over() && s > 38) { s -= 2; h.style.fontSize = s + 'px'; }
              if (over() && dk) dk.remove(); }""")
            pg.screenshot(path=str(out / f"{kind}.jpg"), type="jpeg", quality=92)
        b.close()
    (out / "caption.txt").write_text(caption(item), encoding="utf-8")
    (out / "item.txt").write_text(item["id"], encoding="utf-8")


def wanted():
    token = os.environ.get("IG_ACCESS_TOKEN", "")
    return ["feed", "story"] + ([] if token.startswith("IG") or not token else ["facebook"])


def complete(rec):
    return all(rec.get(k) for k in wanted())


def current_slot(now):
    mins = now.hour * 60 + now.minute
    return next((s for s, (a, b) in SLOTS.items() if a <= mins <= b), "")


def gate():
    """(item or None, slot, message)."""
    items = queue()
    forced = os.environ.get("ITEM", "").strip()
    if forced:
        item = next((x for x in items + holiday() if x["id"] == forced), None)
        return item, "manual", (f"ITEM: drawing {forced}" if item else f"no item {forced} in the queue")
    now = sp.now_pacific()
    slot = current_slot(now)
    if not slot and os.environ.get("IGNORE_WINDOW") != "yes":
        return None, "", f"outside the What's New windows ({now:%H:%M} Pacific)"
    slot = slot or ("am" if now.hour < 15 else "pm")
    key = f"whats-new-{now:%Y-%m-%d}-{slot}"
    took = sp.record(key)
    if took.get("item"):
        if complete(sp.record(f"whats-new-{took['item']}")):
            return None, slot, f"{slot} slot already posted today ({took['item']})"
        item = next((x for x in items + holiday() if x["id"] == took["item"]), None)
        if item:
            return item, slot, f"finishing {item['id']} in the {slot} slot"
    hol = holiday_today(now, slot)
    if hol and not complete(sp.record(f"whats-new-{hol['id']}")):
        return hol, slot, f"{slot} slot: holiday post {hol['id']}"
    for x in items:
        if not complete(sp.record(f"whats-new-{x['id']}")):
            return x, slot, f"{slot} slot: posting {x['id']}"
    return None, slot, "the What's New queue is empty; nothing to post"


def publish(item, slot, dry_run=False):
    token = os.environ.get("IG_ACCESS_TOKEN", "")
    uid = os.environ.get("IG_USER_ID", "") or ("me" if token.startswith("IG") else "")
    cap = (OUT / "caption.txt").read_text(encoding="utf-8")
    if dry_run or slot == "manual":
        return f"DRY RUN: {item['id']} cards rendered (see the run's artifacts); nothing posted"
    if not token or not uid:
        return "no IG_ACCESS_TOKEN / IG_USER_ID secrets; nothing posted"
    now = sp.now_pacific()
    key, slot_key = f"whats-new-{item['id']}", f"whats-new-{now:%Y-%m-%d}-{slot}"
    sp.push_files({f"posted/{slot_key}.json": (json.dumps({"item": item["id"]}) + "\n").encode()},
                  f"What's New {slot} slot: {item['id']}")
    done = sp.record(key)
    stamp = str(int(time.time()))
    feed_rel, story_rel = f"cards/{key}-feed-{stamp}.jpg", f"cards/{key}-story-{stamp}.jpg"
    sp.push_files({feed_rel: (OUT / "feed.jpg").read_bytes(), story_rel: (OUT / "story.jpg").read_bytes(),
                   f"cards/{key}-caption.txt": cap.encode()}, f"Cards for What's New {item['id']}")
    time.sleep(20)
    results, errors = dict(done), []
    if not done.get("feed"):
        try:
            results["feed"] = sp.post(token, uid, sp.RAW + feed_rel, cap)
        except Exception as err:
            errors.append(f"feed: {err}")
    if not done.get("story"):
        try:
            results["story"] = sp.post(token, uid, sp.RAW + story_rel, story=True)
        except Exception as err:
            errors.append(f"story: {err}")
    if "facebook" in wanted() and not done.get("facebook"):
        try:
            results["facebook"] = sp.post_facebook(token, sp.RAW + feed_rel,
                                                   cap.replace("nevadacitynugget.com/", "https://nevadacitynugget.com/")
                                                      .replace("nevadacitynugget.com (link in bio)", "https://nevadacitynugget.com"))
        except Exception as err:
            errors.append(f"facebook: {err}")
    if results != done:
        results["at"] = now.isoformat(timespec="minutes")
        sp.push_files({f"posted/{key}.json": (json.dumps(results, indent=1) + "\n").encode()},
                      f"Posted What's New {item['id']}")
    if errors:
        raise RuntimeError("; ".join(errors))
    return f"POSTED What's New {item['id']} ({slot}): " + ", ".join(f"{k} {results.get(k)}" for k in wanted())


def _item(item_id):
    return next(x for x in queue() + holiday() if x["id"] == item_id)


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    dry = os.environ.get("DRY_RUN") == "yes"
    try:
        if step == "gate":
            item, slot, msg = gate()
            out = os.environ.get("GITHUB_OUTPUT")
            if out:
                with open(out, "a") as f:
                    f.write(f"go={'yes' if item else 'no'}\nitem={item['id'] if item else ''}\nslot={slot}\n")
            sp.report(msg)
        elif step == "render":
            render(_item(os.environ["ITEM_ID"]))
            print((OUT / "caption.txt").read_text(encoding="utf-8"))
        elif step == "publish":
            sp.report(publish(_item(os.environ["ITEM_ID"]), os.environ.get("SLOT", ""), dry_run=dry))
        elif step == "list":
            for x in queue():
                print(x["id"], "|", x["head"])
            for x in holiday():
                print(x["id"], "|", x["date"], x["slot"], "|", x["head"])
        else:
            raise SystemExit("usage: whats_new_post.py gate|render|publish|list")
    except Exception as err:  # report, never print the token
        sp.report(f"ERROR: {type(err).__name__}: {err}")
        sys.exit(1)
