# Allan's ABC — Brand Reference

**Allan's ABC** · ABC - Allan's Breakfast Club & Wine Bar
Rykestraße 13, 10405 Berlin (Prenzlauer Berg)

> Day drinking. Provence rosé. Good times, always.

**Positioning:** the one and only rosé café in Berlin. Australian brunch cooked
by a Frenchman, a sunny terrace, and a fridge full of Provence rosé poured from
eleven in the morning. Not a wine bar by night — that service was retired in
August 2026 and must not reappear in copy.

---

## 1. Colour repository

The palette moved in August 2026 from a teal-led scheme to **Provence rosé**:
salmon pink, awning yellow, sun-bleached cream, with a wine dark in place of
near-black. The logo's turquoise survives as an accent, not as a lead.

### 1.1 Core palette

| Token | Hex | Role |
|---|---|---|
| `--abc-cream` | `#FFF8EC` | Page ground. Sun-bleached linen, never pure white. |
| `--abc-sand` | `#F7E9D2` | Warmer ground, borders, alternating sections. |
| `--abc-blush` | `#FFE6DC` | Palest rosé. Section grounds. |
| `--abc-rose` | `#FFD2C4` | Rosé in the glass. Tags, accents on dark. |
| `--abc-salmon` | `#FF9E86` | The everyday pink. Badges, button hover. |
| `--abc-coral` | `#FF7B6B` | From the client brand board. Buttons, the heart. |
| `--abc-yellow` | `#FFDB4D` | The awning. |
| `--abc-wine` | `#6E2B36` | The dark. A rosé bottle in shadow. Headings, panels. |
| `--abc-ink` | `#2A1A18` | Body text. Warm near-black, never neutral grey. |

### 1.2 Accent and support

| Token | Hex | Role |
|---|---|---|
| `--abc-aqua` | `#8ED7D2` | Header and footer gradient. Sun-faded bar paintwork. |
| `--abc-aqua-light` | `#A7E0DC` | Top of that gradient. |
| `--abc-aqua-deep` | `#7DBDB9` | Bottom of it. **Do not go darker** — wine text drops below 4.5:1. |
| `--abc-teal` / `--abc-teal-dark` | `#00928A` / `#00706A` | The logo script colour. Accent only now. |
| `--abc-terracotta` | `#A8382A` | Link hover. |
| `--abc-ink-muted` | `#6B564F` | Secondary copy. |

### 1.3 Contrast — measured, not guessed

Run `python3 scripts/check_contrast.py` after any palette change. It runs in CI
and fails the build, so a change that breaks contrast never reaches the site.

| Pairing | Ratio | |
|---|---|---|
| ink on cream | **15.79:1** | ✅ body |
| ink on blush | **13.98:1** | ✅ body |
| ink on sand | **13.93:1** | ✅ body |
| ink on rose | **12.12:1** | ✅ body |
| ink on yellow | **12.30:1** | ✅ buttons |
| header/footer: ink on aqua | **10.16:1** | ✅ body |
| link/kicker: wine on cream | **9.65:1** | ✅ body |
| cream on wine | **9.65:1** | ✅ dark panels |
| button hover: ink on salmon | **8.33:1** | ✅ body |
| footer: ink on aqua-deep | **7.82:1** | ✅ body |
| kicker on wine: yellow | **7.51:1** | ✅ |
| accent on wine: rose | **7.40:1** | ✅ |
| button: ink on coral | **6.59:1** | ✅ body |
| secondary copy: ink-muted on cream | **6.48:1** | ✅ body |
| link hover: terracotta on cream | **6.09:1** | ✅ body |
| footer link: wine on aqua-deep | **4.78:1** | ✅ body, and the floor of the aqua ramp |
| coral as text on cream | **2.40:1** | ❌ decorative only |
| cream on coral | **2.40:1** | ❌ never |
| salmon as text on cream | **1.90:1** | ❌ decorative only |

**The four rules that matter:**
1. **Coral and salmon are shape colours.** Text on them is always **ink** —
   never cream or white, which fails at 2.40:1. Coral *looks* dark enough. It isn't.
2. **Wine is the heading and link colour**, and the only dark ground.
3. **Never push the aqua ramp past `#7DBDB9`.** Wine text stops clearing 4.5:1.
4. **Yellow only ever carries ink.**

### 1.4 The hero scrim

The hero photo is bright and yellow, so the wash over it is doing real work.
It is two layers, not one: a vertical gradient under the copy, plus a
horizontal one weighting it to the left where the words sit. That keeps the
top-right of the frame sunny so the awning still reads as yellow.

Checked by compositing the scrim over the **brightest** pixels in the photo
(a sunlit white awning stripe and a yellow parasol): every piece of hero text
clears its requirement, with the headline at 5.18:1 on the left and 3.41:1 at
its right edge, which passes AA for large text at 48px+.

If you change the hero photo, re-check this. A darker photo can take a lighter
scrim; a brighter one cannot.

---

## 2. Typography

| Role | Board spec | Web implementation | Status |
|---|---|---|---|
| Headline | **Bebas Neue** | Bebas Neue (Google Fonts) | ✅ exact |
| Script | **Amalfi Coast** | **Kaushan Script** (Google Fonts) | ⚠️ **substituted** |
| Body | **Montserrat** | Montserrat (Google Fonts) | ✅ exact |

> ⚠️ **Amalfi Coast is a commercial font and is not on Google Fonts.** Kaushan
> Script stands in. The wordmark itself is an **image**, so the real Amalfi
> Coast lettering survives wherever the logo appears. Licence it for web and
> change `--font-script` in `tokens.css` to switch everything at once.

**Fraunces was trialled** as a warmer, Provence-leaning serif in August 2026 and
reverted: the condensed grotesque suits the shouty all-caps voice better.

**Scale:** Bebas is drawn tall and narrow, so it needs open tracking
(`0.02em`) and tight leading (`0.95`) or a heading reads as one solid block.

---

## 3. Patterns & textures

1. **Awning stripes** — yellow and cream, 24px bands. Also used as a **frame
   down both page edges**, painted on `<html>` with `<body>` inset by a margin.
2. **Fish line-drawings** — teal outline fish. Currently unused; belongs to the
   held Fish Evening module.
3. **Scallop / wave** — the sea edge, for section joins.

---

## 4. Logo

`site/assets/logo/allans-heart-logo.png` — coral heart, teal brush script
"Allan's", background knocked out. 520 × 466px.

**Clear space:** ≥ 25% of its height. **Minimum:** 64px wide.
**Never** recolour, stretch, or place on a busy photo without a scrim.
On a coral or salmon ground the heart disappears — put it on a cream chip
(as the footer does).

---

## 5. Voice

Shouty, warm, a bit French, never corporate. Heavy caps. Signs off **"Team A♥️"**.

Lines from the brand board and their own posts, all safe to reuse:

- Rosé all day, everyday.
- Drink Provence water.
- The one and only rosé café in Berlin.
- Day drinking. Good times. Always.
- You look thirsty. (We can help.)
- Welcome to the beach house.
- Drink pink.
- Let's sin till late.
- Good food, good company, beach vibes.
- Margarita o'clock — what are u waiting for?
- Fun. Fresh. A little French.

**Do not** write polished restaurant-marketing English ("nestled in the heart of
Prenzlauer Berg…"). It is the opposite of this brand.

**Do not** describe the place as a wine bar by night. That service has ended.
