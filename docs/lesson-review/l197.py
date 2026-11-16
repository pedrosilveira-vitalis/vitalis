import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 884,
      "Three heuristics, three biases, two kinds of stuck",
      "Most of these questions are an identification task — name the shortcut, then name the error it makes",
      "Top: the three heuristics the exam tests by name, each with the question it answers, the error it "
      "produces and the clinical form that error takes. Availability substitutes ease of recall for frequency; "
      "representativeness substitutes resemblance for probability, which is why base rates get dropped and why "
      "the conjunction fallacy appears; anchoring starts from the first number offered and never adjusts far "
      "enough. Middle: the strategies that are not shortcuts, and the distinction between means-end analysis "
      "and working backward, which are related but separate. Bottom: the two barriers that look alike and are "
      "not — functional fixedness is about what an object can be, mental set is about what a method can "
      "solve."
      )

# ---------------- Panel A: heuristics ----------------
d.rect(40, 160, 840, 244, RED, "none", rx=12, width=2)
d.text(460, 188, "The three heuristics, and the error each one makes",
       color=RED, weight="bold", size=16)

d.text(96, 216, "HEURISTIC", anchor="start", color=GREY, weight="bold", size=11)
d.text(300, 216, "SUBSTITUTES", anchor="start", color=GREY, weight="bold", size=11)
d.text(540, 216, "CLASSIC ERROR", anchor="start", color=GREY, weight="bold", size=11)
d.line(70, 226, 850, 226, GREY, 1, dash="3,3")

rows = [
    ("Availability", "ease of recall", "for frequency", "vivid or recent events", "feel more common", BLUE),
    ("Representativeness", "resemblance", "for probability", "base rates dropped;", "conjunction fallacy", RED),
    ("Anchoring", "the first number", "for a fresh estimate", "adjustment is always", "too small", GOLD),
]
y = 242
for name, s1, s2, e1, e2, col in rows:
    d.rect(70, y, 200, 40, col, FILL[col], rx=7, width=2)
    d.text(170, y + 25, name, color=col, weight="bold", size=13)
    d.text(300, y + 18, s1, anchor="start", color=NAVY, weight="bold", size=12)
    d.text(300, y + 34, s2, anchor="start", color=GREY, size=11)
    d.text(540, y + 18, e1, anchor="start", color=NAVY, size=12)
    d.text(540, y + 34, e2, anchor="start", color=NAVY, size=12)
    y += 46

d.text(460, 392, "in a clinic: recently seen → overdiagnosed · looks typical → base rate ignored "
                 "· first impression → premature closure",
       color=GREY, size=11)

# ---------------- Panel B: strategies ----------------
d.rect(40, 412, 840, 212, BLUE, "none", rx=12, width=2)
d.text(460, 440, "The strategies that are not shortcuts", color=BLUE, weight="bold", size=16)

cards = [
    ("ALGORITHM", "every step, every time", "guarantees the answer;", "may take forever", SAGE),
    ("MEANS–END ANALYSIS", "shrink the gap", "set subgoals that reduce", "current-to-goal distance", BLUE),
    ("WORKING BACKWARD", "start at the goal", "ask what must be true", "just before it — a separate heuristic", GOLD),
    ("ANALOGY", "borrow a structure", "needs deep similarity,", "not surface similarity", RED),
]
x = 66
for title, sub, l1, l2, col in cards:
    d.rect(x, 462, 192, 118, col, FILL[col], rx=10, width=2)
    d.text(x + 96, 488, title, color=col, weight="bold", size=12)
    d.text(x + 96, 510, sub, color=NAVY, weight="bold", size=12)
    d.text(x + 96, 536, l1, color=GREY, size=11)
    d.text(x + 96, 554, l2, color=GREY, size=11)
    x += 198

d.text(460, 604, "insight is none of these: impasse, incubation, then the representation itself changes",
       color=NAVY, weight="bold", size=13)

# ---------------- Panel C: the two barriers ----------------
d.rect(40, 640, 840, 212, GOLD, "none", rx=12, width=2)
d.text(460, 668, "The two barriers students confuse", color=GOLD, weight="bold", size=16)

d.rect(70, 688, 380, 142, RED, FILL[RED], rx=10, width=2)
d.text(260, 714, "FUNCTIONAL FIXEDNESS", color=RED, weight="bold", size=14)
d.text(260, 738, "stuck on what an OBJECT is for", color=NAVY, weight="bold", size=12)
d.text(260, 764, "Duncker's candle: the tack box is", color=GREY, size=11)
d.text(260, 782, "a container, never a shelf", color=GREY, size=11)
d.text(260, 808, "worse when the object is shown in use", color=RED, size=11)

d.rect(470, 688, 380, 142, BLUE, FILL[BLUE], rx=10, width=2)
d.text(660, 714, "MENTAL SET · EINSTELLUNG", color=BLUE, weight="bold", size=14)
d.text(660, 738, "stuck on what a METHOD solves", color=NAVY, weight="bold", size=12)
d.text(660, 764, "Luchins' jars: keep using B − A − 2C", color=GREY, size=11)
d.text(660, 782, "when A − C would do", color=GREY, size=11)
d.text(660, 808, "the old strategy still works — just badly", color=BLUE, size=11)

d.save("heuristics-biases-and-the-two-barriers")
print("ok")
