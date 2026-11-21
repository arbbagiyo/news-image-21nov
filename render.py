#!/usr/bin/env python3
"""Render the front page for Saturday 21 November 2026.

Draws a newspaper front page with PIL: masthead, red dateline, main story
(Gen Z protests across Europe), second story (Trump urges Nvidia to bring
back Huang), a four-item bottom row and an ALSO strip. Deterministic: no
randomness, no timestamps, no network.
"""
import textwrap

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 240, 221)
INK = (26, 26, 26)
RED = (178, 34, 34)
GREY = (110, 105, 90)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def fit(draw, s, path, size, max_w):
    """Largest font size <= `size` that fits `s` in `max_w`."""
    while size > 10 and text_w(draw, s, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def wrap(draw, s, f, max_w):
    """Greedy word wrap of `s` to lines fitting `max_w`."""
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(y, s, f, fill=INK):
    d.text(((W - text_w(d, s, f)) / 2, y), s, font=f, fill=fill)


def rule(y, width=3, x0=32, x1=992):
    d.line([(x0, y), (x1, y)], fill=INK, width=width)


def draw_burst(cx, cy, r, fill):
    import math
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.55
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def draw_megaphone(x, y, s):
    # cone pointing right, handle below, sound arcs
    d.polygon([(x, y + 18 * s), (x + 46 * s, y), (x + 46 * s, y + 36 * s),
               (x, y + 18 * s)], fill=(178, 34, 34))
    d.polygon([(x + 46 * s, y), (x + 56 * s, y + 6 * s),
               (x + 56 * s, y + 30 * s), (x + 46 * s, y + 36 * s)],
              fill=(120, 20, 20))
    d.rectangle([x + 10 * s, y + 18 * s, x + 20 * s, y + 38 * s],
                fill=(60, 60, 60))
    for r in (48, 62):
        d.arc([x + 56 * s - r, y + 18 * s - r, x + 56 * s + r,
               y + 18 * s + r], start=-55, end=55, fill=(178, 34, 34),
              width=4)


def draw_chip(x, y, s):
    d.rounded_rectangle([x, y, x + 56 * s, y + 56 * s], radius=8 * s,
                        fill=(30, 60, 110))
    d.rounded_rectangle([x + 14 * s, y + 14 * s, x + 42 * s, y + 42 * s],
                        radius=4 * s, fill=(247, 240, 221))
    d.text((x + 17 * s, y + 19 * s), "NV", font=font(SANS_B, int(16 * s)),
           fill=(30, 60, 110))
    for i in range(3):
        for xx, yy in ((x - 8 * s, y + (10 + i * 18) * s),
                       (x + 56 * s, y + (10 + i * 18) * s),
                       (x + (10 + i * 18) * s, y - 8 * s),
                       (x + (10 + i * 18) * s, y + 56 * s)):
            d.rectangle([xx, yy, xx + 8 * s, yy + 8 * s], fill=(30, 60, 110))


def draw_quake(x, y, s):
    pts = [(x, y + 28 * s), (x + 10 * s, y + 28 * s), (x + 16 * s, y + 8 * s),
           (x + 24 * s, y + 48 * s), (x + 32 * s, y + 16 * s),
           (x + 40 * s, y + 40 * s), (x + 48 * s, y + 28 * s),
           (x + 56 * s, y + 28 * s)]
    d.line(pts, fill=(178, 34, 34), width=5, joint="curve")


def draw_sun(x, y, s):
    d.ellipse([x + 8 * s, y + 8 * s, x + 40 * s, y + 40 * s],
              fill=(245, 180, 40))
    d.ellipse([x + 34 * s, y + 30 * s, x + 52 * s, y + 48 * s],
              fill=(90, 140, 190))


# ---- Masthead ----
center(6, "THE WORLD", font(SERIF_B, 118))
rule(138, width=4)
rule(146, width=2)

# ---- Dateline ----
center(158, "SATURDAY, 21 NOVEMBER 2026", font(SANS_B, 44), fill=RED)
center(206, "THE DAY'S WORLD NEWS  —  IN ONE PAGE", font(SANS, 21), fill=GREY)
rule(240, width=3)

# ---- Main story: Gen Z protests ----
MX, MW = 32, 620
y = 256
d.text((MX, y), "EUROPE  —  GEN Z TAKES TO THE STREETS",
       font=font(SANS_B, 25), fill=RED)
y = 288
f = fit(d, "GEN Z PROTESTS", SERIF_B, 66, MW)
d.text((MX, y), "GEN Z PROTESTS", font=f, fill=INK)
y += 68
f = fit(d, "SWEEP EUROPE", SERIF_B, 66, MW)
d.text((MX, y), "SWEEP EUROPE", font=f, fill=INK)
y += 70
deck = ("Young protesters rally in 25 countries over wars, living "
        "costs and climate.")
df = font(SERIF, 27)
for line in wrap(d, deck, df, MW):
    d.text((MX, y), line, font=df, fill=INK)
    y += 33
assert y <= 494, f"main deck overflows: y={y}"

# main-story icon: megaphone + burst, right column
draw_burst(830, 330, 52, (220, 60, 40))
draw_burst(830, 330, 30, (245, 180, 40))
draw_megaphone(700, 400, 1.0)
d.text((700, 452), "25 COUNTRIES", font=font(SANS_B, 20), fill=RED)

rule(494, width=3)

# ---- Second story: Trump / Nvidia ----
y = 510
d.text((MX, y), "WASHINGTON  —  TECH", font=font(SANS_B, 25), fill=RED)
y = 540
f = fit(d, "TRUMP URGES NVIDIA", SERIF_B, 60, MW)
d.text((MX, y), "TRUMP URGES NVIDIA", font=f, fill=INK)
y += 60
f = fit(d, "TO BRING BACK HUANG", SERIF_B, 60, MW)
d.text((MX, y), "TO BRING BACK HUANG", font=f, fill=INK)
y += 60
deck2 = ("President calls on the chip giant to reinstate its former "
         "chief and \u201cmake a big apology\u201d.")
for line in wrap(d, deck2, df, MW):
    d.text((MX, y), line, font=df, fill=INK)
    y += 33
assert y <= 730, f"second deck overflows: y={y}"

# second-story icon: chip, right column
draw_chip(724, 560, 1.0)
d.text((700, 626), "CHIPS IN FOCUS", font=font(SANS_B, 20), fill=RED)

rule(738, width=3)

# ---- Bottom row: four items ----
COL_W = 224
GAP = 16
BX = 32
BY = 752
items = [
    ("POLAND", "MISSILE AFTERMATH",
     "Tusk: missile hit as allies drill.",
     "burst"),
    ("MARKETS", "AI SELL-OFF DRAGS ON",
     "Anthropic slides as markets fall.",
     "chart"),
    ("CLIMATE", "COP31 DEAL STALLS",
     "Talks run overtime, no deal yet.",
     "sun"),
    ("PERU", "6.8 QUAKE HITS PERU",
     "Strong tremor in Junin, felt in Lima.",
     "quake"),
]
for i, (kick, head, body, icon) in enumerate(items):
    x = BX + i * (COL_W + GAP)
    d.text((x, BY), kick, font=font(SANS_B, 22), fill=RED)
    if icon == "burst":
        draw_burst(x + 28, BY + 62, 26, (220, 60, 40))
        draw_burst(x + 28, BY + 62, 15, (245, 180, 40))
    elif icon == "chart":
        d.line([(x, BY + 76), (x + 18, BY + 66), (x + 36, BY + 70),
                (x + 56, BY + 52)], fill=(178, 34, 34), width=4)
        d.polygon([(x + 56, BY + 52), (x + 48, BY + 52), (x + 56, BY + 60)],
                  fill=(178, 34, 34))
    elif icon == "sun":
        draw_sun(x, BY + 36, 1.0)
    elif icon == "quake":
        draw_quake(x, BY + 36, 1.0)
    hy = BY + 100
    hf = font(SANS_B, 24)
    for line in wrap(d, head, hf, COL_W):
        d.text((x, hy), line, font=hf, fill=INK)
        hy += 28
    by = hy + 6
    bf = font(SERIF, 20)
    for line in wrap(d, body, bf, COL_W):
        d.text((x, by), line, font=bf, fill=INK)
        by += 25
    assert by <= 966, f"bottom item {i} overflows: by={by}"

# ---- ALSO strip ----
rule(972, width=2)
also = ("ALSO:  Iran war \u2014 Houthi missiles downed  \u00b7  Mamdani: "
        "Rikers to close by 2032")
af = font(SANS, 19)
lines = wrap(d, also, af, 960)
ay = 980
for line in lines:
    d.text((32, ay), line, font=af, fill=GREY)
    ay += 22
assert ay <= 1010, f"also strip overflows: ay={ay}"

img.save("/home/hatch/workspace/makefun/news-image-21nov/entry.png")
print("saved entry.png")
