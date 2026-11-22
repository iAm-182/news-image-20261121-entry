#!/usr/bin/env python3
"""news-image-20261121 v3 - full-day front page for Saturday 21 November 2026.

A newspaper front page drawn with PIL primitives only: original vector
artwork, no photos, no downloaded images. 48 stories, every one an event
of, or first reported on, Saturday 21 November 2026 (any time zone),
checked against live reporting after the day ended. This is the full-day
edition: v2 was built mid-day, so v3 adds the evening's big stories (Iran
strikes US bases in Bahrain, the El Chapo Isidro capture, the Sparta II
drone strike, the Las Vegas GP result, the ATP semi-finals), reports
results instead of previews, and drops ten items v2 dated wrongly (the
Siberia An-12 crash was 17 Nov, Eisenkot's mandate was 8 Nov, the
UK-EU deals, Denmark expulsion, Estonia decision, GTA VI sales figure,
France UN request, Trump data-centre threat and Austria hack disclosure
were all 19-20 Nov, the Onkalo licence was 22 Oct and Tom Skerritt died
21 Oct). Those are named in the DATE CHECK box instead.

Run:  python3 draw.py   ->   writes entry.png (1024x1024) next to this file.
Deterministic: two runs write identical bytes. The layout code measures
every line and fails loudly on overflow instead of truncating text.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
RED = (158, 28, 34)
BROWN = (122, 74, 52)
NAVY = (22, 40, 63)
NAVY2 = (16, 32, 52)
TAN = (217, 201, 163)
GREY = (90, 88, 82)
LINE = (60, 58, 52)
WHITE = (250, 248, 242)
CREAM = (238, 231, 214)
GOLD = (184, 134, 42)
GREEN = (46, 110, 72)
TEAL = (18, 110, 106)
SKY = (198, 220, 238)
ORANGE = (247, 147, 26)
OCHRE = (120, 84, 20)
OLIVE = (90, 60, 44)
BLUE = (40, 90, 160)
PLUM = (60, 60, 90)

F_TITLE = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
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


def text_w(d, text, f):
    return d.textlength(text, font=f)


def wrap_text(d, text, f, max_w):
    """Greedy word wrap; returns the lines that fit max_w."""
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


def draw_lines(d, x, y, lines, f, leading, fill=INK):
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def draw_para(d, x, y, text, f, max_w, leading, fill=INK, max_lines=None):
    """Draw a wrapped paragraph; FAILS if it needs more than max_lines."""
    lines = wrap_text(d, text, f, max_w)
    if max_lines is not None and len(lines) > max_lines:
        raise SystemExit(
            "OVERFLOW para %r needs %d lines, max %d: %s"
            % (text[:40], len(lines), max_lines, lines)
        )
    return draw_lines(d, x, y, lines, f, leading, fill)


def draw_single(d, x, y, text, f, max_w, fill=INK):
    """Draw one line; FAILS if it does not fit (no silent truncation)."""
    if d.textlength(text, font=f) > max_w:
        raise SystemExit(
            "OVERFLOW single line %r width %.0f > %.0f"
            % (text, d.textlength(text, font=f), max_w)
        )
    d.text((x, y), text, font=f, fill=fill)


def hrule(d, x0, x1, y, wdt=1, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=wdt)


def five_star(d, cx, cy, r, fill):
    import math
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rad = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------------------
# Panel illustrations - simple geometric vector art, drawn with PIL only.
# Each takes (d, x, y, w, h): the illustration box inside a card.
# ---------------------------------------------------------------------------

def art_bahrain(d, x, y, w, h):
    """Night sky over Manama: interceptor arcs, explosion burst, skyline."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(14, 20, 38))
    for sx, sy in ((18, 10), (52, 6), (120, 12), (170, 8), (210, 14)):
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=WHITE)
    base = y + h
    for tx, twd, tht in ((10, 26, 34), (42, 18, 46), (66, 30, 28),
                         (102, 20, 40), (128, 26, 32), (160, 18, 38),
                         (184, 24, 30)):
        d.rectangle([x + tx, base - tht, x + tx + twd, base], fill=(70, 88, 120))
        for wy in range(base - tht + 6, base - 4, 9):
            d.rectangle([x + tx + 4, wy, x + tx + twd - 4, wy + 3],
                        fill=(255, 210, 90))
    # explosion burst, top right
    bx, by = x + w - 52, y + 22
    for r, col in ((16, (255, 210, 90)), (11, (255, 140, 40)), (6, RED)):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    # two interceptor arcs
    for i in range(2):
        x0 = x + 24 + i * 58
        d.arc([x0, y + 6, x0 + 56, y + 34], start=200, end=340, fill=GOLD,
              width=3)


def art_warsaw(d, x, y, w, h):
    """Polish flag on a pole, NATO star, jets overhead."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(240, 236, 226))
    fx, fy, fw, fh = x + 22, y + 12, 148, 64
    d.rectangle([fx, fy, fx + 7, y + h - 10], fill=(80, 76, 70))
    d.rectangle([fx + 7, fy, fx + fw, fy + fh // 2], fill=WHITE)
    d.rectangle([fx + 7, fy + fh // 2, fx + fw, fy + fh], fill=(220, 20, 60))
    d.rectangle([fx + 7, fy, fx + fw, fy + fh], outline=INK, width=1)
    # jets: small delta shapes
    for jx, jy in ((x + w - 96, y + 16), (x + w - 64, y + 30)):
        d.polygon([(jx, jy), (jx + 26, jy + 5), (jx, jy + 10)], fill=NAVY)
    cx, cy = x + w - 44, y + h - 42
    d.ellipse([cx - 21, cy - 21, cx + 21, cy + 21], fill=NAVY)
    five_star(d, cx, cy, 16, WHITE)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=NAVY)


def art_cop31(d, x, y, w, h):
    """Green globe, clock hands past midnight."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(226, 238, 226))
    cx, cy, r = x + w // 2 - 44, y + h // 2 + 2, 32
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GREEN)
    d.ellipse([cx - r + 7, cy - 12, cx - 2, cy + 4], fill=(120, 190, 130))
    d.ellipse([cx + 5, cy + 6, cx + r - 6, cy + r - 5], fill=(120, 190, 130))
    # clock face, top right, hands past midnight
    kx, ky, kr = x + w - 46, y + 26, 20
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=WHITE, outline=INK,
              width=2)
    d.line([(kx, ky), (kx, ky - 13)], fill=INK, width=2)
    d.line([(kx, ky), (kx + 10, ky + 6)], fill=INK, width=2)


def art_mexico(d, x, y, w, h):
    """Desert dusk, helicopter silhouette, handcuff rings."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(246, 214, 160))
    d.ellipse([x + w - 56, y + 8, x + w - 8, y + 56], fill=(255, 190, 80))
    d.polygon([(x, y + h), (x + 60, y + 26), (x + 130, y + h)], fill=(160, 110, 60))
    d.polygon([(x + 100, y + h), (x + 170, y + 40), (x + w, y + h)],
              fill=(130, 86, 44))
    # helicopter silhouette
    hx, hy = x + 30, y + 14
    d.ellipse([hx, hy, hx + 52, hy + 12], fill=INK)
    d.line([(hx - 26, hy + 6), (hx + 78, hy + 6)], fill=INK, width=3)
    d.line([(hx + 52, hy + 6), (hx + 74, hy - 8)], fill=INK, width=3)
    d.line([(hx + 24, hy + 12), (hx + 24, hy + 22)], fill=INK, width=3)
    # handcuff rings, bottom right
    for ox in (0, 26):
        d.ellipse([x + w - 66 + ox, y + h - 30, x + w - 44 + ox, y + h - 8],
                  outline=INK, width=3)


def art_sparta(d, x, y, w, h):
    """Grey sea, burning cargo ship, two drone dots, smoke."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(200, 214, 226))
    for wy in (y + h - 26, y + h - 14):
        pts = []
        for i in range(21):
            px = x + i * (w / 20)
            py = wy + (4 if i % 2 == 0 else -4)
            pts.append((px, py))
        d.line(pts, fill=(28, 68, 140), width=3, joint="curve")
    # hull
    hx, hy = x + 26, y + h - 52
    d.polygon([(hx, hy), (hx + 130, hy), (hx + 118, hy + 18), (hx + 10, hy + 18)],
              fill=(90, 30, 30))
    d.rectangle([hx + 18, hy - 16, hx + 52, hy], fill=(200, 200, 200))
    d.rectangle([hx + 60, hy - 10, hx + 96, hy], fill=(160, 160, 160))
    # fire on deck
    for fx, fy, fr, col in ((hx + 84, hy - 16, 10, (255, 210, 90)),
                            (hx + 84, hy - 16, 6, (255, 140, 40)),
                            (hx + 84, hy - 16, 3, RED)):
        d.ellipse([fx - fr, fy - fr, fx + fr, fy + fr], fill=col)
    # smoke puffs
    for sx, sy, sr in ((hx + 84, hy - 34, 7), (hx + 96, hy - 44, 9),
                       (hx + 76, hy - 48, 6)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(140, 140, 140))
    # two drones
    for dx, dy in ((x + w - 52, y + 12), (x + w - 30, y + 26)):
        d.ellipse([dx - 4, dy - 2, dx + 4, dy + 2], fill=INK)
        d.line([(dx - 9, dy), (dx + 9, dy)], fill=INK, width=2)


def art_peru(d, x, y, w, h):
    """Andes peaks, seismic wave, M6.7 callout."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 222, 200))
    d.polygon([(x, y + h), (x + 70, y + 18), (x + 150, y + h)], fill=BROWN)
    d.polygon([(x + 110, y + h), (x + 190, y + 34), (x + w, y + h)],
              fill=OLIVE)
    d.polygon([(x + 58, y + 34), (x + 70, y + 18), (x + 84, y + 36),
               (x + 76, y + 40), (x + 70, y + 32), (x + 64, y + 40)],
              fill=WHITE)
    pts = []
    for i in range(25):
        px = x + 10 + i * (w - 20) / 24
        py = y + h - 24 + (10 if i % 4 == 0 else (-8 if i % 4 == 2 else 0))
        pts.append((px, py))
    d.line(pts, fill=RED, width=3, joint="curve")
    f = font(F_SANS_BOLD, 28)
    d.text((x + w - 102, y + 8), "M6.7", font=f, fill=RED)
    f2 = font(F_SANS_BOLD, 13)
    d.text((x + 14, y + 10), "CENTRAL PERU", font=f2, fill=NAVY)


def art_mercury(d, x, y, w, h):
    """Dark space, cratered Mercury, orbit ellipse, two orbiters."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(12, 16, 28))
    for sx, sy in ((16, 8), (36, 18), (w - 24, 8), (w - 40, 20), (w - 70, 6)):
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=WHITE)
    r = max(12, h // 2 - 8)
    cx, cy = x + w // 2, y + h // 2 + 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 152, 132))
    for ox, oy, orr in ((-r // 2, -r // 3, 4), (r // 3, r // 3, 3),
                        (r // 2, -r // 2, 2)):
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                  fill=(120, 106, 88))
    rx, ry = w // 2 - 14, h // 2 - 4
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=GOLD, width=2)
    d.rectangle([cx - rx - 4, cy - ry - 2, cx - rx + 4, cy - ry + 4],
                fill=(240, 240, 240))
    d.rectangle([cx + rx - 4, cy + ry - 4, cx + rx + 4, cy + ry + 2],
                fill=(240, 240, 240))


def art_f1(d, x, y, w, h):
    """Chequered flag, night race car, trophy cup."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(14, 14, 24))
    fx, fy = x + 12, y + 8
    for r in range(3):
        for c in range(6):
            col = WHITE if (r + c) % 2 == 0 else (20, 20, 20)
            d.rectangle([fx + c * 12, fy + r * 12, fx + c * 12 + 11,
                         fy + r * 12 + 11], fill=col)
    d.rectangle([fx, fy, fx + 72, fy + 36], outline=WHITE, width=1)
    # trophy cup, top right
    tx, ty = x + w - 40, y + 10
    d.polygon([(tx, ty), (tx + 22, ty), (tx + 18, ty + 18), (tx + 4, ty + 18)],
              fill=GOLD)
    d.rectangle([tx + 8, ty + 18, tx + 14, ty + 26], fill=GOLD)
    d.rectangle([tx + 2, ty + 26, tx + 20, ty + 30], fill=GOLD)
    # race car silhouette
    car_y = y + h - 32
    d.rectangle([x + 96, car_y, x + 186, car_y + 14], fill=(196, 38, 38))
    d.polygon([(x + 118, car_y), (x + 130, car_y - 12), (x + 158, car_y - 12),
               (x + 168, car_y)], fill=(196, 38, 38))
    for wx in (112, 168):
        d.ellipse([x + wx, car_y + 10, x + wx + 16, car_y + 26], fill=(10, 10, 10),
                  outline=(200, 200, 200), width=2)
    d.rectangle([x, y + h - 6, x + w - 1, y + h - 1], fill=(255, 210, 90))
    f = font(F_SANS_BOLD, 13)
    d.text((x + 96, y + 10), "LAS VEGAS", font=f, fill=(255, 210, 90))


def art_atp(d, x, y, w, h):
    """Tennis court from above, net, ball on the line."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(40, 110, 70))
    d.rectangle([x + 14, y + 8, x + w - 14, y + h - 8], fill=(70, 140, 95),
                outline=WHITE, width=2)
    d.line([(x + w // 2, y + 8), (x + w // 2, y + h - 8)], fill=WHITE, width=2)
    d.rectangle([x + w // 2 - 3, y + 8, x + w // 2 + 3, y + h - 8],
                fill=(30, 30, 30))
    d.line([(x + 14, y + h // 2), (x + w - 14, y + h // 2)], fill=WHITE,
           width=1)
    # ball on the baseline
    bx, by = x + w - 34, y + h - 22
    d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(200, 230, 60),
              outline=WHITE, width=2)
    d.arc([bx - 9, by - 9, bx + 9, by + 9], start=300, end=60, fill=WHITE,
          width=2)
    f = font(F_SANS_BOLD, 13)
    d.text((x + 20, y + 10), "TURIN", font=f, fill=WHITE)


def art_riyadh(d, x, y, w, h):
    """Night skyline, three interceptor arcs, warning beacon."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(16, 24, 44))
    for sx, sy in ((20, 8), (60, 14), (120, 7), (160, 12)):
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=WHITE)
    base = y + h
    for tx, twd, tht in ((12, 24, 30), (42, 18, 40), (66, 28, 26),
                         (100, 20, 36), (126, 24, 30), (156, 16, 34)):
        d.rectangle([x + tx, base - tht, x + tx + twd, base], fill=(70, 88, 120))
        for wy in range(base - tht + 6, base - 4, 9):
            d.rectangle([x + tx + 4, wy, x + tx + twd - 4, wy + 3],
                        fill=(255, 210, 90))
    for i in range(3):
        x0 = x + 26 + i * 52
        d.arc([x0, y + 4, x0 + 52, y + 32], start=200, end=340, fill=GOLD,
              width=3)
        d.ellipse([x0 + 46, y + 6, x0 + 52, y + 12], fill=(255, 210, 90))
    # red beacon on the tallest tower
    d.ellipse([x + 48, y + h - 48, x + 54, y + h - 42], fill=RED)


def art_gaza(d, x, y, w, h):
    """Flood water, aid crates, four flags."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(214, 230, 240))
    flags = [((16, 8), (200, 60, 60)), ((52, 8), (220, 30, 30)),
             ((88, 8), (40, 90, 160)), ((124, 8), (30, 60, 120))]
    for (fx, fy), col in flags:
        d.rectangle([x + fx, y + fy, x + fx + 4, y + fy + 26], fill=(70, 70, 70))
        d.rectangle([x + fx + 4, y + fy, x + fx + 30, y + fy + 18], fill=col)
        d.rectangle([x + fx + 4, y + fy, x + fx + 30, y + fy + 18],
                    outline=INK, width=1)
    for wy in (y + 44, y + 54):
        pts = []
        for i in range(21):
            px = x + i * (w / 20)
            py = wy + (4 if i % 2 == 0 else -4)
            pts.append((px, py))
        d.line(pts, fill=(28, 68, 140), width=3, joint="curve")
    for bx, by in ((x + 30, y + h - 30), (x + 78, y + h - 30),
                   (x + 126, y + h - 30)):
        d.rectangle([bx, by, bx + 34, by + 22], fill=GOLD,
                    outline=(120, 84, 20), width=2)
        d.line([(bx, by + 11), (bx + 34, by + 11)], fill=(120, 84, 20), width=2)


def art_hormuz(d, x, y, w, h):
    """Strait at dusk, two tankers, projectile streaks, fire."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=(232, 196, 150))
    d.rectangle([x, y + h - 30, x + w - 1, y + h - 1], fill=(40, 90, 130))
    for wy in (y + h - 22, y + h - 12):
        pts = []
        for i in range(21):
            px = x + i * (w / 20)
            py = wy + (3 if i % 2 == 0 else -3)
            pts.append((px, py))
        d.line(pts, fill=(120, 180, 210), width=2, joint="curve")
    # tanker one, left
    d.rectangle([x + 14, y + h - 52, x + 96, y + h - 34], fill=(60, 60, 60))
    d.rectangle([x + 70, y + h - 66, x + 92, y + h - 52], fill=(200, 200, 200))
    # tanker two, right, with fire
    d.rectangle([x + 116, y + h - 52, x + 190, y + h - 34], fill=(80, 40, 40))
    d.rectangle([x + 124, y + h - 64, x + 146, y + h - 52], fill=(200, 200, 200))
    for fr, col in ((9, (255, 210, 90)), (6, (255, 140, 40)), (3, RED)):
        d.ellipse([x + 156 - fr, y + h - 62 - fr, x + 156 + fr, y + h - 62 + fr],
                  fill=col)
    # projectile streaks
    for sx, sy in ((x + 40, y + 12), (x + 120, y + 8)):
        d.line([(sx, sy), (sx + 52, sy + 22)], fill=RED, width=3)
        d.ellipse([sx + 48, sy + 18, sx + 58, sy + 28], fill=RED)


def art_markets(d, x, y, w, h):
    """Falling red chart line, weekly bars, -5.3% callout."""
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=WHITE)
    for gx in range(x + 20, x + w, 36):
        d.line([(gx, y + 6), (gx, y + h - 6)], fill=(232, 232, 232), width=1)
    for gy in range(y + 12, y + h, 22):
        d.line([(x + 6, gy), (x + w - 6, gy)], fill=(236, 236, 236), width=1)
    # weekly bars, descending
    for i, bh in enumerate((34, 30, 26, 20, 12)):
        bx = x + 18 + i * 30
        d.rectangle([bx, y + h - 10 - bh, bx + 18, y + h - 10],
                    fill=(200, 60, 60) if i > 1 else (120, 120, 120))
    pts = [(x + 10, y + 20), (x + 46, y + 24), (x + 82, y + 22),
           (x + 118, y + 32), (x + 154, y + 30), (x + 182, y + h - 10)]
    d.line(pts, fill=RED, width=4, joint="curve")
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - 14, ey - 3), (ex - 5, ey - 14)], fill=RED)
    f = font(F_SANS_BOLD, 20)
    txt = "-5.3%"
    twd = d.textlength(txt, font=f)
    d.rectangle([x + w - twd - 12, y + 2, x + w - 2, y + 26], fill=WHITE)
    d.text((x + w - twd - 6, y + 3), txt, font=f, fill=RED)
    f2 = font(F_SANS_BOLD, 11)
    d.text((x + 8, y + 4), "NASDAQ", font=f2, fill=GREY)


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
    1: (50.5, 26.2), 2: (21.0, 52.0), 3: (30.7, 36.9), 4: (-108.5, 25.6),
    5: (24.0, 60.0), 6: (-76.0, -11.0), 8: (-115.1, 36.2), 9: (7.7, 45.1),
    10: (46.7, 24.7), 11: (34.5, 31.5), 12: (56.5, 26.5), 13: (-74.0, 40.7),
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
    d.ellipse([x + 10, y + h - 22, x + 24, y + h - 8], fill=RED, outline=WHITE,
              width=2)
    d.text((x + 17, y + h - 21), "7", font=font(F_SANS_BOLD, 9), fill=WHITE)
    d.text((x + 28, y + h - 22), "SPACE \u00b7 MERCURY", font=font(F_SANS_BOLD, 10),
           fill=WHITE)


# ---------------------------------------------------------------------------
# Stories - every one an event of, or first reported on, Sat 21 Nov 2026
# (any time zone), checked against live reporting after the day ended.
# ---------------------------------------------------------------------------

ART = {
    "bahrain": art_bahrain, "warsaw": art_warsaw, "cop31": art_cop31,
    "mexico": art_mexico, "sparta": art_sparta, "peru": art_peru,
    "mercury": art_mercury, "f1": art_f1, "atp": art_atp,
    "riyadh": art_riyadh, "gaza": art_gaza, "hormuz": art_hormuz,
    "markets": art_markets,
}

FEATURES = [
    dict(
        n=1, place="MANAMA, BAHRAIN", tag="GULF", art="bahrain",
        head="Iran strikes US bases in Bahrain",
        body=("The IRGC claims strikes hit US Patriot radars at al-Riffa "
              "and Awali. Bahrain says an industrial site caught fire; "
              "no one was hurt."),
        src="(Reuters, AP)",
        strip="IRGC CLAIMS RADARS HIT \u00b7 BAHRAIN: SITE ABLAZE",
    ),
    dict(
        n=2, place="WARSAW, POLAND", tag="NATO", art="warsaw",
        head="Rutte: NATO will defend every inch of Poland",
        body=("The NATO chief stands in Warsaw a day after two Russian "
              "missiles and a drone came down. Poland asks for more "
              "Eastern Sentry forces; the Council meets Monday."),
        src="(PAP, Reuters)",
        strip="EVERY INCH \u00b7 EASTERN SENTRY",
    ),
    dict(
        n=3, place="ANTALYA, T\u00dcRKIYE", tag="CLIMATE", art="cop31",
        head="COP31 grinds on with no deal as Saturday ends",
        body=("A second day of overtime. The draft drops fossil fuels and "
              "a $120bn adaptation target; the EU says no deal beats a "
              "weak one."),
        src="(Reuters, AP)",
        strip="2ND DAY OF OVERTIME \u00b7 TEXT DUE OVERNIGHT",
    ),
]

MEDIUMS = [
    dict(n=4, place="GUASAVE, MEXICO", tag="CARTEL", art="mexico",
         head="Mexico captures \u2018El Chapo Isidro\u2019",
         body=("FBI Top 10 fugitive Meza Flores is seized; 11 die in the "
               "raid. He is flown to Mexico City at dawn."),
         src="(Reuters, AP)"),
    dict(n=5, place="GULF OF FINLAND", tag="BALTIC", art="sparta",
         head="Drones set Russian ship ablaze",
         body=("Two drones hit Sparta II; it burns, drifts into Finnish "
               "waters. 16 crew safe; Finland says Ukraine likely did it."),
         src="(Reuters, Yle)"),
    dict(n=6, place="CENTRAL PERU", tag="QUAKE", art="peru",
         head="Magnitude 6.7 quake shakes Peru",
         body=("Strikes at 00:09 UTC, 9 km from Carhuamayo, 108 km deep. "
               "Felt in Lima; no casualties or serious damage."),
         src="(USGS, AP)"),
    dict(n=7, place="MERCURY", tag="SPACE", art="mercury",
         head="BepiColombo enters Mercury orbit",
         body=("After eight years, the ESA-JAXA craft is captured by "
               "Mercury's gravity. Its science work starts in April 2027."),
         src="(ESA, Nature)"),
    dict(n=8, place="LAS VEGAS", tag="SPORT", art="f1",
         head="Verstappen wins wild Las Vegas GP",
         body=("From pole through 35 lead changes; Norris 2nd, Piastri "
               "3rd. Antonelli 4th, Russell 9th; the Ferraris collide."),
         src="(Formula 1, FIA)"),
    dict(n=9, place="TURIN, ITALY", tag="TENNIS", art="atp",
         head="Zverev and Alcaraz reach ATP final",
         body=("Zverev beats Medvedev 7-6(0), 6-4; Alcaraz beats Shelton "
               "in three sets. The final is on Sunday."),
         src="(ATP)"),
    dict(n=10, place="RIYADH", tag="GULF", art="riyadh",
         head="Saudi defences down three missiles",
         body=("Third night of alerts over the capital as Houthi attacks "
               "intensify; two more missiles hit at Jazan on Friday."),
         src="(Reuters)"),
    dict(n=11, place="GAZA", tag="AID", art="gaza",
         head="Four allies urge aid into flooded Gaza",
         body=("Australia, Canada, Italy and the UK call for immediate, "
               "unrestricted humanitarian access as floods add to "
               "suffering."),
         src="(The Paris Eye)"),
    dict(n=12, place="STRAIT OF HORMUZ", tag="SHIPPING", art="hormuz",
         head="Two more tankers hit off Khasab",
         body=("Projectiles strike Torkel and Arina; no casualties. Iran "
               "says a tanker hit a mine; the IRGC claims a US drone "
               "downed."),
         src="(UKMTO, Reuters)"),
    dict(n=13, place="NEW YORK", tag="MARKETS", art="markets",
         head="Wall Street ends its week in correction",
         body=("S&P 500 falls 3.7% and the Nasdaq 5.3% in the week to "
               "Friday's close; $7 trillion wiped out."),
         src="(Bloomberg)"),
]

BRIEFS = [
    ("KRYVYI RIH", "Boy, 7, and paramedic dead; 58 hurt", "Vilkul"),
    ("PARIS", "Fourth weekend of cost-of-living protests", "AFP"),
    ("CARACAS", "US details $12bn Venezuelan oil revenue", "State Dept"),
    ("PARIS", "Police convicted over Zecler beating", "Court"),
    ("BERLIN", "Suspected Russian spy arrested", "BKA"),
    ("KYIV", "Zelensky: US blocking missile deliveries", "Kyiv"),
    ("BERLIN", "Germany hosts Digital Summit on AI", "Govt"),
    ("BERLIN", "Coalition talks begin: Left, Greens, SPD", "RBB"),
    ("BHOPAL", "India women beat Malaysia 4-1 in hockey", "Hockey India"),
    ("ODISHA", "Akvan weakens; red alert in Bengal, Bihar", "IMD"),
    ("NEW YORK", "Man jailed 19 years in Sikh murder plot", "DOJ"),
    ("HAVANA", "US woman freed after 10 years in Cuba", "AP"),
    ("LOS ANGELES", "Man convicted of starting Palisades Fire", "Court"),
    ("NEW DELHI", "Modi tours three states; Delhi hosts SCO", "PMO"),
    ("WASHINGTON", "US sanctions four Iranians over oil", "Treasury"),
    ("SHENZHEN", "APEC carries on without Trump", "APEC"),
    ("LAUSANNE", "World Boxing backs LA28 governance plan", "IBA"),
    ("BANGKOK", "Thailand, China boost Mekong pact", "NBT"),
    ("KHARAGPUR", "IIT Kharagpur marks 75 years", "IIT"),
    ("CRYPTO", "Bitcoin plunges to $55k, bounces past $60k", "CoinGlass"),
    ("SILICON VALLEY", "Nvidia -23%, worst week since 2008", "Reuters"),
    ("NEW YORK", "Anthropic slides after record IPO", "Nasdaq"),
    ("JERUSALEM", "Eisenkot invites Likud to coalition talks", "Yashar"),
    ("LONDON", "Leeds thrash Chelsea 4-1; Arsenal held 2-2", "PL"),
    ("KATHMANDU", "Nepal PM Shah begins India visit", "PMO"),
    ("BEIJING", "Chinese AI stocks down $1.7tn since June", "Reports"),
    ("WASHINGTON", "Vance splits with Trump on Iran claim", "Reports"),
    ("ROME", "Italy approves Tesla self-driving", "Reports"),
    ("MOGADISHU", "Somalia expels UAE ambassador", "Reports"),
    ("BRUSSELS", "Belgium faces Monday flight shutdown", "Reports"),
    ("SEOUL", "111 caught cheating in Suneung exam", "Reports"),
    ("OTTAWA", "Canada unaware of US defence-ties limit", "Reports"),
    ("JOHANNESBURG", "South Africa holds rate at 7.25%", "SARB"),
    ("ADDIS ABABA", "700,000 displaced in southern Ethiopia", "Reports"),
    ("NAIROBI", "Kenya counts police over Russia hiring fears", "Reports"),
]

STATS = [
    ("48", "STORIES ON\nTHIS PAGE"),
    ("8", "REGIONS\nCOVERED"),
    ("2", "TANKERS HIT\nOFF KHASAB"),
    ("M6.7", "PERU QUAKE\nAT 00:09 UTC"),
    ("-5.3%", "NASDAQ FALL\nIN THE WEEK"),
    ("$55K", "BITCOIN LOW,\nTHEN BOUNCE"),
]

CHIPS = [
    ("EUROPE", RED), ("MIDDLE EAST", BROWN),
    ("EAST ASIA", TEAL), ("SOUTH ASIA", OCHRE),
    ("AMERICAS", NAVY), ("AFRICA", OLIVE),
    ("OCEANIA", BLUE), ("SPACE", PLUM),
]

UTC_STRIP = (
    "SATURDAY IN UTC \u2014 00:09 PERU QUAKE \u00b7 05:00 TANKERS HIT "
    "\u00b7 11:20 EL CHAPO FLOWN OUT \u00b7 18:24 BEPICOLOMBO BURN "
    "\u00b7 EVENING RUTTE IN WARSAW \u00b7 NIGHT IRAN STRIKES BAHRAIN "
    "\u00b7 20:00 VERSTAPPEN WINS"
)

DATE_CHECK = (
    "Every story here happened, or was first reported, on Saturday 21 November 2026 "
    "in some time zone. NOT counted: the Shenzhen summit (ended 19 Nov); the missiles "
    "that crashed in Poland (20 Nov \u2014 today is Rutte's visit); the Siberia An-12 "
    "crash (17 Nov); Eisenkot's mandate (8 Nov \u2014 today is his Likud invitation); "
    "Denmark's expulsion (20 Nov); the UK-EU deals (20 Nov); Estonia's border decision "
    "(20 Nov; closure 1 Dec); GTA VI's $3.79bn sales (announced 20 Nov); France's UN "
    "request (20 Nov); the US AI-chip disclosure (19 Nov); Trump's data-centre threat "
    "(20 Nov); Austria's hack (disclosed 20 Nov); the Onkalo licence (22 Oct); Tom "
    "Skerritt's death (21 Oct); Akvan's landfall "
    "(20 Nov \u2014 today is the flood alerts). Markets are Friday's close."
)

FOOTER = (
    "Drawn with PIL primitives \u2014 original vector artwork, no photos. 48 stories, 8 regions, one page. "
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
    right = "SATURDAY'S NEWS \u00b7 ONE PAGE \u00b7 48 STORIES \u00b7 8 REGIONS"
    draw_single(d, RX - text_w(d, right, font(F_SANS_BOLD, 11)), y + 1, right,
                font(F_SANS_BOLD, 11), RX - M)
    y = 28

    # ---- masthead
    title = "Saturday 21 November 2026"
    tf = font(F_TITLE, 56)
    d.text(((W - text_w(d, title, tf)) / 2, y), title, font=tf, fill=INK)
    y = 92
    sub = ("Iran strikes US bases in Bahrain \u00b7 Rutte in Warsaw \u00b7 COP31 in "
           "overtime \u00b7 Verstappen wins in Vegas")
    sf = font(F_SERIF_IT, 16)
    d.text(((W - text_w(d, sub, sf)) / 2, y), sub, font=sf, fill=BROWN)
    y = 114
    hrule(d, M, RX, y, 3)
    hrule(d, M, RX, y + 5, 1)
    y = 124

    # ---- UTC strip
    d.rectangle([M, y, RX, y + 18], fill=NAVY2)
    uf = font(F_SANS_BOLD, 9)
    draw_single(d, M + 6, y + 4, UTC_STRIP, uf, CW - 12, fill=WHITE)
    y += 18 + 6

    # ---- stats strip
    cell = CW // 6
    for i, (num, cap) in enumerate(STATS):
        cx = M + i * cell
        nf = font(F_SERIF_BOLD, 24)
        d.text((cx + 4, y), num, font=nf, fill=RED)
        for j, ln in enumerate(cap.split("\n")):
            d.text((cx + 4, y + 26 + j * 11), ln, font=font(F_SANS, 9),
                   fill=GREY)
        if i:
            d.line([(cx, y + 2), (cx, y + 44)], fill=(200, 192, 172), width=1)
    y += 48
    hrule(d, M, RX, y, 1)
    y += 6

    # ---- region chips
    cx = M
    for label, col in CHIPS:
        f = font(F_SANS_BOLD, 10)
        wch = text_w(d, label, f) + 12
        d.rounded_rectangle([cx, y, cx + wch, y + 19], radius=3, fill=col)
        d.text((cx + 6, y + 4), label, font=f, fill=WHITE)
        cx += wch + 6
    note = "ALL STORIES: SAT 21 NOV 2026, ANY TIME ZONE"
    d.text((RX - text_w(d, note, font(F_SANS, 10)), y + 4), note,
           font=font(F_SANS, 10), fill=GREY)
    y += 19 + 6

    # ---- three feature cards
    fw = (CW - 2 * 12) // 3
    fh = 204
    for i, s in enumerate(FEATURES):
        fx = M + i * (fw + 12)
        d.rectangle([fx, y, fx + fw - 1, y + fh - 1], outline=INK, width=1)
        ART[s["art"]](d, fx + 1, y + 1, fw - 2, 76)
        d.rectangle([fx + 1, y + 58, fx + fw - 2, y + 77], fill=(0, 0, 0))
        stf = font(F_SANS_BOLD, 11)
        draw_single(d, fx + 8, y + 62, s["strip"], stf, fw - 16,
                    fill=(255, 210, 90))
        ty = y + 82
        kick = "%02d \u00b7 %s \u00b7 %s" % (s["n"], s["place"], s["tag"])
        draw_single(d, fx + 6, ty, kick, font(F_SANS_BOLD, 11), fw - 12, fill=RED)
        ty += 15
        ty = draw_para(d, fx + 6, ty, s["head"], font(F_SERIF_BOLD, 19),
                       fw - 12, 21, max_lines=2)
        ty += 2
        ty = draw_para(d, fx + 6, ty, s["body"], font(F_SERIF, 12), fw - 12, 14,
                       max_lines=3)
        d.text((fx + 6, y + fh - 15), s["src"], font=font(F_SERIF_IT, 10),
               fill=GREY)
    y += fh + 6

    # ---- ten medium cards, two rows of five
    mw = (CW - 4 * 10) // 5
    mh = 136
    for row in range(2):
        for col in range(5):
            s = MEDIUMS[row * 5 + col]
            mx = M + col * (mw + 10)
            my = y + row * (mh + 8)
            d.rectangle([mx, my, mx + mw - 1, my + mh - 1], outline=INK, width=1)
            ART[s["art"]](d, mx + 1, my + 1, mw - 2, 42)
            ty = my + 46
            kick = "%02d \u00b7 %s \u00b7 %s" % (s["n"], s["place"], s["tag"])
            draw_single(d, mx + 5, ty, kick, font(F_SANS_BOLD, 9), mw - 10,
                        fill=RED)
            ty += 12
            ty = draw_para(d, mx + 5, ty, s["head"], font(F_SERIF_BOLD, 13),
                           mw - 10, 14, max_lines=2)
            ty += 1
            ty = draw_para(d, mx + 5, ty, s["body"], font(F_SERIF, 11), mw - 10,
                           12, max_lines=3)
            d.text((mx + 5, my + mh - 12), s["src"], font=font(F_SERIF_IT, 9),
                   fill=GREY)
    y += 2 * mh + 8 + 6

    # ---- bottom: map + briefs
    by = y
    map_w = 280
    d.text((M, by), "WHERE IT HAPPENED", font=font(F_SANS_BOLD, 12), fill=RED)
    draw_map(d, M, by + 17, map_w, 176)
    bx = M + map_w + 12
    bw = RX - bx
    d.text((bx, by), "ALSO ON SATURDAY 21 NOVEMBER \u2014 35 MORE STORIES",
           font=font(F_SANS_BOLD, 12), fill=RED)
    d.text((RX - text_w(d, "BRIEFS 14\u201348", font(F_SANS, 10)), by + 1),
           "BRIEFS 14\u201348", font=font(F_SANS, 10), fill=GREY)
    col_w = (bw - 10) // 2
    bf = font(F_SANS, 10)
    bf_b = font(F_SANS_BOLD, 10)
    ly = by + 17
    for i, (city, text, src) in enumerate(BRIEFS):
        col = 0 if i < 18 else 1
        row = i if i < 18 else i - 18
        lx = bx + col * (col_w + 10)
        yy = ly + row * 11
        num = 14 + i
        label = "%d %s \u2014 " % (num, city)
        lw = text_w(d, label, bf_b)
        rest = "%s (%s)" % (text, src)
        if text_w(d, rest, bf) > col_w - lw:
            raise SystemExit(
                "OVERFLOW brief %d %s: %r too wide for %.0f" % (num, city, rest,
                                                               col_w - lw))
        d.text((lx, yy), label, font=bf_b, fill=INK)
        d.text((lx + lw, yy), rest, font=bf, fill=INK)
    y = by + 17 + 176 + 4

    # ---- date check
    d.rectangle([M, y, RX, y + 70], outline=RED, width=2)
    d.text((M + 8, y + 5), "DATE CHECK", font=font(F_SANS_BOLD, 11), fill=RED)
    draw_para(d, M + 8, y + 19, DATE_CHECK, font(F_SANS, 10), CW - 16, 12,
              fill=INK, max_lines=4)
    y += 70 + 4

    # ---- footer
    draw_single(d, M, y, FOOTER, font(F_SANS, 9), CW, fill=GREY)
    y += 12

    print("layout bottom y =", y, "(canvas", H, ")")
    print("stories:", len(FEATURES) + len(MEDIUMS) + len(BRIEFS))
    if y > 1012:
        raise SystemExit("OVERFLOW layout bottom %d > 1012" % y)
    return img


def main():
    img = build()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote %s %d bytes" % (out, os.path.getsize(out)))


if __name__ == "__main__":
    main()
