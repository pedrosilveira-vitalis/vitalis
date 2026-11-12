import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 740,
      "Counting sigma bonds and lone pairs gives the hybridization",
      "Add sigma bonds + lone pairs on the atom. Ignore pi bonds. The sum is the number of hybrid orbitals.",
      "Three columns compare sp3, sp2 and sp centers: the count of sigma bonds plus lone pairs, the "
      "resulting geometry, bond angle, percent s character, and an example. A lower panel shows a "
      "carbonyl oxygen, where both lone pairs sit in sp2 orbitals because the unhybridized p orbital "
      "is already used by the pi bond.")

cols = [
    (170, "sp³", "4", "tetrahedral", "109.5°", "25% s", "CH₄, NH₃, H₂O", NAVY),
    (450, "sp²", "3", "trigonal planar", "120°", "33% s", "C₂H₄, C=O, benzene", BLUE),
    (730, "sp", "2", "linear", "180°", "50% s", "HC≡CH, CO₂, HCN", RED),
]

for cx, name, cnt, geom, ang, sch, ex, col in cols:
    d.rect(cx - 125, 96, 250, 66, col, FILL[col], rx=12, width=2)
    d.text(cx, 124, name, color=col, weight="bold", size=30)
    d.text(cx, 150, cnt + " sigma bonds + lone pairs", color=col, size=14)

    # geometry sketch
    gy = 228
    d.circle(cx, gy, 11, col, col, 0)
    if name == "sp³":
        for a, b in ((-62, -34), (62, -34), (-30, 46), (34, 40)):
            d.line(cx, gy, cx + a, gy + b, col, 2)
            d.circle(cx + a, gy + b, 7, col, "#ffffff", 2)
    elif name == "sp²":
        for a, b in ((0, -52), (-46, 28), (46, 28)):
            d.line(cx, gy, cx + a, gy + b, col, 2)
            d.circle(cx + a, gy + b, 7, col, "#ffffff", 2)
        d.text(cx, gy + 2, "", color=col)
    else:
        for a in (-62, 62):
            d.line(cx, gy, cx + a, gy, col, 2)
            d.circle(cx + a, gy, 7, col, "#ffffff", 2)

    d.text(cx, gy + 78, geom, color=NAVY, weight="bold", size=17)
    d.text(cx, gy + 102, ang + "  ·  " + sch, color=GREY, size=15)
    d.text(cx, gy + 126, ex, color=col, size=15)

# unhybridized p orbital note
d.rect(60, 388, 780, 52, GREY, FILL[GREY], rx=10, width=2)
d.text(450, 410, "Unhybridized p orbitals left over:  sp³ → none   ·   sp² → one   ·   sp → two",
       color=NAVY, weight="bold", size=17)
d.text(450, 431, "Each leftover p orbital makes one pi bond. Pi bonds never change the hybridization.",
       color=GREY, size=14)

# carbonyl oxygen panel
d.rect(60, 462, 780, 148, SAGE, FILL[SAGE], rx=12, width=2)
d.text(450, 486, "Worked case: the oxygen of a carbonyl (C=O)", color=SAGE, weight="bold", size=19)

ox, oy = 215, 548
d.circle(ox, oy, 16, SAGE, "#ffffff", 2.5)
d.text(ox, oy + 6, "O", color=SAGE, weight="bold", size=19)
d.circle(ox - 92, oy, 16, NAVY, "#ffffff", 2.5)
d.text(ox - 92, oy + 6, "C", color=NAVY, weight="bold", size=19)
d.line(ox - 76, oy - 4, ox - 16, oy - 4, NAVY, 2.5)
d.line(ox - 76, oy + 4, ox - 16, oy + 4, RED, 2.5)
d.text(ox - 46, oy - 14, "σ", color=NAVY, size=14)
d.text(ox - 46, oy + 24, "π", color=RED, size=14)

# two lone pairs in the plane
for dy in (-22, 22):
    d.circle(ox + 26, oy + dy, 3.5, SAGE, SAGE, 0)
    d.circle(ox + 38, oy + dy, 3.5, SAGE, SAGE, 0)
d.text(ox + 52, oy - 17, "lone pair (sp²)", anchor="start", color=SAGE, size=14)
d.text(ox + 52, oy + 27, "lone pair (sp²)", anchor="start", color=SAGE, size=14)

d.lines(560, 518,
        "1 sigma bond + 2 lone pairs = 3 → sp². Both lone pairs occupy sp² orbitals in the "
        "plane. The unhybridized p orbital is already holding the pi bond, so it cannot also hold "
        "a lone pair.",
        chars=42, lh=20, size=15, color=NAVY, anchor="start")

d.legend(60, 644, [(NAVY, "In the C=O panel — Navy: sigma bond", False),
                   (RED, "Red: pi bond from the p orbitals", False),
                   (SAGE, "Sage: lone pairs on oxygen", False)])

d.save("hybridization-counting")
