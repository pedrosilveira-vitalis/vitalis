import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1000,
      "Reliable, valid, or neither",
      "Consistency is not accuracy — and one of them comes first",
      "Top: the target picture, because it settles the relationship in one look. Reliability is how tightly "
      "the shots cluster; validity is whether the cluster sits on the bullseye. A measure can be reliable and "
      "wrong, but it cannot be valid and inconsistent — which is why reliability is necessary for validity "
      "and never sufficient. Middle: the four reliabilities, each with the statistic that reports it and the "
      "question it answers. Bottom: what breaks a group comparison from the inside, including the three "
      "threats that arise because the control group knows it is a control group."
      )

# ---------------- Panel A: the four targets ----------------
d.rect(40, 180, 840, 306, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The target picture", color=NAVY, weight="bold", size=15)

import math

def target(cx, cy, pts, col, label, sub):
    for r, w in ((52, 1.2), (34, 1.2), (17, 1.2)):
        d.circle(cx, cy, r, GREY, "none", width=w)
    d.circle(cx, cy, 4, NAVY, NAVY)
    for px, py in pts:
        d.circle(cx + px, cy + py, 5, col, FILL[col], width=1.6)
    d.text(cx, cy + 76, label, color=col, weight="bold", size=10.5)
    d.text(cx, cy + 92, sub, color=GREY, size=8.5)

tight_off = [(-7, -5), (2, -9), (6, 3), (-3, 7)]
tight_far = [(29, -31), (38, -25), (33, -18), (25, -24)]
spread = [(-38, -22), (33, -9), (-11, 36), (24, 28)]
spread_c = [(-30, -14), (26, -20), (-13, 29), (22, 14)]

target(160, 290, tight_far, RED, "RELIABLE, NOT VALID", "consistent and consistently wrong")
target(365, 290, spread_c, GOLD, "VALID-ISH, NOT RELIABLE", "centred on average, useless per shot")
target(570, 290, spread, GREY, "NEITHER", "no pattern, no accuracy")
target(775, 290, tight_off, SAGE, "RELIABLE AND VALID", "the only one worth having")

d.text(460, 432, "a bathroom scale that reads ten pounds heavy every time is perfectly RELIABLE and completely INVALID",
       color=NAVY, weight="bold", size=10)
d.text(460, 454, "reliability is NECESSARY for validity and never SUFFICIENT — a measure that cannot repeat itself cannot be right twice",
       color=GREY, size=9.5)

# ---------------- Panel B: four reliabilities ----------------
d.rect(40, 502, 840, 198, GOLD, "none", rx=12, width=2)
d.text(460, 530, "Four reliabilities, four questions", color=GOLD, weight="bold", size=14)

rels = [("TEST-RETEST", "same test, same people,\nlater", "correlation\nr > 0.80", BLUE),
        ("INTER-RATER", "two observers,\nsame event", "Cohen's kappa\nor ICC", RED),
        ("INTERNAL CONSISTENCY", "do the items hang\ntogether?", "Cronbach's alpha\n≥ 0.70", SAGE),
        ("PARALLEL FORMS", "two versions of\nthe same test", "correlation between\nthe forms", GOLD)]
cx = 60
for name, q, stat, col in rels:
    d.rect(cx, 550, 200, 134, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 100, 572, name, color=col, weight="bold", size=9.5)
    for j, ln in enumerate(q.split("\n")):
        d.text(cx + 100, 594 + j * 14, ln, color=NAVY, size=8.5)
    d.line(cx + 26, 630, cx + 174, 630, col, 1, dash="3,3")
    for j, ln in enumerate(stat.split("\n")):
        d.text(cx + 100, 650 + j * 14, ln, color=GREY, weight="bold" if j == 0 else "normal", size=8.5)
    cx += 205

# ---------------- Panel C: threats ----------------
d.rect(40, 716, 840, 268, BLUE, "none", rx=12, width=2)
d.text(460, 744, "What breaks the comparison from the inside", color=BLUE, weight="bold", size=14)

left = [("HISTORY", "something happened outside the study"),
        ("MATURATION", "they changed on their own"),
        ("TESTING", "they got better at the test itself"),
        ("INSTRUMENTATION", "the ruler changed, not the thing"),
        ("REGRESSION TO THE MEAN", "extreme scorers drift back"),
        ("ATTRITION", "and worse, differential dropout")]
y = 766
for name, note in left:
    d.rect(60, y, 390, 32, NAVY, FILL[NAVY], rx=6, width=1.3)
    d.text(160, y + 21, name, color=NAVY, weight="bold", size=9)
    d.text(350, y + 21, note, color=GREY, size=8.5)
    y += 36

d.text(665, 766, "AND BECAUSE THE CONTROL GROUP KNOWS", color=RED, weight="bold", size=10.5)
right = [("DIFFUSION OF TREATMENT", "controls get hold of the treatment\nanyway, so the groups converge", RED),
         ("COMPENSATORY RIVALRY", "controls try harder because they\nknow what they were denied", GOLD),
         ("RESENTFUL DEMORALIZATION", "or give up for the same reason,\nflattering the treatment group", GOLD)]
y = 782
for name, note, col in right:
    d.rect(470, y, 390, 60, col, FILL[col], rx=7, width=1.5)
    d.text(665, y + 20, name, color=col, weight="bold", size=9.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(665, y + 36 + j * 13, ln, color=GREY, size=8.5)
    y += 66

d.save("reliable-valid-or-neither")
print("ok")
