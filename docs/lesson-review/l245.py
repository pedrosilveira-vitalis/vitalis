import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 972,
      "Four stages, two curves, and the gap between them",
      "Population grows in the gap — after deaths fall and before births follow",
      "Top: the demographic transition drawn properly. The two rates fall one after the other, not together, "
      "and the shaded gap between them is the population boom. That is the whole model: mortality falls first "
      "because sanitation, food and basic medicine are cheap and need no change in behaviour; fertility falls "
      "later because it requires urbanisation, schooling for girls, contraception and a change in what "
      "children are for. Bottom left: the three pyramid shapes and what each predicts. Bottom right: the "
      "measures, with the trap that catches most people — a crude rate is not adjusted for age, so two "
      "populations with different age structures cannot be compared on one."
      )

# ---------------- Panel A: the transition ----------------
d.rect(40, 180, 840, 346, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The demographic transition", color=NAVY, weight="bold", size=15)

m = d.axes(110, 232, 700, 190, "", "rate per 1,000", (0, 4), (0, 50), ticks_x=0, ticks_y=0)

import math
def birth(x):
    return 44 - 32 / (1 + math.exp(-(x - 2.45) * 3.0))
def death(x):
    return 40 - 31 / (1 + math.exp(-(x - 1.35) * 3.2))

xs = [i / 40.0 for i in range(0, 161)]
d.curve(m, [(x, birth(x)) for x in xs], RED, 3)
d.curve(m, [(x, death(x)) for x in xs], BLUE, 3)

# shaded gap: approximate with vertical lines
for i in range(0, 41):
    x = 0.9 + i * 0.054
    b = birth(x); dd = death(x)
    if b - dd > 1:
        px1, py1 = m(x, b)
        px2, py2 = m(x, dd)
        d.line(px1, py1, px2, py2, SAGE, 1.1)

d.curve(m, [(x, birth(x)) for x in xs], RED, 3)
d.curve(m, [(x, death(x)) for x in xs], BLUE, 3)

d.text(200, 244, "BIRTH RATE", color=RED, weight="bold", size=10)
d.text(200, 302, "DEATH RATE", color=BLUE, weight="bold", size=10)
d.text(490, 256, "population grows here", color=SAGE, weight="bold", size=10.5)

for i, (lab, xpos) in enumerate([("1", 0.45), ("2", 1.5), ("3", 2.6), ("4", 3.6)]):
    px, _ = m(xpos, 0)
    d.text(px, 442, "STAGE " + lab, color=NAVY, weight="bold", size=10)

labels = [("high / high", 0.45), ("deaths FALL", 1.5), ("births FALL", 2.6), ("low / low", 3.6)]
for lab, xpos in labels:
    px, _ = m(xpos, 0)
    d.text(px, 460, lab, color=GREY, size=9)

d.text(460, 490, "a proposed STAGE 5: births fall below deaths and the population shrinks — Japan, Korea, much of eastern Europe",
       color=NAVY, weight="bold", size=9.5)
d.text(460, 508, "the epidemiological transition runs alongside it: infection and famine → chronic degenerative disease",
       color=GREY, size=9)

# ---------------- Panel B: pyramids ----------------
d.rect(40, 542, 410, 410, GOLD, "none", rx=12, width=2)
d.text(245, 570, "Three shapes, three futures", color=GOLD, weight="bold", size=14)

def pyramid(cx, cy, widths, col):
    n = len(widths)
    h = 9
    for i, w in enumerate(widths):
        y = cy + (n - 1 - i) * h
        d.rect(cx - w, y, w - 2, h - 2, col, FILL[col], rx=1.5, width=0.9)
        d.rect(cx + 2, y, w - 2, h - 2, col, FILL[col], rx=1.5, width=0.9)

shapes = [("EXPANSIVE", [46, 42, 38, 33, 28, 23, 17, 11, 6], RED,
           "wide base — high fertility,\nyoung, growing fast;\nhigh YOUTH dependency"),
          ("CONSTRICTIVE", [18, 22, 28, 34, 38, 36, 30, 20, 10], BLUE,
           "narrow base — fertility below\nreplacement, ageing, will shrink;\nhigh OLD-AGE dependency"),
          ("STATIONARY", [30, 31, 32, 32, 31, 29, 24, 16, 8], SAGE,
           "straight sides — fertility near\nreplacement, stable size")]
y = 592
for name, widths, col, note in shapes:
    d.text(132, y + 14, name, color=col, weight="bold", size=10.5)
    pyramid(132, y + 24, widths, col)
    for j, ln in enumerate(note.split("\n")):
        d.text(260, y + 30 + j * 13, ln, anchor="start", color=GREY, size=8.5)
    y += 118

# ---------------- Panel C: the measures ----------------
d.rect(470, 542, 410, 410, BLUE, "none", rx=12, width=2)
d.text(675, 570, "The measures, and the trap", color=BLUE, weight="bold", size=14)

meas = [("CBR · CDR", "births or deaths per 1,000 people", "CRUDE — not adjusted for age", RED),
        ("NRI", "(CBR − CDR) ÷ 10 = % growth a year", "before migration", SAGE),
        ("TFR", "children per woman at current rates", "2.1 is replacement", SAGE),
        ("IMR", "deaths under 1 per 1,000 LIVE BIRTHS", "note the denominator", GOLD),
        ("DEPENDENCY RATIO", "[(0–14) + (65+)] ÷ (15–64) × 100", "per 100 workers", GOLD)]
y = 592
for name, formula, note, col in meas:
    d.rect(494, y, 362, 48, col, FILL[col], rx=7, width=1.5)
    d.text(675, y + 17, name, color=col, weight="bold", size=10.5)
    d.text(675, y + 31, formula, color=NAVY, size=9)
    d.text(675, y + 44, note, color=GREY, size=8.5)
    y += 54

d.rect(494, y + 6, 362, 78, RED, FILL[RED], rx=9, width=2)
d.text(675, y + 26, "THE TRAP", color=RED, weight="bold", size=11)
d.text(675, y + 44, "a retirement town has a high crude death rate", color=NAVY, size=9)
d.text(675, y + 59, "and excellent health. Compare AGE-ADJUSTED", color=NAVY, weight="bold", size=9)
d.text(675, y + 74, "rates, or the comparison means nothing.", color=NAVY, weight="bold", size=9)

d.save("demographic-transition-pyramids-and-measures")
print("ok")
