"""Builds data/slides.json from the images in the slides/ folder.

File name format (dates optional):
  2026-11-16_2026-11-18_turkey-bowl.png  -> shown Nov 16 through Nov 18
  community-time-clubs.png               -> shown until the file is deleted
Slides play in alphabetical order of file name.
"""
import json, os, re, urllib.parse

SLIDES = "slides"
out = []
for name in sorted(os.listdir(SLIDES)):
    if not re.search(r"\.(png|jpe?g|gif|webp|svg)$", name, re.I):
        continue
    m = re.match(r"^(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})[_ -](.+)$", name)
    start, end, rest = (m.group(1), m.group(2), m.group(3)) if m else (None, None, name)
    title = re.sub(r"\.[^.]+$", "", rest)
    title = re.sub(r"^\d+[_ -]+", "", title)
    title = re.sub(r"[_-]+", " ", title).strip()
    title = title[:1].upper() + title[1:]
    out.append({
        "id": "slide-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-"),
        "title": title,
        "start": start,
        "end": end,
        "image": SLIDES + "/" + urllib.parse.quote(name),
    })

os.makedirs("data", exist_ok=True)
with open("data/slides.json", "w") as f:
    json.dump(out, f, indent=1)
print(f"{len(out)} slide(s) written to data/slides.json")
