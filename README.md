# Allan's ABC

Website and brand repository for **Allan's ABC** (ABC - Allan's Breakfast Club & Wine Bar),
Rykestraße 13, 10405 Berlin.

**Live domain:** [allansabc.com](https://allansabc.com/)
**Instagram:** [@allans_abc](https://www.instagram.com/allans_abc/) ·
**Facebook:** [allansbreakfastclub](https://www.facebook.com/allansbreakfastclub/) ·
**Order:** [Wolt](https://wolt.com/en/deu/berlin/restaurant/abc-allans-breakfast-club-wine-bar)

---

## For the restaurant: how to change the website

Everything you'd want to edit lives in **`content/`**. Open that folder and read
its `README.md`. Change a file, click *Commit changes*, and the live site updates
itself in about a minute. If you make a mistake it refuses to publish and the
current site stays up untouched.

You never need to open any other folder.

---

## What's in here

```
content/                  ← EDIT HERE. Menu, hours, photos, text, links.
  README.md               Plain-English guide for non-technical editors
  1-the-basics.yml        Name, address, links, tagline, about text
  2-opening-hours.yml     Hours (feeds the page, footer AND Google)
  3-menu.yml              Food carousel + the two menu PDFs
  4-photos.yml            Every image on the site
  5-sections.yml          Events, booking boxes, on/off switches

build.py                  Turns content/ into the website. GitHub runs it for you.
templates/index.html.j2   The page layout. Rarely needs touching.

site/                     The generated website. Do not hand-edit index.html:
  index.html              it is rebuilt from content/ and your edits would be lost.
  css/                    tokens.css (brand vars) · patterns.css · main.css
  js/main.js
  assets/img/             21 curated, web-optimised photos
  assets/logo/            Logo PNG (transparent), favicon, Facebook profile/cover
  assets/menus/           Official food + drinks menu PDFs
  _modules/               Built but NOT live yet. See _modules/README.md
  CNAME                   allansabc.com

brand/
  BRAND.md                Colour repository, contrast table, type, patterns, voice
  tokens.css              The single source of truth for colour + type

data/
  business.json           Every verified fact about the business, with sources
  instagram.json          40 scraped posts (captions, dates, engagement)
  site_images.json        Image manifest with alt text and provenance
  google_image_urls.txt   Source URLs for the Google Maps photo pull

assets/images/            FULL scrape archive (90 originals, unoptimised)
  google/  (50)  instagram/ (40)  logo/

scripts/
  check_contrast.py       Verifies every colour pairing against WCAG. Run after
                          any palette change.
```

## Running it locally

```bash
python3 -m pip install pyyaml jinja2
python3 build.py
cd site && python3 -m http.server 8765
```

Then open http://localhost:8765

## Deploying

Pushing to `main` triggers `.github/workflows/deploy.yml`, which rebuilds from
`content/` and publishes to GitHub Pages. Nothing else to do.

**One-time setup:** GitHub → Settings → Pages → Source: **GitHub Actions**.
Then add `allansabc.com` as the custom domain. `CNAME` and `.nojekyll` are
already committed.

If the build fails, the deploy step never runs and the live site is untouched.
Check the Actions tab for the reason.

---

## Where the content came from

Everything on the site traces to a real source. Collected 14 Aug 2026:

| Source | What it gave us |
|---|---|
| Client brand board | Palette, fonts, logo, voice, positioning |
| Menu PDFs (Jul + Aug 2026) | Real dish names, ingredients, allergens, "cash only, no split bills" |
| Google Maps (Apify) | Hours, 4.4★/1,550 reviews, attributes, 50 photos |
| Instagram @allans_abc (Apify) | 40 posts, 10-year anniversary, ABC rosé, logo asset |
| Facebook page (Apify) | 6,720 likes, 92%/394 reviews, page created Dec 2014 |

`data/business.json` records the source and confidence for every field.
Anything uncertain is flagged `NEEDS_CONFIRMATION`.

---

## Open items

Things a human needs to decide or verify before this is fully finished:

1. **Photography rights.** The site currently uses photos pulled from Google Maps
   and Instagram. Those belong to the guests and photographers who took them, not
   to the restaurant. **This must be resolved before launch** — either commission
   a shoot, or confirm the restaurant owns/has licence for each image used.
   `data/site_images.json` maps every published image back to its source file so
   you can swap them one by one.
2. **Amalfi Coast font.** Commercial licence, not on Google Fonts. The site
   substitutes **Kaushan Script**. The logo keeps the real lettering because it is
   an image. Licence the real font and change `--font-script` in `brand/tokens.css`
   to switch everything at once.
3. **Opening hours.** Google says Tue + Wed closed. Confirm that is permanent and
   not seasonal. Note the homepage's "brunch from..." line is now derived from
   `2-opening-hours.yml`, so correcting the hours corrects the copy too.
4. **Phone number.** None published anywhere. Bookings currently route to
   Instagram and Facebook DMs, which matches how they actually operate.
5. **Anniversary date.** Not fixed. Instagram said 6 September 2026, the venue
   says that is off and it will most likely land in October. The homepage badge
   and event box therefore say "date coming soon". Put the real date into
   `content/5-sections.yml` (`event.date_line`) and `content/1-the-basics.yml`
   (`badge.text`) once it is decided.
6. **Fish Evening** is deliberately held until January. See `site/_modules/README.md`.

## Conventions

- Colour, type and spacing values live **only** in `brand/tokens.css`. Don't
  hardcode hex values in `main.css`.
- Coral (`#FF7B6B`) is a shape colour. Text on coral is always ink `#1A1A1A`,
  never cream — cream on coral is 2.37:1 and fails badly.
- No em dashes in site copy (client preference).
- The dark surfaces use `--abc-ocean` (#063C46), not near-black. It is from the
  logo's turquoise family and keeps the summer feel.
- Prices belong in the menu PDFs only. The site links to them; it never
  restates them, so the two can't disagree.
- Run `python3 scripts/check_contrast.py` after touching the palette.
