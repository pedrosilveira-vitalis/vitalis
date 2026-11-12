import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 600,
      "Amine basicity is one question: how available is the lone pair?",
      "The scale is the pKₐ of the conjugate acid — higher means the amine holds a proton more willingly.",
      "A horizontal pKa scale of conjugate acids running from minus 5 to 12. Pyrrole sits at minus 3.8 "
      "and an amide near zero because the lone pair is tied up in a pi system; aniline at 4.6 and "
      "pyridine at 5.2 in the middle; ammonia at 9.25 and the aliphatic amines between 9.8 and 10.7 at "
      "the basic end. A lower band lists the three factors that move a nitrogen along the scale: "
      "resonance delocalisation, hybridisation, and inductive effects plus solvation.")

X0, X1 = 110, 840
LO, HI = -5.0, 12.0


def px(v):
    return X0 + (X1 - X0) * (v - LO) / (HI - LO)


AX = 250
d.line(X0, AX, X1, AX, NAVY, 2.5)
for v in range(-4, 13, 2):
    d.line(px(v), AX - 6, px(v), AX + 6, NAVY, 1.5)
    d.text(px(v), AX + 24, str(v), color=GREY, size=13)
d.text(X0 + 4, AX + 50, "← lone pair tied up", anchor="start", color=RED, weight="bold", size=14)
d.text(X1 - 4, AX + 50, "lone pair free →", anchor="end", color=SAGE, weight="bold", size=14)


marks = [
    (-3.8, "pyrrole", "lone pair is 2 of the 6 aromatic π electrons", RED, 1, 0),
    (0.0, "amide N", "lone pair delocalised into C=O", RED, -1, 0),
    (4.6, "aniline", "lone pair delocalised into the ring", GOLD, 1, 0),
    (5.2, "pyridine", "sp² lone pair, in plane, not in the π system", GOLD, -1, 0),
    (9.25, "NH₃", "reference point", BLUE, 1, -58),
    (9.8, "3° amine", "only one N–H to solvate", BLUE, -1, 0),
    (10.7, "1° / 2° amine", "alkyl donation plus good solvation", SAGE, 1, 36),
]

for v, name, why, col, side, dx in marks:
    x = px(v)
    y = AX - 14 if side > 0 else AX + 14
    ty = AX - 92 if side > 0 else AX + 92
    d.line(x, y, x, ty + (18 if side > 0 else -18), col, 2, dash=True)
    d.circle(x, AX, 7, col, col, 0)
    d.text(x + dx, ty, name, color=col, weight="bold", size=16)
    d.lines(x + dx, ty + 22, why, chars=22, lh=15, size=12, color=GREY)

py = 430
d.rect(60, py, 780, 150, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 28, "Three dials, in order of how far they move the needle", color=NAVY, weight="bold", size=17)
for k, (lab, txt) in enumerate([
    ("Resonance", "a lone pair shared with a π system is barely a base at all — worth 5 to 14 pKₐ units"),
    ("Hybridisation", "sp³ holds the pair most loosely, then sp², then sp; nitriles are essentially non-basic"),
    ("Induction and solvation", "alkyl groups donate, EWGs withdraw; in water a 3° ammonium ion has the fewest N–H to solvate"),
]):
    yy = py + 58 + k * 30
    d.text(236, yy, lab, anchor="end", color=NAVY, weight="bold", size=15)
    d.text(252, yy, txt, anchor="start", color=GREY, size=13)

d.save("amine-basicity-scale")
