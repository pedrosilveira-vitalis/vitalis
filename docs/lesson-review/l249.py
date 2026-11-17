import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1006,
      "Which way does the study run?",
      "Cohort, case-control and cross-sectional differ only in where they start",
      "Top: the three observational designs drawn on a single time axis. A cohort study starts at the "
      "exposure and runs forward; a case-control study starts at the outcome and runs backward; a "
      "cross-sectional study takes one vertical slice and so has no direction at all. Everything else about "
      "them follows from that — which measure you can compute, which bias dominates, and whether you can say "
      "what came first. Middle: the signature bias of each design. Bottom: the Bradford Hill considerations, "
      "which are how observational evidence is argued up toward causation when a trial is impossible."
      )

# ---------------- Panel A: the time axis ----------------
d.rect(40, 180, 840, 320, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The same timeline, entered from three places", color=NAVY, weight="bold", size=15)

# axis
d.line(140, 460, 820, 460, GREY, 2)
d.text(140, 480, "PAST", anchor="start", color=GREY, weight="bold", size=9)
d.text(820, 480, "FUTURE", anchor="end", color=GREY, weight="bold", size=9)
for xv, lab in ((250, "exposure"), (640, "outcome")):
    d.line(xv, 452, xv, 468, GREY, 1.5)
    d.text(xv, 446, lab, color=GREY, size=8.5)

# cohort
d.rect(140, 228, 290, 62, BLUE, FILL[BLUE], rx=8, width=1.8)
d.text(285, 248, "COHORT", color=BLUE, weight="bold", size=11)
d.text(285, 266, "start at the EXPOSURE, follow forward", color=NAVY, size=8.5)
d.text(285, 282, "who develops the outcome?", color=BLUE, weight="bold", size=8.5)
d.arrow(250, 302, 640, 302, BLUE, width=2)

# case-control
d.rect(500, 316, 330, 62, RED, FILL[RED], rx=8, width=1.8)
d.text(665, 336, "CASE-CONTROL", color=RED, weight="bold", size=11)
d.text(665, 354, "start at the OUTCOME, look backward", color=NAVY, size=8.5)
d.text(665, 370, "what were they exposed to?", color=RED, weight="bold", size=8.5)
d.arrow(640, 390, 250, 390, RED, width=2)

# cross-sectional
d.line(440, 410, 440, 460, NAVY, 2.5, dash="5,3")
d.text(440, 404, "CROSS-SECTIONAL — one slice, no direction", color=NAVY, weight="bold", size=9)

# ---------------- Panel B: measure and signature bias ----------------
d.rect(40, 516, 840, 212, GOLD, "none", rx=12, width=2)
d.text(460, 544, "What each one yields, and what it suffers from", color=GOLD, weight="bold", size=14)

rows = [("COHORT", BLUE, "RELATIVE RISK\nand true INCIDENCE",
         "LOSS TO FOLLOW-UP", "if dropouts differ from stayers,\nthe remaining sample is no longer the cohort"),
        ("CASE-CONTROL", RED, "ODDS RATIO only\n(≈ RR when disease is rare)",
         "RECALL BIAS", "people who are ill search their past harder\nthan the healthy controls do"),
        ("CROSS-SECTIONAL", NAVY, "PREVALENCE\n(≈ incidence × duration)",
         "NEYMAN BIAS", "a quickly fatal or quickly cured disease is\nunder-represented: you only ever see survivors")]
y = 566
for name, col, measure, bias, note in rows:
    d.rect(60, y, 800, 48, col, FILL[col], rx=7, width=1.5)
    d.text(146, y + 27, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(measure.split("\n")):
        d.text(344, y + 19 + j * 14, ln, color=NAVY, size=8.5)
    d.text(520, y + 27, bias, color=col, weight="bold", size=9.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(718, y + 19 + j * 14, ln, color=GREY, size=8)
    y += 54

# ---------------- Panel C: Bradford Hill ----------------
d.rect(40, 744, 840, 246, SAGE, "none", rx=12, width=2)
d.text(460, 772, "Arguing from association toward causation", color=SAGE, weight="bold", size=14)
d.text(460, 792, "the Bradford Hill considerations — a checklist, never a proof", color=GREY, size=9.5)

hill = [("TEMPORALITY", "the exposure came FIRST", "the only one that is strictly required", RED),
        ("STRENGTH", "a large RR or OR", "a weak one is easier for a confounder to fake", BLUE),
        ("DOSE-RESPONSE", "more exposure, more disease", "also called a biological gradient", GOLD),
        ("CONSISTENCY", "found again elsewhere", "different populations, different designs", SAGE),
        ("PLAUSIBILITY", "a mechanism that makes sense", "and coherence with what else is known", NAVY),
        ("REVERSIBILITY", "remove it and risk falls", "the experimental hint inside observation", GREY)]
y = 810
cx = 60
for i, (name, what, note, col) in enumerate(hill):
    if i == 3:
        y = 810
        cx = 470
    d.rect(cx, y, 390, 52, col, FILL[col], rx=7, width=1.4)
    d.text(cx + 100, y + 22, name, color=col, weight="bold", size=10)
    d.text(cx + 100, y + 38, what, color=NAVY, size=8.5)
    d.text(cx + 285, y + 30, note, color=GREY, size=8)
    y += 58

d.save("three-designs-on-one-timeline-and-bradford-hill")
print("ok")
