# How to change the website

**You are in the right place.** Everything you can change is in this folder.
You do not need to know how to code, and you cannot break the website from here.

---

## The short version

1. Click the file you want to change.
2. Click the **pencil icon** (top right).
3. Change the words.
4. Scroll down, click the green **Commit changes** button.
5. Wait about a minute. The website updates itself.

That's it. There is no step 6.

---

## Which file do I want?

| I want to change... | Open this file |
|---|---|
| A dish, its description, or a price | `3-menu.yml` |
| The food or drinks menu PDF | `3-menu.yml` (and upload the PDF, see below) |
| Opening hours | `2-opening-hours.yml` |
| Any photo on the site | `4-photos.yml` |
| Address, Instagram, Wolt or email links | `1-the-basics.yml` |
| The big title, tagline, or "about us" text | `1-the-basics.yml` |
| The event box, booking boxes, cash-only notice | `5-sections.yml` |
| Hide a whole section for a while | `5-sections.yml` (see "Turning things off") |

---

## The rules (there are only four)

**1. Only change what's AFTER the colon.**

```yaml
name: Eggs Benny
```
`name:` stays. `Eggs Benny` is yours to change.

**2. Don't change the spacing at the start of a line.**

The indentation is how the file knows what belongs to what. If a line starts
with two spaces, keep the two spaces.

**3. If your text contains a colon, wrap the whole thing in "quotes".**

This is the single most common mistake. It looks harmless and it isn't:

```yaml
note: Margaritas: cheaper than therapy     ← BREAKS
note: "Margaritas: cheaper than therapy"   ← FINE
```

Same goes for text starting with `#`, `-`, `@`, `&` or `*`. When in doubt,
add the quotes. Quotes are never wrong.

**4. Times and postcodes need quotes too.**

```yaml
open: "10:00"     ← right
open: 10:00       ← wrong, comes out looking strange
```

---

## Adding or removing a dish

In `3-menu.yml`, each dish is a block starting with `- name:`. To add one, copy
an existing block and change the words. To remove one, delete its whole block.

```yaml
  - name: Eggs Benny
    tag: The famous one
    description: Two poached eggs, brioche, Allan's hollandaise.
    photo: dish-eggs-benny
```

- `tag:` is the little coloured label. Delete the line for no label.
- `photo:` must match a name in `4-photos.yml`. If it doesn't, the build stops
  and tells you which names are available.
- To show a price, add a `price:` line with just the number, no € sign:
  `price: 14.50` shows as **€14.50**, and `price: 10` shows as **€10**.
  Leave the line out and no price shows. Right now no dish shows a price,
  because the PDFs carry the real ones. Add prices here whenever you want them
  on the homepage too.

Six dishes fill the layout neatly. Any number works.

---

## Changing a photo

**The easy way:** name your new photo exactly the same as the old one, upload it
to `site/assets/img/`, and you're done. Nothing else to change.

**The other way:** upload your photo with any name, then open `4-photos.yml` and
change the matching `file:` line to your new file name.

To upload: go to the `site/assets/img/` folder, click **Add file → Upload files**,
drag your photo in, and commit.

Always update the `description:` too. It's read aloud to blind visitors and it's
what shows if the image fails to load.

---

## Changing a menu PDF

Go to `site/assets/menus/`, click **Add file → Upload files**, and upload the new
PDF **using the same file name as the old one**:

- `allans-abc-food-menu.pdf`
- `allans-abc-drinks-menu.pdf`

Then you don't have to touch anything else. If you use a different name, update
the `file:` lines in `3-menu.yml` to match.

---

## Turning things off

In `5-sections.yml`, anything with `show:` can be switched off:

```yaml
event:
  show: no      ← the anniversary box disappears from the site
```

The link to it disappears from the top menu automatically too. Change it back to
`yes` whenever you want it back. Nothing is deleted.

Good candidates: turn the `event` box off after the party, turn it back on for
the next one.

---

## What if I get it wrong?

**Nothing bad happens.** The website checks your changes before publishing. If
something's wrong, it refuses to publish and **the current site stays up exactly
as it is**.

To see what went wrong: click the **Actions** tab at the top of GitHub, then the
red ✗ entry. The message tells you the file, the line, and what to fix.

To undo: go to the file, click the pencil, and put back what you changed. Or
open the file's **History** and revert to the previous version.

---

## What the numbers in the file names mean

Nothing important. They just keep the files in a sensible reading order:
basics, then hours, then menu, then photos, then everything else.
