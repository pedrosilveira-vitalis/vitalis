import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 900,
      "Does the person predict the act, or does the room?",
      "The answer turned out to be: ask how many acts, and how strong the room",
      "Top: the argument in sequence. Trait theory promised prediction; Mischel counted the correlations and "
      "found them stuck around 0.30, which is nine per cent of the variance; Epstein pointed out that one "
      "observation is one test item, and that averaging fourteen days of behaviour pushes the same "
      "correlations to 0.7 or 0.8; and the field settled on interaction, with Mischel himself supplying its "
      "best version. Middle: situational strength, which decides when a trait gets to show at all — traits "
      "predict in the weak room and go quiet in the strong one. Bottom left: if-then signatures, the "
      "reformulation that makes consistency compatible with varying behaviour. Bottom right: the two families "
      "of test and what each one trades away."
      )

# ---------------- Panel A: the argument ----------------
d.rect(40, 174, 840, 190, BLUE, "none", rx=12, width=2)
d.text(460, 202, "How the debate actually went", color=BLUE, weight="bold", size=16)

beats = [
    ("TRAIT THEORY", "know the person,", "predict the behaviour", GREY),
    ("MISCHEL 1968", "r ≈ 0.30 across situations", "only 9% of the variance", RED),
    ("EPSTEIN", "one act = one test item", "average 14 days → r ≈ 0.7–0.8", SAGE),
    ("INTERACTIONISM", "B = f(P × S)", "and Mischel wrote it", BLUE),
]
x = 62
for name, l1, l2, col in beats:
    d.rect(x, 222, 198, 108, col, FILL[col], rx=10, width=2)
    d.text(x + 99, 248, name, color=col, weight="bold", size=13)
    d.text(x + 99, 276, l1, color=NAVY, weight="bold", size=12)
    d.text(x + 99, 300, l2, color=GREY, size=11)
    if x < 650:
        d.arrow(x + 198, 276, x + 206, 276, GREY, width=1.8)
    x += 206

d.text(460, 350, "the fight was never traits versus situations — it was how to measure either one properly",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel B: situational strength ----------------
d.rect(40, 384, 840, 186, GOLD, "none", rx=12, width=2)
d.text(460, 412, "Situational strength decides whether a trait can show",
       color=GOLD, weight="bold", size=16)

d.rect(70, 432, 380, 122, RED, FILL[RED], rx=10, width=2)
d.text(260, 456, "STRONG SITUATION", color=RED, weight="bold", size=14)
d.text(260, 480, "clear norms · real consequences · no ambiguity", color=NAVY, size=12)
d.text(260, 504, "a job interview · a funeral · a drill", color=GREY, size=11)
d.text(260, 532, "everyone behaves the same → traits predict badly",
       color=RED, weight="bold", size=12)

d.rect(470, 432, 380, 122, SAGE, FILL[SAGE], rx=10, width=2)
d.text(660, 456, "WEAK SITUATION", color=SAGE, weight="bold", size=14)
d.text(660, 480, "ambiguous · unstructured · little pressure", color=NAVY, size=12)
d.text(660, 504, "a free afternoon · an open task · a party", color=GREY, size=11)
d.text(660, 532, "people diverge → traits predict well", color=SAGE, weight="bold", size=12)

# ---------------- Panel C: if-then ----------------
d.rect(40, 590, 420, 278, SAGE, "none", rx=12, width=2)
d.text(250, 618, "If-then signatures", color=SAGE, weight="bold", size=15)

d.text(250, 644, "the same child, two settings", color=GREY, size=11)
rows = [
    ("IF teased by peers", "THEN aggressive", RED),
    ("IF asked by an adult", "THEN cooperative", SAGE),
    ("IF the task is open-ended", "THEN persistent", BLUE),
]
y = 664
for a, b, col in rows:
    d.rect(66, y, 368, 48, col, FILL[col], rx=8, width=2)
    d.text(176, y + 29, a, color=col, weight="bold", size=12)
    d.text(330, y + 29, b, color=NAVY, weight="bold", size=12)
    y += 54

d.text(250, 836, "the behaviour varies; the PATTERN does not", color=NAVY, weight="bold", size=12)
d.text(250, 856, "that stable pattern is the personality", color=GREY, size=11)

# ---------------- Panel D: two families of test ----------------
d.rect(480, 590, 400, 278, BLUE, "none", rx=12, width=2)
d.text(680, 618, "Two families of test", color=BLUE, weight="bold", size=15)

d.rect(506, 638, 348, 106, GOLD, FILL[GOLD], rx=10, width=2)
d.text(680, 662, "PROJECTIVE · Rorschach, TAT", color=GOLD, weight="bold", size=13)
d.text(680, 684, "ambiguous stimulus, interpreted response", color=NAVY, size=11)
d.text(680, 706, "harder to fake · reaches implicit material", color=SAGE, size=11)
d.text(680, 728, "lower reliability, shakier validity", color=RED, size=11)

d.rect(506, 756, 348, 106, BLUE, FILL[BLUE], rx=10, width=2)
d.text(680, 780, "OBJECTIVE · MMPI, NEO-PI", color=BLUE, weight="bold", size=13)
d.text(680, 802, "fixed items, scored by key, no interpreter", color=NAVY, size=11)
d.text(680, 824, "reliable · researchable · strong norms", color=SAGE, size=11)
d.text(680, 846, "easy to fake — hence the MMPI's L, F and K scales", color=RED, size=11)

d.save("person-situation-debate-and-assessment")
print("ok")
