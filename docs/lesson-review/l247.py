import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1010,
      "Naming a study design in two questions",
      "Ask what the researcher did, then ask where the study starts",
      "Top: the decision tree that names almost any design a passage can describe. The first question is "
      "whether the researcher did anything to anyone; the second is whether assignment was random. If the "
      "researcher did nothing, the design is observational, and the question becomes where in time the study "
      "begins: at the outcome and looking back, at the exposure and looking forward, or at one moment with no "
      "time at all. Middle: what each observational design can and cannot compute, which is how passages "
      "usually test the difference. Bottom: the two validities, which pull against each other, and the "
      "specific threats named for each."
      )

# ---------------- Panel A: decision tree ----------------
d.rect(40, 180, 840, 336, NAVY, "none", rx=12, width=2)
d.text(460, 208, "What kind of study is this?", color=NAVY, weight="bold", size=15)

d.rect(330, 228, 260, 44, NAVY, FILL[NAVY], rx=9, width=1.8)
d.text(460, 248, "did the researcher ASSIGN", color=NAVY, weight="bold", size=10)
d.text(460, 264, "the exposure or treatment?", color=NAVY, weight="bold", size=10)

d.arrow(400, 274, 250, 300, SAGE, label="yes", width=1.6, lx=-14, ly=-6)
d.arrow(520, 274, 672, 300, GREY, label="no", width=1.6, lx=14, ly=-6)

# yes branch
d.rect(120, 304, 260, 40, SAGE, FILL[SAGE], rx=8, width=1.6)
d.text(250, 329, "was assignment RANDOM?", color=NAVY, weight="bold", size=10)

d.arrow(190, 346, 150, 374, SAGE, label="yes", width=1.4, lx=-16, ly=-4)
d.arrow(310, 346, 350, 374, GOLD, label="no", width=1.4, lx=14, ly=-4)

d.rect(48, 378, 190, 64, SAGE, FILL[SAGE], rx=8, width=1.8)
d.text(143, 400, "TRUE EXPERIMENT", color=SAGE, weight="bold", size=10.5)
d.text(143, 418, "the only design that", color=GREY, size=8.5)
d.text(143, 432, "establishes causation", color=GREY, size=8.5)

d.rect(256, 378, 190, 64, GOLD, FILL[GOLD], rx=8, width=1.8)
d.text(351, 400, "QUASI-EXPERIMENT", color=GOLD, weight="bold", size=10.5)
d.text(351, 418, "nonequivalent groups,", color=GREY, size=8.5)
d.text(351, 432, "interrupted time series", color=GREY, size=8.5)

# no branch
d.rect(542, 304, 300, 40, GREY, FILL[GREY], rx=8, width=1.6)
d.text(692, 329, "where does the study START?", color=NAVY, weight="bold", size=10)

d.rect(474, 378, 132, 64, RED, FILL[RED], rx=8, width=1.8)
d.text(540, 398, "CASE-CONTROL", color=RED, weight="bold", size=9.5)
d.text(540, 416, "starts at the", color=GREY, size=8.5)
d.text(540, 430, "OUTCOME, looks back", color=GREY, size=8.5)

d.rect(614, 378, 132, 64, BLUE, FILL[BLUE], rx=8, width=1.8)
d.text(680, 398, "COHORT", color=BLUE, weight="bold", size=9.5)
d.text(680, 416, "starts at the", color=GREY, size=8.5)
d.text(680, 430, "EXPOSURE, follows", color=GREY, size=8.5)

d.rect(754, 378, 126, 64, NAVY, FILL[NAVY], rx=8, width=1.8)
d.text(817, 398, "CROSS-SECTIONAL", color=NAVY, weight="bold", size=9)
d.text(817, 416, "one moment,", color=GREY, size=8.5)
d.text(817, 430, "no time at all", color=GREY, size=8.5)

d.text(460, 472, "random SAMPLING is how people get into the study — it buys external validity", color=GREY, size=9.5)
d.text(460, 492, "random ASSIGNMENT is how they get into a group — it buys internal validity, and only it licenses a causal claim",
       color=NAVY, weight="bold", size=9.5)

# ---------------- Panel B: what each can compute ----------------
d.rect(40, 532, 840, 170, GOLD, "none", rx=12, width=2)
d.text(460, 560, "What each observational design can compute", color=GOLD, weight="bold", size=14)

cols = [("CASE-CONTROL", RED, ["ODDS RATIO only", "no incidence, no prevalence",
                               "good for RARE disease", "worst for RECALL BIAS"]),
        ("COHORT", BLUE, ["RELATIVE RISK", "true INCIDENCE", "exposure recorded before",
                          "the outcome, so little recall bias"]),
        ("CROSS-SECTIONAL", NAVY, ["PREVALENCE", "association, but no", "temporal order — you cannot",
                                   "tell which came first"])]
cx = 60
for name, col, items in cols:
    d.rect(cx, 578, 266, 108, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 133, 600, name, color=col, weight="bold", size=11)
    for j, ln in enumerate(items):
        d.text(cx + 133, 622 + j * 15, ln, color=GREY, size=8.5)
    cx += 280

# ---------------- Panel C: the two validities ----------------
d.rect(40, 718, 840, 266, BLUE, "none", rx=12, width=2)
d.text(460, 746, "The two validities pull against each other", color=BLUE, weight="bold", size=14)

d.rect(60, 766, 390, 196, SAGE, FILL[SAGE], rx=10, width=1.8)
d.text(255, 790, "INTERNAL VALIDITY", color=SAGE, weight="bold", size=12)
d.text(255, 808, "did the IV really cause the change in the DV?", color=NAVY, size=9)
d.line(90, 820, 420, 820, SAGE, 1, dash="3,3")
threats = ["confounding — a third variable drives both",
           "selection bias — the groups differed to begin with",
           "history — something else happened during the study",
           "maturation — participants changed on their own",
           "testing — measuring changed what was measured",
           "regression to the mean — extreme scores drift back",
           "attrition — and worse, differential dropout"]
for j, t in enumerate(threats):
    d.text(255, 838 + j * 17, t, color=GREY, size=8.5)

d.rect(470, 766, 390, 196, GOLD, FILL[GOLD], rx=10, width=1.8)
d.text(665, 790, "EXTERNAL VALIDITY", color=GOLD, weight="bold", size=12)
d.text(665, 808, "does the finding travel beyond this study?", color=NAVY, size=9)
d.line(500, 820, 830, 820, GOLD, 1, dash="3,3")
d.text(665, 842, "POPULATION validity", color=NAVY, weight="bold", size=9.5)
d.text(665, 858, "to other people — a result from undergraduates", color=GREY, size=8.5)
d.text(665, 872, "may not hold for the patients in a clinic", color=GREY, size=8.5)
d.text(665, 898, "ECOLOGICAL validity", color=NAVY, weight="bold", size=9.5)
d.text(665, 914, "to the real world — behaviour in a controlled lab", color=GREY, size=8.5)
d.text(665, 928, "may not be behaviour anywhere else", color=GREY, size=8.5)
d.text(665, 950, "tightening control raises one and lowers the other", color=GOLD, weight="bold", size=9)

d.save("naming-a-study-design-and-the-two-validities")
print("ok")
