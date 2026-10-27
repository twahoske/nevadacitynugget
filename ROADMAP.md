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
- Mobile overflow fixed (Oct 26, 2026): long section labels now wrap and the "Wire" button stays
  inside the column on phones; no sideways scroll from 320px to 414px wide

## Fixes & housekeeping (added Oct 26, 2026)
- **Mobile overflow.** On phones the page scrolls sideways about 20px, and the "Wire" share button
  in section headers overflows. Fix without disturbing the 1941 design.
- **Radio roster.** Done Oct 26, 2026. Verified on Spinitron: The Playground (Susie Rex) is now
  scheduled every other Monday, 12:00 to 2:00 PM, and is on the station's Oct 26 listing; added to
  assets/kvmr-schedule.json, which clears the Monday noon gap. Also added The Music Grotto (Walter
  Windex), Mondays 2:00 to 4:00 PM, flagged ambiguous (page says 4th Mondays, description says 2nd & 4th).
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

## Site policies (added Oct 27, 2026)
- **Standards & Disclosures, Privacy, and Terms of Use pages** (standards.html, privacy.html, terms.html), in the
  Sources & Methods design. Standards covers ownership (The Hat Store), no paid placement, how the paper is made ("set by machine,
  checked by hand"), accuracy, corrections, tips, and accessibility. Privacy reflects what the site actually does: no
  cookies, analytics, or trackers; GitHub Pages logs visitor IPs; Google Fonts serves the type; reader email handled
  via Gmail and Claude. Terms covers sharing and quoting, reader submissions, the not-an-alert-system notice, and
  California law. Linked from sources.html, the sitemap, and the homepage structured data.
- **To go live after merge:** add a standing footer disclaimer ("Compiled by our digital overlords, checked by hand,
  and meant to inform and amuse. Mistakes happen; corrections run at the bottom of the next edition.") and a link line
  (Standards & Disclosures · Privacy · Terms of Use) to the
  morning task prompt and today's artifact; publish the three pages to the artifact as supporting files like
  sources.html; add them to the Site Publisher's do-not-touch list.
- **Before the newsletter launches (Up next #1):** update privacy.html to name the service and what it records.
- **Worth a lawyer's look (not legal advice):** the liability and governing-law clauses, a DMCA designated agent
  before reader photos open (Photo of the Day), the machine-compilation disclosure wording, and whether to form an LLC (or a nonprofit) and carry media
  liability insurance; the pages say "the publisher" until then. The CCPA's business
  thresholds ($26.625M revenue, 100,000+ consumers, or selling data) almost certainly don't reach the Nugget today;
  CalOPPA's posted-privacy-policy rule does, and privacy.html is written to meet it.

## Dated runs
- **Merchant of the Day launches Monday, November 2, 2026** (Up next #3). Week one (Nov 2-8) is written and
  scheduled through the scoop pipeline (assets/features.json on the artifact): National Exchange Hotel, SPD Market,
  Harmony Books, Lika's Quarter Café, Three Forks, Bonanza Gift Shop, Nevada City Winery. Week two is due by Nov 9.
- **The Bill of Fare, October 29 to November 11, 2026** (Up next #2): first two weeks scheduled; extend by Nov 11.
- **The Morgue, November 16-26, 2026:** items from the November 19, 1945 Nugget.
- **Arts & Culture, October 27 to November 9, 2026:** "Sparky Parker Goes Big On Broad Street,"
  Todd's interview with David "Sparky" Parker on his Big Works show at Szabo Vineyards Tasting Room,
  316 Broad St., with six photos used with the artist's permission. First scoop through the pipeline below.

## The scoop pipeline (added Oct 26, 2026)
How the publisher's own reporting gets into the paper on a schedule, and stays there.
- **Write it interactively.** Todd sends his interview notes, photos, and links in a project thread.
  Claude writes the finished section in the paper's design (byline, quotes lightly trimmed and never
  altered in meaning, only the links Todd supplied, house rules), with photos downscaled, stripped of
  metadata, and embedded as data URIs in a .photoset so they work on the artifact, the website, and
  in the archive with no extra files.
- **Schedule it.** The section is stored on the artifact as assets/features/<id>.html and listed in
  assets/features.json with start and end dates (inclusive, Pacific), a placement, and whether the
  first-day email mentions it.
- **Run it.** Each morning edition splices every active entry in verbatim with the shell (never
  retyped); the Evening Edition leaves it untouched and re-splices it if the morning missed it; the
  site copy needs no change. A feature drops off after its end date and stays in the archived editions.
- **Next:** a short "Now showing" index of active features in Coming Attractions or the footer, and
  a reader-facing note on Sources & Methods that publisher-reported stories carry a byline.

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
   **Launches Thu, Oct 29, 2026.** A daily grid (breakfast, lunch, dinner at $ / $$ / $$$) runs directly after
   Amusements through the scoop pipeline, one snippet per day, rotating evenly among about two dozen places open
   that day. Hours and prices come from each restaurant's own site or menu, or its Google listing via the publisher;
   an empty cell says so rather than guessing. Tiers: $ = most plates under $15, $$ = $15 to $30, $$$ = mains over $30.
   Disclosures: no one pays to appear; the publisher owns The Hat Store; Java John's was co-founded by the publisher's
   husband (sold 2002, no stake). Scheduled Oct 29 to Nov 11; the next run needs hours re-checked (winter hours shift).
3. **Merchant of the Day (business spotlight). Launches Mon, Nov 2, 2026.** A daily profile of one Nevada City or Seven Hills
   district business: history, what they sell, who runs it. Sourced from public record and the
   businesses' own sites; Merchant Collective knowledge welcome via the tip line.
   **Built Oct 27, 2026:** each profile runs as a one-day feature directly after the Police Blotter, ends with a
   "Pay a visit" box (hours only as the business posts them) and a standing line that no one pays to appear and
   that the publisher owns The Hat Store. No task prompt change needed; new weeks are added in an interactive session.
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
8. **Nature & Hikes (Trails & Vistas).** Todd asked for a nature and hikes section (Oct 27, 2026);
   it grows the earlier Trails & Vistas idea. Local hikes and sights around Nevada City:
   Deer Creek Tribute Trail, Hirschman's Pond, Sugarloaf, Independence Trail, Malakoff Diggins
   and company, with distance, difficulty, trailhead, and seasonal notes from land-manager and
   trail-organization sources (BYLT, South Yuba River State Park, county). Rotating pick of the
   day or a weekend feature. Also: trail conditions (closures, fire-season and storm notices,
   only as posted by the land manager, with the source linked) and short seasonal nature notes
   (what's blooming, turning, or running on the river this week), written from what we can
   actually see or source, never invented.
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
