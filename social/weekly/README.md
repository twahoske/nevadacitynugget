# Saturday "This Weekend" posts

`.github/workflows/social-extras.yml` posts on Saturday mornings (about 9 AM Pacific)
only when `social/weekly/YYYY-MM-DD.json` exists for that Saturday. Thursday
(Thirsty Thursday, from the Bar Guide) and Friday (the Geezer Gig) need no file.

Fields (all text, no em-dashes, facts only from sources seen):

    {
      "kick": "This Weekend",                 red tag
      "head": "Live Music Tonight",           big headline
      "deck": "One-line italic summary",
      "detail": "Saturday, Nov. 21",          small caps line
      "items_label": "On the Bill",
      "items": ["Band · Venue · 9 PM", ...],  up to 4 on the card
      "caption": "Full Instagram/Facebook caption, with sources and hashtags"
    }
