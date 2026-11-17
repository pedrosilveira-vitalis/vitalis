import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 962,
      "Three dimensions that need not move together",
      "Weber's point was that one number cannot locate a person in a hierarchy",
      "Top: class, status and party as three independent axes, with the cases where they come apart — which "
      "is exactly what vignettes are built from. The professor and the executive, the old family with the name "
      "but not the money, the union with the votes but neither. When they disagree for one person that is "
      "status inconsistency, and it carries its own psychological cost. Bottom left: the social gradient in "
      "health, the single most important stratification finding for this exam, because it runs the whole "
      "length of the hierarchy rather than appearing only at the bottom. Bottom right: the four pathways by "
      "which position gets under the skin, and the forms of capital that keep position where it is."
      )

# ---------------- Panel A: three dimensions ----------------
d.rect(40, 180, 840, 300, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Class · Status · Party", color=NAVY, weight="bold", size=15)

dims = [("CLASS", "ECONOMIC", "what you own and what\nyou can sell in the market",
         "property and acquisition classes", BLUE),
        ("STATUS", "PRESTIGE", "the honour a group commands;\nshared lifestyle and boundaries",
         "defended by social closure", GOLD),
        ("PARTY", "POWER", "organised to get its way\nagainst resistance",
         "unions, lobbies, parties", RED)]
cx = 70
for name, kind, note, extra, col in dims:
    d.rect(cx, 228, 250, 150, col, FILL[col], rx=10, width=2)
    d.text(cx + 125, 254, name, color=col, weight="bold", size=14)
    d.text(cx + 125, 274, kind, color=NAVY, weight="bold", size=10)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 125, 300 + j * 15, ln, color=GREY, size=9.5)
    d.text(cx + 125, 348, extra, color=col, weight="bold", size=9)
    cx += 270

d.text(460, 402, "WHEN THEY DISAGREE FOR ONE PERSON: STATUS INCONSISTENCY", color=NAVY, weight="bold", size=11)
cases = [("the professor", "low class, high status"),
         ("the old family", "no money left, name intact"),
         ("the union", "neither — but it has the votes")]
cx = 70
for who, what in cases:
    d.rect(cx, 420, 250, 44, GREY, FILL[GREY], rx=7, width=1.4)
    d.text(cx + 125, 438, who, color=NAVY, weight="bold", size=10)
    d.text(cx + 125, 454, what, color=GREY, size=9)
    cx += 270

# ---------------- Panel B: the gradient ----------------
d.rect(40, 496, 410, 452, RED, "none", rx=12, width=2)
d.text(245, 524, "The social gradient in health", color=RED, weight="bold", size=14)
d.text(245, 544, "Whitehall: all employed, none poor", color=GREY, size=9.5)

m = d.axes(96, 566, 300, 150, "employment grade", "mortality", (0, 4), (0, 4),
           ticks_x=0, ticks_y=0)
d.curve(m, [(0.4, 3.3), (1.3, 2.4), (2.2, 1.6), (3.1, 1.0), (3.7, 0.7)], RED, 3)
for x, y, lab in [(0.4, 3.3, "lowest"), (3.7, 0.7, "highest")]:
    px, py = m(x, y)
    d.circle(px, py, 5, RED, RED)
d.text(130, 582, "lowest grade", anchor="start", color=RED, weight="bold", size=9)
d.text(380, 706, "highest grade", anchor="end", color=SAGE, weight="bold", size=9)

d.text(245, 784, "every step up lowers mortality", color=NAVY, weight="bold", size=11)
d.text(245, 800, "so it is not just absolute deprivation —", color=GREY, size=9.5)
d.text(245, 816, "relative position has its own effect", color=GREY, size=9.5)

d.rect(64, 826, 362, 108, GOLD, FILL[GOLD], rx=9, width=2)
d.text(245, 848, "WHICH IS WHY RELATIVE POVERTY MATTERS", color=GOLD, weight="bold", size=9.5)
for j, ln in enumerate(["ABSOLUTE poverty: below a fixed line — the World",
                        "Bank's international line is now $3.00 a day",
                        "RELATIVE poverty: far below your own society's norm;",
                        "shame and exclusion register physiologically"]):
    d.text(245, 868 + j * 16, ln, color=NAVY if j % 2 == 0 else GREY,
           weight="bold" if j % 2 == 0 else "normal", size=8.5)

# ---------------- Panel C: pathways and capital ----------------
d.rect(470, 496, 410, 452, SAGE, "none", rx=12, width=2)
d.text(675, 524, "How position gets under the skin", color=SAGE, weight="bold", size=14)

paths = [("MATERIAL", "food, housing, safety, time", BLUE),
         ("PSYCHOSOCIAL", "chronic stress, low control → HPA axis\n→ cortisol → allostatic load", RED),
         ("BEHAVIOURAL", "smoking, diet, exercise — themselves\nshaped by stress and environment", GOLD),
         ("ACCESS", "insurance, transport, time off, distrust", BLUE),
         ("EXPOSURE", "highways, plants, pollution", GREY)]
y = 546
for name, note, col in paths:
    lines = note.split("\n")
    h = 26 + len(lines) * 13
    d.rect(494, y, 362, h, col, FILL[col], rx=7, width=1.5)
    d.text(560, y + 17, name, anchor="start", color=col, weight="bold", size=10)
    for j, ln in enumerate(lines):
        d.text(690, y + 17 + j * 13, ln, anchor="start" if len(lines) > 1 else "start",
               color=GREY, size=8.5)
    y += h + 6

d.text(675, 800, "AND WHAT KEEPS IT IN PLACE", color=NAVY, weight="bold", size=11)

caps = [("ECONOMIC CAPITAL", "money and property"),
        ("CULTURAL CAPITAL", "embodied, objectified, credentialed"),
        ("SOCIAL CAPITAL", "who you know, and who vouches"),
        ("HABITUS", "what you think is realistic for you")]
y = 816
for name, note in caps:
    d.rect(494, y, 362, 28, NAVY, FILL[NAVY], rx=6, width=1.4)
    d.text(510, y + 18, name, anchor="start", color=NAVY, weight="bold", size=9)
    d.text(840, y + 18, note, anchor="end", color=GREY, size=8.5)
    y += 31

d.save("weber-dimensions-health-gradient-and-capital")
print("ok")
