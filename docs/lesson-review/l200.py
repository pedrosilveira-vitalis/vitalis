import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 902,
      "What a score means, and what heritability does not mean",
      "A normal curve, four theories and one statistic that is read wrong more than any other",
      "Top: the IQ distribution is defined, not discovered — mean 100, standard deviation 15, with the "
      "clinical cut-offs two deviations out on each side, and the whole scale renormed periodically because raw "
      "performance keeps rising. Middle: the four frameworks, from the single general factor that keeps falling "
      "out of factor analysis to the models built to capture what the tests leave out. Bottom: the statistic "
      "worth slowing down for. Heritability is the share of variance within one population in one environment "
      "that tracks genetic differences; it says nothing about any individual, nothing about the gap between two "
      "groups, and nothing about whether the trait can be changed. The clearest proof is that the number itself "
      "moves — it falls where deprivation makes environments vary more."
      )

# ---------------- Panel A: the distribution ----------------
d.rect(40, 170, 840, 250, BLUE, "none", rx=12, width=2)
d.text(460, 198, "The scale is built, not found", color=BLUE, weight="bold", size=16)

import math
m = d.axes(120, 218, 680, 134, "", "", (55, 145), (0, 1.08),
           ticks_x=None, ticks_y=None)
pts = [(x, math.exp(-((x - 100) ** 2) / (2 * 15.0 ** 2))) for x in range(55, 146)]
d.curve(m, pts, BLUE, 2.8)
for v, lab, col in [(70, "70", RED), (85, "85", GREY), (100, "100", NAVY),
                    (115, "115", GREY), (130, "130", SAGE)]:
    px, py = m(v, 0)
    tx, ty = m(v, math.exp(-((v - 100) ** 2) / (2 * 15.0 ** 2)))
    d.line(px, py, tx, ty, col, 1.4, dash="4,4")
    d.text(px, py + 20, lab, color=col, weight="bold", size=12)

px, _ = m(70, 0)
d.text(px, 232, "−2 SD", color=RED, weight="bold", size=11)
d.text(px, 248, "intellectual disability", color=RED, size=10)
d.text(px, 262, "requires adaptive deficits too", color=GREY, size=10)
px, _ = m(130, 0)
d.text(px, 232, "+2 SD", color=SAGE, weight="bold", size=11)
d.text(px, 248, "gifted range", color=SAGE, size=10)

d.text(460, 396, "mean 100 · SD 15 · renormed every few decades, because the Flynn effect adds "
                 "about 3 points a decade to raw performance",
       color=GREY, size=11)

# ---------------- Panel B: four frameworks ----------------
d.rect(40, 436, 840, 190, SAGE, "none", rx=12, width=2)
d.text(460, 464, "Four answers to \"intelligence of what kind?\"", color=SAGE, weight="bold", size=16)

cards = [
    ("SPEARMAN", "g, plus task-specific s", "everything correlates\npositively — that is g", BLUE),
    ("CATTELL", "fluid vs crystallised", "Gf peaks early and falls;\nGc holds or grows", SAGE),
    ("GARDNER", "eight intelligences", "popular in schools; weak\nfactor-analytic support", GOLD),
    ("STERNBERG", "analytical · creative · practical", "\"street smarts\" is the\npractical branch", RED),
]
x = 62
for name, sub, note, col in cards:
    d.rect(x, 484, 198, 120, col, FILL[col], rx=10, width=2)
    d.text(x + 99, 510, name, color=col, weight="bold", size=13)
    d.text(x + 99, 534, sub, color=NAVY, weight="bold", size=11)
    n1, n2 = note.split("\n")
    d.text(x + 99, 562, n1, color=GREY, size=11)
    d.text(x + 99, 578, n2, color=GREY, size=11)
    x += 204

# ---------------- Panel C: heritability ----------------
d.rect(40, 642, 840, 230, RED, "none", rx=12, width=2)
d.text(460, 670, "Heritability: what the number is, and what it is not",
       color=RED, weight="bold", size=16)

d.rect(70, 690, 380, 160, SAGE, FILL[SAGE], rx=10, width=2)
d.text(260, 714, "IT IS", color=SAGE, weight="bold", size=13)
for i, t in enumerate(["the share of VARIANCE in one population",
                       "attributable to genetic differences",
                       "measured in one environment, at one time",
                       "0.50–0.80 for adults in Western samples"]):
    d.text(260, 740 + i * 24, t, color=NAVY, size=12)
d.text(260, 840, "MZ .86 together · .75 apart · DZ .60", color=GREY, weight="bold", size=11)

d.rect(470, 690, 380, 160, RED, FILL[RED], rx=10, width=2)
d.text(660, 714, "IT IS NOT", color=RED, weight="bold", size=13)
for i, t in enumerate(["a statement about any one person",
                       "an explanation of a gap between groups",
                       "a ceiling on what environments can do",
                       "a fixed constant — it falls under deprivation"]):
    d.text(660, 740 + i * 24, t, color=NAVY, size=12)
d.text(660, 840, "height is highly heritable and still rose with nutrition",
       color=GREY, weight="bold", size=11)

d.save("iq-distribution-theories-and-heritability")
print("ok")
