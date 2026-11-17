import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 964,
      "Addiction is a shift in what the drug is for",
      "From chasing the high to escaping its absence — and the circuit changes with it",
      "Top: the opponent-process arc. Early on the drug is taken for the A process, the pleasure, and the "
      "behaviour is positively reinforced. With repetition the A process shrinks through tolerance while the B "
      "process, the compensatory dysphoria, grows and outlasts it. The motive flips to negative reinforcement: "
      "using to stop feeling bad. Bottom left: where that happens anatomically — the ventral tegmental area to "
      "nucleus accumbens pathway that every drug of abuse converges on, the amygdala and hippocampus that attach "
      "cues to it, and the migration of control from prefrontal cortex to dorsal striatum that turns a choice "
      "into a habit. Bottom right: the two adaptations that make up tolerance, and the diagnostic rule that "
      "keeps a medical patient from being mislabelled."
      )

# ---------------- Panel A: opponent process ----------------
d.rect(40, 180, 840, 318, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Opponent process · the same drug, two different jobs", color=NAVY, weight="bold", size=15)

m = d.axes(110, 240, 700, 160, "", "", (0, 10), (-1.1, 1.1), ticks_x=0, ticks_y=0)
d.line(110, 320, 810, 320, GREY, 1.2, dash="4,3")
d.text(100, 324, "0", anchor="end", color=GREY, size=9)

import math
early_a = [(x, 0.95 * math.exp(-((x - 1.2) ** 2) / 0.6)) for x in [i / 20 for i in range(0, 81)]]
early_b = [(x, -0.35 * math.exp(-((x - 2.6) ** 2) / 2.4)) for x in [i / 20 for i in range(0, 81)]]
d.curve(m, early_a, RED, 2.4)
d.curve(m, early_b, BLUE, 2.4)
d.text(312, 266, "A · the high", color=RED, weight="bold", size=11)
d.text(248, 370, "B · the rebound", color=BLUE, weight="bold", size=11)
d.text(215, 412, "EARLY USE", color=NAVY, weight="bold", size=12)
d.text(215, 430, "big A, small B — positive reinforcement", color=GREY, size=10)

late_a = [(x, 0.3 * math.exp(-((x - 6.2) ** 2) / 0.6)) for x in [i / 20 for i in range(100, 201)]]
late_b = [(x, -0.85 * math.exp(-((x - 8.0) ** 2) / 4.0)) for x in [i / 20 for i in range(100, 201)]]
d.curve(m, late_a, RED, 2.4)
d.curve(m, late_b, BLUE, 2.4)
d.text(600, 296, "A shrinks", color=RED, weight="bold", size=11)
d.text(752, 346, "B grows and lasts", color=BLUE, weight="bold", size=11)
d.text(655, 412, "AFTER CHRONIC USE", color=NAVY, weight="bold", size=12)
d.text(655, 430, "small A, big B — negative reinforcement", color=GREY, size=10)

d.text(460, 466, "the person now uses to stop feeling bad, not to feel good",
       color=NAVY, weight="bold", size=12)
d.text(460, 486, "withdrawal is always roughly the opposite of the drug's own effect", color=GREY, size=10)

# ---------------- Panel B: circuit ----------------
d.rect(40, 514, 410, 428, RED, "none", rx=12, width=2)
d.text(245, 542, "Where it happens", color=RED, weight="bold", size=15)

d.rect(78, 566, 150, 52, RED, FILL[RED], rx=8, width=1.8)
d.text(153, 590, "VTA", color=RED, weight="bold", size=13)
d.text(153, 608, "dopamine source", color=GREY, size=9)
d.arrow(232, 592, 268, 592, RED)
d.rect(272, 566, 150, 52, RED, FILL[RED], rx=8, width=1.8)
d.text(347, 590, "N. ACCUMBENS", color=RED, weight="bold", size=11.5)
d.text(347, 608, "ventral striatum", color=GREY, size=9)
d.text(245, 638, "every drug of abuse ends up raising dopamine here", color=NAVY, weight="bold", size=10)
d.text(245, 656, "far above anything food or sex produces", color=GREY, size=9.5)

d.rect(78, 674, 344, 54, GOLD, FILL[GOLD], rx=8, width=1.8)
d.text(250, 696, "AMYGDALA + HIPPOCAMPUS", color=GOLD, weight="bold", size=11.5)
d.text(250, 714, "attach places, people and paraphernalia to the drug → cue-induced craving", color=GREY, size=9)

d.rect(78, 742, 344, 54, BLUE, FILL[BLUE], rx=8, width=1.8)
d.text(250, 764, "PREFRONTAL CORTEX", color=BLUE, weight="bold", size=11.5)
d.text(250, 782, "weakens: the brake on using despite consequences", color=GREY, size=9)

d.arrow(250, 800, 250, 826, NAVY, label="control migrates", lx=74, ly=0, label_size=9)

d.rect(78, 832, 344, 54, NAVY, FILL[NAVY], rx=8, width=2)
d.text(250, 854, "DORSAL STRIATUM", color=NAVY, weight="bold", size=11.5)
d.text(250, 872, "goal-directed choice becomes automatic habit", color=GREY, size=9)

d.text(245, 912, "which is why insight alone does not stop it", color=RED, weight="bold", size=11)

# ---------------- Panel C: tolerance + rule ----------------
d.rect(470, 514, 410, 428, SAGE, "none", rx=12, width=2)
d.text(675, 542, "Two kinds of tolerance", color=SAGE, weight="bold", size=15)

tol = [("PHARMACOKINETIC", "the liver gets faster",
        "CYP450 induction — alcohol induces CYP2E1,\nso less drug reaches the brain per dose", GOLD),
       ("PHARMACODYNAMIC", "the receptors adapt",
        "downregulation, desensitisation, and in opioids\nupregulated adenylyl cyclase — the cell fights back", BLUE),
       ("BEHAVIOURAL", "the setting learns too",
        "tolerance is partly conditioned to the usual place;\nusing somewhere new is how people overdose", RED)]
y = 566
for name, tag, note, col in tol:
    d.rect(494, y, 362, 78, col, FILL[col], rx=8, width=1.8)
    d.text(675, y + 20, name, color=col, weight="bold", size=11.5)
    d.text(675, y + 38, tag, color=NAVY, size=10)
    for j, ln in enumerate(note.split("\n")):
        d.text(675, y + 56 + j * 13, ln, color=GREY, size=9)
    y += 86

d.rect(494, 828, 362, 100, NAVY, FILL[NAVY], rx=10, width=2.4)
d.text(675, 852, "AND THE RULE THAT PROTECTS PATIENTS", color=NAVY, weight="bold", size=10.5)
for j, ln in enumerate(["Tolerance and withdrawal do NOT count toward",
                        "a substance use disorder when the drug is taken",
                        "solely under appropriate medical supervision.",
                        "Physical dependence is not addiction."]):
    d.text(675, 872 + j * 15, ln, color=NAVY if j == 3 else GREY,
           weight="bold" if j == 3 else "normal", size=9.5)

d.save("opponent-process-reward-circuit-and-tolerance")
print("ok")
