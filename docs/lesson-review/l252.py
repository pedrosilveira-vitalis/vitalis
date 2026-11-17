import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1016,
      "Two ways to be wrong",
      "The decision table, and which direction each bias pushes the result",
      "Top: the 2×2 that organises hypothesis testing. The truth sits in the columns and your decision in the "
      "rows, which gives exactly two ways to be wrong and exactly two ways to be right. Alpha is the rate of "
      "the false alarm, beta the rate of the miss, and power is the complement of beta. Tightening alpha "
      "trades one error for the other; only a bigger sample shrinks both at once. Middle: what moves power, "
      "and the confidence interval as the same test read off an interval. Bottom: the biases sorted by the "
      "direction they push the result, because passages usually ask which way the error runs rather than "
      "what the bias is called."
      )

# ---------------- Panel A: the 2x2 ----------------
d.rect(40, 180, 840, 288, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The decision table", color=NAVY, weight="bold", size=15)

d.text(455, 240, "THE TRUTH", color=GREY, weight="bold", size=10)
d.text(340, 262, "H₀ is TRUE", color=NAVY, weight="bold", size=10)
d.text(340, 276, "(there is no effect)", color=GREY, size=8.5)
d.text(620, 262, "H₀ is FALSE", color=NAVY, weight="bold", size=10)
d.text(620, 276, "(there is a real effect)", color=GREY, size=8.5)

d.text(150, 328, "YOU REJECT H₀", color=NAVY, weight="bold", size=10)
d.text(150, 344, "“there is an effect”", color=GREY, size=8.5)
d.text(150, 408, "YOU FAIL TO REJECT", color=NAVY, weight="bold", size=10)
d.text(150, 424, "“not enough evidence”", color=GREY, size=8.5)

cells = [(250, 292, RED, "TYPE I ERROR", "false positive · “I cried wolf”", "probability = α"),
         (530, 292, SAGE, "CORRECT", "you found a real effect", "probability = POWER = 1 − β"),
         (250, 372, SAGE, "CORRECT", "nothing there, nothing claimed", "probability = 1 − α"),
         (530, 372, GOLD, "TYPE II ERROR", "false negative · “I missed the wolf”", "probability = β")]
for x, y, col, name, note, prob in cells:
    d.rect(x, y, 180, 72, col, FILL[col], rx=8, width=1.8)
    d.text(x + 90, y + 24, name, color=col, weight="bold", size=10.5)
    d.text(x + 90, y + 42, note, color=NAVY, size=8)
    d.text(x + 90, y + 60, prob, color=GREY, weight="bold", size=8.5)

d.text(460, 456, "lowering α trades a Type I error for a Type II error — only a LARGER SAMPLE reduces both at once",
       color=NAVY, weight="bold", size=10)

# ---------------- Panel B: power and CIs ----------------
d.rect(40, 484, 410, 250, GOLD, "none", rx=12, width=2)
d.text(245, 512, "What raises POWER", color=GOLD, weight="bold", size=14)

pw = [("bigger SAMPLE", "the one you can actually change", SAGE),
      ("bigger EFFECT", "a real difference that is large", SAGE),
      ("less VARIABILITY", "tighter measurement, cleaner design", SAGE),
      ("larger α", "but you buy it with Type I errors", RED)]
y = 536
for name, note, col in pw:
    d.rect(64, y, 362, 40, col, FILL[col], rx=7, width=1.4)
    d.text(245, y + 17, name, color=col, weight="bold", size=10)
    d.text(245, y + 32, note, color=GREY, size=8.5)
    y += 45

d.text(245, 724, "convention: α = 0.05, β = 0.20, power = 0.80", color=NAVY, weight="bold", size=9.5)

d.rect(470, 484, 410, 250, BLUE, "none", rx=12, width=2)
d.text(675, 512, "The same test, read off an interval", color=BLUE, weight="bold", size=13.5)

d.rect(494, 532, 362, 56, SAGE, FILL[SAGE], rx=8, width=1.6)
d.text(675, 554, "a DIFFERENCE: does the CI contain 0?", color=NAVY, weight="bold", size=10)
d.text(675, 574, "if not, it is significant at α = 0.05", color=GREY, size=8.5)

d.rect(494, 596, 362, 56, SAGE, FILL[SAGE], rx=8, width=1.6)
d.text(675, 618, "a RATIO (RR or OR): does it contain 1?", color=NAVY, weight="bold", size=10)
d.text(675, 638, "if not, it is significant at α = 0.05", color=GREY, size=8.5)

d.rect(494, 660, 362, 62, RED, FILL[RED], rx=8, width=1.8)
d.text(675, 680, "WIDTH", color=RED, weight="bold", size=10)
d.text(675, 698, "wider: smaller N, more variability,", color=GREY, size=8.5)
d.text(675, 712, "or a HIGHER confidence level (99% > 95%)", color=GREY, size=8.5)

# ---------------- Panel C: biases by direction ----------------
d.rect(40, 750, 840, 248, SAGE, "none", rx=12, width=2)
d.text(460, 778, "Which way does the bias push?", color=SAGE, weight="bold", size=14)

d.text(245, 804, "INFLATES THE EFFECT", color=RED, weight="bold", size=11)
d.text(675, 804, "HIDES OR SHRINKS THE EFFECT", color=BLUE, weight="bold", size=11)

infl = [("recall bias", "the ill search their past harder"),
        ("publication bias", "null results stay in the drawer"),
        ("lead-time bias", "earlier diagnosis, not longer life"),
        ("length-time bias", "screening catches the slow cancers"),
        ("observer bias", "if the rater knows the group")]
shr = [("non-differential misclassification", "noise in either variable"),
       ("diffusion of treatment", "controls get the treatment too"),
       ("low power", "a real effect goes undetected"),
       ("ceiling and floor effects", "the scale runs out of room"),
       ("attrition", "either way, depending on who leaves")]
y = 820
for (n1, d1), (n2, d2) in zip(infl, shr):
    d.rect(60, y, 390, 32, RED, FILL[RED], rx=6, width=1.2)
    d.text(150, y + 21, n1, color=RED, weight="bold", size=9)
    d.text(350, y + 21, d1, color=GREY, size=8)
    d.rect(470, y, 390, 32, BLUE, FILL[BLUE], rx=6, width=1.2)
    d.text(580, y + 21, n2, color=BLUE, weight="bold", size=8.5)
    d.text(770, y + 21, d2, color=GREY, size=8)
    y += 35

d.save("two-ways-to-be-wrong-and-bias-direction")
print("ok")
