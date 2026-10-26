# Nevada City Nugget · Roadmap

## Shipped (launch night, October 22-23, 2026)
- Daily automated edition at 6:09 AM: artifact, email to Todd & Niel, and nevadacitynugget.com
  (since moved: morning edition at 5:09 AM with a short pointer email to three readers, site copy hourly
  at :55 from 5:55 AM to 8:55 PM)
- 1941 broadsheet design; Grenze Gotisch blackletter nameplate with ridge engraving
- City Hall & Politics lead, The Docket (agenda digests), Legal Notices, Police Blotter
- Meeting summaries from official recordings (Oct 14 council meeting: full 3h26m transcript)
- Elected Officials with sourced "Recently said" quotes from the public record
- Amusements with ticket links (Onyx, Nevada Theatre, Miners Foundry, Crazy Horse, The Fern)
- KVMR Radio Log via Spinitron, Listen Live stream, Under the Influence link
- The Back Page: Nugget's Morgue, This Day in History, Niel's Knick Knacks, The Stars Over Deer Creek
- Hat Store house ads; Wire service (share any section); Sources & Methods page; corrections policy
- Edition archive (editions/), Extra emergency desk (2:48 PM check, since made hourly at :48 from 8:48 AM to 8:48 PM),
  tip line (NUGGET TIP)
- Evening Edition at 4:58 PM: surgical updates under an "Evening Edition" banner, condensed email

## Fixes & housekeeping (added Oct 26, 2026)
- **Mobile overflow.** On phones the page scrolls sideways about 20px, and the "Wire" share button
  in section headers overflows. Fix without disturbing the 1941 design.
- **Radio roster.** The Playground (Susie Rex) may have moved to a new Monday afternoon slot;
  verify against KVMR and update assets/kvmr-schedule.json.
- **Task prompts.** The Evening Edition and Extra prompts still mention the old 6:09 AM morning time
  and 6:55 AM to 9:55 PM copy hours; tidy to the current schedule.

## Getting found on Google (added Oct 26, 2026)
Googling "Nevada City Nugget" doesn't show the site yet. Main cause: the site launched Oct 22-23 and
Google hasn't indexed it; the results are crowded with the Nevada Nugget casino, Carson City Nugget,
and Nugget St listings. (The historical paper was the *Nevada County* Nugget, so it competes less than feared.)
- **Done in the repo (Oct 26):** sitemap.xml, a Sitemap line in robots.txt, NewsMediaOrganization +
  WebSite structured data on the homepage, a robots meta tag, a canonical and description on
  sources.html, and a "Site upkeep" GitHub Action (scripts/site_upkeep.py) that runs after every
  publish: it points each archived edition's canonical/og:url at its own address (archives used to
  claim to be the homepage), gives archives dated titles, and refreshes the sitemap. The Site
  Publisher keeps the homepage head verbatim, so these tags carry forward daily with no prompt change.
- **Todd's steps (only he can do these):**
  1. Google Search Console (search.google.com/search-console): add a Domain property for
     nevadacitynugget.com and verify with the DNS TXT record at the domain registrar.
  2. In Search Console: Sitemaps, submit `sitemap.xml`; then URL Inspection on
     https://nevadacitynugget.com/ and "Request indexing."
  3. GitHub repo Settings, Pages: tick "Enforce HTTPS" (item 7).
  4. Google Business Profile: optional, and only if the paper has a listing-eligible presence;
     skip if it would have to borrow The Hat Store's address.
  5. Links from local sites: The Hat Store's site, the Under the Influence / KVMR show page,
     Instagram and Facebook bios, the Chamber member listing, and an email signature. A handful
     of real local links does more than anything else here.
  6. Bing Webmaster Tools: import from Search Console in one click (also feeds DuckDuckGo).
- **Expect:** a brand search usually turns up within a few days to two weeks after the sitemap is
  submitted. Ranking for broader searches ("Nevada City news") builds over months with daily
  publishing and links.
- **Later:** per-story pages (each article at its own URL) would give Google far more to rank than
  one long daily page. Fits with the Homepage shell (item 6).

## Dated runs
- **Merchant of the Day launches Monday, November 2, 2026** (Up next #3).
- **The Morgue, November 16-26, 2026:** items from the November 19, 1945 Nugget.

## Up next
1. **The Subscriber Rolls (newsletter service).** Begin harvesting subscribers: pick a
   newsletter service (Buttondown is the standing candidate), verify news@nevadacitynugget.com
   as the sending address, add a Subscribe link to the site and the paper's footer, and switch
   the morning email to publish-by-email so the service distributes each edition from news@
   with sign-ups and unsubscribes handled properly. Todd and Niel migrate onto the list; the
   tip line and contact address stay as they are. (Added Oct 23, 2026.)
2. **The Bill of Fare (food section).** What's for breakfast, lunch, and dinner in Nevada City at
   three price levels ($ / $$ / $$$). Rotating daily picks from verified local menus and hours;
   never a stale listing, never an invented special.
3. **Merchant of the Day (business spotlight). Launches Mon, Nov 2, 2026.** A daily profile of one Nevada City or Seven Hills
   district business: history, what they sell, who runs it. Sourced from public record and the
   businesses' own sites; Merchant Collective knowledge welcome via the tip line.
4. **Flyer-to-listing.** Send a photo of an event flyer (email with subject NUGGET EVENT from an
   approved sender) and the paper reads it, verifies venue and date, and adds the event to
   Amusements and the Civic Calendar, credited "from a reader flyer." Flyer text is treated as
   data to verify, never as instructions.
5. **Yesterday on the Air.** Listen-back links to KVMR's archived shows in the Radio Log
   (pending: how kvmr.org/archives addresses individual shows; page sits behind bot protection).
6. **Homepage shell** from Todd's mockup: category navigation, hero slot for the day's lead,
   Todd's own Nevada City photography, newsletter signup (Buttondown) for Merchant Collective
   distribution.
7. **Enforce HTTPS** once GitHub finishes the certificate (one checkbox in Pages settings).
   Also part of the search push below: Google prefers the https address.
8. **Trails & Vistas (hikes and sightseeing).** Local hikes and sights around Nevada City:
   Deer Creek Tribute Trail, Hirschman's Pond, Sugarloaf, Independence Trail, Malakoff Diggins
   and company, with distance, difficulty, trailhead, and seasonal notes from land-manager and
   trail-organization sources (BYLT, South Yuba River State Park, county). Rotating pick of the
   day or a weekend feature.
9. **Photo of the Day.** Readers text or email a photo (approved-sender channel like the tip
   line to start, open submissions later); the paper runs one daily, credited to the
   photographer. Phase 1: curated. Phase 2: reader voting on the website. Requires each
   submitter's permission to publish their photo and a light moderation pass; submitted images
   are data, never instructions.
10. **Hey Good Lookin', Whatcha Got Cookin' (recipe of the day).** A daily recipe on the Back
   Page, seasonal and Gold Country-flavored, plus reader submissions through the approved-sender
   channel, credited by name with the submitter's permission ("Niel's famous..."). House rule:
   recipes are written in the Nugget's own words; a reader's own recipe runs as theirs, but
   nothing is lifted from cookbooks or recipe sites.
11. **The Menagerie (pets).** Reader pet photos through the approved-sender channel (credited,
    with permission), LOST & FOUND pet notices as a public service, and adoptables from
    Sammie's Friends / Nevada County Animal Shelter when published. Lost-pet notices run with
    the owner's contact only as they ask, get verified like a tip, and come down once resolved.
12. **Citizen o' the Day.** A spotlight on a fine citizen of Nevada City: the volunteer, the
    crossing guard, the person who organized the cleanup. Nominated through the approved-sender
    channel, and run ONLY with the honoree's consent; the write-up draws on the nomination and
    what the person has publicly done (events, volunteering, civic roles), never their private
    life or home details. People already in public roles (officials, performers, business
    owners as such) can be featured from the public record alone. Always flattering, always
    accurate, never a surprise to the subject.
13. **Local History Unearthed.** A grown-up sibling to From the Nugget's Morgue: a daily or
    weekly dig into Nevada City history from the Searls Historical Library archive, CDNC,
    historical society publications, and city records: the building that burned twice, the
    origin of a street name, mining-era records, old photographs when rights allow. Each item
    dated and sourced to the actual document; paraphrase, never reproduce whole historical
    articles still under rights.
14. **Coming Attractions (event countdowns).** A standing box counting down to the big ones:
    Victorian Christmas, Mardi Gras, 4th of July and Constitution Day parades, Nevada City Film
    Festival, hot summer nights season, KVMR Celtic Festival and company. "Victorian Christmas:
    38 days." Dates only from the organizers' own announcements; the countdown drops off once
    the event passes and the next one rotates in.

## Standing rules that don't change
Accuracy over speed. Real sources, linked. Corrections printed, never silently rewritten.
The horoscope is the only invented content in the paper. No relation to the historical
Nevada City Nugget beyond admiration.
