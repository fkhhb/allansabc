#!/usr/bin/env python3
"""Build the Allan's ABC website from the files in content/.

    python3 build.py

Reads every .yml file in content/, renders templates/index.html.j2, and writes
site/index.html. Nobody editing the website should ever need to run this by
hand: GitHub runs it automatically whenever a content file changes.

The job of this script is to fail LOUDLY and CLEARLY when someone makes a typo,
because the person editing the content is not a developer. Every error message
should name the file, and say what to do about it.
"""
from __future__ import annotations

import base64
import re
import sys
from urllib.parse import quote
from pathlib import Path

try:
    import yaml
    from jinja2 import Environment, FileSystemLoader, StrictUndefined
except ImportError:
    sys.exit("Missing build tools. Run:  python3 -m pip install pyyaml jinja2")

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
SITE = ROOT / "site"
OUTPUT = SITE / "index.html"

problems: list[str] = []


def fail(message: str) -> None:
    problems.append(message)


def load_content() -> dict:
    """Load every content/*.yml into one dictionary keyed by short name.

    content/1-the-basics.yml  ->  data["the_basics"]
    """
    data = {}
    files = sorted(CONTENT.glob("*.yml"))
    if not files:
        sys.exit(f"No .yml files found in {CONTENT}")

    for path in files:
        # "1-the-basics.yml" -> "the_basics"
        key = re.sub(r"^\d+-", "", path.stem).replace("-", "_")
        try:
            loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            mark = getattr(exc, "problem_mark", None)
            where = f" near line {mark.line + 1}" if mark else ""
            fail(
                f"{path.name} is not valid YAML{where}.\n"
                f"      This is almost always a spacing problem, a missing colon,\n"
                f"      or a line that needs \"quotes\" around it.\n"
                f"      Details: {getattr(exc, 'problem', exc)}"
            )
            continue
        if loaded is None:
            fail(f"{path.name} is empty.")
            continue
        data[key] = loaded
    return data


def check_required(data: dict) -> None:
    """Catch the mistakes that would produce a broken-looking page."""
    required = {
        "the_basics": ["name", "address", "links"],
        "opening_hours": ["days"],
        "menu": ["carousel", "menus"],
        "photos": ["hero", "dishes", "gallery"],
        "sections": ["visit", "footer"],
    }
    for file_key, keys in required.items():
        if file_key not in data:
            fail(f"Missing content file for '{file_key}'.")
            continue
        for key in keys:
            if key not in data[file_key]:
                fail(f"'{key}' is missing from {file_key.replace('_', '-')}.yml")

    if problems:
        return

    # Every carousel entry must resolve to a photo defined in 4-photos.yml.
    photos = data["photos"].get("dishes", {}) or {}
    carousel = data["menu"].get("carousel") or []
    if not carousel:
        fail("The carousel list in 3-menu.yml is empty. Add at least one photo name.")
    for ref in carousel:
        if ref not in photos:
            options = ", ".join(sorted(photos)) or "none defined"
            fail(
                f"The carousel in 3-menu.yml lists '{ref}',\n"
                f"      but there is no '{ref}' in the dishes list in 4-photos.yml.\n"
                f"      Available names: {options}"
            )

    # Opening hours must be one or the other, never neither.
    for day in data["opening_hours"].get("days", []) or []:
        label = day.get("day", "(unnamed day)")
        if day.get("closed"):
            continue
        if not (day.get("open") and day.get("close")):
            fail(
                f"{label} in 2-opening-hours.yml needs both an 'open:' and a\n"
                f"      'close:' time, or 'closed: yes' if we aren't open that day."
            )


def check_files_exist(data: dict) -> None:
    """Warn about photos and menus pointing at files that aren't in the repo."""
    referenced: list[tuple[str, str]] = []

    photos = data.get("photos", {})
    for key in ("hero", "about", "rose", "event", "visit"):
        if isinstance(photos.get(key), dict) and photos[key].get("file"):
            referenced.append((f"4-photos.yml ({key})", photos[key]["file"]))
    for name, entry in (photos.get("dishes") or {}).items():
        if entry.get("file"):
            referenced.append((f"4-photos.yml ({name})", entry["file"]))
    for i, entry in enumerate(photos.get("gallery") or [], 1):
        if entry.get("file"):
            referenced.append((f"4-photos.yml (gallery #{i})", entry["file"]))
    for which, entry in (data.get("menu", {}).get("menus") or {}).items():
        if entry.get("file"):
            referenced.append((f"3-menu.yml ({which} menu)", entry["file"]))

    for where, target in referenced:
        if target.startswith(("http://", "https://")):
            continue  # hosted elsewhere, nothing for us to check
        if not (SITE / target).exists():
            fail(
                f"{where} points at '{target}',\n"
                f"      but there is no such file in site/{target.rsplit('/', 1)[0]}/.\n"
                f"      Upload it, or correct the file name."
            )


def apply_defaults(data: dict) -> None:
    """Fill in every optional setting.

    Someone editing content should be able to delete a line they don't need
    without the build falling over, so anything optional gets a sensible value
    here rather than being demanded by the template.
    """
    basics = data["the_basics"]
    sections = data["sections"]

    basics.setdefault("badge", {}).setdefault("show", False)
    basics["badge"].setdefault("text", "")
    basics.setdefault("stats", [])
    basics.setdefault("scrolling_words", [])
    basics.setdefault("about", {}).setdefault("paragraphs", [])
    basics["about"].setdefault("intro", "")
    basics["about"].setdefault("heading", basics.get("name", ""))
    basics.setdefault("seo_line", basics.get("script_line", ""))

    # Sections default to visible: forgetting "show" should not hide the page.
    for name in ("rose", "gallery", "event", "book"):
        sections.setdefault(name, {}).setdefault("show", True)
    sections["rose"].setdefault("paragraphs", [])
    sections["rose"].setdefault("heading", "")
    sections["rose"].setdefault("kicker", "")
    sections["book"].setdefault("boxes", [])
    sections["visit"].setdefault("facts", [])
    sections["visit"].setdefault("notice", {}).setdefault("show", False)
    sections["visit"]["notice"].setdefault("icon", "")

    for box in sections["book"]["boxes"]:
        box.setdefault("icon", "")
        box.setdefault("show_email_underneath", False)
        for button in box.setdefault("buttons", []):
            button.setdefault("style", "primary")
            button.setdefault("is_email", False)
            button.setdefault("subject_enc", "")
            button.setdefault("body_enc", "")

    for day in data["opening_hours"]["days"]:
        day.setdefault("closed", False)

    data["opening_hours"].setdefault("note", "")
    data["opening_hours"].setdefault("footer_summary", [])
    data["menu"].setdefault("menu_note", "")

    # A photo entry that exists but has no description still needs the key.
    photos = data["photos"]
    for key in ("hero", "about", "rose", "event", "visit"):
        photos.setdefault(key, {}).setdefault("description", "")
        photos[key].setdefault("file", "")
    for entry in list((photos.get("dishes") or {}).values()) + list(photos.get("gallery") or []):
        entry.setdefault("description", "")


def add_derived(data: dict) -> None:
    """Work out the values the template needs but nobody should have to type."""
    basics = data["the_basics"]

    addr = basics["address"]
    basics["address_one_line"] = (
        f"{addr['street']}, {addr['postcode']} {addr['city']}"
    )

    # Multi-line fields: split so the template can insert real line breaks.
    for holder, field in (
        (basics, "tagline"),
        (basics.get("about", {}), "heading"),
        (data["sections"].get("rose", {}), "heading"),
    ):
        if holder and isinstance(holder.get(field), str):
            holder[f"{field}_lines"] = [
                line.strip() for line in holder[field].strip().splitlines() if line.strip()
            ]

    # Hours: a display string per day, plus the weekday number the JavaScript
    # uses to highlight today. Sunday is 0 to match the browser's getDay().
    weekday_number = {
        "sunday": 0, "monday": 1, "tuesday": 2, "wednesday": 3,
        "thursday": 4, "friday": 5, "saturday": 6,
    }
    for day in data["opening_hours"]["days"]:
        day["index"] = weekday_number.get(str(day["day"]).strip().lower(), -1)
        day["display"] = (
            "Closed" if day.get("closed") else f"{day['open']} – {day['close']}"
        )

    # Resolve carousel names into real photo entries.
    photos = data["photos"]["dishes"]
    data["menu"]["carousel_images"] = [
        photos[name] for name in data["menu"]["carousel"] if name in photos
    ]

    # kicker: AUTO builds the opening line from the hours, so it can never drift
    # out of step with them. Days are grouped by opening time, most common first.
    if str(data["menu"].get("kicker", "")).strip().upper() == "AUTO":
        by_time = {}
        for day in data["opening_hours"]["days"]:
            if not day.get("closed"):
                by_time.setdefault(day["open"], []).append(str(day["day"])[:3])
        if by_time:
            groups = sorted(by_time.items(), key=lambda kv: (-len(kv[1]), kv[0]))
            data["menu"]["kicker"] = "Brunch " + ", ".join(
                f"from {time} {' '.join(days)}" for time, days in groups
            )
        else:
            data["menu"]["kicker"] = "Brunch"

    # --- Email obfuscation -------------------------------------------------
    # The address must not appear anywhere in the delivered HTML, or address
    # harvesters scrape it straight off the page. It is base64-encoded, the
    # string reversed, then split across two attributes; main.js reassembles it
    # and writes the real mailto: on load.
    #
    # This defeats automated harvesters that pattern-match raw HTML, which is
    # what sends spam. It is NOT encryption: anything running a real browser
    # can still read the address once the script has run. That is the accepted
    # trade-off, and the reason the address is also kept out of the JSON-LD.
    email = basics["links"].get("events_email", "")
    encoded = base64.b64encode(email.encode("utf-8")).decode("ascii")[::-1]
    half = len(encoded) // 2
    basics["links"]["events_email_a"] = encoded[:half]
    basics["links"]["events_email_b"] = encoded[half:]

    subject = "Event enquiry at Allan's ABC"
    body = ("Hi Allan,\n\nI'd like to ask about an event at Allan's ABC.\n\n"
            "Date:\nNumber of guests:\nWhat we're celebrating:\n\nThanks!\n")
    basics["links"]["events_subject"] = quote(subject)
    basics["links"]["events_body"] = quote(body)

    # Without JavaScript the buttons fall back to the Instagram DM, which is a
    # real way to reach them, rather than to a dead link.
    for box in data["sections"].get("book", {}).get("boxes", []) or []:
        for button in box.get("buttons", []) or []:
            if button.get("link") != "EMAIL":
                continue
            button["link"] = basics["links"]["instagram"]
            button["is_email"] = True
            # A button may carry its own subject and body (a job application
            # asks for different things than an event enquiry). Otherwise it
            # inherits the event wording.
            button["subject_enc"] = quote(button.get("email_subject") or subject)
            button["body_enc"] = quote(button.get("email_body") or body)

    # The scrolling strip is duplicated so the loop can run seamlessly.
    words = basics.get("scrolling_words") or []
    basics["scrolling_words_doubled"] = list(words) + list(words)


def render_menu_pages(data: dict) -> list:
    """Turn each menu PDF into page images.

    Android hands PDF links to whichever viewer is installed, and some of those
    reflow the layout and drop the right-hand price column. Serving pictures of
    the pages means every device shows what the designer actually laid out.

    Regenerated on every build, so uploading a new PDF is still the only step
    needed to change the menu. If PyMuPDF is unavailable the build still
    succeeds: the menu page falls back to whatever images are already there.
    """
    try:
        import fitz
    except ImportError:
        print("  note: PyMuPDF not installed, reusing existing menu page images")
        fitz = None

    # Pillow writes a smaller file (progressive, optimised: ~300KB a page against
    # ~380KB), but it is a separate install. When it is missing, PyMuPDF's own
    # JPEG encoder produces the same picture, so the build carries on rather than
    # failing over a file-size optimisation.
    try:
        import PIL  # noqa: F401
        have_pillow = True
    except ImportError:
        have_pillow = False
        print("  note: Pillow not installed, using PyMuPDF's own JPEG encoder")

    out_dir = SITE / "assets" / "menus" / "pages"
    out_dir.mkdir(parents=True, exist_ok=True)
    groups = []

    titles = {"food": "Food menu", "drinks": "Drinks menu"}
    for key in ("food", "drinks"):
        entry = (data["menu"].get("menus") or {}).get(key) or {}
        rel = entry.get("file")
        if not rel:
            continue
        pdf = SITE / rel
        images = []
        if fitz and pdf.exists():
            doc = fitz.open(pdf)
            for i, page in enumerate(doc):
                pm = page.get_pixmap(dpi=160)
                name = f"{key}-{i + 1}.jpg"
                if have_pillow:
                    pm.pil_save(out_dir / name, format="JPEG", quality=86,
                                optimize=True, progressive=True)
                else:
                    pm.save(out_dir / name, jpg_quality=86)
                images.append({"file": f"assets/menus/pages/{name}",
                               "w": pm.width, "h": pm.height})
            doc.close()
        else:
            for f in sorted(out_dir.glob(f"{key}-*.jpg")):
                images.append({"file": f"assets/menus/pages/{f.name}",
                               "w": 1323, "h": 1871})
        if images:
            groups.append({"id": key, "title": titles[key],
                           "pdf": rel, "images": images})
    return groups


def main() -> int:
    data = load_content()
    if problems:
        report()
        return 1

    check_required(data)
    check_files_exist(data)
    if problems:
        report()
        return 1

    apply_defaults(data)
    add_derived(data)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        autoescape=True,
    )
    menu_pages = render_menu_pages(data)

    template = env.get_template("index.html.j2")
    OUTPUT.write_text(template.render(**data), encoding="utf-8")

    menu_tpl = env.get_template("menu.html.j2")
    (SITE / "menu.html").write_text(
        menu_tpl.render(menu_pages=menu_pages, **data), encoding="utf-8")

    dishes = len(data["menu"]["carousel_images"])
    gallery = len(data["photos"]["gallery"])
    open_days = sum(1 for d in data["opening_hours"]["days"] if not d.get("closed"))
    print("Website rebuilt successfully.")
    print(f"  {dishes} carousel photos, {gallery} gallery photos, open {open_days} days a week")
    print(f"  Written to {OUTPUT.relative_to(ROOT)} and site/menu.html")
    print(f"  {sum(len(g['images']) for g in menu_pages)} menu page images rendered from the PDFs")
    return 0


def report() -> None:
    print("\n" + "=" * 70)
    print(" The website could not be rebuilt. Nothing has changed on the live site.")
    print("=" * 70 + "\n")
    for problem in problems:
        print(f"  •  {problem}\n")
    print("Fix the above in the content/ folder and save again.")
    print("If you're stuck, undo your last change and the site carries on as before.\n")


if __name__ == "__main__":
    sys.exit(main())
