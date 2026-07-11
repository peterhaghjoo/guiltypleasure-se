#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CI-variant av og_gen.py: renderar og-bilder + apple-touch-icon ur den SUBSETTADE
webbfonten (fonts/gp-bold.woff2) — inga råa OTF:er behövs i repot.
woff2 -> ttf (temporärt) eftersom PIL/FreeType inte alltid läser woff2 direkt."""
import pathlib, tempfile
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).parent
MOSSA, DISCO, GRADDE, ELD = "#24270e", "#ff99ff", "#fff8eb", "#ff450a"

# woff2 -> ttf i tempfil
f = TTFont(str(ROOT/"fonts/gp-bold.woff2"))
f.flavor = None
TTF = str(pathlib.Path(tempfile.gettempdir())/"gp-bold-ci.ttf")
f.save(TTF)

def og(fname, big, sub, tag="GUILTY PLEASURE CAFÉ"):
    W,H = 1200,630
    im = Image.new("RGB",(W,H),MOSSA)
    d = ImageDraw.Draw(im)
    f_tag = ImageFont.truetype(TTF, 34)
    f_sub = ImageFont.truetype(TTF, 44)
    size = 150
    while size > 60:
        f_big = ImageFont.truetype(TTF, size)
        if max(d.textlength(line, font=f_big) for line in big.split("\n")) <= W-160: break
        size -= 6
    d.ellipse((80, 86, 104, 110), fill=ELD)
    d.text((122, 78), tag, font=f_tag, fill=GRADDE)
    bb = d.multiline_textbbox((0,0), big, font=f_big, spacing=14)
    y = (H - (bb[3]-bb[1]))//2 - 40
    d.multiline_text((80, y), big, font=f_big, fill=DISCO, spacing=14)
    d.text((80, y + (bb[3]-bb[1]) + 70), sub, font=f_sub, fill=GRADDE)
    d.rounded_rectangle((80, H-74, 400, H-58), radius=8, fill=ELD)
    im.save(ROOT/fname, optimize=True)
    print(fname, im.size, f"{(ROOT/fname).stat().st_size//1024} KB")

og("og.png",         "Where cravings\nmeet good vibes", "Brunch · Dinner · Disco — Umeå · Sundsvall")
og("og-umea.png",    "GP's Umeå",       "Skolgatan 62 · Brunch · Dinner · Disco")
og("og-sundsvall.png","GP's Sundsvall", "Storgatan 12 · Brunch · Dinner · Disco")
og("og-meny.png",    "Menyn",           "Comfort food · cocktails · No Regrets 0.0")

# apple-touch-icon 180x180
im = Image.new("RGB",(180,180),MOSSA)
d = ImageDraw.Draw(im)
fnt = ImageFont.truetype(TTF, 92)
bb = d.textbbox((0,0),"GP",font=fnt)
d.text(((180-(bb[2]-bb[0]))//2-bb[0], (180-(bb[3]-bb[1]))//2-bb[1]), "GP", font=fnt, fill=DISCO)
im.save(ROOT/"apple-touch-icon.png", optimize=True)
print("apple-touch-icon.png", f"{(ROOT/'apple-touch-icon.png').stat().st_size//1024} KB")
