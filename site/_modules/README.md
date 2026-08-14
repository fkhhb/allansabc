# Held modules

Finished, tested sections that are **deliberately not in `index.html` yet**.
They are built and ready — they just have a date on them.

| Module | Go live | Owner decision |
|---|---|---|
| `fish-evening.html` | **January 2026** | Bondi Fish Evening is on hold until January. Built, styled and checked; do not publish before then. |

---

## Switching on the Fish Evening (January)

Four edits, about five minutes. Everything needed is already in the repo — no new
CSS, no new images, no new fonts.

### 1. Paste the section into `index.html`

Open `_modules/fish-evening.html`, copy **the whole file**, and paste it into
`index.html` directly after the closing `</section>` of the Brunch block
(the one with `id="brunch"`) and before the Rosé block (`id="rose"`).

The file already includes its own wave divider, which is what makes the join
between the cream Brunch section and the teal Fish section read as water.

### 2. Put the nav link back

In **both** navs in `index.html` — `.header__nav` and `.mobile-nav` — add the list
item back between Brunch and Rosé:

```html
<li><a href="#fish">Fish Evening</a></li>
```

### 3. Restore the full brand tagline

The hero currently runs a shortened tagline, because leading the site with
"Fish focused" while there is no fish service would be a promise the kitchen
can't keep. In January, restore the full board line in `index.html`:

```html
<!-- launch version (Aug–Dec) -->
<p class="hero__tagline">Day drinking. Good times.<br>Always.</p>

<!-- January version — the full brand-board line -->
<p class="hero__tagline">Day drinking. Good times.<br>Fish focused. Always.</p>
```

`--fs-hero` and the `32ch` cap on `.hero__tagline` already accommodate the longer
line at every breakpoint — checked at 320px, 768px and 1440px.

### 4. Restore the two fish lines in the marquee

The marquee currently runs four phrases, duplicated once for a seamless
`-50%` loop. Swap the two placeholder phrases back:

| Currently | Restore to |
|---|---|
| `Good food, good company` | `Weekdays are for fish &amp; apéro` |
| `Ten years on Rykestraße` | `Eat fish <em>·</em> Drink rosé <em>·</em> Be happy` |

**Change them in both halves of the track.** The animation translates by exactly
`-50%`, so the second half must stay an exact copy of the first or the loop
visibly jumps.

---

## What is already done

- Section markup, headings, menu list, CTA — complete.
- `.pattern-fish` (the tiled teal fish motif) is already in `css/patterns.css`
  and is not used anywhere else, so it has been left in place.
- `assets/img/dish-fish.jpg` is already exported and optimised.
- Contrast checked: cream on teal at heading size is 3.60:1 (AA-large, passes);
  body copy inside the section uses `rgba(cream, .88)` on teal, and the yellow
  kicker on teal clears comfortably.
- The `#fish` anchor and the wave divider have no other references in the site,
  so removing the section left no dead links. Verified with a link check.
