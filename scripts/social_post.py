#!/usr/bin/env python3
"""Post this morning's Nugget to Instagram (one feed post and one Story) and to
the Nugget's Facebook Page (the feed card, with clickable links).

Run by .github/workflows/social-post.yml. Once a day, after the website shows
today's date in its folio, it:

  1. reads the lead story and three more headlines from https://nevadacitynugget.com/
     (it skips anything marked Promotional, Courtesy, Sponsored or Paid),
  2. draws a 1080x1350 feed card and a 1080x1920 Story card in the paper's
     1941 style (Playwright + Chromium),
  3. pushes both JPEGs to the social-cards branch, which Instagram fetches
     from raw.githubusercontent.com (main and the website are never touched),
  4. publishes them with Meta's official Instagram content-publishing API, and
     posts the feed card to the Facebook Page (Page tokens only; needs the
     pages_manage_posts permission),
  5. records what it posted in social-cards:posted/YYYY-MM-DD.json, so a day is
     never posted twice, and a half-finished day (feed done, Story failed) only
     retries the missing part.

Steps (each is a subcommand, so the workflow can skip the browser install on
the many hourly runs that have nothing to do):

  gate     decide whether today still needs posting; with WAIT=yes keep looking
           every 2 minutes until the site shows today's paper or the window closes
  render   draw out/feed.jpg, out/story.jpg and write out/caption.txt
  publish  push the cards, post them, record the result

Window: 5:45-10:00 AM Pacific (a manual run skips the window check).
Secrets: IG_ACCESS_TOKEN and IG_USER_ID. A token that starts with "IG" (Instagram
Login) goes to graph.instagram.com; any other (a Facebook Page token) goes to
graph.facebook.com. DRY_RUN=yes renders and reports, and pushes or posts nothing.
"""
import html as htmlmod
import json
import os
import pathlib
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

SITE = "https://nevadacitynugget.com/"
REPO = "twahoske/nevadacitynugget"
BRANCH = "social-cards"
RAW = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/"
GRAPH_VERSION = "v23.0"
START, END = 5 * 60 + 45, 10 * 60  # Pacific minutes after midnight
UA = {"User-Agent": "nevadacitynugget-social-post"}
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "out"
SKIP_META = re.compile(r"promotional|courtesy|sponsored|paid", re.I)
SKIP_HEAD = re.compile(r"^(otherwise|quiet\b)|\bquiet record\b", re.I)
HASHTAGS = "#NevadaCity #NevadaCityCA #NevadaCounty #GoldCountry #LocalNews"


# ---------------------------------------------------------------- reading the paper

def now_pacific():
    return datetime.now(ZoneInfo("America/Los_Angeles"))


def long_date(now):
    return f"{now:%A}, {now:%B} {now.day}, {now.year}"


def text(fragment):
    return " ".join(htmlmod.unescape(re.sub(r"<[^>]*>", " ", fragment)).split())


def fetch_site():
    url = SITE + "?social-check=" + str(int(time.time()))
    req = urllib.request.Request(url, headers={"Cache-Control": "no-cache", **UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def folio(page):
    """(volume line, date) from the folio; the date is the last <b> (house rule)."""
    m = re.search(r'class="folio"[^>]*>(.*?)</div>', page, re.S)
    if not m:
        return None, None
    bolds = [text(b) for b in re.findall(r"<b>(.*?)</b>", m.group(1), re.S)]
    if not bolds:
        return None, None
    return (bolds[0] if len(bolds) > 1 else ""), bolds[-1]


def stories(page):
    """Headlines in paper order: dicts with meta, head, deck."""
    found, seen = [], set()
    for body in re.findall(r"<article\b[^>]*>(.*?)</article>", page, re.S):
        h = re.search(r"<h3[^>]*>(.*?)</h3>", body, re.S)
        if not h:
            continue
        head = text(h.group(1))
        meta_m = re.search(r'<p class="meta">(.*?)</p>', body, re.S)
        meta = text(meta_m.group(1)) if meta_m else ""
        deck_m = re.search(r'<p class="subdeck">(.*?)</p>', body, re.S)
        deck = text(deck_m.group(1)) if deck_m else ""
        if (len(head) < 12 or head in seen or SKIP_META.search(meta) or SKIP_HEAD.search(head)
                or re.match(r"^(Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day,", head)):
            continue
        seen.add(head)
        found.append({"meta": meta, "head": head, "deck": deck})
    return found


def clip(s, n):
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0].rstrip(" ,;:·")
    return cut + "…"


def caption(vol, date, lead, more):
    lines = [f"{date}" + (f" · {vol}" if vol else ""), "", lead["head"]]
    if lead["deck"]:
        lines.append(lead["deck"])
    if more:
        lines += ["", "Also in today's paper:"] + [f"❦ {s['head']}" for s in more]
    lines += ["", "Read the whole paper free at nevadacitynugget.com (link in bio). New every morning by 6.",
              "", HASHTAGS]
    return "\n".join(lines).replace("—", ",")[:2100]


# ---------------------------------------------------------------- the cards

CARD = """<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Besley:ital,wght@0,400;0,600;0,700;0,800;0,900;1,400;1,600&family=Grenze+Gotisch:wght@900&display=swap">
<style>
:root{--paper:#f0ead9;--ink:#201c13;--soft:#5f5743;--mid:#564e3b;--rule:#9c927a;--red:#7e2a18;--d:"Besley",Georgia,serif}
html,body{margin:0}
.pg{width:1080px;height:__H__px;box-sizing:border-box;background:var(--paper);background-image:radial-gradient(ellipse at 50% 0%,rgba(0,0,0,.05),transparent 65%);color:var(--ink);padding:__PAD__;display:flex;flex-direction:column;position:relative;font-family:var(--d)}
.pg::before{content:"";position:absolute;inset:22px;border:3px solid var(--ink);outline:1.5px solid var(--ink);outline-offset:-10px}
.banner{text-align:center;font-weight:900;font-size:22px;letter-spacing:.34em;text-transform:uppercase;border-top:3px solid var(--ink);border-bottom:3px solid var(--ink);padding:8px 0}
h1{font-family:"Grenze Gotisch",var(--d);font-weight:900;font-size:118px;line-height:.95;margin:22px 0 0;text-align:center;white-space:nowrap}
.folio{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;column-gap:18px;border-top:3px solid var(--ink);border-bottom:1.5px solid var(--ink);padding:9px 4px;margin-top:16px;font-size:17px;letter-spacing:.08em;text-transform:uppercase}
.folio b{font-weight:800}.f-r{text-align:right}.f-c{text-align:center;padding:0 22px;border-inline:1.5px solid var(--rule)}
.body{flex:1;display:flex;flex-direction:column;justify-content:center;min-height:0}
.kick{text-align:center;color:var(--red);font-weight:800;font-size:24px;letter-spacing:.16em;text-transform:uppercase}
.head{text-align:center;font-weight:900;font-size:__HS__px;line-height:1.02;letter-spacing:-.01em;margin:16px 0 0}
.deck{text-align:center;font-style:italic;font-weight:600;font-size:32px;line-height:1.25;color:var(--mid);margin:20px 20px 0}
.also{margin-top:34px;border-top:1.5px solid var(--ink);padding-top:16px}
.also p.k{margin:0 0 10px;text-align:center;font-weight:800;font-size:20px;letter-spacing:.24em;text-transform:uppercase}
.also ul{list-style:none;margin:0;padding:0}
.also li{font-size:28px;line-height:1.25;font-weight:600;padding:9px 0 9px 42px;position:relative;border-bottom:1px solid var(--rule)}
.also li::before{content:"❦";position:absolute;left:4px;top:8px;color:var(--red)}
.foot{border-top:3px solid var(--ink);padding-top:14px;margin-top:22px;text-align:center;font-weight:800;font-size:30px;letter-spacing:.12em;text-transform:uppercase}
.foot small{display:block;font-weight:400;font-style:italic;font-size:22px;letter-spacing:.03em;text-transform:none;color:var(--mid);margin-top:4px}
</style></head><body><div class="pg" id="pg">
<div class="banner">A Modern-Vintage Daily Paper</div>
<h1>Nevada City Nugget</h1>
<div class="folio"><span><b>__VOL__</b></span><span class="f-c"><b>__DATE__</b></span><span class="f-r"><b>Nevada City</b></span></div>
<div class="body" id="body">
<div class="kick">__KICK__</div>
<div class="head" id="head">__HEAD__</div>
__DECK__
__ALSO__
</div>
<div class="foot">Read Today's Paper Free<small>nevadacitynugget.com · link in bio · new every morning by 6</small></div>
</div></body></html>"""

FIT = """() => {
  const body = document.getElementById('body'), head = document.getElementById('head');
  let size = parseFloat(getComputedStyle(head).fontSize);
  const start = size;
  const items = [...document.querySelectorAll('.also li')];
  let guard = 0;
  while (body.scrollHeight > body.clientHeight + 1 && guard++ < 200) {
    const d = document.querySelector('.deck');
    if (size > 64) { size -= 4; head.style.fontSize = size + 'px'; }
    else if (d) { d.remove(); }
    else if (items.length > 1) { items.pop().remove(); }
    else break;
  }
  while (size < start) {  // after a cut, grow the headline back into the room
    head.style.fontSize = (size + 2) + 'px';
    if (body.scrollHeight > body.clientHeight + 1) { head.style.fontSize = size + 'px'; break; }
    size += 2;
  }
  return {size, left: document.querySelectorAll('.also li').length};
}"""


def card_html(kind, vol, date, lead, more):
    e = htmlmod.escape
    story = kind == "story"
    deck = f'<div class="deck">{e(clip(lead["deck"], 120 if kind == "feed" else 170))}</div>' if lead["deck"] else ""
    also = ""
    if more:
        also = ('<div class="also"><p class="k">Also in Today\'s Paper</p><ul>'
                + "".join(f"<li>{e(clip(s['head'], 90))}</li>" for s in more) + "</ul></div>")
    kick = clip(lead["meta"].split("·")[0].strip(), 40) or "Today's Lead"
    return (CARD.replace("__H__", "1920" if story else "1350")
            .replace("__PAD__", "250px 74px 250px" if story else "56px 74px 58px")
            .replace("__HS__", "96" if story else "80")
            .replace("__VOL__", e(vol or "Daily"))
            .replace("__DATE__", e(date))
            .replace("__KICK__", e(kick))
            .replace("__HEAD__", e(lead["head"]))
            .replace("__DECK__", deck)
            .replace("__ALSO__", also))


def render(page=None):
    page = page or fetch_site()
    vol, date = folio(page)
    found = stories(page)
    if not found:
        raise SystemExit("no headlines found on the site; nothing rendered")
    lead, more = found[0], found[1:4]
    OUT.mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
        for kind, h in (("feed", 1350), ("story", 1920)):
            pg = b.new_page(viewport={"width": 1080, "height": h}, device_scale_factor=1)
            pg.set_content(card_html(kind, vol, date, lead, more), wait_until="networkidle")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(500)
            fit = pg.evaluate(FIT)
            pg.screenshot(path=str(OUT / f"{kind}.jpg"), type="jpeg", quality=92)
            print(f"{kind}: headline {fit['size']}px, {fit['left']} more headlines")
        b.close()
    (OUT / "caption.txt").write_text(caption(vol, date, lead, more), encoding="utf-8")
    (OUT / "date.txt").write_text(date, encoding="utf-8")
    print(caption(vol, date, lead, more))


# ---------------------------------------------------------------- the record branch

def git(*args, check=True, cwd=None):
    return subprocess.run(["git", *args], cwd=cwd or ROOT, check=check,
                          capture_output=True, text=True).stdout.strip()


def record(day):
    """Today's record from the social-cards branch, or {} if none."""
    git("fetch", "--depth=1", "origin", f"{BRANCH}:refs/remotes/origin/{BRANCH}", check=False)
    out = subprocess.run(["git", "show", f"origin/{BRANCH}:posted/{day}.json"], cwd=ROOT,
                         capture_output=True, text=True)
    return json.loads(out.stdout) if out.returncode == 0 else {}


def push_files(files, message):
    """Commit files ({path: bytes}) to the social-cards branch and push."""
    work = ROOT / ".social-cards"
    if not work.exists():
        exists = subprocess.run(["git", "rev-parse", "--verify", f"origin/{BRANCH}"], cwd=ROOT,
                                capture_output=True).returncode == 0
        if exists:
            git("worktree", "add", str(work), f"origin/{BRANCH}")
            git("checkout", "-B", BRANCH, cwd=work)
        else:
            git("worktree", "add", "--detach", str(work))
            git("checkout", "--orphan", BRANCH, cwd=work)
            git("rm", "-rf", "--quiet", ".", cwd=work)
            (work / "README.md").write_text(
                "Daily Instagram cards and post records for nevadacitynugget.com.\n"
                "Written by .github/workflows/social-post.yml on main. Not part of the website.\n")
    for rel, data in files.items():
        path = work / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    git("add", "-A", cwd=work)
    if not git("status", "--porcelain", cwd=work):
        return
    git("-c", "user.name=github-actions[bot]",
        "-c", "user.email=41898282+github-actions[bot]@users.noreply.github.com",
        "commit", "-m", message, cwd=work)
    for attempt in range(5):
        if subprocess.run(["git", "push", "origin", f"HEAD:{BRANCH}"], cwd=work).returncode == 0:
            return
        subprocess.run(["git", "pull", "--rebase", "origin", BRANCH], cwd=work)
        time.sleep(3 * (attempt + 1))
    raise RuntimeError("could not push to the social-cards branch")


# ---------------------------------------------------------------- Instagram

def graph(token, path, params=None, method="GET"):
    base = "https://graph.instagram.com" if token.startswith("IG") else "https://graph.facebook.com"
    params = dict(params or {}, access_token=token)
    url = f"{base}/{GRAPH_VERSION}/{path}"
    data = None
    if method == "GET":
        url += "?" + urllib.parse.urlencode(params)
    else:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        try:
            detail = json.loads(detail)["error"]["message"]
        except Exception:
            pass
        raise RuntimeError(f"Instagram said {err.code}: {detail}") from None


def post(token, uid, image_url, caption_text=None, story=False):
    params = {"image_url": image_url}
    if story:
        params["media_type"] = "STORIES"
    else:
        params["caption"] = caption_text
    cid = graph(token, f"{uid}/media", params, "POST")["id"]
    for _ in range(30):  # Instagram fetches the image; wait until it is ready
        status = graph(token, cid, {"fields": "status_code"}).get("status_code")
        if status == "FINISHED":
            break
        if status in ("ERROR", "EXPIRED"):
            raise RuntimeError(f"Instagram could not prepare the {'Story' if story else 'post'} ({status})")
        time.sleep(4)
    return graph(token, f"{uid}/media_publish", {"creation_id": cid}, "POST")["id"]


# ---------------------------------------------------------------- steps

def wanted():
    """What a finished day holds: Instagram feed + Story, plus the Facebook Page
    when the token is a Facebook Page token (Instagram Login tokens start "IG")."""
    token = os.environ.get("IG_ACCESS_TOKEN", "")
    return ["feed", "story"] + ([] if token.startswith("IG") or not token else ["facebook"])


def facebook_caption(cap):
    """Facebook makes links clickable, so point straight at the paper."""
    return cap.replace("nevadacitynugget.com (link in bio)", "https://nevadacitynugget.com")


def post_facebook(token, image_url, message):
    page = graph(token, "me", {"fields": "id"})["id"]
    res = graph(token, f"{page}/photos", {"url": image_url, "message": message}, "POST")
    return res.get("post_id") or res["id"]


def in_window(now):
    m = now.hour * 60 + now.minute
    return START <= m <= END


def gate(wait=False, ignore_window=False, pause=120):
    while True:
        now = now_pacific()
        day = now.strftime("%Y-%m-%d")
        if not ignore_window and not in_window(now):
            return False, f"outside the 5:45-10:00 AM window ({now:%H:%M} Pacific); nothing to do"
        done = record(day)
        if all(done.get(k) for k in wanted()):
            return False, f"already posted for {day}; nothing to do"
        try:
            _, shown = folio(fetch_site())
        except Exception as err:
            shown = f"error {type(err).__name__}"
        if shown == long_date(now):
            return True, f"site shows {shown}; posting"
        msg = f'site folio shows "{shown}", not "{long_date(now)}"'
        if not wait or now.hour * 60 + now.minute + pause / 60 > END:
            return False, msg + "; nothing posted"
        print(msg + "; will look again", flush=True)
        time.sleep(pause)


def publish(dry_run=False):
    token = os.environ.get("IG_ACCESS_TOKEN", "")
    uid = os.environ.get("IG_USER_ID", "") or ("me" if token.startswith("IG") else "")
    day = now_pacific().strftime("%Y-%m-%d")
    cap = (OUT / "caption.txt").read_text(encoding="utf-8")
    if dry_run:
        return "DRY RUN: cards rendered (see the run's artifacts); nothing pushed or posted"
    if not token or not uid:
        return "no IG_ACCESS_TOKEN / IG_USER_ID secrets yet; cards rendered, nothing posted"
    done = record(day)
    stamp = str(int(time.time()))
    feed_rel, story_rel = f"cards/{day}-feed-{stamp}.jpg", f"cards/{day}-story-{stamp}.jpg"
    push_files({feed_rel: (OUT / "feed.jpg").read_bytes(), story_rel: (OUT / "story.jpg").read_bytes(),
                f"cards/{day}-caption.txt": cap.encode()}, f"Cards for {day}")
    time.sleep(20)  # let raw.githubusercontent.com see the new files
    results, errors = dict(done), []
    if not done.get("feed"):
        try:
            results["feed"] = post(token, uid, RAW + feed_rel, cap)
        except Exception as err:
            errors.append(f"feed: {err}")
    if not done.get("story"):
        try:
            results["story"] = post(token, uid, RAW + story_rel, story=True)
        except Exception as err:
            errors.append(f"story: {err}")
    if "facebook" in wanted() and not done.get("facebook"):
        try:
            results["facebook"] = post_facebook(token, RAW + feed_rel, facebook_caption(cap))
        except Exception as err:
            errors.append(f"facebook: {err}")
    if results != done:
        results["at"] = now_pacific().isoformat(timespec="minutes")
        push_files({f"posted/{day}.json": (json.dumps(results, indent=1) + "\n").encode()},
                   f"Posted {day}")
    if errors:
        raise RuntimeError("; ".join(errors))
    return (f"POSTED {day}: feed {results.get('feed')}, Story {results.get('story')}"
            + (f", Facebook {results.get('facebook')}" if "facebook" in wanted() else ""))


def report(msg):
    print(msg)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write(msg + "\n")


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    dry = os.environ.get("DRY_RUN") == "yes"
    try:
        if step == "gate":
            go, msg = gate(wait=os.environ.get("WAIT") == "yes",
                           ignore_window=os.environ.get("IGNORE_WINDOW") == "yes")
            out = os.environ.get("GITHUB_OUTPUT")
            if out:
                with open(out, "a") as f:
                    f.write(f"go={'yes' if go or dry else 'no'}\n")
            report(msg)
        elif step == "render":
            render()
        elif step == "publish":
            report(publish(dry_run=dry))
        else:
            raise SystemExit("usage: social_post.py gate|render|publish")
    except Exception as err:  # report, never print the token
        report(f"ERROR: {type(err).__name__}: {err}")
        sys.exit(1)
