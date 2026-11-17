import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1018,
      "Mood episodes are sorted by duration and by damage",
      "Two axes decide the diagnosis: how long it lasted and how much it broke",
      "Top: the mood episodes laid out against duration, with the severity line that separates hypomania from "
      "mania. Four days with no marked impairment is hypomania; a week, or any length that lands the person in "
      "hospital, is mania; psychotic features during the episode make it mania whatever its length. Which "
      "episodes a person has had, not how they look today, fixes the diagnosis — which is why bipolar II so "
      "often gets called unipolar depression. Bottom left: the three biological threads, and the one observation "
      "the monoamine story alone cannot explain, the weeks-long lag before the drug works. Bottom right: the "
      "treatment lines, including the one combination that is actively dangerous."
      )

# ---------------- Panel A: episodes vs duration ----------------
d.rect(40, 180, 840, 344, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Duration, and the severity line", color=NAVY, weight="bold", size=15)

x0 = 150
scale = 86.0  # px per "unit"
ticks = [(0, "2 wk"), (1, "4 d"), (2, "1 wk"), (3, "2 yr")]

# elevated side
d.text(64, 248, "ELEVATED", anchor="start", color=RED, weight="bold", size=10)
d.rect(150, 232, 180, 30, GOLD, FILL[GOLD], rx=6, width=1.8)
d.text(240, 252, "HYPOMANIA · ≥ 4 days", color=GOLD, weight="bold", size=11)
d.rect(350, 232, 240, 30, RED, FILL[RED], rx=6, width=1.8)
d.text(470, 252, "MANIA · ≥ 7 days", color=RED, weight="bold", size=11)
d.rect(610, 232, 244, 30, RED, "none", rx=6, width=1.8)
d.text(732, 252, "…or any length, if hospitalised", color=RED, weight="bold", size=10.5)

d.text(240, 282, "no marked impairment", color=GREY, size=10)
d.text(470, 282, "marked impairment, may be psychotic", color=GREY, size=10)

d.line(96, 302, 854, 302, GREY, 1.6, dash="5,4")
d.text(475, 318, "the severity line — impairment, hospitalisation or psychosis makes it mania",
       color=NAVY, weight="bold", size=11)

# depressed side
d.text(64, 352, "DEPRESSED", anchor="start", color=BLUE, weight="bold", size=10)
d.rect(150, 336, 240, 30, BLUE, FILL[BLUE], rx=6, width=1.8)
d.text(270, 356, "MAJOR DEPRESSIVE EPISODE · ≥ 2 weeks", color=BLUE, weight="bold", size=10.5)
d.rect(410, 336, 300, 30, SAGE, FILL[SAGE], rx=6, width=1.8)
d.text(560, 356, "PERSISTENT DEPRESSIVE DISORDER · ≥ 2 years", color=SAGE, weight="bold", size=10.5)
d.text(270, 386, "5 of 9 symptoms, one of them low mood or anhedonia", color=GREY, size=10)
d.text(560, 386, "never symptom-free for 2 months at a stretch", color=GREY, size=10)

# which diagnosis
d.line(96, 406, 854, 406, GREY, 1, dash="3,3")
d.text(460, 428, "the diagnosis follows the episodes a person has EVER had", color=NAVY, weight="bold", size=12)
cards = [("BIPOLAR I", "one manic episode, ever", RED),
         ("BIPOLAR II", "hypomania + a depressive episode,\nnever mania", GOLD),
         ("MDD", "depressive episodes only", BLUE),
         ("CYCLOTHYMIA", "sub-threshold both ways, ≥ 2 years", SAGE)]
cx = 68
for name, note, col in cards:
    d.rect(cx, 444, 192, 62, col, FILL[col], rx=8, width=1.8)
    d.text(cx + 96, 466, name, color=col, weight="bold", size=11.5)
    lines = note.split("\n")
    for j, ln in enumerate(lines):
        d.text(cx + 96, 486 + j * 13 - (6 if len(lines) > 1 else 0), ln, color=GREY, size=9.5)
    cx += 200

# ---------------- Panel B: biology ----------------
d.rect(40, 540, 410, 462, BLUE, "none", rx=12, width=2)
d.text(245, 568, "Three biological threads", color=BLUE, weight="bold", size=15)

th = [("MONOAMINES", "5-HT, noradrenaline, dopamine low at the synapse.\n"
                     "Every classical antidepressant raises them.", BLUE),
      ("HPA AXIS", "cortisol high, dexamethasone fails to suppress it,\n"
                   "CRH raised — and the hippocampus shrinks.", RED),
      ("NEUROPLASTICITY", "BDNF down; antidepressants, exercise and ECT\n"
                          "all push it back up.", SAGE)]
y = 590
for name, body, col in th:
    d.rect(64, y, 362, 76, col, FILL[col], rx=8, width=1.8)
    d.text(245, y + 24, name, color=col, weight="bold", size=12)
    for j, ln in enumerate(body.split("\n")):
        d.text(245, y + 44 + j * 15, ln, color=NAVY, size=9.5)
    y += 86

d.rect(64, 852, 362, 130, GOLD, FILL[GOLD], rx=10, width=2)
d.text(245, 878, "THE AWKWARD FACT", color=GOLD, weight="bold", size=12)
for j, ln in enumerate(["Synaptic serotonin rises within hours.",
                        "The patient gets better in two to six weeks.",
                        "So the monoamine rise is the trigger, not the cure —",
                        "the slow part is receptor and plasticity change.",
                        "Ketamine skips it: NMDA block, AMPA potentiation,",
                        "BDNF release, relief in hours."]):
    d.text(245, 900 + j * 15, ln, color=NAVY, size=9.5)

# ---------------- Panel C: treatment ----------------
d.rect(470, 540, 410, 462, SAGE, "none", rx=12, width=2)
d.text(675, 568, "What is given, and why", color=SAGE, weight="bold", size=15)

tx = [("SSRI / SNRI", "first line for depression; block SERT, and NET too", BLUE),
      ("TCA", "same blockade plus H1, muscarinic, alpha — and lethal\nin overdose through cardiac sodium channels", BLUE),
      ("MAOI", "works well for atypical features; tyramine foods\nrisk hypertensive crisis", BLUE),
      ("BUPROPION", "dopamine and noradrenaline; no sexual side effects", BLUE),
      ("LITHIUM", "first line in bipolar; GSK-3β and inositol;\nnarrow window 0.6–1.2 mEq/L", RED),
      ("VALPROATE · LAMOTRIGINE", "mania; and lamotrigine for the depressed pole", RED)]
y = 590
for name, note, col in tx:
    lines = note.split("\n")
    h = 40 if len(lines) == 1 else 52
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.6)
    d.text(675, y + 18, name, color=col, weight="bold", size=11)
    for j, ln in enumerate(lines):
        d.text(675, y + 34 + j * 14, ln, color=GREY, size=9.5)
    y += h + 7

d.rect(494, y + 4, 362, 64, RED, FILL[RED], rx=10, width=2.4)
d.text(675, y + 28, "DO NOT: antidepressant alone in bipolar", color=RED, weight="bold", size=12)
d.text(675, y + 48, "it can flip the patient into mania or rapid cycling", color=NAVY, size=10)

d.save("mood-episodes-duration-biology-and-treatment")
print("ok")
