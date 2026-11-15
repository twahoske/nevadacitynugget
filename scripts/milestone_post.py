#!/usr/bin/env python3
"""Celebrate Total Circulation milestones on Instagram (feed + Story) and the
Facebook Page (Todd, Nov 15 2026).

Total Circulation is the figure under the date on nevadacitynugget.com: copies of
today's paper read on the site since Oct. 30, 2026, one per phone or computer per
Pacific day, kept by the Nugget's own counter (nugget-tally Worker). Nothing else
is added to it.

Milestones: 500, 1,000, 1,500, 2,000, 3,000, 4,000, 5,000, 7,500, 10,000, then
every 5,000 to 25,000, every 25,000 to 100,000, and every 50,000 after. The site's
own box (in the Wire Service script, words and art in /milestones/) uses the same
ladder and the same rule: a milestone is celebrated on the day it is passed and the
day after. This script posts each milestone once, between 9 AM and 8:30 PM Pacific,
and records it in social-cards:posted/milestone-N.json.

Steps (run by .github/workflows/milestone-post.yml):
  gate     is there a fresh, unposted milestone? (FORCE=N skips the check, for tests)
  render   draw out/feed.jpg, out/story.jpg, out/caption.txt
  publish  push the cards to the social-cards branch, post them, record the result
DRY_RUN=yes renders and reports and posts nothing (a manual run's default); FORCE is always a dry run.
"""
import base64
import html as htmlmod
import json
import os
import pathlib
import sys
import time
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import social_post as sp  # noqa: E402  (shares the card branch, Graph calls and record)

TALLY = "https://nugget-tally.todd-c0b.workers.dev/today"
ROOT = sp.ROOT
OUT = sp.OUT
DATA = ROOT / "milestones" / "milestones.json"
LADDER = [500, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000]
WINDOW = (9 * 60, 20 * 60 + 30)
TAGS = "#NevadaCity #NevadaCityCA #NevadaCounty #GoldCountry #LocalNews"


def next_after(m):
    for n in LADDER:
        if n > m:
            return n
    return m + (5000 if m < 25000 else 25000 if m < 100000 else 50000)


def crossed(d):
    """The milestone passed today or yesterday (Pacific), else 0. Same rule as the site."""
    total = d.get("total")
    if not isinstance(total, int):
        return 0
    before = total - (d.get("readers") or 0) - (d.get("yesterday") or 0)
    m, n = 0, LADDER[0]
    while n <= total:
        if n > before:
            m = n
        n = next_after(n)
    return m


def fmt(n):
    return f"{n:,}"


def entry(m):
    data = json.loads(DATA.read_text(encoding="utf-8"))
    e = next((x for x in data["milestones"] if x["n"] == m), None)
    if not e:
        e = data["beyond"][round(m / 5000) % len(data["beyond"])]
    def fill(s):
        return (s or "").replace("{N}", fmt(m)).replace("{NEXT}", fmt(next_after(m)))
    return {k: fill(v) if isinstance(v, str) else v for k, v in e.items()}, data


def since_text(since):
    try:
        y, mo, d = (int(x) for x in since.split("-"))
    except Exception:
        return "since counting began"
    mon = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."][mo - 1]
    return f"since {mon} {d}, {y}"


def caption(m, since="2026-10-30"):
    e, _ = entry(m)
    lines = ["EXTRA! EXTRA!", "", e["head"], "", e["deck"], "",
             f"That's {fmt(m)} copies of the Nugget read at nevadacitynugget.com {since_text(since)}, "
             "one per phone or computer a day. We count honestly and keep no names. "
             "Thank you for reading, and for passing us along.", "",
             f"Read today's paper free at nevadacitynugget.com (link in bio). Next stop: {fmt(next_after(m))}.", "",
             TAGS]
    return "\n".join(lines).replace("—", ",")[:2100]


CARD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Besley:ital,wght@0,400;0,700;0,800;0,900;1,400;1,600&family=Grenze+Gotisch:wght@900&display=swap">
<style>
:root{--paper:#f0ead9;--ink:#201c13;--mid:#c9bfa6;--rule:#9c927a;--red:#7e2a18;--glow:#d08a6a;--d:"Besley",Georgia,serif}
*{box-sizing:border-box;margin:0}
html,body{width:1080px;height:__H__px;overflow:hidden}
body{background:var(--ink);background-image:radial-gradient(ellipse at 50% 32%,rgba(240,234,217,.07),transparent 60%),radial-gradient(ellipse at 50% 120%,rgba(0,0,0,.35),transparent 60%);color:var(--paper);font-family:var(--d);padding:__PAD__;display:flex}
.frame{flex:1;border:3px solid var(--paper);outline:1px solid var(--paper);outline-offset:-12px;display:flex;flex-direction:column;align-items:center;text-align:center;padding:34px 46px 30px;gap:__GAP__px;position:relative;overflow:hidden}
.extra{font-weight:900;font-size:30px;text-transform:uppercase;letter-spacing:.34em;color:var(--paper);background:var(--red);padding:10px 0 9px .34em;width:calc(100% + 92px);margin-top:-34px}
.name{font-family:"Grenze Gotisch",serif;font-weight:900;font-size:__NAME__px;line-height:1;letter-spacing:.01em}
.rule{width:100%;border-top:3px double var(--paper);border-bottom:1px solid var(--paper);padding:9px 0 8px;font-weight:800;font-size:22px;letter-spacing:.28em;text-transform:uppercase}
.medal{position:relative;width:__M__px;height:__M__px;display:grid;place-items:center;flex:none}
.medal::before{content:"";position:absolute;inset:-56px;border-radius:50%;background:repeating-conic-gradient(from 4deg,rgba(240,234,217,.10) 0 7deg,transparent 7deg 14deg)}
.medal .disc{position:relative;width:100%;height:100%;border-radius:50%;background:var(--paper);box-shadow:0 0 0 7px var(--red),0 0 0 13px var(--ink),0 0 0 17px var(--paper);display:grid;place-items:center}
.medal img{width:82%;height:82%}
.num{position:relative;z-index:1;font-weight:900;font-size:__NUM__px;line-height:.86;letter-spacing:-.01em;text-shadow:7px 7px 0 var(--red)}
.k{font-weight:800;font-size:26px;letter-spacing:.34em;text-transform:uppercase;color:var(--mid);margin-top:10px;position:relative;z-index:2}
h1{font-weight:900;font-size:__HEAD__px;line-height:1.08;text-wrap:balance;max-width:900px}
.deck{font-size:__DECK__px;line-height:1.38;font-style:italic;color:var(--mid);max-width:860px;text-wrap:pretty}
.foot{margin-top:auto;width:100%;border-top:3px double var(--paper);padding-top:14px;display:flex;justify-content:space-between;font-weight:800;font-size:19px;letter-spacing:.12em;text-transform:uppercase;white-space:nowrap;gap:20px}
.foot b{color:var(--glow)}
</style></head><body><div class="frame">
<div class="extra">Extra ✱ Extra ✱ Extra</div>
<div class="name">The Nevada City Nugget</div>
<div class="rule">Circulation Milestone</div>
<div class="medal"><div class="disc"><img src="__ART__" alt=""></div></div>
<div class="num">__N__</div>
<div class="k">Copies Read</div>
<h1>__HEAD_T__</h1>
__DECK_T__
<div class="foot"><span>Free every morning by 6</span><b>nevadacitynugget.com</b></div>
</div></body></html>"""


def card_html(kind, m):
    e, _ = entry(m)
    esc = htmlmod.escape
    svg = (ROOT / "milestones" / f"{e.get('art', 'wreath')}.svg").read_bytes()
    story = kind == "story"
    deck = f'<p class="deck">{esc(e["deck"])}</p>'
    return (CARD.replace("__H__", "1920" if story else "1350")
            .replace("__PAD__", "200px 50px 220px" if story else "44px 50px")
            .replace("__GAP__", "26" if story else "16")
            .replace("__NAME__", "84" if story else "70")
            .replace("__M__", "400" if story else "300")
            .replace("__NUM__", ("250" if story else "210") if len(fmt(m)) <= 5 else ("200" if story else "170"))
            .replace("__HEAD__", "56" if story else "46")
            .replace("__DECK__", "32" if story else "27")
            .replace("__ART__", "data:image/svg+xml;base64," + base64.b64encode(svg).decode())
            .replace("__N__", esc(fmt(m)))
            .replace("__HEAD_T__", esc(e["head"]))
            .replace("__DECK_T__", deck))


def render(m, out=OUT, since="2026-10-30"):
    out.mkdir(parents=True, exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        for kind, h in (("feed", 1350), ("story", 1920)):
            pg = b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=1)
            pg.set_content(card_html(kind, m), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(500)
            # shrink the headline if a long one crowds the frame
            pg.evaluate("""() => { const f = document.querySelector('.frame'), h = document.querySelector('h1');
              const dk = document.querySelector('.deck');
              let s = parseFloat(getComputedStyle(h).fontSize), t = dk ? parseFloat(getComputedStyle(dk).fontSize) : 0;
              while (f.scrollHeight > f.clientHeight + 1 && dk && t > 22) { t -= 1; dk.style.fontSize = t + 'px'; }
              while (f.scrollHeight > f.clientHeight + 1 && s > 30) { s -= 2; h.style.fontSize = s + 'px'; }
              if (f.scrollHeight > f.clientHeight + 1 && dk) dk.remove(); }""")
            pg.screenshot(path=str(out / f"{kind}.jpg"), type="jpeg", quality=92)
        b.close()
    (out / "caption.txt").write_text(caption(m, since), encoding="utf-8")
    (out / "milestone.txt").write_text(str(m), encoding="utf-8")


def tally():
    req = urllib.request.Request(TALLY, headers=sp.UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def wanted():
    token = os.environ.get("IG_ACCESS_TOKEN", "")
    return ["feed", "story"] + ([] if token.startswith("IG") or not token else ["facebook"])


def gate():
    force = os.environ.get("FORCE", "").replace(",", "").strip()
    if force:
        return int(force), {"since": "2026-10-30"}, f"FORCE: drawing the {int(force):,} milestone"
    d = tally()
    m = crossed(d)
    if not m:
        return 0, d, f"Total Circulation {d.get('total')}: no milestone passed today or yesterday"
    now = sp.now_pacific()
    mins = now.hour * 60 + now.minute
    if not (WINDOW[0] <= mins <= WINDOW[1]):
        return 0, d, f"{fmt(m)} passed; outside 9 AM-8:30 PM Pacific ({now:%H:%M}), will post in the window"
    done = sp.record(f"milestone-{m}")
    if all(done.get(k) for k in wanted()):
        return 0, d, f"{fmt(m)} milestone already posted"
    return m, d, f"Total Circulation {d.get('total')}: {fmt(m)} milestone passed; posting"


def publish(m, dry_run=False):
    token = os.environ.get("IG_ACCESS_TOKEN", "")
    uid = os.environ.get("IG_USER_ID", "") or ("me" if token.startswith("IG") else "")
    cap = (OUT / "caption.txt").read_text(encoding="utf-8")
    if dry_run:
        return f"DRY RUN: {fmt(m)} milestone cards rendered (see the run's artifacts); nothing posted"
    if not token or not uid:
        return "no IG_ACCESS_TOKEN / IG_USER_ID secrets; nothing posted"
    key = f"milestone-{m}"
    done = sp.record(key)
    stamp = str(int(time.time()))
    feed_rel, story_rel = f"cards/{key}-feed-{stamp}.jpg", f"cards/{key}-story-{stamp}.jpg"
    sp.push_files({feed_rel: (OUT / "feed.jpg").read_bytes(), story_rel: (OUT / "story.jpg").read_bytes(),
                   f"cards/{key}-caption.txt": cap.encode()}, f"Cards for the {fmt(m)} milestone")
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
            results["facebook"] = sp.post_facebook(token, sp.RAW + feed_rel, sp.facebook_caption(cap))
        except Exception as err:
            errors.append(f"facebook: {err}")
    if results != done:
        results["at"] = sp.now_pacific().isoformat(timespec="minutes")
        sp.push_files({f"posted/{key}.json": (json.dumps(results, indent=1) + "\n").encode()},
                      f"Posted the {fmt(m)} milestone")
    if errors:
        raise RuntimeError("; ".join(errors))
    return f"POSTED the {fmt(m)} milestone: " + ", ".join(f"{k} {results.get(k)}" for k in wanted())


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    # A drawn-on-request milestone (FORCE) is only ever a look, never a post.
    dry = os.environ.get("DRY_RUN") == "yes" or bool(os.environ.get("FORCE", "").strip())
    try:
        if step == "gate":
            m, d, msg = gate()
            out = os.environ.get("GITHUB_OUTPUT")
            if out:
                with open(out, "a") as f:
                    f.write(f"go={'yes' if m else 'no'}\nmilestone={m}\nsince={d.get('since') or '2026-10-30'}\n")
            sp.report(msg)
        elif step == "render":
            render(int(os.environ["MILESTONE"]), since=os.environ.get("SINCE") or "2026-10-30")
            print((OUT / "caption.txt").read_text(encoding="utf-8"))
        elif step == "publish":
            sp.report(publish(int(os.environ["MILESTONE"]), dry_run=dry))
        else:
            raise SystemExit("usage: milestone_post.py gate|render|publish")
    except Exception as err:  # report, never print the token
        sp.report(f"ERROR: {type(err).__name__}: {err}")
        sys.exit(1)
