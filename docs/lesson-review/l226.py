import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 980,
      "Why the pills take weeks when the blockade is instant",
      "And the three levels any MCAT treatment passage is built from",
      "Top: the antidepressant delay, which is the most asked mechanism in this lesson. Reuptake blockade raises "
      "synaptic serotonin within hours, but the somatodendritic autoreceptors sense the rise and throttle firing "
      "back, so little reaches the forebrain. Only after those autoreceptors desensitise over weeks does firing "
      "recover on top of the blockade, and the slow plasticity changes follow. Bottom left: the four questions "
      "worth asking about any psychiatric drug class, with the answers that recur. Bottom right: the three "
      "levels of the biopsychosocial frame — passages almost always ask you to place an intervention in one of "
      "them, or to notice that a good treatment plan needs all three."
      )

# ---------------- Panel A: the delay ----------------
d.rect(40, 180, 840, 330, NAVY, "none", rx=12, width=2)
d.text(460, 208, "The antidepressant lag, in three stages", color=NAVY, weight="bold", size=15)

stages = [("DAY 1", "SERT is blocked", RED,
           ["serotonin rises in the synapse", "— and at the cell body too", "autoreceptors detect it and",
            "CUT the firing rate", "net effect at the target: small"]),
          ("WEEKS 1–3", "autoreceptors desensitise", GOLD,
           ["the 5-HT1A brake wears off", "firing recovers while the", "reuptake block stays on",
            "now serotonin actually rises", "downstream — symptoms start to lift"]),
          ("WEEKS 4–6", "the slow changes land", SAGE,
           ["postsynaptic receptors adapt", "BDNF rises", "hippocampal neurogenesis",
            "full response, if it comes", "this is why nobody stops at week 2"])]
cx = 68
for head, sub, col, lines in stages:
    d.rect(cx, 228, 262, 238, col, FILL[col], rx=10, width=2)
    d.text(cx + 131, 254, head, color=col, weight="bold", size=14)
    d.text(cx + 131, 274, sub, color=NAVY, weight="bold", size=10.5)
    d.line(cx + 40, 286, cx + 222, 286, col, 1, dash="3,3")
    for j, ln in enumerate(lines):
        d.text(cx + 131, 308 + j * 22, ln, color=NAVY if j in (3, 4) else GREY, size=10)
    cx += 276
for ax in (336, 612):
    d.arrow(ax, 347, ax + 18, 347, GREY)

d.text(460, 492, "immediate chemistry, delayed clinical effect — the gap is the autoreceptor",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel B: drug classes ----------------
d.rect(40, 526, 410, 432, BLUE, "none", rx=12, width=2)
d.text(245, 554, "Ask four things of any drug", color=BLUE, weight="bold", size=15)

rows = [("SSRI / SNRI", "block SERT ± NET", "depression, all the anxiety\ndisorders, OCD, PTSD", BLUE),
        ("TCA · MAOI", "same blockade, dirtier", "anticholinergic load;\ntyramine → hypertensive crisis", BLUE),
        ("TYPICAL ANTIPSYCH.", "D2 antagonist", "positive symptoms;\nEPS and tardive dyskinesia", RED),
        ("ATYPICAL", "D2 + 5-HT2A", "less EPS; metabolic syndrome;\nclozapine → agranulocytosis", RED),
        ("BENZODIAZEPINE", "GABA-A, more Cl⁻", "fast anxiolysis; tolerance,\ndependence, respiratory risk", GOLD),
        ("LITHIUM", "inositol, GSK-3", "bipolar; narrow window\n0.6–1.2 mEq/L, monitor levels", SAGE)]
y = 578
for name, mech, use, col in rows:
    d.rect(64, y, 362, 58, col, FILL[col], rx=7, width=1.5)
    d.text(150, y + 20, name, color=col, weight="bold", size=10.5)
    d.text(350, y + 20, mech, color=NAVY, weight="bold", size=9.5)
    for j, ln in enumerate(use.split("\n")):
        d.text(245, y + 35 + j * 12, ln, color=GREY, size=9)
    y += 62

# ---------------- Panel C: three levels ----------------
d.rect(470, 526, 410, 432, SAGE, "none", rx=12, width=2)
d.text(675, 554, "Three levels, one patient", color=SAGE, weight="bold", size=15)

levels = [("BIOLOGICAL", RED,
           "drugs, ECT, TMS, DBS\nbarrier: side effects, metabolism"),
          ("PSYCHOLOGICAL", BLUE,
           "CBT and its cousins, behavioural work,\npsychodynamic, humanistic, DBT\nbarrier: avoidance, low insight"),
          ("SOCIOCULTURAL", GOLD,
           "family, group and community work,\nculturally adapted therapy, ACT teams\nbarrier: stigma, poverty, racism, access")]
y = 578
for name, col, body in levels:
    lines = body.split("\n")
    h = 34 + len(lines) * 15
    d.rect(494, y, 362, h, col, FILL[col], rx=8, width=1.8)
    d.text(675, y + 22, name, color=col, weight="bold", size=12)
    for j, ln in enumerate(lines):
        d.text(675, y + 40 + j * 15, ln, color=GREY, size=9.5)
    y += h + 10

d.rect(494, y + 6, 362, 128, NAVY, FILL[NAVY], rx=10, width=2.2)
d.text(675, y + 30, "COMBINING THEM BEATS ANY ONE ALONE", color=NAVY, weight="bold", size=10.5)
for j, ln in enumerate(["depression — SSRI plus CBT",
                        "schizophrenia — antipsychotic, cognitive",
                        "remediation, family psychoeducation, work support",
                        "PTSD — trauma-focused CBT first, SSRI adjunct",
                        "addiction — medication, motivational work,",
                        "and the social conditions for relapse"]):
    d.text(675, y + 50 + j * 14, ln, color=GREY, size=9)

d.save("antidepressant-lag-drug-classes-and-three-levels")
print("ok")
