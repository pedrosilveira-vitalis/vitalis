import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1004,
      "What makes a variable a confound",
      "Not every nuisance is a confound — only the ones that travel with the IV",
      "Top: the test that decides it. A variable outside the manipulation has to do two things at once to be a "
      "confound: affect the outcome AND vary with the group. Hold it constant across groups and it is merely "
      "extraneous; it adds noise and costs power, but it cannot create a false result. Let it track the "
      "independent variable and it becomes a rival explanation for the finding, which is what internal "
      "validity means. Middle: the four defences, and what each one actually buys. Bottom: the blinding "
      "ladder, with the specific bias each level removes — passages routinely describe one level and ask "
      "which bias remains."
      )

# ---------------- Panel A: the two-part test ----------------
d.rect(40, 180, 840, 274, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The two-part test", color=NAVY, weight="bold", size=15)

d.rect(300, 228, 320, 44, GREY, FILL[GREY], rx=9, width=1.8)
d.text(460, 254, "a variable you did not manipulate", color=NAVY, weight="bold", size=11)

d.arrow(460, 274, 460, 298, GREY)

d.rect(270, 302, 380, 40, NAVY, FILL[NAVY], rx=8, width=1.6)
d.text(460, 327, "does it affect the DEPENDENT variable?", color=NAVY, weight="bold", size=10.5)

d.arrow(370, 344, 250, 374, GREY, label="no", width=1.4, lx=-12, ly=-6)
d.arrow(550, 344, 640, 374, NAVY, label="yes", width=1.4, lx=14, ly=-6)

d.rect(72, 378, 300, 54, GREY, FILL[GREY], rx=8, width=1.6)
d.text(222, 400, "IRRELEVANT", color=GREY, weight="bold", size=10.5)
d.text(222, 418, "ignore it", color=GREY, size=9)

d.rect(496, 378, 380, 40, NAVY, FILL[NAVY], rx=8, width=1.6)
d.text(686, 403, "does it VARY WITH the independent variable?", color=NAVY, weight="bold", size=10)

d.text(460, 466, " ", color=NAVY, size=9)

# second-level outcomes
d.rect(40, 470, 410, 116, SAGE, "none", rx=12, width=2)
d.text(245, 496, "NO — held constant across groups", color=SAGE, weight="bold", size=11.5)
d.text(245, 518, "EXTRANEOUS / NUISANCE VARIABLE", color=NAVY, weight="bold", size=10.5)
d.text(245, 538, "adds random noise, widens the spread,", color=GREY, size=9)
d.text(245, 554, "costs statistical power — but it pushes", color=GREY, size=9)
d.text(245, 570, "neither group's result in either direction", color=GREY, size=9)

d.rect(470, 470, 410, 116, RED, "none", rx=12, width=2)
d.text(675, 496, "YES — it tracks the groups", color=RED, weight="bold", size=11.5)
d.text(675, 518, "CONFOUNDING VARIABLE", color=RED, weight="bold", size=10.5)
d.text(675, 538, "a rival explanation for the finding: the", color=GREY, size=9)
d.text(675, 554, "difference may be its doing, not the IV's.", color=GREY, size=9)
d.text(675, 570, "This is the threat to INTERNAL VALIDITY", color=GREY, size=9)

# ---------------- Panel B: the four defences ----------------
d.rect(40, 602, 840, 180, GOLD, "none", rx=12, width=2)
d.text(460, 630, "Four defences, and what each buys", color=GOLD, weight="bold", size=14)

defs = [("RANDOM ASSIGNMENT", "balances KNOWN and", "UNKNOWN confounds", "the only one that\nhandles the unknown", SAGE),
        ("HOLDING CONSTANT", "same room, same time,", "same instructions", "turns a confound into\nan extraneous variable", BLUE),
        ("MATCHING / STRATIFYING", "balance one named", "variable on purpose", "protects against bad\nluck in small samples", GOLD),
        ("COUNTERBALANCING", "vary the ORDER of", "conditions", "for within-subjects\norder effects only", NAVY)]
cx = 60
for name, l1, l2, note, col in defs:
    d.rect(cx, 648, 200, 118, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 100, 670, name, color=col, weight="bold", size=9.5)
    d.text(cx + 100, 690, l1, color=NAVY, size=8.5)
    d.text(cx + 100, 704, l2, color=NAVY, size=8.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 100, 728 + j * 14, ln, color=GREY, size=8.5)
    cx += 205

# ---------------- Panel C: the blinding ladder ----------------
d.rect(40, 798, 840, 184, BLUE, "none", rx=12, width=2)
d.text(460, 826, "The blinding ladder: which bias each rung removes", color=BLUE, weight="bold", size=14)

rungs = [("NONE", "everyone knows", "placebo effect, demand characteristics,\nexperimenter bias all live here", RED),
         ("SINGLE-BLIND", "participants do not know", "removes the PLACEBO EFFECT and\nDEMAND CHARACTERISTICS", GOLD),
         ("DOUBLE-BLIND", "participants and the staff\nwho treat and assess", "adds EXPERIMENTER / OBSERVER BIAS —\nthe standard for a drug trial", SAGE),
         ("TRIPLE-BLIND", "the data analysts too", "guards against selective analysis\nand framing of the results", BLUE)]
y = 846
for name, who, buys, col in rungs:
    d.rect(60, y, 800, 30, col, FILL[col], rx=6, width=1.4)
    d.text(150, y + 19, name, color=col, weight="bold", size=10)
    who_lines = who.split("\n")
    d.text(330, y + 19 if len(who_lines) == 1 else y + 13, who_lines[0], color=NAVY, size=8.5)
    if len(who_lines) > 1:
        d.text(330, y + 25, who_lines[1], color=NAVY, size=8.5)
    buys_lines = buys.split("\n")
    d.text(660, y + 13, buys_lines[0], color=GREY, size=8.5)
    d.text(660, y + 25, buys_lines[1], color=GREY, size=8.5)
    y += 33

d.save("what-makes-a-variable-a-confound")
print("ok")
