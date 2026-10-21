#!/usr/bin/env python3
"""Render an image as the grid of numbers a sensor records, each coloured by what it measured.

    python3 render.py --src retina.jpg --out banner.png [options]

Adapted from the hex-glyph renderer in usamahz/cpu-performance-engineering
(misc/notes/banner/render.py). The change is the point of this repository: every glyph is
the cell's own sampled value written in hexadecimal, not random digits, so the banner is
literally the image as an array of numbers. In --mode bayer each cell shows the single
channel a Bayer colour filter array would have recorded at that site, in that channel's
colour, which is what reaches the image signal processor before demosaicing.
"""
import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BAYER = (("R", "G"), ("G", "B"))  # RGGB, the most common layout


def lum(c):
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def boost(c, sat, gain, lift):
    l = lum(c)
    return tuple(max(0, min(255, int((l + (v - l) * sat) * gain + lift))) for v in c)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=3000)
    ap.add_argument("--height", type=int, default=1100)
    ap.add_argument("--crop", default="0.06,0.29,0.94,0.61",
                    help="fractional box x0,y0,x1,y1; aspect forced to width:height around its centre")
    ap.add_argument("--cell", type=int, default=22, help="cell width in px, two glyphs wide; height is cell*0.62")
    ap.add_argument("--mode", choices=["values", "bayer"], default="values")
    ap.add_argument("--base", type=float, default=0.30, help="brightness of the image under the glyphs")
    ap.add_argument("--sat", type=float, default=1.05)
    ap.add_argument("--gain", type=float, default=1.12)
    ap.add_argument("--lift", type=float, default=10)
    ap.add_argument("--contrast", type=float, default=1.0, help="tonal stretch of the crop before sampling")
    ap.add_argument("--detail", type=float, default=0.0,
                    help="strength of the structure map that sets glyph brightness; 0 turns it off")
    ap.add_argument("--detail-radius", type=float, default=18.0, help="blur radius of the high-pass, in px")
    ap.add_argument("--colour", type=float, default=1.0, help="saturation of the final image; below one calms it")
    ap.add_argument("--font", default=FONT)
    ap.add_argument("--quality", type=int, default=64)
    a = ap.parse_args()

    src = Image.open(a.src).convert("RGB")
    W, H = src.size
    x0, y0, x1, y1 = (float(v) for v in a.crop.split(","))
    bx0, by0, bx1, by1 = x0 * W, y0 * H, x1 * W, y1 * H
    want = a.width / a.height
    bw, bh = bx1 - bx0, by1 - by0
    if bw / bh > want:
        nw = bh * want
        bx0 += (bw - nw) / 2
        bx1 = bx0 + nw
    else:
        nh = bw / want
        by0 += (bh - nh) / 2
        by1 = by0 + nh
    crop = src.crop((int(bx0), int(by0), int(bx1), int(by1))).resize((a.width, a.height), Image.Resampling.LANCZOS)

    if a.contrast != 1.0:
        crop = ImageEnhance.Contrast(ImageOps.autocontrast(crop, cutoff=(0.5, 2))).enhance(a.contrast)

    # Structure map. In a fundus photograph the vessels have most contrast in the green
    # channel, so a high-pass of green finds them; elsewhere it finds whatever edges exist.
    detail = None
    if a.detail:
        green = crop.split()[1]
        high = ImageChops.subtract(green.filter(ImageFilter.GaussianBlur(a.detail_radius)), green, 1.0, 128)
        detail = ImageOps.autocontrast(high, cutoff=2)

    cw = a.cell
    ch = max(8, int(round(cw * 0.62)))
    cols, rows = a.width // cw, a.height // ch
    cells = crop.resize((cols, rows), Image.Resampling.BOX).load()
    dmap = detail.resize((cols, rows), Image.Resampling.BOX).load() if detail else None

    img = ImageEnhance.Brightness(crop).enhance(a.base)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(a.font, int(ch * 0.95))

    for r in range(rows):
        for c in range(cols):
            col = cells[c, r]
            if a.mode == "bayer":
                channel = BAYER[r % 2][c % 2]
                i = "RGB".index(channel)
                value = col[i]
                colour = [0, 0, 0]
                colour[i] = min(255, int(value * a.gain + a.lift))
                colour = tuple(colour)
            else:
                value = int(round(lum(col)))
                colour = boost(col, a.sat, a.gain, a.lift)
            if dmap is not None:
                # bright glyphs on tissue, dim glyphs on vessels and dark structure
                d = (dmap[c, r] - 128) / 127.0
                f = max(0.15, 1.0 - a.detail * max(0.0, d)) + 0.35 * max(0.0, -d)
                colour = tuple(max(0, min(255, int(v * f))) for v in colour)
            draw.text((c * cw + 1, r * ch), f"{value:02x}", font=font, fill=colour)

    if a.colour != 1.0:
        img = ImageEnhance.Color(img).enhance(a.colour)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix.lower() == ".avif":
        img.save(out, quality=a.quality)
    else:
        img.save(out, optimize=True)
    print(f"wrote {out} {img.size} cells {cols}x{rows}")


if __name__ == "__main__":
    main()
