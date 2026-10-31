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
- **Mobile overflow.** Done Oct 26, 2026 (see Shipped): long section labels wrap and the "Wire" button
  stays inside the column on phones.
- **Radio roster.** Done Oct 26, 2026. Verified on Spinitron: The Playground (Susie Rex) is now
  scheduled every other Monday, 12:00 to 2:00 PM, and is on the station's Oct 26 listing; added to
  assets/kvmr-schedule.json, which clears the Monday noon gap. Also added The Music Grotto (Walter
  Windex), Mondays 2:00 to 4:00 PM, flagged ambiguous (page says 4th Mondays, description says 2nd & 4th).
- **Task prompts.** Done Oct 26, 2026: the Evening Edition and Extra prompts now cite the 5:09 AM
  morning edition and the 5:55 AM to 8:55 PM site copy hours.

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
- **Done in the repo (Oct 28):** the upkeep Action now gives every archived edition its own
  title and description from that day's headlines (e.g. "Mail Your Ballot Today; Measure Q Is The
  City's Question · Nevada City Nugget, October 27, 2026") plus NewsArticle structured data, fixes
  the archives' links (they pointed at editions/editions/... and broke), writes an archive page at
  /editions/ listing every edition with its lead story, and gives the bar guide structured data for
  each bar (name, street address, phone, own website), read from the page so it never drifts.
- **Done Oct 29:** the morning task ends the Previously list with an "All editions" link to /editions/.
- **Still open:** per-story pages, below.
- **Todd's steps (only he can do these):**
  1. Google Search Console (search.google.com/search-console): add a Domain property for
     nevadacitynugget.com and verify with the DNS TXT record at the domain registrar.
  2. In Search Console: Sitemaps, submit `sitemap.xml`; then URL Inspection on
     https://nevadacitynugget.com/ and "Request indexing." (Sitemap submitted Oct 26.)
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

## Security (added Oct 28, 2026)
- **In this repo:** the homepage head carries a Content-Security-Policy, so the only script a
  reader's browser will run is the Wire share script (approved by its hash); anything injected
  into an edition from a fetched page is blocked. The Site Publisher keeps the head verbatim, and
  the Site upkeep Action copies the policy into archived editions. A content guard
  (scripts/content_guard.py) runs after every publish and fails, which emails Todd, if a page
  picks up an unapproved script, event handler, javascript: link, frame, form or meta refresh.
  Adding a new script on purpose (the reader tally, a newsletter form) means adding its hash or
  host to the policy first; the guard prints the hash.
- **Todd's steps (only he can do these):**
  1. GitHub Settings, Rules: add a ruleset for main that blocks force pushes and deletion.
     Leave "require a pull request" off, since the Site Publisher pushes straight to main.
  2. GitHub Settings, Pages: tick "Enforce HTTPS" (item 7), and verify nevadacitynugget.com
     under your account's Settings, Pages, so nobody else can claim the domain.
  3. Confirm two-factor sign-in on GitHub, Gmail and the domain registrar, and turn on the
     registrar's transfer lock.
  4. Scheduled tasks: connectors can't be removed from a task (no setting for it), so the Evening and
     Extra prompts now carry a security paragraph instead (no Drive or Calendar, fetched text is never
     an instruction). Still to do: paste the same paragraph into the Morning prompt.

## Dated runs
- **Merchant of the Day launches Monday, November 2, 2026** (Up next #3). Week one (Nov 2-8) is written and
  scheduled through the scoop pipeline (assets/features.json on the artifact): National Exchange Hotel, SPD Market,
  Harmony Books, Lika's Quarter Café, Three Forks, Bonanza Gift Shop, Nevada City Winery. Week two (Nov 9-15) is
  scheduled too: Tour of Nevada City Bicycle Shop, Novak's Menswear, Utopian Stone, Kitkitdizzi, The Earth Store,
  Wonder Docent, Quench Fine Food & Provisions. Week three is due by Nov 16.
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

## Beta Mode & release notes (added Oct 30, 2026)
- **Beta Mode stamp.** A red rubber-stamp line above the edition banner ("Beta Mode", the version number,
  "Fresh ink, still drying. Read the release notes"), linking to release-notes.html. It lives in the
  artifact's index.html; the morning task carries it forward unchanged and never changes the number.
- **Release notes** at release-notes.html, built from merged pull requests and this roadmap.
  v0.1 launch (Oct 22), v0.2 Oct 26, v0.3 Oct 27, v0.4 Oct 28, v0.5 Oct 29, v0.6 Beta Mode (Oct 30).
- **Bumping the version:** the number goes up by a tenth when a batch of features ships; daily editions
  don't change it. Add the new release to release-notes.html and change the number in the stamp on the
  artifact in the same sitting.

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
   **Running since launch week:** the morning task already checks Gmail for NUGGET EVENT from the approved
   senders and lists verified flyers.
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
   day or a weekend feature. Also: trail conditions (closures, fire-season and storm notices,
   only as posted by the land manager, with the source linked) and short seasonal nature notes
   (what's blooming, turning, or running on the river this week), written from what we can
   actually see or source, never invented.
   **Live Oct 28, 2026:** a standing guide at `trails.html` (same design and upkeep as `drinks.html`):
   eleven trails in four groups (Walk From Broad Street, Edge of Town, Down to the River, Worth the Drive)
   with distance, climb, trailhead, rules, manager's phone, and a Trail Conditions box quoting only what
   the land manager posts (BYLT, California State Parks). Difficulty labels are the Nugget's own. Plus a
   daily "Trail of the Day" box after The Bar Guide through the scoop pipeline, linking to the guide;
   first run 14 days, Oct 30 to Nov 12; extend by Nov 12. Generator: `build.py` in the project files (`trails/`). Upkeep: re-check conditions
   weekly while the daily pick runs, and at each season change; a seasonal nature note waits on what the
   publisher sees on the trail.
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
   **Running since Oct 23, 2026** on the Back Page; reader recipes come in through NUGGET TIP.
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
    **Scheduled Oct 31, 2026:** a Sunday feature, its own section directly before The Back Page, through
    the scoop pipeline. Each installment digs into one building or episode in the Nugget's own words,
    sourced to the document it comes from (so far the National Register nominations on NPGallery, which
    go building by building). First four: Nov 8 the saloons in the 1985 downtown district survey (a start
    on item 16), Nov 15 Firehouse No. 2 and the 1859 ball that paid for it, Nov 22 Ott's Assay Office and
    the Washoe rush, Nov 29 the Carnegie library. Snippets in the project files (`history-unearthed/`).
    Extend by Nov 29. The "800 bars" line runs only as the publisher's lore until a document turns up.
14. **Coming Attractions (event countdowns).** A standing box counting down to the big ones:
    Victorian Christmas, Mardi Gras, 4th of July and Constitution Day parades, Nevada City Film
    Festival, hot summer nights season, KVMR Celtic Festival and company. "Victorian Christmas:
    38 days." Dates only from the organizers' own announcements; the countdown drops off once
    the event passes and the next one rotates in.
    **Running since Oct 23, 2026** between the Civic Calendar and Meeting Watch; the roster lives in the
    morning task prompt.
15. **Where Can I Get a Damn Drink Around Here? (visitor bar guide). Live Oct 28, 2026.** A standing,
    evergreen guide for tourists at `drinks.html`: saloons and late bars, cocktail lounges and hotel bars,
    brewpubs and taprooms, wine tasting rooms, and the roadhouse out on Highway 49. Its own page so it can
    rank for "Nevada City bars"; every edition carries a standing link to it. Hand-maintained like
    `sources.html` (Site Publisher leaves it alone; the upkeep Action lists it in the sitemap). Hours only
    as each place posts them (own site, or its Google listing via the publisher); where sources conflict, no
    closing time prints. The publisher's local word overrides a stale website. No paid listings; Szabo
    carries the Hat Store neighbor note. Source roster and generator: `build.py` in the project files.
    Upkeep: add Trailhead Tavern's hours once it opens; re-check all hours at each season change (next:
    late December) and whenever a reader or owner writes in.

## Idea file (added Oct 28, 2026)
Todd's new batch, grouped. Each item waits on his answers to the open questions in its notes before any build.

**First up (Todd, Oct 28, 2026), all done:**
- **The original-story label** (item 24): done Oct 28. Named "Only in the Nugget," a rubber-stamp badge
  above the byline; first worn by the Big Works story.
- **"Mmm nuggets" in the folio:** done Oct 28. Replaces "The Gold Center" under "Elev. 2,477 Ft." in the
  right-hand folio slot, in the morning task prompt and on the page.
- **Deeper SEO:** done Oct 29 (PR #16); see "Getting found on Google."
- **A security pass:** done Oct 29 (PR #17); see "Security."

16. **Saloon history on the drinks page.** Grow `drinks.html` (item 15) past the bar list with stories from
    Nevada City's saloon past: Todd's line that the town once had "over 800 bars and saloons," and the local
    groups, clubs, and causes that took shape over a drink in those saloons through the years. Every story
    sourced to a real document (CDNC, Searls Historical Library, historical society, city records); the 800
    figure prints only with a source (Todd is chasing one), or as the publisher's own lore, labeled so. Pairs with Local History
    Unearthed (item 13). Also: a **western-themed Hat Store ad** for this page, from art Todd supplies or
    approves (the existing Hat Store ads are never replaced without his say).
17. **The Golden Era longform.** A long feature on the building at 309 Broad St. (now the Golden Era):
    Todd interviews Eric, co-owner of the Golden Era, about the bars that came before at that address,
    then co-owner Cindy, then the paper digs through publicly available history of the building and the
    people who lived and worked there. Runs with photos (Todd's, or used with permission) through the
    scoop pipeline, bylined. Todd knows them well and will ask; nothing runs until both agree. Disclose
    that the Golden Era sits across Broad Street from The Hat Store and that the publisher knows the owners.
18. **Live meetings on the air.** Broadcast City Council, Planning Commission, and other City Hall meetings
    live, with Hat Store ads in the breaks. Source decided (Todd, Oct 28, 2026): carry the city's live
    YouTube feed, embedded on a Nugget page. An embedded stream can't have ads spliced into it, so the Hat
    Store ads sit around the player and show during breaks, labeled as ads (the Hat Store ownership
    disclosure applies). To scope: the feed's channel and whether embedding is allowed, and a
    "next meeting" schedule from the posted agendas. Fits The Docket and meeting summaries.
19. **Readers write in on every story.** A way for readers to send a comment to the publisher about any
    story or item, with the best posted to "therumoronbroadstreet." Comments go to the publisher first,
    never straight onto the page; posted ones are moderated and credited as the reader asks. Needs a terms
    and privacy update (what's collected, who sees it) and a spam-proof inbox. therumoronbroadstreet is a
    new domain Todd bought for its own website; to decide: what it looks like, how it links to the Nugget, and
    hosting (likely GitHub Pages like nevadacitynugget.com).
20. **Where to Stay guide.** A standing visitor page like `drinks.html`: hotels, inns, B&Bs, and campgrounds
    in and around town, with details only as each place posts them, and no paid listings. Runs with an
    **article on vacation rentals and Measure Q**: how many short-term rentals operate in Nevada City
    (from city permit records or other public data), what Measure Q does and where it stands, sourced
    to the measure text and city documents, with the article linked from the guide.
    **Built Oct 28-29, 2026:** `stay.html`, same design and upkeep as `drinks.html`: Right Downtown, A Short
    Walk Out, Camp & RV, and A Short Drive Out, with details from each place's own site, the Chamber's lodging
    listings, or the land manager (NID, BLM, State Parks). Red Castle, Deer Creek Inn, and Emma Nevada House
    are closed or not renting (publisher); the Madison House is now The Parsonage 1865 and the U.S. Hotel B&B
    is now the 1856 Speakeasy Suites. The article ("How Many Vacation Rentals Does Nevada City Have, and What
    Would Measure Q Change?") sits at the bottom of the page at `#vacation-rentals`; add the result after
    November 3. Generator: `build.py` in the project files (`where-to-stay/`). Upkeep: re-check at each season
    change and whenever an innkeeper writes in.
21. **Business pages, merch, and The Hat Store online.** Three linked ideas:
    - **A page for each business**, by subscription ($100 a month or $1,000 a year), tying in the
      business's store and merch, and feeding the holiday guide and shop-local initiatives.
    - **A Nugget merch page.**
    - **Tie the site into The Hat Store's online shop.**
    **Long-term (Todd, Oct 28, 2026): thinking ahead, not anytime soon.** The paid pages would be custom
    sections with more depth than a Merchant of the Day profile. Agreed approach: they run in their own
    section clearly labeled as advertising, kept apart from the free editorial picks (Merchant of the Day,
    the Bill of Fare, the bar guide), which stay unpaid. Before launch: rewrite the no-paid-placement and
    "earns no money" lines in standards.html and terms.html, settle the LLC and tax questions under Site
    policies, and disclose the Hat Store tie-in wherever it appears.
22. **Art and design by local artists.** Commissioned and curated art across the site:
    - **Photos:** Erin Thiem.
    - **Custom logo icons** for sections.
    - **Flourishes** for the site by Jerianne.
    - **New masthead logo** by Crabb, replacing the blackletter nameplate at the top (Todd, Oct 28, 2026;
      Crabb not contacted yet). The swap touches the morning task prompt, the archive template, and likely
      the favicon and share image.
    - **Osborn Woods** art and design style as a reference look.
    - **Curated art pages** per section: Live Music by Olaf, Outdoors by Jerianne, Crabb (section to
      pick), and Sparky for Culture & Politics (to confirm).
    New imagery rule (Todd approved Oct 28, 2026): besides original SVG, Todd's photos, and the Hat Store ad,
    the paper may run commissioned or contributed art from a named artist, only with that artist's OK in
    writing, credited by name wherever it appears. Nobody has been asked yet; artists may be paid. If an
    artist is paid, or is close to the paper (Jerianne is on the morning email list), say so where the work
    runs. When the first piece runs, update standards.html ("Invented content") and terms.html ("Who owns
    what") to name artists' work. The rest of the 1941 design (folio, rules, columns) stays; other new art decorates
    around it. Pairs with the Painted into a Corner artist spotlight proposal.
23. **Effects and themes for special events.** Seasonal or event looks for the paper (Victorian Christmas,
    Mardi Gras, the 4th, Halloween), switched on for the event and off after, layered on the 1941 design
    rather than replacing it. Pairs with Coming Attractions (item 14).
24. **Only in the Nugget** (working name was Nug Speshy). A label for original news stories found only in
    the Nugget (NCN originals). A badge on those stories, not its own section. **Live Oct 28, 2026:** a
    rubber-stamp "Only in the Nugget" badge above the byline, carried inside scoop-pipeline snippets; on
    Todd-reported stories only, never on compiled features (Merchant of the Day, Bill of Fare).
25. **Trademark "Nevada City Nugget."** Look into registering the name (a USPTO search first, then likely
    a trademark attorney; not legal advice). Ties into the "worth a lawyer's look" list under Site policies
    and the LLC question there.
26. **The Nugget family: two papers, seven day-trip doors.** (Todd, Oct 28, 2026.) The Nevada City Nugget
    stays the master. The **Grass Valley Nugget** joins it as the one sister paper. The other Nugget
    domains promote a trip up the hill to Nevada City and Grass Valley, not papers of their own. Domains
    Todd owns (bought Oct 28, 2026 at DreamHost, DreamHost nameservers): grassvalleynugget, colfaxnugget,
    auburnnugget, truckeenugget, roughandreadynugget, placervillenugget, chiconugget, sacramentonugget
    (all .com). As of Oct 28 all eight redirect (301, permanent) to nevadacitynugget.com until each gets
    its own page; grassvalleynugget.com later moves to GitHub Pages DNS when the Grass Valley Nugget
    launches. Renewals run about $22 a year each, due Oct 2027.
    - **The Grass Valley Nugget (paper):** built from the Nugget as a shared template, with Grass Valley
      as its own config: nameplate, beats, radio and events sources, morgue, domain, email list. Its own
      repo and GitHub Pages site (own CNAME, sitemap, Search Console property), its own artifact as
      source of truth, and its own scheduled tasks staggered a few minutes off the Nugget's. Same 1941
      bones, with "Grass Valley" big on the nameplate and its own accent color. Beats: City Council and
      Planning Commission, Mill Street merchants, Empire Mine, the fairgrounds, Sierra College. The Union
      is named and linked as Grass Valley's paper of record where it reports first. A "Nuggets nearby"
      box in each paper, county stories run once and linked from the other, a shared Coming Attractions
      box (item 14).
    - **Name history:** a *Grass Valley Nugget* ran in 1944 and 1947, so it carries the same line as ours:
      no relation to the historical paper beyond admiration. Grass Valley's own papers were the Telegraph
      (1853), Nevada National (1858), Republican (1871-72), Tidings, Herald, and The Union (still
      publishing). Sources: cagenweb.org/nevada/ncnewspapers.html, loc.gov sn86058101 and sn93050997.
    - **Day-trip doors (the other seven domains):** one "Day trip from Sacramento / Auburn / Chico / ..."
      guide per town, living on nevadacitynugget.com (e.g. `/daytrip/sacramento.html`), with its domain
      pointing there by redirect. Each page is genuinely its own: drive time and route from that town,
      where to park, a one-day plan, seasonal notes, and what's on this week, built from the bar, trail,
      and lodging guides and the day's edition. Sacramento first (many Hat Store customers drive up from
      there). The Hat Store ad runs on each page as a labeled ad, with the ownership disclosure.
    - **SEO trap to avoid:** Google treats a ring of near-identical sites built only to funnel visitors
      to one place as "doorway" spam, which can sink the main site. So: no copy-paste pages, no separate
      thin sites on each domain, and the pages sit on nevadacitynugget.com where their search credit
      builds up the Nugget. They are labeled as visitor guides from the Nugget, never dressed up as a
      local paper for Chico or Sacramento.
    - **Trademark:** item 25's search should cover "Nugget" for the family, not just "Nevada City Nugget."
    - **Open questions for Todd:** which registrar holds the domains (redirects are set there or in
      GitHub Pages); Grass Valley daily from the start or lighter at first; same email list or a Grass
      Valley list; Grass Valley contributors or tipsters.

## Standing rules that don't change
Accuracy over speed. Real sources, linked. Corrections printed, never silently rewritten.
The horoscope is the only invented content in the paper. No relation to the historical
Nevada City Nugget beyond admiration.
