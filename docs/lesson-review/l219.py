import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 910,
      "A manual that had to choose: agreement or truth",
      "DSM-III bought reliability with criteria — validity is still outstanding",
      "Top: what every DSM diagnosis is made of, and why it is built that way. Fixed symptom counts, a "
      "minimum duration, a requirement of real impairment and a list of things that must be ruled out are all "
      "there for one purpose: so that two clinicians looking at the same patient reach the same answer. Before "
      "1980 they often did not. Middle: the cost of that choice. Reliability is agreement; validity is whether "
      "the thing agreed upon is real, and the comorbidity and heterogeneity of the categories suggest the "
      "joints are not being cut cleanly — which is what the dimensional models and RDoC are responding to. "
      "Bottom: the four Ds, with the warnings attached to each, and the social weight a diagnosis carries once "
      "it is applied."
      )

# ---------------- Panel A: anatomy of a diagnosis ----------------
d.rect(40, 180, 840, 196, BLUE, "none", rx=12, width=2)
d.text(460, 208, "What every DSM entry contains — and why", color=BLUE, weight="bold", size=16)

parts = [
    ("CRITERIA", "5 of 9, 3 of 6…", "counts, not impressions", SAGE),
    ("DURATION", "2 weeks · 6 months", "excludes passing states", BLUE),
    ("IMPAIRMENT", "distress or dysfunction", "suffering is not enough alone", GOLD),
    ("EXCLUSIONS", "not a drug, not a disease,", "not another disorder", RED),
]
x = 62
for name, mid, note, col in parts:
    d.rect(x, 228, 198, 106, col, FILL[col], rx=10, width=2)
    d.text(x + 99, 254, name, color=col, weight="bold", size=13)
    d.text(x + 99, 280, mid, color=NAVY, weight="bold", size=12)
    d.text(x + 99, 306, note, color=GREY, size=11)
    x += 206

d.text(460, 358, "all of it exists to make two clinicians agree — that is the DSM-III revolution, in 1980",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel B: reliability vs validity ----------------
d.rect(40, 396, 840, 212, RED, "none", rx=12, width=2)
d.text(460, 424, "What was bought, and what was not", color=RED, weight="bold", size=16)

d.rect(70, 444, 380, 146, SAGE, FILL[SAGE], rx=10, width=2)
d.text(260, 468, "RELIABILITY — bought", color=SAGE, weight="bold", size=14)
d.text(260, 492, "do two clinicians agree?", color=NAVY, weight="bold", size=12)
d.text(260, 516, "measured with kappa, 0 to 1", color=GREY, size=11)
d.text(260, 536, "PTSD and ADHD score well", color=GREY, size=11)
d.text(260, 556, "some personality disorders do not", color=GREY, size=11)
d.text(260, 580, "agreement is not the same as truth", color=SAGE, weight="bold", size=11)

d.rect(470, 444, 380, 146, RED, FILL[RED], rx=10, width=2)
d.text(660, 468, "VALIDITY — still owed", color=RED, weight="bold", size=14)
d.text(660, 492, "is the category a real thing?", color=NAVY, weight="bold", size=12)
d.text(660, 516, "comorbidity is the rule, not the exception", color=GREY, size=11)
d.text(660, 536, "two patients, one diagnosis, one shared symptom", color=GREY, size=11)
d.text(660, 556, "no lab test confirms any of it", color=GREY, size=11)
d.text(660, 580, "hence dimensional models, and RDoC", color=RED, weight="bold", size=11)

# ---------------- Panel C: the four Ds ----------------
d.rect(40, 628, 450, 250, GOLD, "none", rx=12, width=2)
d.text(265, 656, "The four Ds, with their caveats", color=GOLD, weight="bold", size=15)

ds = [
    ("DEVIANCE", "differs from the norm", "rare is not disordered — an IQ of 160 is rare"),
    ("DISTRESS", "it hurts to live with", "not always present, as in antisocial PD"),
    ("DYSFUNCTION", "it costs you something real", "the most consistent criterion of the four"),
    ("DANGER", "risk to self or others", "the least common; raises urgency, not diagnosis"),
]
y = 676
for name, what, caveat in ds:
    d.rect(66, y, 398, 42, GOLD, FILL[GOLD], rx=8, width=1.8)
    d.text(150, y + 18, name, color=GOLD, weight="bold", size=12)
    d.text(150, y + 34, what, color=NAVY, size=10)
    d.text(330, y + 26, caveat, color=GREY, size=10)
    y += 46

d.text(265, 870, "a culturally sanctioned response to a common stressor is not a disorder",
       color=NAVY, weight="bold", size=11)

# ---------------- Panel D: labelling ----------------
d.rect(510, 628, 370, 250, GREY, "none", rx=12, width=2)
d.text(695, 656, "What a label does next", color=GREY, weight="bold", size=15)

d.rect(536, 676, 318, 92, GREY, "#e9e4da", rx=10, width=2)
d.text(695, 700, "ROSENHAN, 1973", color=NAVY, weight="bold", size=13)
d.text(695, 722, "healthy volunteers reported one word: “thud”", color=NAVY, size=11)
d.text(695, 740, "all admitted; then normal behaviour was read", color=GREY, size=11)
d.text(695, 756, "through the diagnosis — note-taking became a symptom", color=GREY, size=11)

d.text(695, 792, "public stigma · self-stigma · structural stigma", color=RED, weight="bold", size=12)
d.text(695, 812, "lowers help-seeking and adherence", color=GREY, size=11)
d.line(560, 828, 830, 828, GREY, 1, dash="3,3")
d.text(695, 848, "and yet: a name gives access to treatment,", color=SAGE, size=11)
d.text(695, 864, "accommodation, and other people who have it", color=SAGE, size=11)

d.save("dsm-anatomy-reliability-and-labelling")
print("ok")
