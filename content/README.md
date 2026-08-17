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

## The food carousel

The homepage does not list dishes or prices. It shows a sliding row of food
photos and two buttons that open the real menus. That way a price only ever
lives in one place: the PDF.

To change which photos slide across, edit the `carousel` list in `3-menu.yml`:

```yaml
carousel:
  - dish-eggs-benny
  - dish-french-toast
  - dish-benny-salmon
```

Each name must match one in the `dishes` list in `4-photos.yml`. Reorder them,
add more, take some out. Three is the fewest that looks right; there is no
maximum. If you type a name that doesn't exist, the build stops and lists the
names you can use.

---

## The opening-hours line above the food

In `3-menu.yml` you'll see:

```yaml
kicker: AUTO
```

`AUTO` means the line is written from `2-opening-hours.yml` every time the site
builds, so it can never end up saying something the hours don't. Right now it
produces:

> Brunch from 10:00 Mon Thu Fri, from 09:30 Sat Sun

Change an opening time and that line changes with it. If you'd rather write your
own words, just replace `AUTO` with them.

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

## Putting the anniversary date in

The date is not fixed, so the site says **"date coming soon"** in two places.
When the day is decided, change both. They are the only two lines involved.

In `5-sections.yml`:

```yaml
event:
  date_line: Saturday 10 October · 11:00–20:00      ← was: Date coming soon
```

In `1-the-basics.yml`:

```yaml
badge:
  text: ★ 10 years · Sat 10 Oct                     ← was: ★ 10 years · Date coming soon
```

Keep the badge short. It sits on the photo at the top of the homepage and it is
one line, so a long date will crowd it.

While you're there, `event.text` says "we are still settling on the day" and the
button says "Follow for the date". Once the date is up, that paragraph can lose
its last sentence, and the button reads better as `Save your spot`.

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

---

## The events email

The address lives in `1-the-basics.yml` under `events_email`. Change it there
and every link on the site follows.

It is deliberately **not written into the website's code**. It gets scrambled
when the site is built, and unscrambled in the visitor's browser when the page
loads. That way the address-harvesting robots that trawl websites for email
addresses to spam find nothing to take, but a real person clicking "Email us"
gets their mail app opening with the address and a short template already
filled in.

Worth knowing: this stops the automated harvesting that causes spam. It is not
a secret. Anyone determined enough can still read the address off the page, and
of course anyone you email can see it.

If a visitor has JavaScript switched off, those buttons quietly fall back to
your Instagram DMs instead, so nobody hits a dead end.
