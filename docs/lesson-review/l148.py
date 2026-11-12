import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 650,
      "The ¹H scale, and the three patterns worth recognising on sight",
      "Chemical shift tells you the environment, integration counts the protons, splitting counts the neighbours.",
      "A proton chemical-shift scale from 12 to 0 ppm, printed the way a spectrum is, with the zones "
      "marked: carboxylic acid at 10 to 12, aldehyde at 9 to 10, aromatic at 6.5 to 8.5, vinyl at 4.5 to "
      "6.5, carbon bonded to oxygen or halogen at 3 to 4, allylic benzylic and alpha-to-carbonyl at 2 to "
      "3, and plain alkyl from 0.5 to 2, with TMS at zero. Below, a panel gives the n plus one rule with "
      "Pascal intensities, and another shows the three signature patterns: the ethyl triplet and quartet, "
      "the isopropyl doublet and septet, and the tert-butyl nine-proton singlet.")

X0, X1 = 72, 846
HI, LO = 12.0, 0.0


def px(v):
    return X0 + (X1 - X0) * (HI - v) / (HI - LO)


AX = 250
d.line(X0, AX, X1, AX, NAVY, 2.5)
for v in range(0, 13):
    d.line(px(v), AX - 6, px(v), AX + 6, NAVY, 1.2)
    if v % 2 == 0:
        d.text(px(v), AX + 24, str(v), color=GREY, size=12)
d.text(px(0) - 6, AX + 46, "TMS", anchor="end", color=GREY, weight="bold", size=12)
d.text(X0 + 4, AX + 46, "← downfield, deshielded", anchor="start", color=RED, weight="bold", size=13)

zones = [
    (10.0, 12.0, "COOH", RED, 1),
    (9.0, 10.0, "CHO", RED, -1),
    (6.5, 8.5, "aromatic", GOLD, 1),
    (4.5, 6.5, "vinyl", GOLD, -1),
    (3.0, 4.0, "C–O, C–X", BLUE, 1),
    (2.0, 3.0, "benzylic / α to C=O", BLUE, -1),
    (0.5, 2.0, "plain alkyl", SAGE, 1),
]
for lo, hi, name, col, side in zones:
    x1, x2 = px(hi), px(lo)
    y = AX - 50 if side > 0 else AX + 62
    w = max(x2 - x1, 34)
    d.rect(x1, y - 17, w, 34, col, FILL[col], rx=6, width=2)
    cx = x1 + w / 2
    if w >= 120:
        d.text(cx, y + 5, name, color=col, weight="bold", size=14)
    else:
        ly = y - 28 if side > 0 else y + 36
        d.text(cx, ly, name, color=col, weight="bold", size=13)

d.text(458, 128, "exchangeable –OH and –NH₂ wander anywhere from 1 to 5 ppm, broad, and vanish on a D₂O shake",
       color=GREY, size=13)

# n+1 panel
py = 372
d.rect(60, py, 380, 254, NAVY, FILL[NAVY], rx=12, width=2)
d.text(250, py + 28, "n + 1, with Pascal intensities", color=NAVY, weight="bold", size=17)
rows = [("0", "singlet", "1"), ("1", "doublet", "1 : 1"), ("2", "triplet", "1 : 2 : 1"),
        ("3", "quartet", "1 : 3 : 3 : 1"), ("4", "quintet", "1 : 4 : 6 : 4 : 1")]
yy = py + 58
for n, name, pat in rows:
    d.text(104, yy, n + " neighbour" + ("" if n == "1" else "s"), anchor="start", color=NAVY, size=14)
    d.text(262, yy, name, anchor="start", color=BLUE, weight="bold", size=14)
    d.text(412, yy, pat, anchor="end", color=GREY, size=13)
    yy += 28
d.text(250, py + 212, "Two different neighbours with different J give", color=GREY, size=13)
d.text(250, py + 232, "a doublet of doublets, not a triplet.", color=NAVY, weight="bold", size=14)

# signature patterns panel
d.rect(460, py, 380, 254, SAGE, FILL[SAGE], rx=12, width=2)
d.text(650, py + 28, "Three patterns to know on sight", color=SAGE, weight="bold", size=17)
sig = [("–CH₂CH₃", "quartet (2H) + triplet (3H)", "ethyl"),
       ("–CH(CH₃)₂", "septet (1H) + doublet (6H)", "isopropyl"),
       ("–C(CH₃)₃", "one singlet, 9H", "tert-butyl"),
       ("–OCH₃", "one singlet near δ 3.3", "methoxy")]
yy = py + 62
for formula, pattern, name in sig:
    d.text(486, yy, formula, anchor="start", color=NAVY, weight="bold", size=15)
    d.text(814, yy, name, anchor="end", color=SAGE, weight="bold", size=13)
    d.text(486, yy + 19, pattern, anchor="start", color=GREY, size=13)
    yy += 46

d.save("nmr-shift-and-splitting")
