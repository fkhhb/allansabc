# Allan's ABC — Brand Reference

**Allan's Brunch & Aperitivo** · ABC — Allan's Breakfast Club & Wine Bar
Rykestraße 13, 10405 Berlin (Prenzlauer Berg)

> Day drinking. Good times. Fish focused. Always.

---

## 1. Colour repository

### 1.1 Core palette (authoritative — from the client brand board)

| Token | Hex | RGB | Role |
|---|---|---|---|
| `--abc-coral` | `#FF7B6B` | 255, 123, 107 | Primary brand colour. The heart, the "A", headline accents, CTAs. |
| `--abc-teal` | `#00928A` | 0, 146, 138 | Secondary. Script logotype, section grounds, the venue's own paintwork. |
| `--abc-yellow` | `#FFDB4D` | 255, 219, 77 | Accent / energy. The awning stripe, the bar stools, highlights. |
| `--abc-cream` | `#FFF7E6` | 255, 247, 230 | Page background. Warm paper, never pure white. |
| `--abc-ink` | `#1A1A1A` | 26, 26, 26 | Body text, footer ground. Never pure black on cream. |

### 1.2 Sampled from real assets (verification)

These were measured off the actual logo file and venue photography. They confirm the
board palette is drawn from the real venue rather than invented.

| Source | Sampled | Nearest core token | Note |
|---|---|---|---|
| Logo heart (`ig_07`) | `#FD947D` | `--abc-coral` | JPEG-softened; board value is the true spec. |
| Logo script (`ig_07`) | `#3D7C76` | `--abc-teal` | Rendered over coral, so reads darker. |
| Bar / wall panelling | `#60A0A0` | `--abc-teal` (tinted) | The real teal woodwork, sun-faded. |
| Awning + stools | `#D0B070` → `#FFDB4D` | `--abc-yellow` | Warm yellow, photographed in daylight. |

**Conclusion:** use the board values as spec. The sampled values are what the brand
looks like *in the wild* and are useful for choosing photography that sits well
against the palette.

### 1.3 Derived / support tones (built for the website, not on the board)

Needed for real UI: hovers, borders, shadows, muted text. All derived from the core five.

| Token | Hex | Derivation | Use |
|---|---|---|---|
| `--abc-coral-dark` | `#E85F4F` | coral, −12% L | Button hover / pressed. |
| `--abc-coral-soft` | `#FFE4DF` | coral @ 18% on cream | Tinted cards, badges. |
| `--abc-teal-dark` | `#00706A` | teal, −10% L | Teal button hover, footer links. |
| `--abc-teal-soft` | `#D6EDEB` | teal @ 15% on cream | Alternating section ground. |
| `--abc-yellow-dark` | `#F0C42F` | yellow, −8% L | Stripe shadow, hover. |
| `--abc-sand` | `#F3E7CE` | cream, −5% L | Borders, dividers, subtle fills. |
| `--abc-ink-muted` | `#5C5751` | ink @ 70% on cream | Secondary body copy. |

### 1.4 Contrast — checked, not guessed

WCAG AA needs 4.5:1 for body text, 3:1 for large text (≥24px or ≥19px bold).

Measured, not estimated — recompute with `scripts/check_contrast.py` after any palette change.

| Pair | Ratio | Verdict |
|---|---|---|
| ink `#1A1A1A` on cream `#FFF7E6` | **16.33:1** | ✅ AAA — default body |
| cream on ink `#1A1A1A` | **16.33:1** | ✅ AAA — footer |
| ink on yellow `#FFDB4D` | **12.84:1** | ✅ AAA — ink-on-yellow buttons |
| ink-muted `#5C5751` on cream | **6.71:1** | ✅ AA — secondary copy |
| ink on coral `#FF7B6B` | **6.88:1** | ✅ AA — **the** coral-button combination |
| teal-dark `#00706A` on cream | **5.59:1** | ✅ AA — links and body |
| cream on teal-dark `#00706A` | **5.59:1** | ✅ AA |
| teal-dark on yellow `#FFDB4D` | **4.39:1** | ⚠️ Large text only |
| teal `#00928A` on cream | **3.60:1** | ⚠️ **Large text / headings only.** Not for body. |
| cream on teal `#00928A` | **3.60:1** | ⚠️ Large text only |
| coral-dark `#E85F4F` on cream | **3.19:1** | ⚠️ Large text only |
| coral `#FF7B6B` on cream | **2.37:1** | ❌ **Decorative only.** Never text. |
| cream on coral `#FF7B6B` | **2.37:1** | ❌ **Never white/cream text on coral.** |

**The three rules that matter:**
1. **Coral is a shape colour, not a text colour.** Coral fills, **ink** text on top —
   never cream or white, which fails at 2.37:1. This is the easiest mistake to make
   with this palette because coral *looks* dark enough. It isn't.
2. **Teal at full strength is for headings.** Use `--abc-teal-dark` whenever teal
   carries body-size text or a link.
3. **Yellow only ever carries ink.** Teal-dark on yellow squeaks by at large sizes;
   nothing else clears.

---

## 2. Typography

| Role | Board spec | Web implementation | Status |
|---|---|---|---|
| Headline | **Bebas Neue** | Bebas Neue (Google Fonts) | ✅ exact |
| Script | **Amalfi Coast** | **Kaushan Script** (Google Fonts) | ⚠️ **substituted** |
| Body | **Montserrat** | Montserrat (Google Fonts) | ✅ exact |

> ⚠️ **Amalfi Coast is a commercial font and is not available on Google Fonts.**
> The site uses **Kaushan Script** as the closest free brush-script stand-in.
> The wordmark itself is used as an **image** (`allans-heart-logo.png`), so the real
> Amalfi Coast lettering is preserved wherever the logo appears. If you licence
> Amalfi Coast for web, swap `--font-script` in `brand/tokens.css` and the whole site
> picks it up.

**Scale** (set in `tokens.css`, fluid via `clamp()`):
Bebas is drawn tall and narrow — it needs wider letter-spacing than a normal sans
or it reads as a solid block. All Bebas headings carry `letter-spacing: 0.02em`
and `line-height: 0.95`.

---

## 3. Patterns & textures

Three, all from the board, all reproduced as CSS/SVG in `site/css/patterns.css`:

1. **Yellow stripes** — the awning. `repeating-linear-gradient`, 24px bands,
   yellow on cream. Used as section top-caps and the takeaway-bag motif.
2. **Fish line-drawings** — teal outline fish, tiled. Used at low opacity behind
   the Fish Evening section.
3. **Scallop / wave** — teal arcs. Used as a section divider (the "sea" edge).

---

## 4. Logo

`assets/images/logo/allans-heart-logo.png` — coral heart, teal brush script "Allan's",
background knocked out to transparent. 838 × 751px.

**Clear space:** ≥ 25% of the logo's height on all sides.
**Minimum size:** 64px wide on screen — below that the script closes up.
**Do not:** recolour, add a drop shadow, place on a busy photo without a scrim, or
stretch. On photography, use the cream or coral lockup over a dark scrim.

Secondary marks in use on social: the "A♥ Brunch & Aperitivo" stacked lockup
(coral A, teal script), and an older circular "BERLIN / ABC / ALLAN'S" badge.

---

## 5. Voice

Shouty, warm, a bit French, never corporate. Heavy caps. Real punctuation optional.
Signs off **"Team A♥️"**.

Lines pulled from the board and their own posts — all safe to reuse:

- Eat fish. Drink rosé. Be happy.
- Day drinking. Good times. Fish focused. Always.
- Rosé all day, everyday.
- You look thirsty. (We can help.)
- Fresh fish every day.
- Weekdays are for fish & apéro.
- Let's keep it fishy & pink.
- Good food, good company, beach vibes.
- Margarita o'clock — what are u waiting for?
- Fight for your right to party.
- Fun. Fresh. A little French. A lot of fish.

**Do not** write in polished restaurant-marketing English ("nestled in the heart of
Prenzlauer Berg…"). It is the opposite of this brand.
