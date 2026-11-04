#!/usr/bin/env python3
"""
Build an Explorer outfit atlas for the dashboard from an 11-pose sprite sheet.

The sheet must hold the 11 poses in this order, left to right and top to bottom,
with space between figures and a transparent background:
  walk 1-4, watch 1-2, adjust outfit 1-2, push-up up, push-up down, pointing

Usage (needs: pip install pillow numpy scipy):
  python3 tools/build_outfit.py path/to/sprite_sheet.png christmas

Writes sprites/<outfit>.js in the same format as sprites.js, so index.html can load it.
Then add a row for the outfit to data/mascot.json.
"""
import base64, io, json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

POSES = ["walk1", "walk2", "walk3", "walk4", "watch1", "watch2",
         "tie1", "tie2", "pushUp", "pushDown", "point"]
STANDING_HEIGHT = 232   # matches the default atlas in sprites.js
ALPHA_MIN = 20          # ignore faint halo pixels
GAP = 2                 # pixels between frames in the atlas


def find_figures(rgba):
    solid = rgba[:, :, 3] > ALPHA_MIN
    labels, _ = ndimage.label(ndimage.binary_dilation(solid, iterations=6))
    figs = []
    for i, sl in enumerate(ndimage.find_objects(labels), start=1):
        mask = (labels[sl] == i) & solid[sl]
        if mask.sum() < 4000:
            continue
        figs.append(dict(y0=sl[0].start, y1=sl[0].stop, x0=sl[1].start, x1=sl[1].stop, mask=mask))
    # reading order: group into rows by vertical center, then left to right
    for f in figs:
        f["cy"] = (f["y0"] + f["y1"]) / 2
    figs.sort(key=lambda f: f["cy"])
    rows = []
    for f in figs:
        if rows and abs(f["cy"] - rows[-1][0]["cy"]) < (rows[-1][0]["y1"] - rows[-1][0]["y0"]) * 0.4:
            rows[-1].append(f)
        else:
            rows.append([f])
    return [f for r in rows for f in sorted(r, key=lambda f: f["x0"])]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sheet, outfit = sys.argv[1], sys.argv[2]
    rgba = np.array(Image.open(sheet).convert("RGBA"))
    figs = find_figures(rgba)
    if len(figs) != len(POSES):
        sys.exit(f"Found {len(figs)} figures, expected {len(POSES)}. Check for touching poses or stray marks.")

    # one scale for the whole sheet, from the standing (non-walking, non-push-up) poses
    standing = [f["y1"] - f["y0"] for f, n in zip(figs, POSES) if n[:4] in ("watc", "tie1", "tie2", "poin")]
    scale = STANDING_HEIGHT / float(np.median(standing))

    crops, frames, x = [], {}, 0
    for f, name in zip(figs, POSES):
        crop = rgba[f["y0"]:f["y1"], f["x0"]:f["x1"]].copy()
        crop[:, :, 3] = np.where(f["mask"], crop[:, :, 3], 0)
        img = Image.fromarray(crop)
        img = img.resize((max(1, round(img.width * scale)), max(1, round(img.height * scale))), Image.LANCZOS)
        a = np.array(img)[:, :, 3] > ALPHA_MIN
        ax = 0.0 if name.startswith("push") else round(float(ndimage.center_of_mass(a)[1]), 1)
        frames[name] = {"x": x, "y": 0, "w": img.width, "h": img.height, "ax": ax}
        crops.append((x, img))
        x += img.width + GAP

    atlas = Image.new("RGBA", (x - GAP, max(i.height for _, i in crops)), (0, 0, 0, 0))
    for px, img in crops:
        atlas.alpha_composite(img, (px, 0))
    buf = io.BytesIO()
    atlas.save(buf, "WEBP", quality=90, method=6)
    src = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()

    out = Path(__file__).resolve().parent.parent / "sprites" / f"{outfit}.js"
    out.parent.mkdir(exist_ok=True)
    out.write_text("(window.EXPLORER_OUTFITS = window.EXPLORER_OUTFITS || {})[" + json.dumps(outfit) + "] = "
                   + json.dumps({"src": src, "frames": frames}) + ";\n")
    print(f"{outfit}: scale {scale:.4f}, atlas {atlas.width}x{atlas.height}, {out.stat().st_size // 1024} KB -> {out}")


if __name__ == "__main__":
    main()
