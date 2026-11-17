import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 972,
      "Not biology, but biological in its effects",
      "Race has no genetic basis and still shows up in telomeres and birth weights",
      "Top: the chain the exam wants you to be able to run in both directions. Race is a social category, not "
      "a genetic one — there is more variation inside any racial group than between groups — yet it has been "
      "used to allocate housing, schooling, work and care for generations, and those allocations leave marks "
      "that are entirely physical. The weathering hypothesis is the hinge: chronic exposure to disadvantage "
      "and discrimination accelerates biological ageing, which is why a college-educated Black woman can have "
      "worse birth outcomes than a white woman with less schooling. Bottom left: the three levels at which "
      "racism operates, which is the single most common classification question. Bottom right: prejudice "
      "against discrimination, and where the other terms sit."
      )

# ---------------- Panel A: the chain ----------------
d.rect(40, 180, 840, 296, NAVY, "none", rx=12, width=2)
d.text(460, 208, "From a category with no biology to effects that are entirely biological",
       color=NAVY, weight="bold", size=14)

steps = [("A SOCIAL CATEGORY", "assigned by appearance,\nredrawn by law and era", GREY),
         ("USED TO ALLOCATE", "housing, schooling, work,\npolicing, credit, care", GOLD),
         ("CHRONIC STRESS", "and chronic exposure —\npollution, violence, scarcity", RED),
         ("BIOLOGY CHANGES", "allostatic load, cortisol,\nshortened telomeres", RED)]
cx = 60
for name, note, col in steps:
    d.rect(cx, 232, 192, 92, col, FILL[col], rx=9, width=1.8)
    d.text(cx + 96, 258, name, color=col, weight="bold", size=10.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(cx + 96, 280 + j * 15, ln, color=GREY, size=9)
    cx += 205
for ax in (256, 461, 666):
    d.arrow(ax, 278, ax + 10, 278, GREY, width=1.6)

d.rect(70, 340, 780, 58, SAGE, FILL[SAGE], rx=9, width=2)
d.text(460, 362, "THE EVIDENCE THAT RULES OUT A PURELY ECONOMIC EXPLANATION", color=SAGE, weight="bold", size=10.5)
d.text(460, 382, "college-educated Black women have worse birth outcomes than white women with less education",
       color=NAVY, weight="bold", size=10)

d.text(460, 424, "and the trap to avoid: a few conditions track ANCESTRY, not race", color=RED, weight="bold", size=11)
d.text(460, 444, "sickle cell trait follows malaria-endemic ancestry; Tay-Sachs follows specific founder populations",
       color=GREY, size=9.5)
d.text(460, 462, "neither makes race a biological category — using race as a proxy for genotype is a methodological error",
       color=GREY, size=9.5)

# ---------------- Panel B: three levels ----------------
d.rect(40, 492, 410, 456, RED, "none", rx=12, width=2)
d.text(245, 520, "Three levels, one question type", color=RED, weight="bold", size=14)

lv = [("INDIVIDUAL", "one person's beliefs and acts",
       "a clinician spends less time with\ncertain patients", BLUE),
      ("INSTITUTIONAL", "a policy inside one institution",
       "a rule that is neutral on its face and\nunequal in its results — no racist\nactor is required", GOLD),
      ("STRUCTURAL", "all the institutions together",
       "housing, schooling, credit, policing\nand medicine compounding across\ngenerations", RED)]
y = 544
for name, tag, note, col in lv:
    lines = note.split("\n")
    h = 48 + len(lines) * 14
    d.rect(64, y, 362, h, col, FILL[col], rx=9, width=1.8)
    d.text(245, y + 22, name, color=col, weight="bold", size=12)
    d.text(245, y + 38, tag, color=NAVY, size=9.5)
    for j, ln in enumerate(lines):
        d.text(245, y + 56 + j * 14, ln, color=GREY, size=9)
    y += h + 10

d.rect(64, y + 4, 362, 86, NAVY, FILL[NAVY], rx=9, width=2)
d.text(245, y + 26, "AND THE CONTEMPORARY FORM", color=NAVY, weight="bold", size=10)
d.text(245, y + 46, "COLOURBLIND RACISM", color=NAVY, weight="bold", size=11)
d.text(245, y + 64, "denies that race still matters and reads", color=GREY, size=9)
d.text(245, y + 78, "the resulting inequality as culture or merit", color=GREY, size=9)

# ---------------- Panel C: the vocabulary ----------------
d.rect(470, 492, 410, 456, BLUE, "none", rx=12, width=2)
d.text(675, 520, "Attitude, act, and the rest", color=BLUE, weight="bold", size=14)

d.rect(494, 542, 176, 76, GOLD, FILL[GOLD], rx=8, width=1.8)
d.text(582, 566, "PREJUDICE", color=GOLD, weight="bold", size=12)
d.text(582, 586, "an ATTITUDE", color=NAVY, weight="bold", size=10)
d.text(582, 604, "held, not acted on", color=GREY, size=9)

d.rect(680, 542, 176, 76, RED, FILL[RED], rx=8, width=1.8)
d.text(768, 566, "DISCRIMINATION", color=RED, weight="bold", size=11.5)
d.text(768, 586, "an ACT", color=NAVY, weight="bold", size=10)
d.text(768, 604, "differential treatment", color=GREY, size=9)

terms = [("IMPLICIT BIAS", "prejudice the holder is unaware of; shows\nup in timed tasks and in clinical decisions"),
         ("STEREOTYPE THREAT", "fear of confirming the stereotype,\nwhich then degrades performance"),
         ("CODE-SWITCHING", "adjusting speech and manner to fit\nthe dominant setting; it costs effort"),
         ("GLASS CEILING", "an unseen barrier to the top, justified\nin vague terms like “executive presence”"),
         ("INTERSECTIONALITY", "identities combine into positions that\nneither axis explains on its own")]
y = 634
for name, note in terms:
    d.rect(494, y, 362, 56, BLUE, FILL[BLUE], rx=7, width=1.5)
    d.text(675, y + 20, name, color=BLUE, weight="bold", size=10.5)
    for j, ln in enumerate(note.split("\n")):
        d.text(675, y + 35 + j * 13, ln, color=GREY, size=8.5)
    y += 61

d.save("race-as-social-category-levels-and-vocabulary")
print("ok")
