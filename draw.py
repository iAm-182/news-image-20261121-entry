#!/usr/bin/env python3
"""news-image-20261121 v2 — front page for Saturday 21 November 2026.

Original newspaper front page drawn with PIL primitives only. No photos,
no downloaded images, no external assets. 44 stories, every one of them an
event of Saturday 21 November 2026 or first reported that day (any time
zone), verified against live reporting on 21 Nov 2026. Two things v1 got
wrong are fixed here: the Shenzhen trilateral summit ENDED on 19 Nov, so it
is not listed as today's news (it is named in the DATE CHECK box instead),
and the Poland missile crash was 20 Nov — today's story is Rutte flying to
Warsaw and Poland asking NATO for reinforcements.

Run:  python3 draw.py   ->   writes entry.png (1024x1024) next to this file.
Deterministic: two runs write identical bytes.
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (158, 28, 34)
REDBRIGHT = (176, 32, 38)
BROWN = (122, 74, 52)
NAVY = (22, 40, 63)
NAVY2 = (16, 32, 52)
TAN = (217, 201, 163)
TAN2 = (226, 212, 178)
GREY = (90, 88, 82)
LINE = (60, 58, 52)
WHITE = (250, 248, 242)
CREAM = (238, 231, 214)
GOLD = (184, 134, 42)
GREEN = (46, 110, 72)
TEAL = (18, 110, 106)
SKY = (198, 220, 238)
ORANGE = (247, 147, 26)

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


def tw(d, text, f):
    return d.textlength(text, font=f)


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


def fit_one(d, text, f, max_w):
    """Shorten with an ellipsis until the single line fits."""
    if d.textlength(text, font=f) <= max_w:
        return text
    while len(text) > 4 and d.textlength(text + "\u2026", font=f) > max_w:
        text = text[:-1]
    return text + "\u2026"


def para(d, x, y, text, f, max_w, leading, fill=INK, max_lines=None):
    """Draw a wrapped paragraph; returns y after the last line."""
    lines = wrap(d, text, f, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def hrule(d, x0, x1, y, wdt=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------------------
# Panel illustrations — simple geometric vector art, drawn with PIL only.
# Each takes (d, x, y, w, h): the illustration box inside a card.
# ---------------------------------------------------------------------------

def art_poland(d, x, y, w, h):
    """White-red Polish flag, missile streaks, NATO compass star."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 236, 226))
    # flag: white over red, waving on a pole
    fx, fy, fw, fh = x + 24, y + 14, 150, 66
    d.rectangle([fx, fy, fx + 8, y + h - 8], fill=(80, 76, 70))
    d.rectangle([fx + 8, fy, fx + fw, fy + fh // 2], fill=(255, 255, 255))
    d.rectangle([fx + 8, fy + fh // 2, fx + fw, fy + fh], fill=(220, 20, 60))
    d.rectangle([fx + 8, fy, fx + fw, fy + fh], outline=INK, width=1)
    # three missile streaks crossing the sky
    for i, yy in enumerate((y + 22, y + 44, y + 66)):
        x0 = x + w - 130 + i * 12
        d.line([(x0, yy), (x0 + 96, yy + 10)], fill=RED, width=4)
        d.ellipse([x0 + 92, yy + 4, x0 + 104, yy + 16], fill=RED)
        d.ellipse([x0 - 4, yy - 3, x0 + 6, yy + 7], fill=(255, 210, 90))
    # NATO compass star, bottom right, clear of the strip
    cx, cy = x + w - 42, y + h - 46
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=NAVY)
    star(d, cx, cy, 17, WHITE)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=NAVY)


def art_cop31(d, x, y, w, h):
    """Green globe, rising sun, OVERTIME banner."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 238, 226))
    cx, cy, r = x + w // 2 - 40, y + h // 2 + 6, 46
    # sun rays
    for i in range(12):
        a = math.radians(i * 30)
        d.line([(cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a)),
                (cx + (r + 14) * math.cos(a), cy + (r + 14) * math.sin(a))],
               fill=GOLD, width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 72))
    d.ellipse([cx - r + 10, cy - 18, cx - 2, cy + 6], fill=(120, 190, 130))
    d.ellipse([cx + 6, cy + 8, cx + r - 8, cy + r - 6], fill=(120, 190, 130))
    # overtime banner
    f = font(F_SANS_BOLD, 16)
    txt = "OVERTIME"
    twd = d.textlength(txt, font=f)
    bx = x + w - twd - 26
    d.rectangle([bx - 8, y + 8, bx + twd + 8, y + 32], fill=RED)
    d.text((bx, y + 9), txt, font=f, fill=WHITE)


def art_peru(d, x, y, w, h):
    """Andes peaks, seismic wave, M6.7 callout."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 222, 200))
    # mountains
    d.polygon([(x, y + h), (x + 70, y + 18), (x + 150, y + h)], fill=(122, 74, 52))
    d.polygon([(x + 110, y + h), (x + 190, y + 34), (x + w, y + h)],
              fill=(90, 60, 44))
    # snow caps
    d.polygon([(x + 58, y + 34), (x + 70, y + 18), (x + 84, y + 36),
               (x + 76, y + 40), (x + 70, y + 32), (x + 64, y + 40)],
              fill=WHITE)
    # seismic wave across the bottom
    pts = []
    for i in range(25):
        px = x + 10 + i * (w - 20) / 24
        py = y + h - 26 + (10 if i % 4 == 0 else (-8 if i % 4 == 2 else 0))
        pts.append((px, py))
    d.line(pts, fill=RED, width=3, joint="curve")
    f = font(F_SANS_BOLD, 30)
    d.text((x + w - 108, y + 8), "M6.7", font=f, fill=RED)
    f2 = font(F_SANS_BOLD, 14)
    d.text((x + 16, y + 10), "CENTRAL PERU", font=f2, fill=NAVY)


def art_mercury(d, x, y, w, h):
    """Dark space, cratered Mercury, two orbiters on an ellipse."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(12, 16, 28))
    for sx, sy, sr in ((16, 8, 1), (36, 18, 1), (w - 24, 8, 1),
                       (w - 40, 20, 1), (w - 70, 6, 1)):
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=WHITE)
    r = max(12, h // 2 - 8)
    cx, cy = x + w // 2, y + h // 2 + 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 152, 132))
    for ox, oy, orr in ((-r // 2, -r // 3, 4), (r // 3, r // 3, 3),
                        (r // 2, -r // 2, 2)):
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                  fill=(120, 106, 88))
    # orbit ellipse + two orbiters
    rx, ry = w // 2 - 14, h // 2 - 4
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=GOLD, width=2)
    d.rectangle([cx - rx - 4, cy - ry - 2, cx - rx + 4, cy - ry + 4],
                fill=(240, 240, 240))
    d.rectangle([cx + rx - 4, cy + ry - 4, cx + rx + 4, cy + ry + 2],
                fill=(240, 240, 240))


def art_markets(d, x, y, w, h):
    """Falling red chart line, -5.3% callout on a white patch."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(255, 255, 255))
    for gx in range(x + 20, x + w, 36):
        d.line([(gx, y + 6), (gx, y + h - 6)], fill=(232, 232, 232), width=1)
    for gy in range(y + 12, y + h, 22):
        d.line([(x + 6, gy), (x + w - 6, gy)], fill=(236, 236, 236), width=1)
    pts = [(x + 10, y + 22), (x + 40, y + 26), (x + 70, y + 24),
           (x + 100, y + 34), (x + 130, y + 32), (x + 158, y + 42),
           (x + 182, y + h - 8)]
    d.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts[1:-1]:
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED)
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 14, ey - 3), (ex - 5, ey - 14)], fill=RED)
    # callout on a white patch so the line never crosses the text
    f = font(F_SANS_BOLD, 22)
    txt = "-5.3%"
    twd = d.textlength(txt, font=f)
    d.rectangle([x + w - twd - 14, y + 2, x + w - 2, y + 28], fill=WHITE)
    d.text((x + w - twd - 8, y + 3), txt, font=f, fill=RED)
    f2 = font(F_SANS_BOLD, 11)
    d.text((x + 8, y + 4), "NASDAQ", font=f2, fill=GREY)


def art_riyadh(d, x, y, w, h):
    """Night skyline, three interceptor streaks."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(16, 24, 44))
    for sx, sy, sr in ((20, 8, 1), (60, 14, 1), (120, 7, 1), (160, 12, 1)):
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=WHITE)
    # towers, heights scaled to the box
    base = y + h
    for tx, twd, tht in ((12, 24, 30), (42, 18, 40), (66, 28, 26),
                         (100, 20, 36), (126, 24, 30), (156, 16, 34)):
        d.rectangle([x + tx, base - tht, x + tx + twd, base],
                    fill=(70, 88, 120))
        for wy in range(base - tht + 6, base - 4, 9):
            d.rectangle([x + tx + 4, wy, x + tx + twd - 4, wy + 3],
                        fill=(255, 210, 90))
    # three interceptor arcs across the upper sky
    for i in range(3):
        x0 = x + 26 + i * 52
        d.arc([x0, y + 4, x0 + 52, y + 32], start=200, end=340, fill=GOLD,
              width=3)
        d.ellipse([x0 + 46, y + 6, x0 + 52, y + 12], fill=(255, 210, 90))


def art_denmark(d, x, y, w, h):
    """Embassy building, Danish flag, red EXPELLED stamp."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 232, 238))
    d.rectangle([x, y + h - 10, x + w - 1, y + h - 1], fill=(148, 162, 178))
    bh = min(30, h - 18)
    bx, bw = x + w // 2 - 52, 104
    by = y + h - 10 - bh
    d.rectangle([bx, by, bx + bw, y + h - 10], fill=(245, 242, 235))
    d.rectangle([bx - 5, by - 4, bx + bw + 5, by], fill=(90, 100, 114))
    for i in range(3):
        cx0 = bx + 10 + i * 32
        d.rectangle([cx0, by + 8, cx0 + 12, y + h - 10], fill=(120, 128, 140))
    d.rectangle([bx + 44, by + bh - 12, bx + 62, y + h - 10], fill=(60, 68, 80))
    px = bx - 26
    d.rectangle([px, y + 4, px + 3, y + h - 10], fill=(70, 70, 70))
    d.rectangle([px + 3, y + 4, px + 32, y + 19], fill=(178, 34, 34))
    d.rectangle([px + 11, y + 4, px + 15, y + 19], fill=(255, 255, 255))
    d.rectangle([px + 3, y + 10, px + 32, y + 13], fill=(255, 255, 255))
    f = font(F_SANS_BOLD, 13)
    txt = "EXPELLED"
    twd = d.textlength(txt, font=f)
    sx, sy = x + w - twd - 20, y + 6
    d.rectangle([sx - 5, sy - 2, sx + twd + 5, sy + 17], outline=RED, width=2)
    d.text((sx, sy), txt, font=f, fill=RED)


def art_bitcoin(d, x, y, w, h):
    """Orange coin with a B, red down arrow, price on a white patch."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(250, 244, 232))
    cx, cy, r = x + 46, y + h // 2 + 2, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ORANGE)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 110, 0), width=2)
    f = font(F_SANS_BOLD, 28)
    d.text((cx - 10, cy - 16), "B", font=f, fill=WHITE)
    # falling steps, kept clear of the price patch
    pts = [(x + 92, y + 30), (x + 116, y + 34), (x + 116, y + 40),
           (x + 140, y + 44), (x + 140, y + h - 8)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 12, ey - 2), (ex - 2, ey - 12)], fill=RED)
    f2 = font(F_SANS_BOLD, 18)
    txt = "$58.8k"
    twd = d.textlength(txt, font=f2)
    d.rectangle([x + w - twd - 12, y + 2, x + w - 2, y + 24], fill=(250, 244, 232))
    d.text((x + w - twd - 6, y + 3), txt, font=f2, fill=RED)


def art_nvidia(d, x, y, w, h):
    """Black chip, green eye, red slide."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(18, 22, 18))
    # chip
    cx0, cy0, cw, ch = x + 16, y + 12, 84, 44
    d.rectangle([cx0, cy0, cx0 + cw, cy0 + ch], fill=(30, 36, 30),
                outline=(118, 185, 0), width=2)
    for i in range(4):
        d.line([(cx0 + 12 + i * 20, cy0 - 5), (cx0 + 12 + i * 20, cy0)],
               fill=(118, 185, 0), width=3)
        d.line([(cx0 + 12 + i * 20, cy0 + ch),
                (cx0 + 12 + i * 20, cy0 + ch + 5)], fill=(118, 185, 0),
               width=3)
    f = font(F_SANS_BOLD, 15)
    d.text((cx0 + 8, cy0 + 12), "NVDA", font=f, fill=(118, 185, 0))
    # red slide
    pts = [(x + 118, y + 14), (x + 146, y + 26), (x + 172, y + 40),
           (x + 192, y + h - 12)]
    d.line(pts, fill=RED, width=4, joint="curve")


def art_gaza(d, x, y, w, h):
    """Flood water, aid crates, four flags."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(214, 230, 240))
    # four small flags: AU, CA, IT, UK
    flags = [((16, 8), (200, 60, 60)), ((52, 8), (220, 30, 30)),
             ((88, 8), (40, 90, 160)), ((124, 8), (30, 60, 120))]
    for (fx, fy), col in flags:
        d.rectangle([x + fx, y + fy, x + fx + 4, y + fy + 26], fill=(70, 70, 70))
        d.rectangle([x + fx + 4, y + fy, x + fx + 30, y + fy + 18], fill=col)
        d.rectangle([x + fx + 4, y + fy, x + fx + 30, y + fy + 18],
                    outline=INK, width=1)
    # flood waves
    for wy in (y + 44, y + 54):
        pts = []
        for i in range(21):
            px = x + i * (w / 20)
            py = wy + (4 if i % 2 == 0 else -4)
            pts.append((px, py))
        d.line(pts, fill=(28, 68, 140), width=3, joint="curve")
    # aid crates
    for bx, by in ((x + 30, y + h - 30), (x + 78, y + h - 30),
                   (x + 126, y + h - 30)):
        d.rectangle([bx, by, bx + 34, by + 22], fill=(184, 134, 42),
                    outline=(120, 84, 20), width=2)
        d.line([(bx, by + 11), (bx + 34, by + 11)], fill=(120, 84, 20), width=2)


def art_israel(d, x, y, w, h):
    """Knesset-style building, Star of David, blue/white."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 238, 246))
    bh = min(26, h - 20)
    bx, bw = x + w // 2 - 56, 112
    by = y + h - 10 - bh
    d.rectangle([bx, by, bx + bw, y + h - 10], fill=(245, 245, 245),
                outline=NAVY, width=2)
    d.polygon([(bx - 6, by), (bx + bw // 2, by - 10), (bx + bw + 6, by)],
              fill=NAVY)
    for i in range(4):
        cx0 = bx + 10 + i * 26
        d.rectangle([cx0, by + 8, cx0 + 12, y + h - 10], fill=NAVY)
    # Star of David
    cx, cy = x + w - 34, y + 22
    d.polygon([(cx, cy - 14), (cx + 12, cy + 8), (cx - 12, cy + 8)],
              outline=(0, 56, 184), width=2)
    d.polygon([(cx, cy + 14), (cx + 12, cy - 8), (cx - 12, cy - 8)],
              outline=(0, 56, 184), width=2)


def art_siberia(d, x, y, w, h):
    """Grey sky, transport plane silhouette, smoke, snow."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(220, 224, 228))
    d.rectangle([x, y + h - 8, x + w - 1, y + h - 1], fill=WHITE)
    # plane silhouette diving
    d.polygon([(x + 16, y + 12), (x + 110, y + 24), (x + 148, y + 30),
               (x + 112, y + 33), (x + 24, y + 22)], fill=(40, 44, 50))
    d.polygon([(x + 52, y + 15), (x + 72, y + 6), (x + 80, y + 17)],
              fill=(40, 44, 50))
    d.polygon([(x + 120, y + 27), (x + 138, y + 20), (x + 142, y + 30)],
              fill=(40, 44, 50))
    # smoke puffs, kept inside the box
    for sx, sy, sr in ((140, 36, 6), (156, 42, 8), (172, 38, 6)):
        d.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                  fill=(140, 140, 140))
    # snow dots
    for sx, sy in ((24, 40), (60, 44), (96, 38), (34, 46), (80, 46)):
        d.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2], fill=WHITE)


def art_f1(d, x, y, w, h):
    """Chequered flag, night race car, neon strip."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(14, 14, 24))
    # chequered flag
    fx, fy = x + 12, y + 8
    for r in range(3):
        for c in range(6):
            col = (255, 255, 255) if (r + c) % 2 == 0 else (20, 20, 20)
            d.rectangle([fx + c * 12, fy + r * 12, fx + c * 12 + 11,
                         fy + r * 12 + 11], fill=col)
    d.rectangle([fx, fy, fx + 72, fy + 36], outline=WHITE, width=1)
    # race car silhouette
    car_y = y + h - 34
    d.rectangle([x + 96, car_y, x + 186, car_y + 14], fill=(196, 38, 38))
    d.polygon([(x + 118, car_y), (x + 130, car_y - 12), (x + 158, car_y - 12),
               (x + 168, car_y)], fill=(196, 38, 38))
    for wx in (112, 168):
        d.ellipse([x + wx, car_y + 10, x + wx + 16, car_y + 26], fill=(10, 10, 10),
                  outline=(200, 200, 200), width=2)
    # neon strip
    d.rectangle([x, y + h - 6, x + w - 1, y + h - 1], fill=(255, 210, 90))
    f = font(F_SANS_BOLD, 13)
    d.text((x + 96, y + 10), "LAS VEGAS", font=f, fill=(255, 210, 90))


# ---------------------------------------------------------------------------
# Simplified world map (stylised, approximate coastlines)
# ---------------------------------------------------------------------------

CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 16),
     (-105, 20), (-115, 30), (-125, 40), (-125, 49), (-140, 60), (-165, 60)],
    [(-80, 10), (-60, 10), (-50, 0), (-35, -8), (-40, -20), (-50, -30),
     (-65, -40), (-70, -55), (-73, -40), (-70, -20), (-80, -5)],
    [(-10, 36), (-9, 43), (0, 48), (-2, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (28, 60), (30, 70), (40, 68), (45, 60), (40, 50),
     (30, 45), (23, 40), (19, 42), (12, 44), (3, 42), (-2, 37)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -20), (32, -29), (25, -34),
     (18, -35), (12, -18), (8, 4), (-8, 5), (-15, 11)],
    [(40, 68), (60, 70), (70, 72), (90, 75), (110, 77), (130, 72), (160, 70),
     (180, 66), (170, 60), (160, 55), (140, 45), (130, 35), (122, 30),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (80, 13), (75, 8),
     (70, 20), (60, 25), (50, 28), (45, 30), (42, 40)],
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (150, -37),
     (153, -27), (146, -19), (142, -11), (135, -12), (130, -13), (122, -17),
     (114, -22)],
]

# story number -> (lon, lat) for the map pins
PINS = {
    1: (21, 52), 2: (30.7, 36.9), 3: (-76, -11), 5: (-74, 40.7),
    6: (46.7, 24.7), 7: (12.6, 55.7), 8: (-0.1, 51.5), 9: (-121, 37.4),
    10: (34.5, 31.5), 11: (35.2, 31.8), 12: (85, 58), 13: (-115.1, 36.2),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=NAVY2)
    def proj(lon, lat):
        px = x + (lon + 168.0) / 360.0 * w
        py = y + (84.0 - lat) / 142.0 * h
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=TAN)
    for lon in (-120, -60, 0, 60, 120):
        px = x + (lon + 168.0) / 360.0 * w
        d.line([(px, y), (px, y + h)], fill=(44, 66, 96), width=1)
    for lat in (60, 30, 0, -30):
        py = y + (84.0 - lat) / 142.0 * h
        d.line([(x, py), (x + w, py)], fill=(44, 66, 96), width=1)
    for n, (lon, lat) in sorted(PINS.items()):
        px, py = proj(lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=WHITE,
                  width=2)
        f = font(F_SANS_BOLD, 9 if n < 10 else 8)
        twd = d.textlength(str(n), font=f)
        d.text((px - twd / 2, py - 5), str(n), font=f, fill=WHITE)
    # space tag for story 4 (BepiColombo at Mercury)
    d.ellipse([x + 10, y + h - 22, x + 24, y + h - 8], fill=RED, outline=WHITE,
              width=2)
    d.text((x + 17, y + h - 21), "4", font=font(F_SANS_BOLD, 9), fill=WHITE)
    d.text((x + 28, y + h - 22), "SPACE \u00b7 MERCURY", font=font(F_SANS_BOLD, 10),
           fill=WHITE)


# ---------------------------------------------------------------------------
# Stories — every one an event of, or first reported on, Sat 21 Nov 2026
# (any time zone), verified against live reporting on 21 Nov 2026.
# ---------------------------------------------------------------------------

ART = {
    "poland": art_poland, "cop31": art_cop31, "peru": art_peru,
    "mercury": art_mercury, "markets": art_markets, "riyadh": art_riyadh,
    "denmark": art_denmark, "bitcoin": art_bitcoin, "nvidia": art_nvidia,
    "gaza": art_gaza, "israel": art_israel, "siberia": art_siberia,
    "f1": art_f1,
}

FEATURES = [
    dict(
        n=1, place="WARSAW, POLAND", tag="NATO", art="poland",
        head="Rutte flies to Warsaw as Poland seeks NATO reinforcements",
        body=("NATO chief heads to Poland today after two Russian missiles "
              "and a drone came down in the south-east; Warsaw calls it a "
              "grave violation and asks for more Eastern Sentry forces."),
        src="(Reuters, AP)",
        strip="RUTTE IN WARSAW TODAY \u00b7 EASTERN SENTRY",
    ),
    dict(
        n=2, place="ANTALYA, TURKEY", tag="CLIMATE", art="cop31",
        head="COP31 talks run into overtime with no deal in sight",
        body=("Negotiators work an extra day after the draft deal drops every "
              "mention of fossil fuels and a $120bn adaptation target; small "
              "island states warn the summit risks being a failure."),
        src="(AP, Reuters)",
        strip="3RD DRAFT DUE SATURDAY \u00b7 NO FOSSIL FUELS",
    ),
    dict(
        n=3, place="CENTRAL PERU", tag="QUAKE", art="peru",
        head="Magnitude 6.7 earthquake shakes Peru's Andes",
        body=("Tremor strikes 9 km from Carhuamayo at 00:09 UTC, felt across "
              "Lima; no casualties or serious damage reported as aftershock "
              "checks continue through the morning."),
        src="(USGS, AFP)",
        strip="00:09 UTC \u00b7 DEPTH 108 KM \u00b7 NO TSUNAMI",
    ),
]

MEDIUMS = [
    dict(n=4, place="MERCURY", tag="SPACE", art="mercury",
         head="BepiColombo enters orbit around Mercury",
         body=("After eight years in space, ESA and JAXA's twin orbiters are "
               "captured by the innermost planet; science starts April 2027."),
         src="(ESA, Sky & Telescope)"),
    dict(n=5, place="NEW YORK", tag="MARKETS", art="markets",
         head="Wall Street ends its week in correction",
         body=("S&P 500 falls 3.7%, Nasdaq drops 5.3% into the red for the "
               "year; about $7 trillion of US stock value wiped out in a week."),
         src="(Bloomberg, Coinbell)"),
    dict(n=6, place="RIYADH", tag="GULF", art="riyadh",
         head="Saudi defences down three Houthi missiles over Riyadh",
         body=("Third night of alerts in the capital; two more missiles hit "
               "at Jazan on Friday as the cross-border attacks intensify."),
         src="(Reuters)"),
    dict(n=7, place="COPENHAGEN", tag="SECURITY", art="denmark",
         head="Denmark expels Russian diplomat over 'assassination plot'",
         body=("Copenhagen says Moscow plotted to kill rapper Kyivstoner, an "
               "American-Ukrainian citizen; Moscow denies the claim."),
         src="(Reuters, DR)"),
    dict(n=8, place="CRYPTO", tag="CRYPTO", art="bitcoin",
         head="Bitcoin slides below $59,000 as $1.9bn is liquidated",
         body=("292,000 traders wiped out in a day; Ether falls 7.6% and the "
               "fear index sits at 12, deep in extreme fear."),
         src="(Cointelegraph, CoinGecko)"),
    dict(n=9, place="SILICON VALLEY", tag="TECH", art="nvidia",
         head="Nvidia's worst week since 2008 as chip probe opens",
         body=("Shares fall 23% in a week; the firm hires a top law firm to "
               "probe claims about its chief's alleged link to a Chinese spy."),
         src="(Bloomberg, Munich Eye)"),
    dict(n=10, place="GAZA", tag="AID", art="gaza",
         head="Four allies urge Israel to let aid into flooded Gaza",
         body=("Australia, Canada, Italy and the UK call for immediate, "
               "unrestricted humanitarian access as floods add to suffering."),
         src="(The Paris Eye)"),
    dict(n=11, place="JERUSALEM", tag="ISRAEL", art="israel",
         head="President taps Eisenkot to form Israel's next government",
         body=("Herzog picks the former army chief over sitting PM Netanyahu, "
               "opening a new round of coalition talks in Jerusalem."),
         src="(The Paris Eye)"),
    dict(n=12, place="SIBERIA", tag="CRASH", art="siberia",
         head="Russian military transport plane crashes; 19 killed",
         body=("All aboard die when the aircraft comes down in an unpopulated "
               "area of western Siberia, the defence ministry says."),
         src="(Munich Eye)"),
    dict(n=13, place="LAS VEGAS", tag="SPORT", art="f1",
         head="Russell tops final practice; qualifying under the lights",
         body=("Mercedes quickest in FP3 ahead of Antonelli and Norris; five "
               "drivers carry grid penalties into tonight's session."),
         src="(Formula 1, Sky Sports)"),
]

BRIEFS = [
    ("KRYVYI RIH", "Russian strike kills 2, injures 42, incl. children", "Vilkul"),
    ("LONDON", "UK-EU sign food, carbon, youth-mobility deals", "Council"),
    ("WASHINGTON", "US approved ~900k AI chip exports to China", "House"),
    ("PARIS", "Fourth weekend of cost-of-living protests in France", "AFP"),
    ("CARACAS", "US details $12bn in Venezuelan oil and mineral revenue", "State Dept"),
    ("PARIS", "Police convicted over 2020 Zecler beating", "Court"),
    ("HELSINKI", "Finland approves world's first nuclear waste repository", "STUK"),
    ("BERLIN", "Suspected Russian spy arrested", "BKA"),
    ("KYIV", "Zelensky accuses US of blocking paid missile deliveries", "Kyiv"),
    ("BERLIN", "Germany hosts Digital Summit on AI's global role", "Govt"),
    ("BERLIN", "Coalition talks begin: Left, Greens and SPD", "RBB"),
    ("HOLLYWOOD", "Tom Skerritt, star of 'Top Gun' and 'Alien', dies at 93", "AP"),
    ("VIENNA", "Austria's Foreign Ministry website hacked", "ORF"),
    ("HORMUZ", "Tanker strike and fire reported in Strait of Hormuz", "UKMTO"),
    ("TURIN", "Zverev beats Fils to reach ATP Finals semi-finals", "ATP"),
    ("BHOPAL", "India women beat Malaysia 4-1 in hockey opener", "Hockey India"),
    ("ODISHA", "Akvan weakens; red alert as rains lash Bengal, Bihar", "IMD"),
    ("WASHINGTON", "Trump threatens penalties on US tech AI hubs", "White House"),
    ("NEW YORK", "Man jailed 19 years in Sikh separatist murder plot", "DOJ"),
    ("HAVANA", "American woman freed after 10 years in Cuba returns home", "AP"),
    ("TALLINN", "Estonia shuts all border crossings to Russia", "ERR"),
    ("LOS ANGELES", "Man convicted of starting the Palisades Fire", "Court"),
    ("LOS ANGELES", "GTA VI takes $3.79bn on first day", "Take-Two"),
    ("NEW YORK", "Anthropic slides 9% a day after its record IPO", "Nasdaq"),
    ("NEW DELHI", "Modi visits 3 states; Delhi Zoo shut for SCO forum", "PMO"),
    ("WASHINGTON", "US sanctions four Iranians over oil revenues", "Treasury"),
    ("NEW YORK", "France seeks UN Security Council meeting on Poland", "UN"),
    ("SHENZHEN", "APEC goes on without Trump after he flies home", "APEC"),
    ("LAUSANNE", "World Boxing backs governance plan for LA28", "IBA"),
    ("BANGKOK", "Thailand, China boost Mekong pollution pact", "NBT"),
    ("KHARAGPUR", "IIT Kharagpur marks 75 years; Modi joins jubilee", "IIT"),
]

STATS = [
    ("44", "STORIES ON\nTHIS PAGE"),
    ("6", "CONTINENTS\nCOVERED"),
    ("3", "MISSILES DOWN\nOVER RIYADH"),
    ("M6.7", "PERU QUAKE\nAT 00:09 UTC"),
    ("-5.3%", "NASDAQ FALL\nINTO THE RED"),
    ("$58.8k", "BITCOIN, DOWN\nBELOW $59K"),
]

CHIPS = [
    ("EUROPE", RED), ("MIDDLE EAST", (122, 74, 52)),
    ("ASIA-PACIFIC", TEAL), ("AMERICAS", NAVY),
    ("AFRICA", (120, 84, 20)), ("SPACE", (60, 60, 90)),
]

DATE_CHECK = (
    "Every story on this page happened, or was first reported, on Saturday 21 November 2026 "
    "in some time zone. NOT counted as today: the Shenzhen trilateral summit (ended Thu 19 Nov), "
    "the missiles that crashed in Poland (Fri 20 Nov — today's news is Rutte's visit), Cyclone "
    "Akvan's landfall (Fri 20 Nov — today's news is the flood alerts), and Anthropic's IPO debut "
    "(19–20 Nov — today's news is the slide). Check the datelines: 21 November 2026."
)

FOOTER = (
    "Drawn with PIL primitives — original vector artwork, no photos. 44 stories, 6 continents, one page. "
    "THE WORLD TODAY \u00b7 Saturday 21 November 2026 \u00b7 All times UTC unless stated."
)


# ---------------------------------------------------------------------------
# Page build
# ---------------------------------------------------------------------------

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 14
    RX = W - M
    CW = W - 2 * M

    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=2)

    # ---- top bar
    y = 12
    d.text((M, y), "THE WORLD IN ONE DAY", font=font(F_SANS_BOLD, 13), fill=RED)
    right = "SATURDAY'S NEWS \u00b7 ONE PAGE \u00b7 44 STORIES \u00b7 6 CONTINENTS"
    d.text((RX - tw(d, right, font(F_SANS_BOLD, 11)), y + 1), right,
           font=font(F_SANS_BOLD, 11), fill=INK)

    # ---- masthead
    y = 30
    title = "Saturday 21 November 2026"
    tf = font(F_SERIF_BLACK, 60)
    d.text(((W - tw(d, title, tf)) / 2, y), title, font=tf, fill=INK)
    y = 96
    sub = ("Rutte flies to Warsaw \u00b7 COP31 in overtime \u00b7 Peru quake \u00b7 "
           "BepiColombo reaches Mercury")
    sf = font(F_SERIF_IT, 17)
    d.text(((W - tw(d, sub, sf)) / 2, y), sub, font=sf, fill=BROWN)
    y = 120
    hrule(d, M, RX, y, 3)
    hrule(d, M, RX, y + 5, 1)

    # ---- stats strip
    y = 128
    cell = CW // 6
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * cell
        nf = font(F_SERIF_BOLD, 26)
        d.text((cx + 4, y), num, font=nf, fill=RED)
        para(d, cx + 4, y + 30, cap, font(F_SANS, 10), cell - 10, 12, fill=GREY,
             max_lines=1)
        if i:
            d.line([(cx, y + 2), (cx, y + 44)], fill=(200, 192, 172), width=1)
    y = 176
    hrule(d, M, RX, y, 1)

    # ---- region chips
    y = 182
    cx = M
    for label, col in CHIPS:
        f = font(F_SANS_BOLD, 10)
        wch = tw(d, label, f) + 12
        d.rounded_rectangle([cx, y, cx + wch, y + 19], radius=3, fill=col)
        d.text((cx + 6, y + 4), label, font=f, fill=WHITE)
        cx += wch + 6
    note = "ALL STORIES: SAT 21 NOV 2026, ANY TIME ZONE"
    d.text((RX - tw(d, note, font(F_SANS, 10)), y + 4), note,
           font=font(F_SANS, 10), fill=GREY)

    # ---- three feature cards
    y = 207
    fw = (CW - 2 * 12) // 3
    fh = 232
    for i, s in enumerate(FEATURES):
        fx = M + i * (fw + 12)
        d.rectangle([fx, y, fx + fw - 1, y + fh - 1], outline=INK, width=1)
        ART[s["art"]](d, fx + 1, y + 1, fw - 2, 100)
        # strip over the bottom of the illustration
        d.rectangle([fx + 1, y + 80, fx + fw - 2, y + 101], fill=(0, 0, 0))
        stf = font(F_SANS_BOLD, 11)
        d.text((fx + 8, y + 85), s["strip"], font=stf, fill=(255, 210, 90))
        ty = y + 106
        kick = f"{s['n']:02d} \u00b7 {s['place']} \u00b7 {s['tag']}"
        d.text((fx + 6, ty), kick, font=font(F_SANS_BOLD, 11), fill=RED)
        ty += 16
        ty = para(d, fx + 6, ty, s["head"], font(F_SERIF_BOLD, 20), fw - 12, 22,
                  max_lines=2)
        ty += 3
        ty = para(d, fx + 6, ty, s["body"], font(F_SERIF, 12), fw - 12, 15,
                  max_lines=3)
        d.text((fx + 6, y + fh - 16), s["src"], font=font(F_SERIF_IT, 10),
               fill=GREY)
    y += fh + 8

    # ---- ten medium cards, two rows of five
    mw = (CW - 4 * 10) // 5
    mh = 142
    for row in range(2):
        for col in range(5):
            s = MEDIUMS[row * 5 + col]
            mx = M + col * (mw + 10)
            my = y + row * (mh + 8)
            d.rectangle([mx, my, mx + mw - 1, my + mh - 1], outline=INK, width=1)
            ART[s["art"]](d, mx + 1, my + 1, mw - 2, 52)
            ty = my + 57
            kick = f"{s['n']:02d} \u00b7 {s['place']} \u00b7 {s['tag']}"
            d.text((mx + 5, ty), fit_one(d, kick, font(F_SANS_BOLD, 9), mw - 10),
                   font=font(F_SANS_BOLD, 9), fill=RED)
            ty += 13
            ty = para(d, mx + 5, ty, s["head"], font(F_SERIF_BOLD, 13), mw - 10,
                      14, max_lines=2)
            ty += 1
            ty = para(d, mx + 5, ty, s["body"], font(F_SERIF, 11), mw - 10, 12,
                      max_lines=2)
            d.text((mx + 5, my + mh - 13), s["src"], font=font(F_SERIF_IT, 9),
                   fill=GREY)
    y += 2 * mh + 8 + 8

    # ---- bottom: map + briefs
    by = y
    map_w = 280
    d.text((M, by), "WHERE IT HAPPENED", font=font(F_SANS_BOLD, 12), fill=RED)
    draw_map(d, M, by + 17, map_w, 172)
    bx = M + map_w + 12
    bw = RX - bx
    d.text((bx, by), "ALSO ON SATURDAY 21 NOVEMBER \u2014 31 MORE STORIES",
           font=font(F_SANS_BOLD, 12), fill=RED)
    d.text((RX - tw(d, "BRIEFS 14\u201344", font(F_SANS, 10)), by + 1),
           "BRIEFS 14\u201344", font=font(F_SANS, 10), fill=GREY)
    col_w = (bw - 10) // 2
    bf = font(F_SANS, 10)
    bf_b = font(F_SANS_BOLD, 10)
    ly = by + 17
    for i, (city, text, src) in enumerate(BRIEFS):
        col = 0 if i < 16 else 1
        row = i if i < 16 else i - 16
        lx = bx + col * (col_w + 10)
        yy = ly + row * 11
        num = 14 + i
        label = f"{num} {city} \u2014 "
        d.text((lx, yy), label, font=bf_b, fill=INK)
        rest = fit_one(d, f"{text} ({src})", bf, col_w - tw(d, label, bf_b))
        d.text((lx + tw(d, label, bf_b), yy), rest, font=bf, fill=INK)
    y = by + 17 + 176 + 8

    # ---- date check
    d.rectangle([M, y, RX, y + 54], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK", font=font(F_SANS_BOLD, 11), fill=RED)
    para(d, M + 8, y + 19, DATE_CHECK, font(F_SANS, 10), CW - 16, 12, fill=INK,
         max_lines=3)
    y += 60

    # ---- footer
    para(d, M, y, FOOTER, font(F_SANS, 9), CW, 11, fill=GREY, max_lines=1)

    print("layout bottom y =", y, "(canvas", H, ")")
    print("stories:", len(FEATURES) + len(MEDIUMS) + len(BRIEFS))
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} {os.path.getsize(out)} bytes")


if __name__ == "__main__":
    main()
