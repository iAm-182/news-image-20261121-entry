#!/usr/bin/env python3
"""news-image-20261121 — draw the front page for Saturday 21 November 2026.

Original newspaper front page drawn with PIL primitives only. No photos,
no downloaded images, no external assets. Every story on the page happened,
or was first reported, on Saturday 21 November 2026 (any time zone).

Run:  python3 draw.py   ->   writes entry.png (1024x1024) next to this file.
Deterministic: two runs write identical bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (250, 248, 243)
INK = (18, 18, 18)
NAVY = (13, 36, 68)
NAVY2 = (24, 58, 102)
RED = (178, 34, 34)
REDBRIGHT = (196, 38, 38)
BLUE = (28, 68, 140)
SKY = (198, 220, 238)
SKY2 = (168, 198, 224)
GREY = (96, 96, 96)
LINE = (40, 40, 40)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
GREEN = (34, 110, 68)

F_SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
F_SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
F_SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
F_SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
F_SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
F_SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(d, cx, y, text, f, fill):
    """Draw text centred on cx; returns its height."""
    w = d.textlength(text, font=f)
    d.text((cx - w / 2, y), text, font=f, fill=fill)
    return d.textbbox((0, 0), text, font=f)[3]


def draw_wrapped_center(d, cx, y, text, f, fill, max_w, leading):
    """Centre-wrapped paragraph; returns y just below the last line."""
    for line in wrap(d, text, f, max_w):
        h = draw_center(d, cx, y, line, f, fill)
        y += h + leading
    return y


def rule(d, x0, x1, y, wdt, fill):
    d.rectangle([x0, y, x1, y + wdt - 1], fill=fill)


# ---------------------------------------------------------------------------
# Panel illustrations — simple geometric vector art, drawn with PIL only.
# Each takes (d, x, y, w, h): the illustration box inside a panel.
# ---------------------------------------------------------------------------

def art_denmark(d, x, y, w, h):
    """Embassy building under a grey sky, Danish flag, red EXPELLED stamp."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 232, 238))
    # sky + distant rooftops
    d.rectangle([x, y + h - 20, x + w - 1, y + h - 1], fill=(148, 162, 178))
    # embassy building: 200 wide, sits on the rooftops strip
    bx, bw = x + w // 2 - 100, 200
    by = y + h - 20 - 50
    d.rectangle([bx, by, bx + bw, y + h - 20], fill=(245, 242, 235))
    d.rectangle([bx - 8, by - 8, bx + bw + 8, by], fill=(90, 100, 114))
    for i in range(4):
        cx0 = bx + 16 + i * 46
        d.rectangle([cx0, by + 12, cx0 + 18, y + h - 20], fill=(120, 128, 140))
    d.rectangle([bx + 78, by + 34, bx + 122, y + h - 20], fill=(60, 68, 80))
    # flag pole + Danish flag, kept inside the box
    px = bx - 40
    d.rectangle([px, y + 4, px + 4, y + h - 20], fill=(70, 70, 70))
    d.rectangle([px + 4, y + 4, px + 48, y + 26], fill=(178, 34, 34))
    d.rectangle([px + 17, y + 4, px + 23, y + 26], fill=(255, 255, 255))
    d.rectangle([px + 4, y + 13, px + 48, y + 18], fill=(255, 255, 255))
    # red stamp
    f = font(F_SANS_BOLD, 21)
    txt = "EXPELLED"
    tw = d.textlength(txt, font=f)
    sx, sy = x + w - tw - 34, y + 10
    d.rectangle([sx - 8, sy - 4, sx + tw + 8, sy + 26], outline=RED, width=3)
    d.text((sx, sy), txt, font=f, fill=RED)


def art_markets(d, x, y, w, h):
    """Falling red chart line on white, with a big -5.3% callout."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255))
    # faint grid
    for gx in range(x + 24, x + w, 44):
        d.line([(gx, y + 8), (gx, y + h - 8)], fill=(232, 232, 232), width=1)
    for gy in range(y + 16, y + h, 30):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(236, 236, 236), width=1)
    # falling line (kept clear of the top-right callout)
    pts = [(x + 14, y + 26), (x + 60, y + 34), (x + 105, y + 30),
           (x + 150, y + 50), (x + 195, y + 46), (x + 240, y + 68),
           (x + 285, y + 64), (x + 320, y + h - 16)]
    d.line(pts, fill=RED, width=5, joint="curve")
    for px, py in pts[1:-1]:
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED)
    # arrow head at the end
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 16, ey - 4), (ex - 6, ey - 16)], fill=RED)
    # callout
    f = font(F_SANS_BOLD, 40)
    d.text((x + w - 168, y + 6), "-5.3%", font=f, fill=RED)
    f2 = font(F_SANS_BOLD, 17)
    d.text((x + 14, y + 6), "NASDAQ", font=f2, fill=GREY)


def art_ukeu(d, x, y, w, h):
    """EU circle of gold stars on deep blue, with a UK red cross corner."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY2)
    import math
    cx, cy, r = x + w // 2 - 52, y + h // 2, 30
    for i in range(12):
        a = math.radians(i * 30 - 90)
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        star(d, sx, sy, 6, GOLD)
    # small Union Jack block, bottom right
    jx, jy, jw, jh = x + w - 118, y + h - 44, 96, 34
    d.rectangle([jx, jy, jx + jw, jy + jh], fill=(250, 250, 250))
    d.rectangle([jx, jy + jh // 2 - 4, jx + jw, jy + jh // 2 + 4], fill=RED)
    d.rectangle([jx + jw // 2 - 4, jy, jx + jw // 2 + 4, jy + jh], fill=RED)
    d.rectangle([jx, jy, jx + jw, jy + jh], outline=NAVY, width=2)
    # pound / euro marks
    f = font(F_SERIF_BOLD, 26)
    d.text((x + 16, y + h - 40), "£  €", font=f, fill=WHITE)


def star(d, cx, cy, r, fill):
    """Five-point star centred at (cx, cy)."""
    import math
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


def art_summit(d, x, y, w, h):
    """Three flags on poles: USA, China, Russia — the Shenzhen trilateral."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(238, 234, 224))
    # table line
    d.rectangle([x, y + h - 12, x + w - 1, y + h - 9], fill=(120, 110, 96))
    flags = [
        ("usa", 60),
        ("chn", 190),
        ("rus", 320),
    ]
    for kind, fx in flags:
        fx += x
        fy = y + 8
        fw, fh = 104, 42
        # pole
        d.rectangle([fx + 52, y + 2, fx + 56, y + h - 10], fill=(80, 76, 70))
        d.ellipse([fx + 49, y - 1, fx + 59, y + 9], fill=GOLD)
        if kind == "usa":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255))
            for s in range(3):
                d.rectangle([fx, fy + s * 15, fx + fw, fy + s * 15 + 7],
                            fill=(178, 34, 34))
            d.rectangle([fx, fy, fx + 44, fy + 21], fill=NAVY)
        elif kind == "chn":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            star(d, fx + 20, fy + 12, 8, GOLD)
            star(d, fx + 36, fy + 8, 4, GOLD)
            star(d, fx + 41, fy + 17, 4, GOLD)
            star(d, fx + 36, fy + 26, 4, GOLD)
        else:
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(255, 255, 255))
            d.rectangle([fx, fy + 14, fx + fw, fy + 28], fill=(0, 57, 166))
            d.rectangle([fx, fy + 28, fx + fw, fy + fh], fill=(213, 0, 50))
    # (table line above carries the scene; no name plates needed)


# ---------------------------------------------------------------------------
# Front-page layout
# ---------------------------------------------------------------------------

PANELS = [
    ("DENMARK EXPELS RUSSIAN DIPLOMAT",
     "Copenhagen says Moscow plotted to kill rapper Kyivstoner",
     art_denmark),
    ("STOCKS PLUNGE INTO CORRECTION",
     "S&P 500 falls 3.7%; Nasdaq down 5.3% as AI shares sell off",
     art_markets),
    ("UK AND EU SIGN FOOD AND TRADE DEALS",
     "Burnham signs food, carbon, youth-mobility deals",
     art_ukeu),
    ("TRUMP, XI AND PUTIN MEET — FEW RESULTS",
     "First trilateral summit in Shenzhen ends with little concrete",
     art_summit),
]

MORE = [
    ("IPO", "Anthropic falls 9% a day after its record IPO"),
    ("GAMES", "GTA VI takes $3.79bn in first-day sales"),
    ("WEATHER", "Cyclone Akvan crosses the Odisha coast"),
    ("BORDERS", "Estonia shuts all crossings to Russia"),
    ("JUSTICE", "Jury convicts man who started LA's Palisades Fire"),
    ("GULF", "Saudi coalition intercepts Houthi missiles over Riyadh"),
    ("SPORT", "F1: Las Vegas Grand Prix under the lights tonight"),
    ("CHIPS", "US approves ~880,000 AI chip sales to China"),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    cx = W // 2
    margin = 16
    cw = W - 2 * margin  # 992 content width

    # outer border
    d.rectangle([8, 8, W - 9, H - 9], outline=NAVY, width=5)

    y = 20
    # --- masthead band -----------------------------------------------------
    d.rectangle([margin, y, W - margin - 1, y + 52], fill=NAVY)
    f = font(F_SANS_BOLD, 40)
    draw_center(d, cx, y + 6, "THE WORLD TODAY", f, WHITE)
    y += 52 + 8
    # --- date line ---------------------------------------------------------
    f = font(F_SERIF_BOLD, 46)
    draw_center(d, cx, y, "SATURDAY 21 NOVEMBER 2026", f, NAVY)
    y += 58
    rule(d, margin, W - margin - 1, y, 4, RED)
    y += 14

    # --- lead headline ------------------------------------------------------
    f = font(F_SERIF_BOLD, 70)
    draw_center(d, cx, y, "RUSSIAN MISSILES", f, INK)
    y += 78
    draw_center(d, cx, y, "HIT POLAND", f, INK)
    y += 78
    # --- lead subhead -------------------------------------------------------
    f = font(F_SERIF_IT, 25)
    y = draw_wrapped_center(
        d, cx, y + 2,
        "Two missiles and a suspected drone come down in the south-east; "
        "Warsaw calls it a deliberate provocation — NATO condemns a grave "
        "violation of its airspace",
        f, NAVY, 940, 6)
    y += 4
    rule(d, margin, W - margin - 1, y, 3, RED)
    y += 12

    # --- second headline ----------------------------------------------------
    f = font(F_SERIF_BOLD, 35)
    draw_center(d, cx, y, "KYIV HIT IN MASSIVE OVERNIGHT STRIKE", f, INK)
    y += 44
    f = font(F_SERIF_IT, 22)
    draw_center(d, cx, y,
                "At least eight killed as Russia pounds the capital; France "
                "seeks a UN Security Council meeting",
                f, NAVY)
    y += 30

    # --- four illustrated panels -------------------------------------------
    pw = (cw - 12) // 2
    ph = 170
    for i, (title, label, art) in enumerate(PANELS):
        px = margin + (i % 2) * (pw + 12)
        py = y + (i // 2) * (ph + 12)
        d.rectangle([px, py, px + pw - 1, py + ph - 1], outline=NAVY, width=2)
        art(d, px + 2, py + 2, pw - 4, 80)
        f = font(F_SANS_BOLD, 24)
        ty = py + 88
        lines = wrap(d, title, f, pw - 16)
        for line in lines[:2]:
            draw_center(d, px + pw // 2, ty, line, f, INK)
            ty += 28
        f = font(F_SERIF, 19)
        ly = ty + 2
        for line in wrap(d, label, f, pw - 16)[:1]:
            draw_center(d, px + pw // 2, ly, line, f, (60, 60, 60))
    y += 2 * ph + 12 + 10

    # --- more of the day ----------------------------------------------------
    f = font(F_SANS_BOLD, 23)
    d.text((margin, y), "MORE OF THE DAY", font=f, fill=NAVY)
    rule(d, margin + 218, W - margin - 1, y + 12, 2, RED)
    y += 34
    col_w = (cw - 24) // 2
    fk = font(F_SANS_BOLD, 18)
    ft = font(F_SANS, 18)
    for i, (kick, text) in enumerate(MORE):
        col = i % 2
        row = i // 2
        ix = margin + col * (col_w + 24)
        iy = y + row * 26
        d.text((ix, iy), kick + "  ", font=fk, fill=RED)
        kw = d.textlength(kick + "  ", font=fk)
        d.text((ix + kw, iy), text, font=ft, fill=INK)
    y += 4 * 26 + 8

    # --- footer: date check --------------------------------------------------
    d.rectangle([margin, y, W - margin - 1, y + 30], fill=NAVY)
    f = font(F_SANS_BOLD, 17)
    draw_center(d, cx, y + 6,
                "SATURDAY 21 NOVEMBER 2026  ·  EVERY STORY FIRST REPORTED TODAY",
                f, WHITE)
    y += 30

    print("layout bottom y =", y, "(canvas", H, ")")
    return img


if __name__ == "__main__":
    image = build()
    out = os.path.join(HERE, "entry.png")
    image.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")
