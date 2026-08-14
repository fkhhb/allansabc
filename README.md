# Allan's ABC

Website and brand repository for **Allan's ABC** (ABC - Allan's Breakfast Club & Wine Bar),
Rykestraße 13, 10405 Berlin.

**Live domain:** [allansabc.com](https://allansabc.com/)
**Instagram:** [@allans_abc](https://www.instagram.com/allans_abc/) ·
**Facebook:** [allansbreakfastclub](https://www.facebook.com/allansbreakfastclub/) ·
**Order:** [Wolt](https://wolt.com/en/deu/berlin/restaurant/abc-allans-breakfast-club-wine-bar)

---

## What's in here

```
site/                     The website. Static HTML/CSS/JS, no build step.
  index.html
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

No build, no dependencies. Serve the folder:

```bash
cd site && python3 -m http.server 8765
```

Then open http://localhost:8765

## Deploying

`site/` is a static folder. It works on GitHub Pages, Netlify, Vercel or any host.

For **GitHub Pages**: Settings → Pages → deploy from branch `main`, folder `/site`.
`CNAME` and `.nojekyll` are already in place for the `allansabc.com` domain.

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
   not seasonal, and confirm the evening/bar hours, which Google does not list.
4. **Phone number.** None published anywhere. Bookings currently route to
   Instagram and Facebook DMs, which matches how they actually operate.
5. **Anniversary date.** Sunday 6 September 2026, 11:00–20:00, taken from their
   own Instagram. Worth a sanity check before it goes on the homepage.
6. **Fish Evening** is deliberately held until January. See `site/_modules/README.md`.

## Conventions

- Colour, type and spacing values live **only** in `brand/tokens.css`. Don't
  hardcode hex values in `main.css`.
- Coral (`#FF7B6B`) is a shape colour. Text on coral is always ink `#1A1A1A`,
  never cream — cream on coral is 2.37:1 and fails badly.
- No em dashes in site copy (client preference).
- Run `python3 scripts/check_contrast.py` after touching the palette.
