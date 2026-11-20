#!/usr/bin/env python3
"""Draw entry.png: one picture summing up the world news of Friday 20 November 2026.

Everything is drawn from scratch with PIL shapes and text -- no photos, no
copyrighted assets, no outlet logos. Run: python3 make_image.py
"""
import math

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (13, 21, 38)
PANEL = (22, 35, 61)
BORDER = (44, 74, 124)
ACCENT = (255, 180, 84)
TEXT = (242, 245, 250)
SUB = (185, 199, 221)
CYAN = (110, 200, 255)
GREEN = (120, 230, 160)
RED = (255, 110, 110)

BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def panel(draw, box, title, lines, title_size=34, line_size=26):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=PANEL, outline=BORDER, width=3)
    tx = x0 + 20
    ty = y0 + 16
    draw.text((tx, ty), title, font=font(title_size), fill=ACCENT)
    ty += title_size + 10
    for ln in lines:
        for part in wrap(draw, ln, font(line_size, bold=False), x1 - x0 - 40):
            draw.text((tx, ty), part, font=font(line_size, bold=False), fill=TEXT)
            ty += line_size + 6
    return ty


def flag_us(draw, x, y, w=64, h=40):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(0, 0, 0))
    for i in range(0, 7, 2):
        draw.rectangle([x, y + i * h // 7, x + w, y + (i + 1) * h // 7], fill=(200, 40, 50))
    draw.rectangle([x, y, x + w * 2 // 5, y + h * 4 // 7], fill=(40, 60, 160))


def flag_cn(draw, x, y, w=64, h=40):
    draw.rectangle([x, y, x + w, y + h], fill=(215, 40, 40), outline=(0, 0, 0))
    draw.ellipse([x + 8, y + 8, x + 22, y + 22], fill=(255, 220, 60))


def flag_ru(draw, x, y, w=64, h=40):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(0, 0, 0))
    draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(50, 90, 200))
    draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(215, 40, 40))


def leader(draw, cx, cy, suit):
    draw.ellipse([cx - 26, cy - 60, cx + 26, cy - 8], fill=(235, 200, 165))  # head
    draw.pieslice([cx - 52, cy - 6, cx + 52, cy + 80], 180, 360, fill=suit)    # shoulders
    draw.rectangle([cx - 52, cy + 30, cx + 52, cy + 66], fill=suit)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- Header: the day, named big ----
    d.text((24, 22), "FRIDAY 20 NOVEMBER 2026", font=font(62), fill=TEXT)
    d.text((26, 96), "The day in one picture — world news", font=font(30, bold=False), fill=ACCENT)
    d.rectangle([24, 140, 1000, 146], fill=ACCENT)

    # ---- Main panel: Shenzhen summit ----
    box = (24, 162, 560, 606)
    d.rounded_rectangle(box, radius=14, fill=PANEL, outline=BORDER, width=3)
    d.text((44, 178), "SHENZHEN SUMMIT", font=font(38), fill=ACCENT)
    # flags + leaders around a table
    flag_us(d, 78, 240)
    flag_cn(d, 260, 240)
    flag_ru(d, 442, 240)
    leader(d, 110, 380, (60, 70, 90))
    leader(d, 292, 380, (90, 40, 40))
    leader(d, 474, 380, (40, 50, 80))
    d.rectangle([60, 440, 524, 470], fill=(120, 85, 50))  # table
    lines = [
        "First-ever US–China–Russia summit.",
        "Joint peace declaration:",
        "\"Nuclear war must never be fought.\"",
    ]
    ty = 488
    for ln in lines:
        d.text((44, ty), ln, font=font(28, bold=False), fill=TEXT)
        ty += 38

    # ---- Cyclone Akvan ----
    box = (24, 622, 560, 1000)
    d.rounded_rectangle(box, radius=14, fill=PANEL, outline=BORDER, width=3)
    d.text((44, 638), "CYCLONE AKVAN", font=font(38), fill=ACCENT)
    # spiral storm
    cx, cy = 170, 790
    for r in range(96, 10, -14):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20 + r, end=300 + r, fill=CYAN, width=9)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=TEXT)
    for i in range(5):  # rain streaks
        x = 300 + i * 48
        d.line([x, 730, x - 18, 790], fill=CYAN, width=6)
        d.line([x, 810, x - 18, 870], fill=CYAN, width=6)
    d.text((44, 906), "Severe storm hits Odisha, India", font=font(28, bold=False), fill=TEXT)
    d.text((44, 946), "100,000+ evacuated · winds 90–100 km/h", font=font(26, bold=False), fill=SUB)

    # ---- Right column panels ----
    rx0, rx1 = 576, 1000
    panels = [
        ("ANTHROPIC IPO", ["Record debut: ~$81B raised (est.)", "Biggest IPO in history"], GREEN),
        ("GTA VI LAUNCH", ["Biggest game launch ever", "~$1.8B on day one (est.)"], (255, 140, 200)),
        ("TRUMP ON IRAN", ["\"We'll see after Jan 1\"", "Decision waits until 2027"], RED),
        ("EUROPE & UKRAINE", ["Europe says it is ready for talks with Russia"], CYAN),
        ("HAYABUSA2", ["Japan's probe calls off asteroid landing — engine trouble"], SUB),
    ]
    y = 162
    for i, (title, lines, color) in enumerate(panels):
        box = (rx0, y, rx1, y + 156)
        d.rounded_rectangle(box, radius=14, fill=PANEL, outline=BORDER, width=3)
        d.rectangle([rx0, y, rx0 + 10, y + 156], fill=color)
        d.text((rx0 + 26, y + 12), title, font=font(30), fill=color)
        ty = y + 52
        for ln in lines:
            for part in wrap(d, ln, font(24, bold=False), 272):
                d.text((rx0 + 26, ty), part, font=font(24, bold=False), fill=TEXT)
                ty += 30
        # small icon per panel, right side, below the title row
        ix, iy = rx1 - 96, y + 46
        if i == 0:  # rising bars
            for j, bh in enumerate([26, 44, 64, 88]):
                d.rectangle([ix + j * 20, iy + 96 - bh, ix + j * 20 + 14, iy + 96], fill=GREEN)
            d.line([ix - 4, iy + 78, ix + 84, iy + 2], fill=TEXT, width=5)
        elif i == 1:  # gamepad
            d.rounded_rectangle([ix - 8, iy + 34, ix + 92, iy + 88], radius=24, outline=TEXT, width=5)
            d.ellipse([ix + 52, iy + 48, ix + 66, iy + 62], fill=(255, 140, 200))
            d.ellipse([ix + 68, iy + 62, ix + 82, iy + 76], fill=(255, 140, 200))
            d.line([ix + 14, iy + 61, ix + 38, iy + 61], fill=TEXT, width=6)
            d.line([ix + 26, iy + 49, ix + 26, iy + 73], fill=TEXT, width=6)
        elif i == 2:  # calendar
            d.rounded_rectangle([ix, iy + 8, ix + 84, iy + 92], radius=8, outline=TEXT, width=5)
            d.rectangle([ix, iy + 8, ix + 84, iy + 32], fill=RED)
            d.text((ix + 10, iy + 42), "2027", font=font(30), fill=TEXT)
        elif i == 3:  # speech bubbles
            d.rounded_rectangle([ix - 6, iy + 6, ix + 52, iy + 46], radius=10, outline=CYAN, width=5)
            d.rounded_rectangle([ix + 30, iy + 50, ix + 92, iy + 90], radius=10, outline=TEXT, width=5)
        else:  # probe + asteroid
            d.ellipse([ix + 44, iy + 52, ix + 92, iy + 96], fill=(150, 150, 160))
            d.rectangle([ix + 8, iy + 18, ix + 34, iy + 44], fill=SUB)
            d.rectangle([ix - 14, iy + 24, ix + 6, iy + 38], fill=CYAN)
            d.rectangle([ix + 36, iy + 24, ix + 56, iy + 38], fill=CYAN)
            d.line([ix + 21, iy + 44, ix + 40, iy + 66], fill=SUB, width=4)
        y += 166

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
