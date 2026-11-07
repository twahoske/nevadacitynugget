#!/usr/bin/env python3
"""Send this morning's Nevada City Nugget to Buttondown subscribers.

The 6:25 AM Subscriber Send task mails the morning email to
drafts@mg.buttondown.email, which saves it as a Buttondown draft. This script
(run by .github/workflows/subscriber-send.yml) sends that draft to every
subscriber, once a day, only when all of these hold:

  1. it is between 5:45 and 9:00 AM Pacific (a manual run skips this check),
  2. no email with today's subject has been sent or queued yet,
  3. a draft whose subject is exactly "Nevada City Nugget · <Weekday, Month D, YYYY>" exists,
  4. the folio on https://nevadacitynugget.com/ shows today's date.

Otherwise it changes nothing. Needs the repository secret BUTTONDOWN_API_KEY.
DRY_RUN=yes reports what it would do and sends nothing. WAIT=yes keeps checking
every 2 minutes until it sends, finds it already sent, or the window closes
(GitHub's own cron proved unreliable, so the morning edition's push starts a
waiting run). Standard library only.
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

API = "https://api.buttondown.com/v1"
SITE = "https://nevadacitynugget.com/"
START, END = 5 * 60 + 45, 9 * 60  # Pacific minutes after midnight
LIVE = {"about_to_send", "scheduled", "in_flight", "sent", "partially_sent",
        "resending", "throttled", "paused"}
UA = {"User-Agent": "nevadacitynugget-subscriber-send"}


def today(now=None):
    now = now or datetime.now(ZoneInfo("America/Los_Angeles"))
    return now, f"{now:%A}, {now:%B} {now.day}, {now.year}"


def folio_date(html):
    m = re.search(r'class="folio"[^>]*>(.*?)</div>', html, re.S)
    if not m:
        return None
    bolds = re.findall(r"<b>(.*?)</b>", m.group(1), re.S)
    if not bolds:
        return None
    return " ".join(re.sub(r"<[^>]*>", "", bolds[-1]).split())


def bd(key, path, method="GET", body=None):
    req = urllib.request.Request(
        API + path, method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={"Authorization": "Token " + key, "Content-Type": "application/json", **UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode()
    return json.loads(text) if text else {}


def site_folio():
    url = SITE + "?send-check=" + str(int(time.time()))
    req = urllib.request.Request(url, headers={"Cache-Control": "no-cache", **UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return folio_date(r.read().decode("utf-8", "replace"))


def run(key, now=None, ignore_window=False, dry_run=False, api=bd, folio=site_folio):
    now, date = today(now)
    minutes = now.hour * 60 + now.minute
    if not ignore_window and not (START <= minutes <= END):
        return f"outside the 5:45-9:00 AM window ({now:%H:%M} Pacific); nothing to do"
    if not key:
        return "no BUTTONDOWN_API_KEY secret; nothing sent"
    subject = "Nevada City Nugget · " + date
    q = urllib.parse.urlencode({"ordering": "-creation_date", "excluded_fields": "body"})
    emails = api(key, "/emails?" + q).get("results", [])
    same = [e for e in emails if (e.get("subject") or "").strip() == subject]
    done = next((e for e in same if e.get("status") in LIVE), None)
    if done:
        return f'already {done["status"]}: "{subject}"; nothing sent'
    draft = next((e for e in same if e.get("status") == "draft"), None)
    if not draft:
        return f'no draft titled "{subject}" yet; will look again'
    shown = folio()
    if shown != date:
        return f'site folio shows "{shown}", not "{date}"; draft left alone, will look again'
    if dry_run:
        return f'DRY RUN: would send draft {draft["id"]} "{subject}"'
    api(key, f'/emails/{draft["id"]}', "PATCH", {"status": "about_to_send"})
    return f'SENT: queued draft {draft["id"]} "{subject}" to subscribers'


def run_waiting(key, dry_run=False, pause=120, **kw):
    while True:
        try:
            msg = run(key, dry_run=dry_run, **kw)
        except Exception as err:  # a network blip should not end the wait
            msg = f"error {type(err).__name__}: {err}; will look again"
        print(msg, flush=True)
        if "will look again" not in msg:
            return msg
        now, _ = today()
        if now.hour * 60 + now.minute + pause / 60 > END:
            return msg + " (window closed)"
        time.sleep(pause)


if __name__ == "__main__":
    try:
        key = os.environ.get("BUTTONDOWN_API_KEY", "")
        dry = os.environ.get("DRY_RUN") == "yes"
        if os.environ.get("WAIT") == "yes":
            msg = run_waiting(key, dry_run=dry)
        else:
            msg = run(key, ignore_window=os.environ.get("IGNORE_WINDOW") == "yes", dry_run=dry)
    except Exception as err:  # report, never print the key
        print(f"ERROR: {type(err).__name__}: {err}")
        sys.exit(1)
    print(msg)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write(msg + "\n")
