import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 972,
      "Two reasons to go along, and what each leaves behind",
      "One changes what you say; the other changes what you believe",
      "Top: normative and informational influence side by side, with the two experiments that isolate them. "
      "Asch's lines were unambiguous — participants could see the right answer and said the wrong one anyway, "
      "which is normative influence and leaves private belief intact. Sherif's moving dot was genuinely "
      "ambiguous — participants had nothing to go on but each other, which is informational influence and the "
      "group norm stayed with them when they were later tested alone. Middle: Asch's variations, each one "
      "isolating a single factor, with the ally result that matters most. Bottom: the levels of change, and the "
      "two phenomena at the far ends — a consistent minority that converts the majority, and a cohesive group "
      "that talks itself into a bad decision."
      )

# ---------------- Panel A: NSI vs ISI ----------------
d.rect(40, 180, 840, 272, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Why people go along", color=NAVY, weight="bold", size=15)

d.rect(70, 228, 390, 206, RED, FILL[RED], rx=10, width=2)
d.text(265, 254, "NORMATIVE", color=RED, weight="bold", size=14)
d.text(265, 274, "“I want to belong”", color=NAVY, weight="bold", size=11)
d.line(110, 288, 420, 288, RED, 1, dash="3,3")
for j, ln in enumerate(["the situation is CLEAR — you know the answer",
                        "you say the group's answer anyway",
                        "public compliance, private belief UNCHANGED",
                        "needs an audience: anonymity kills it"]):
    d.text(265, 310 + j * 20, ln, color=NAVY if j == 2 else GREY,
           weight="bold" if j == 2 else "normal", size=10)
d.rect(130, 396, 270, 26, RED, "none", rx=6, width=1.6)
d.text(265, 414, "ASCH · the lines", color=RED, weight="bold", size=11)

d.rect(460, 228, 390, 206, BLUE, FILL[BLUE], rx=10, width=2)
d.text(655, 254, "INFORMATIONAL", color=BLUE, weight="bold", size=14)
d.text(655, 274, "“they probably know better”", color=NAVY, weight="bold", size=11)
d.line(500, 288, 810, 288, BLUE, 1, dash="3,3")
for j, ln in enumerate(["the situation is AMBIGUOUS — you don't know",
                        "you use the group as evidence",
                        "private acceptance: the belief CHANGES",
                        "survives being alone afterwards"]):
    d.text(655, 310 + j * 20, ln, color=NAVY if j == 2 else GREY,
           weight="bold" if j == 2 else "normal", size=10)
d.rect(520, 396, 270, 26, BLUE, "none", rx=6, width=1.6)
d.text(655, 414, "SHERIF · the moving dot", color=BLUE, weight="bold", size=11)

# ---------------- Panel B: Asch variations ----------------
d.rect(40, 468, 840, 230, GOLD, "none", rx=12, width=2)
d.text(460, 496, "What Asch changed, and what happened", color=GOLD, weight="bold", size=15)

d.text(460, 520, "baseline: about 32% of critical trials conformed; 75% conformed at least once; 25% never did",
       color=NAVY, weight="bold", size=10.5)

vars_ = [("GROUP SIZE", "1 → 3 or 4", "conformity climbs, then flattens;\nfifteen is no worse than four", GOLD),
         ("ONE ALLY", "unanimity broken", "32% → about 5%\nthe ally need not even be right", SAGE),
         ("WRITE IT DOWN", "no audience", "conformity falls sharply —\nthe normative motive evaporates", BLUE),
         ("HARDER LINES", "task made ambiguous", "conformity RISES — now it is\ninformational, not normative", RED)]
cx = 60
for name, change, result, col in vars_:
    d.rect(cx, 540, 200, 142, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 100, 564, name, color=col, weight="bold", size=11)
    d.rect(cx + 24, 574, 152, 24, col, "none", rx=5, width=1.4)
    d.text(cx + 100, 591, change, color=col, weight="bold", size=9.5)
    for j, ln in enumerate(result.split("\n")):
        d.text(cx + 100, 620 + j * 15, ln, color=NAVY, size=9.5)
    cx += 205

# ---------------- Panel C: levels ----------------
d.rect(40, 714, 410, 238, SAGE, "none", rx=12, width=2)
d.text(245, 742, "How deep did the change go?", color=SAGE, weight="bold", size=14)

lv = [("COMPLIANCE", "goes along in public, disagrees in private;\nstops when the group stops watching", GOLD),
      ("IDENTIFICATION", "adopts it to keep a valued relationship;\nlasts as long as the relationship does", BLUE),
      ("INTERNALISATION", "genuinely believes it now;\npersists with no group present at all", SAGE)]
y = 762
for name, note, col in lv:
    d.rect(64, y, 362, 58, col, FILL[col], rx=8, width=1.6)
    d.text(245, y + 21, name, color=col, weight="bold", size=11)
    for j, ln in enumerate(note.split("\n")):
        d.text(245, y + 37 + j * 13, ln, color=GREY, size=9)
    y += 62

# ---------------- Panel D: the two extremes ----------------
d.rect(470, 714, 410, 238, RED, "none", rx=12, width=2)
d.text(675, 742, "Two things at the edges", color=RED, weight="bold", size=14)

d.rect(494, 762, 362, 86, BLUE, FILL[BLUE], rx=9, width=2)
d.text(675, 784, "MINORITY INFLUENCE", color=BLUE, weight="bold", size=12)
d.text(675, 802, "a small group that stays CONSISTENT", color=NAVY, weight="bold", size=10)
d.text(675, 820, "makes the majority think harder, so it produces", color=GREY, size=9)
d.text(675, 836, "conversion — real private change, not compliance", color=GREY, size=9)

d.rect(494, 858, 362, 86, RED, FILL[RED], rx=9, width=2)
d.text(675, 880, "GROUPTHINK", color=RED, weight="bold", size=12)
d.text(675, 898, "cohesion beats accuracy", color=NAVY, weight="bold", size=10)
d.text(675, 916, "self-censorship, illusion of unanimity, mindguards;", color=GREY, size=9)
d.text(675, 932, "the fix is structured dissent, not better intentions", color=GREY, size=9)

d.save("normative-versus-informational-asch-variations-and-levels")
print("ok")
