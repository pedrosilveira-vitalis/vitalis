import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 898,
      "Two domains, two settings, one age cut-off",
      "Most of these diagnoses hinge on a threshold the vignette states outright",
      "Top: ADHD and autism side by side, in the terms the criteria actually use. ADHD needs symptoms before "
      "age twelve and in two or more settings — that second requirement is what separates a disorder from a "
      "classroom problem, and vignettes almost always say it explicitly. Autism needs both of its domains, "
      "social communication and restricted repetitive behaviour; one alone is not enough, which is what the "
      "separate diagnosis of social pragmatic communication disorder exists for. Bottom left: the cognitive "
      "profile of autism as actually measured, which is a three-way split rather than the common assumption. "
      "Bottom right: the comorbidities, which are the rule here rather than the exception, with the rates the "
      "exam quotes."
      )

# ---------------- Panel A: ADHD vs ASD ----------------
d.rect(40, 180, 840, 298, BLUE, "none", rx=12, width=2)
d.text(460, 208, "The two that get compared", color=BLUE, weight="bold", size=16)

d.rect(70, 228, 380, 232, BLUE, FILL[BLUE], rx=10, width=2)
d.text(260, 254, "ADHD", color=BLUE, weight="bold", size=16)
d.text(260, 280, "INATTENTION and/or HYPERACTIVITY-IMPULSIVITY", color=NAVY, weight="bold", size=11)
d.line(110, 292, 410, 292, BLUE, 1, dash="3,3")
for i, t in enumerate(["onset before age 12  (it was 7 in DSM-IV)",
                       "present in TWO or more settings",
                       "out of step with developmental level",
                       "real impairment, not just noise"]):
    d.text(260, 314 + i * 22, t, color=NAVY, size=11)
d.text(260, 416, "stimulants work by raising dopamine", color=GREY, size=11)
d.text(260, 434, "and noradrenaline in frontostriatal circuits", color=GREY, size=11)

d.rect(470, 228, 380, 232, SAGE, FILL[SAGE], rx=10, width=2)
d.text(660, 254, "AUTISM SPECTRUM DISORDER", color=SAGE, weight="bold", size=15)
d.text(660, 280, "BOTH domains are required", color=NAVY, weight="bold", size=11)
d.line(510, 292, 810, 292, SAGE, 1, dash="3,3")
d.text(660, 314, "A · social communication and interaction", color=NAVY, weight="bold", size=11)
d.text(660, 332, "reciprocity, nonverbal signals, relationships", color=GREY, size=10)
d.text(660, 356, "B · restricted, repetitive behaviour", color=NAVY, weight="bold", size=11)
d.text(660, 374, "stereotypies, sameness, fixated interests, sensory", color=GREY, size=10)
d.text(660, 404, "domain A alone → social pragmatic", color=SAGE, weight="bold", size=11)
d.text(660, 422, "communication disorder, not autism", color=SAGE, weight="bold", size=11)
d.text(660, 444, "severity is rated per domain, 1 to 3", color=GREY, size=10)

# ---------------- Panel B: cognitive profile ----------------
d.rect(40, 494, 420, 380, GOLD, "none", rx=12, width=2)
d.text(250, 522, "Autism and measured ability", color=GOLD, weight="bold", size=15)

bars = [("intellectual disability", "IQ ≤ 70", 37.9, RED),
        ("borderline", "IQ 71–85", 23.5, GOLD),
        ("average or above", "IQ > 85", 38.6, SAGE)]
y = 552
for name, iq, pct, col in bars:
    d.text(250, y, name, color=col, weight="bold", size=12)
    d.text(250, y + 17, iq, color=GREY, size=10)
    w = pct * 7.4
    d.rect(66, y + 28, w, 22, col, FILL[col], rx=5, width=1.8)
    d.text(74 + w, y + 44, "%.1f%%" % pct, anchor="start", color=col, weight="bold", size=12)
    y += 74

d.text(250, 790, "a three-way split, not a majority either way", color=NAVY, weight="bold", size=12)
d.text(250, 812, "CDC ADDM, 8-year-olds, 2020 surveillance", color=GREY, size=10)
d.line(80, 828, 420, 828, GREY, 1, dash="3,3")
d.text(250, 848, "prevalence about 1 in 36 · boys about 4× girls", color=NAVY, size=11)
d.text(250, 866, "girls are probably under-identified", color=GREY, size=10)

# ---------------- Panel C: comorbidity ----------------
d.rect(480, 494, 400, 380, RED, "none", rx=12, width=2)
d.text(680, 522, "Comorbidity is the rule", color=RED, weight="bold", size=15)

pairs = [
    ("ASD + ADHD", "30–50%", "DSM-5 allows both at once; DSM-IV did not", BLUE),
    ("ASD + intellectual disability", "about 38%", "rate it separately from the autism", GOLD),
    ("learning disorder + ADHD", "30–50%", "different mechanisms, same report card", SAGE),
    ("Tourette's + ADHD", "about 50%", "and about 40% with OCD", RED),
    ("anxiety + any of them", "very high", "often the reason they present at all", GREY),
]
y = 548
for name, rate, note, col in pairs:
    d.rect(506, y, 348, 56, col, FILL[col], rx=8, width=1.8)
    d.text(640, y + 22, name, color=col, weight="bold", size=11)
    d.text(810, y + 22, rate, anchor="end", color=NAVY, weight="bold", size=12)
    d.text(680, y + 42, note, color=GREY, size=10)
    y += 62

d.text(680, 866, "a child who meets two sets of criteria gets two diagnoses",
       color=NAVY, weight="bold", size=11)

d.save("adhd-autism-criteria-and-comorbidity")
print("ok")
