import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 962,
      "Two axes of mobility, and two ways to measure it",
      "Across generations or within a life; against your parents or against everyone else",
      "Top: the four combinations that the vocabulary describes, laid out on the two questions that generate "
      "them — whose lifetime is being compared, and in which direction. Horizontal movement sits at the "
      "centre: a change of job without a change of stratum. Middle: absolute against relative mobility, the "
      "pair most often confused, because a country can have plenty of one and almost none of the other. The "
      "two figures underneath are the standard illustration: nearly everyone born in 1940 out-earned their "
      "parents, while barely half of those born in 1984 did, even though the rank ordering changed little "
      "either way. Bottom: the transition matrix as the exam uses it, and the measures that summarise it."
      )

# ---------------- Panel A: the four types ----------------
d.rect(40, 180, 840, 258, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Who is being compared with whom?", color=NAVY, weight="bold", size=15)

d.rect(300, 228, 270, 34, GREY, FILL[GREY], rx=7, width=1.5)
d.text(435, 250, "INTERgenerational", color=NAVY, weight="bold", size=11)
d.rect(580, 228, 270, 34, GREY, FILL[GREY], rx=7, width=1.5)
d.text(715, 250, "INTRAgenerational", color=NAVY, weight="bold", size=11)
d.text(170, 250, "parent → child  vs.  one career", color=GREY, size=9.5)

rows = [("UP", SAGE, "the miner's daughter\nbecomes a surgeon", "the clerk works up\nto plant manager"),
        ("DOWN", RED, "the professor's son\nends up in retail", "the professional is\nlaid off at fifty")]
y = 272
for name, col, left, right in rows:
    d.rect(70, y, 220, 64, col, FILL[col], rx=8, width=1.8)
    d.text(180, y + 38, name, color=col, weight="bold", size=14)
    for text, x in ((left, 300), (right, 580)):
        d.rect(x, y, 270, 64, col, FILL[col], rx=8, width=1.6)
        for j, ln in enumerate(text.split("\n")):
            d.text(x + 135, y + 26 + j * 16, ln, color=NAVY, size=10)
    y += 72

d.text(460, 424, "and HORIZONTAL mobility is a move with no change of stratum at all",
       color=GREY, weight="bold", size=10)

# ---------------- Panel B: absolute vs relative ----------------
d.rect(40, 446, 840, 206, GOLD, "none", rx=12, width=2)
d.text(460, 474, "Absolute against relative", color=GOLD, weight="bold", size=15)

d.rect(70, 494, 390, 136, SAGE, FILL[SAGE], rx=10, width=2)
d.text(265, 518, "ABSOLUTE", color=SAGE, weight="bold", size=13)
d.text(265, 538, "do you have MORE than your parents had?", color=NAVY, size=10)
d.text(265, 562, "rises and falls with economic growth", color=GREY, size=9.5)
d.text(265, 590, "90% of the 1940 cohort out-earned their parents", color=NAVY, weight="bold", size=10)
d.text(265, 610, "about 50% of the 1984 cohort did", color=NAVY, weight="bold", size=10)

d.rect(490, 494, 390, 136, BLUE, FILL[BLUE], rx=10, width=2)
d.text(685, 518, "RELATIVE", color=BLUE, weight="bold", size=13)
d.text(685, 538, "do you RANK differently from your parents?", color=NAVY, size=10)
d.text(685, 562, "unmoved by growth; it is about position", color=GREY, size=9.5)
d.text(685, 590, "a country can be richer every decade", color=NAVY, weight="bold", size=10)
d.text(685, 610, "and still have the same families on top", color=NAVY, weight="bold", size=10)

# ---------------- Panel C: the matrix ----------------
d.rect(40, 668, 410, 276, RED, "none", rx=12, width=2)
d.text(245, 696, "Born at the bottom, ending where?", color=RED, weight="bold", size=14)
d.text(245, 716, "United States, by parental income quintile", color=GREY, size=9)

d.text(245, 742, "PERFECTLY MOBILE SOCIETY", color=GREY, weight="bold", size=10)
cx = 76
for i in range(5):
    d.rect(cx, 752, 64, 30, GREY, FILL[GREY], rx=5, width=1.4)
    d.text(cx + 32, 772, "20%", color=NAVY, weight="bold", size=10)
    cx += 70

d.text(245, 812, "WHAT IS ACTUALLY OBSERVED", color=RED, weight="bold", size=10)
obs = [("bottom", 33, RED), ("2nd", 24, GOLD), ("3rd", 19, GOLD), ("4th", 16, SAGE), ("top", 8, SAGE)]
cx = 76
for lab, pct, col in obs:
    d.rect(cx, 822, 64, 30, col, FILL[col], rx=5, width=1.4)
    d.text(cx + 32, 842, "%d%%" % pct, color=col, weight="bold", size=10)
    d.text(cx + 32, 866, lab, color=GREY, size=8.5)
    cx += 70

d.text(245, 896, "a child born in the bottom fifth has about a 1 in 13", color=NAVY, weight="bold", size=9.5)
d.text(245, 914, "chance of reaching the top fifth — not 1 in 5", color=NAVY, weight="bold", size=9.5)
d.text(245, 932, "figures approximate; they vary sharply by region", color=GREY, size=8.5)

# ---------------- Panel D: measures ----------------
d.rect(470, 668, 410, 276, BLUE, "none", rx=12, width=2)
d.text(675, 696, "The numbers that summarise it", color=BLUE, weight="bold", size=14)

meas = [("IGE", "how much of a parent's income advantage\ncarries to the child; 0 = free, 1 = fixed",
         "US about 0.45–0.50 · Denmark about 0.15", BLUE),
        ("RANK-RANK SLOPE", "percentile gained per parental percentile",
         "US about 0.34", BLUE),
        ("GINI", "income inequality, 0 to 1 — not mobility,\nbut it tracks with it",
         "US about 0.39–0.41 · Denmark about 0.29", GOLD),
        ("GREAT GATSBY CURVE", "plot the two against each other and they line up:",
         "more unequal countries are less mobile", RED)]
y = 718
for name, note, fig, col in meas:
    lines = note.split("\n")
    h = 34 + len(lines) * 12
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 17, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(lines):
        d.text(675, y + 30 + j * 12, ln, color=GREY, size=8.5)
    d.text(675, y + h - 6, fig, color=NAVY, weight="bold", size=9)
    y += h + 5

d.save("mobility-types-absolute-relative-and-measures")
print("ok")
