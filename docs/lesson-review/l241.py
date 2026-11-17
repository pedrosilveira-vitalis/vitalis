import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 946,
      "Where the gap comes from, and what each mechanism is called",
      "The headline number hides four different things, each with its own name",
      "Top: the gender pay gap decomposed. The single figure most people quote is the ratio of median earnings, "
      "and which figure you get depends on whether part-time workers are counted — so always check the measure "
      "before comparing two numbers. Underneath it sit four separable mechanisms, each named in its own right "
      "and each testable: men and women are sorted into different occupations, the work women do is paid less "
      "for comparable skill, parenthood moves the two sexes in opposite directions, and a gap survives inside "
      "the same job. Bottom left: the vertical barriers, which are about promotion rather than pay. Bottom "
      "right: the frameworks, from the social construction of gender through to minority stress."
      )

# ---------------- Panel A: decomposing the gap ----------------
d.rect(40, 180, 840, 318, NAVY, "none", rx=12, width=2)
d.text(460, 208, "One headline number, four mechanisms", color=NAVY, weight="bold", size=15)

d.rect(230, 228, 460, 62, GREY, FILL[GREY], rx=9, width=1.8)
d.text(460, 252, "CHECK THE MEASURE FIRST", color=NAVY, weight="bold", size=11)
d.text(460, 274, "full-time year-round ≠ all workers — the two give different cents-on-the-dollar",
       color=GREY, size=9.5)

mech = [("OCCUPATIONAL\nSEGREGATION", "men and women end up in\ndifferent jobs", BLUE),
        ("DEVALUATION", "work associated with women is\npaid less for comparable skill", GOLD),
        ("MOTHERHOOD PENALTY\nFATHERHOOD BONUS", "the same event moves the two\nsexes in opposite directions", RED),
        ("WITHIN-JOB GAP", "a gap survives inside the same\noccupation — so sorting is not all", SAGE)]
cx = 60
for name, note, col in mech:
    d.rect(cx, 308, 200, 124, col, FILL[col], rx=9, width=1.8)
    lines = name.split("\n")
    for j, ln in enumerate(lines):
        d.text(cx + 100, 332 + j * 14, ln, color=col, weight="bold", size=10)
    d.line(cx + 26, 362, cx + 174, 362, col, 1, dash="3,3")
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 100, 384 + j * 15, ln, color=GREY, size=9)
    cx += 205

d.text(460, 458, "the last one matters most for exam logic: if sorting explained everything,",
       color=NAVY, weight="bold", size=10)
d.text(460, 476, "the within-occupation gap would be zero — and it is not", color=NAVY, weight="bold", size=10)

# ---------------- Panel B: vertical barriers ----------------
d.rect(40, 514, 410, 414, RED, "none", rx=12, width=2)
d.text(245, 542, "Barriers to moving UP", color=RED, weight="bold", size=14)
d.text(245, 562, "these are about promotion, not pay", color=GREY, size=9.5)

bars = [("GLASS CEILING", "qualified women stop short of the top;\nthe refusal is justified in vague terms", RED),
        ("GLASS ESCALATOR", "men in nursing, teaching and social work\nrise faster than the women around them", GOLD),
        ("STICKY FLOOR", "held in the lowest-paid grades rather\nthan blocked near the top", BLUE),
        ("DOUBLE BIND", "the same assertiveness read as confidence\nin a man and aggression in a woman", SAGE)]
y = 584
for name, note, col in bars:
    d.rect(64, y, 362, 72, col, FILL[col], rx=8, width=1.8)
    d.text(245, y + 22, name, color=col, weight="bold", size=11.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(245, y + 41 + j * 14, ln, color=GREY, size=9)
    y += 80

d.text(245, 914, "all four persist after controlling for education and experience",
       color=NAVY, weight="bold", size=9.5)

# ---------------- Panel C: frameworks ----------------
d.rect(470, 514, 410, 414, BLUE, "none", rx=12, width=2)
d.text(675, 542, "The frameworks to name", color=BLUE, weight="bold", size=14)

fw = [("SEX ≠ GENDER", "chromosomes, hormones and anatomy against\nroles, identity and expression", BLUE),
      ("PERFORMATIVITY", "Butler: gender is not something one is but\nsomething repeatedly done", BLUE),
      ("PATRIARCHY", "institutional, not personal — it shows up in law,\nin firms and in norms at once", RED),
      ("INTERSECTIONALITY", "Crenshaw: the categories multiply rather than\nadd; a position neither axis explains", GOLD),
      ("MINORITY STRESS", "Meyer: LGBTQ+ health gaps come from stigma,\ndiscrimination and concealment", SAGE),
      ("MEDICALIZATION", "homosexuality left the DSM in 1973; gender\ndysphoria remains, and that is contested", GREY)]
y = 566
for name, note, col in fw:
    d.rect(494, y, 362, 56, col, FILL[col], rx=7, width=1.5)
    d.text(675, y + 20, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(675, y + 35 + j * 13, ln, color=GREY, size=8.5)
    y += 60

d.save("pay-gap-mechanisms-vertical-barriers-and-frameworks")
print("ok")
