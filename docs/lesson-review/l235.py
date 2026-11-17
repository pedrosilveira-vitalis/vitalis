import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 946,
      "What works, what backfires, and what the fix is aimed at",
      "Changing minds is the hard route; changing the procedure is the reliable one",
      "Top: Allport's four conditions as a gate. Contact helps on average even when they are missing, but the "
      "effect is far larger when all four hold, and contact under the wrong conditions — unequal, competitive, "
      "unsanctioned — can entrench the stereotype instead. Middle: the forms contact can take, which matter "
      "because none of them requires meeting anyone. Bottom left: interventions ranked by how well the "
      "evidence holds up, from the structural fixes that remove the opportunity for bias down to the two that "
      "can rebound. Bottom right: the generalization problem, which is why a good experience with one person "
      "so often leaves the category untouched."
      )

# ---------------- Panel A: the four conditions ----------------
d.rect(40, 180, 840, 206, SAGE, "none", rx=12, width=2)
d.text(460, 208, "Allport's four conditions", color=SAGE, weight="bold", size=15)

four = [("EQUAL STATUS", "inside the contact situation —\nnot one group serving the other"),
        ("COMMON GOALS", "something neither group\nreaches on its own"),
        ("COOPERATION", "genuine interdependence,\nnot shared proximity"),
        ("INSTITUTIONAL SUPPORT", "the law, the school, the boss\nvisibly behind it")]
cx = 60
for name, note in four:
    d.rect(cx, 228, 200, 100, SAGE, FILL[SAGE], rx=9, width=1.8)
    d.text(cx + 100, 254, name, color=SAGE, weight="bold", size=10.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 100, 278 + j * 15, ln, color=GREY, size=9)
    cx += 205

d.text(460, 350, "contact helps on average without them; it helps far more with them",
       color=NAVY, weight="bold", size=11)
d.text(460, 370, "and under unequal, competitive, unsanctioned contact it can make things worse", color=GREY, size=9.5)

# ---------------- Panel B: forms of contact ----------------
d.rect(40, 402, 840, 136, BLUE, "none", rx=12, width=2)
d.text(460, 430, "And it need not be face to face", color=BLUE, weight="bold", size=14)

forms = [("DIRECT", "you meet them yourself", BLUE),
         ("EXTENDED", "you know that a friend of yours\nhas a friend in the out-group", BLUE),
         ("IMAGINED", "you simply picture a positive\nencounter in some detail", GOLD),
         ("VICARIOUS", "you watch a positive intergroup\nrelationship, including in media", GOLD)]
cx = 60
for name, note, col in forms:
    d.rect(cx, 450, 200, 72, col, FILL[col], rx=8, width=1.6)
    d.text(cx + 100, 472, name, color=col, weight="bold", size=11)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 100, 490 + j * 13, ln, color=GREY, size=8.5)
    cx += 205

# ---------------- Panel C: what works ----------------
d.rect(40, 554, 410, 374, NAVY, "none", rx=12, width=2)
d.text(245, 582, "Ranked by how well it holds up", color=NAVY, weight="bold", size=14)

work = [("CHANGE THE PROCEDURE", "blind review, standardised criteria,\nstructured interviews — removes the\nopportunity rather than the attitude", SAGE),
        ("COOPERATIVE LEARNING", "the jigsaw classroom: unique pieces,\nso nobody succeeds alone", SAGE),
        ("PERSPECTIVE-GETTING", "ask and listen; beats imagining it,\nwhich mostly projects your own view", BLUE),
        ("IMPLEMENTATION INTENTIONS", "a specific if-then plan, not a resolve\nto be fair", BLUE),
        ("IMPLICIT BIAS TRAINING", "raises awareness; little durable change\nin behaviour, and can licence it", GOLD),
        ("SUPPRESSING THE THOUGHT", "rebound — the stereotype comes back\nMORE accessible than before", RED)]
y = 600
for name, note, col in work:
    lines = note.split("\n")
    h = 24 + len(lines) * 12
    d.rect(64, y, 362, h, col, FILL[col], rx=7, width=1.5)
    d.text(245, y + 16, name, color=col, weight="bold", size=10)
    for j, ln in enumerate(lines):
        d.text(245, y + 29 + j * 12, ln, color=GREY, size=8.5)
    y += h + 4

# ---------------- Panel D: generalization ----------------
d.rect(470, 554, 410, 374, RED, "none", rx=12, width=2)
d.text(675, 582, "The generalization problem", color=RED, weight="bold", size=14)

d.rect(494, 602, 362, 56, SAGE, FILL[SAGE], rx=8, width=1.8)
d.text(675, 626, "you have a good experience", color=NAVY, weight="bold", size=11)
d.text(675, 644, "with ONE out-group member", color=GREY, size=9.5)

d.arrow(675, 662, 675, 690, GREY)

d.rect(494, 696, 170, 108, RED, FILL[RED], rx=8, width=1.8)
d.text(579, 718, "SEEN AS ATYPICAL", color=RED, weight="bold", size=10)
d.text(579, 740, "“not like the rest”", color=NAVY, size=9.5)
d.text(579, 762, "SUBTYPED", color=RED, weight="bold", size=11)
d.text(579, 784, "the category survives", color=GREY, size=9)

d.rect(686, 696, 170, 108, SAGE, FILL[SAGE], rx=8, width=1.8)
d.text(771, 718, "SEEN AS TYPICAL", color=SAGE, weight="bold", size=10)
d.text(771, 740, "a normal member", color=NAVY, size=9.5)
d.text(771, 762, "GENERALISES", color=SAGE, weight="bold", size=11)
d.text(771, 784, "the category updates", color=GREY, size=9)

d.rect(494, 816, 362, 96, NAVY, FILL[NAVY], rx=9, width=2)
d.text(675, 838, "SO THE PARADOX", color=NAVY, weight="bold", size=10.5)
for j, ln in enumerate(["the most impressive counter-example is the",
                        "easiest to dismiss; prejudice falls further when",
                        "the person is ordinary and clearly of the group"]):
    d.text(675, 858 + j * 16, ln, color=GREY, size=9)

d.save("contact-conditions-interventions-and-generalization")
print("ok")
