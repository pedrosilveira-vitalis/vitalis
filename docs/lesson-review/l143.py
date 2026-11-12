import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 668,
      "One attack, then a fork: keep the oxygen or lose it as water",
      "Every nucleophile does the same first thing. What differs is whether the intermediate stops at protonation or dehydrates.",
      "A flow diagram. A nucleophile attacks the sp2 carbonyl carbon to give a tetrahedral alkoxide "
      "intermediate, which then forks. On the left branch the oxygen is simply protonated and the "
      "reaction stops, giving hydrates, hemiacetals, cyanohydrins and alcohols. On the right branch the "
      "oxygen is protonated and leaves as water, giving acetals and ketals, imines and enamines. A note "
      "records that these condensations need acid and that imine formation is fastest near pH 4 to 5.")

# top: the common step
d.rect(250, 96, 400, 76, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, 124, "Nu attacks the carbonyl carbon", color=NAVY, weight="bold", size=18)
d.text(450, 150, "sp\u00b2 \u2192 sp\u00b3, trigonal planar \u2192 tetrahedral", color=GREY, size=14)

d.arrow(450, 174, 450, 206, NAVY)

d.rect(290, 208, 320, 62, GOLD, FILL[GOLD], rx=12, width=2)
d.text(450, 234, "tetrahedral alkoxide intermediate", color=GOLD, weight="bold", size=17)
d.text(450, 256, "R\u2082C(Nu)\u2013O\u207b", color=GREY, size=14)

d.arrow(390, 272, 250, 312, SAGE)
d.text(286, 288, "protonate O", color=SAGE, weight="bold", size=14)
d.arrow(510, 272, 650, 312, RED)
d.text(620, 288, "protonate O, lose H\u2082O", color=RED, weight="bold", size=14)

LEFT = [
    ("H\u2082O", "hydrate (gem-diol)"),
    ("one R'OH", "hemiacetal"),
    ("CN\u207b (from HCN)", "cyanohydrin"),
    ("H:\u207b (NaBH\u2084, LiAlH\u2084)", "alcohol"),
]
RIGHT = [
    ("second R'OH", "acetal / ketal"),
    ("R'NH\u2082 (1\u00b0 amine)", "imine (Schiff base)"),
    ("R'\u2082NH (2\u00b0 amine)", "enamine"),
]

for x0, col, head, rows in ((60, SAGE, "Addition stops here", LEFT),
                            (470, RED, "Condensation: water leaves", RIGHT)):
    d.rect(x0, 318, 370, 236, col, FILL[col], rx=12, width=2)
    d.text(x0 + 185, 344, head, color=col, weight="bold", size=18)
    y = 370
    for nu, prod in rows:
        d.text(x0 + 20, y + 16, nu, anchor="start", color=NAVY, size=14)
        d.text(x0 + 350, y + 16, prod, anchor="end", color=col, weight="bold", size=15)
        if (nu, prod) != rows[-1]:
            d.line(x0 + 18, y + 28, x0 + 352, y + 28, GREY, 1)
        y += 44

d.rect(60, 566, 780, 82, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, 594, "The right-hand branch needs acid \u2014 and not too much of it",
       color=NAVY, weight="bold", size=17)
d.text(450, 616, "Acid protonates the leaving OH, but it also protonates the amine: imine and enamine formation peak near pH 4\u20135.",
       color=GREY, size=13)
d.text(450, 634, "The Wittig is the outlier \u2014 the oxygen leaves with phosphorus as Ph\u2083P=O, giving C=C.", color=GREY, size=13)

d.save("carbonyl-addition-fork")
