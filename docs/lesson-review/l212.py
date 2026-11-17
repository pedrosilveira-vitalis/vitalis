import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 898,
      "Two axes, three stages, two appraisals",
      "Whether something is a stressor is decided twice before the body commits",
      "Top: Selye's curve, which is worth seeing rather than listing. Resistance dips below normal during "
      "alarm, because the defences are still being mobilised; it climbs above normal through the resistance "
      "stage, where the organism looks fine and is quietly spending reserves; then it falls away in "
      "exhaustion. Middle: the two stress axes side by side. The sympathetic-adrenal-medullary arm fires in "
      "seconds and is the one you feel; the HPA axis takes minutes, lasts hours, and is the one that does "
      "the long-term damage when its negative feedback stops working. Bottom: Lazarus and Folkman's two "
      "appraisals, and the rule that decides which kind of coping will actually help — whether the "
      "stressor can be changed at all."
      )

# ---------------- Panel A: GAS curve ----------------
d.rect(40, 174, 840, 236, BLUE, "none", rx=12, width=2)
d.text(460, 202, "General Adaptation Syndrome", color=BLUE, weight="bold", size=16)

m = d.axes(120, 226, 700, 120, "", "resistance to the stressor",
           (0, 10), (0, 1.2), ticks_x=None, ticks_y=None)

# baseline
bx0, by0 = m(0, 0.6)
bx1, by1 = m(10, 0.6)
d.line(bx0, by0, bx1, by1, GREY, 1.4, dash="5,4")
d.text(bx1 + 6, by1 + 4, "normal", anchor="start", color=GREY, size=10)

pts = []
for i in range(0, 201):
    x = i / 20.0
    if x < 1.0:
        y = 0.6 - 0.32 * x
    elif x < 2.0:
        y = 0.28
    elif x < 6.5:
        y = 0.28 + 0.72 * min(1.0, (x - 2.0) / 1.8)
    else:
        y = 1.0 - 0.95 * ((x - 6.5) / 3.5) ** 1.6
    pts.append((x, max(0.03, y)))
d.curve(m, pts, BLUE, 3)

for cx, lab, col in [(1.0, "ALARM", RED), (4.3, "RESISTANCE", SAGE), (8.4, "EXHAUSTION", GOLD)]:
    px, py = m(cx, 0)
    d.text(px, py + 22, lab, color=col, weight="bold", size=12)
for cx in (2.0, 6.5):
    px, py0 = m(cx, 0)
    _, py1 = m(cx, 1.15)
    d.line(px, py0, px, py1, GREY, 1, dash="3,3")

px, py = m(1.45, 0.47)
d.text(px, py, "defences still", color=RED, size=10)
d.text(px, py + 13, "being mobilised", color=RED, size=10)
px, py = m(4.3, 1.12)
d.text(px, py, "looks fine, spending reserves", color=SAGE, weight="bold", size=11)
px, py = m(8.2, 0.20)
d.text(px, py, "reserves gone → illness", color=GOLD, weight="bold", size=11)

d.text(460, 394, "allostatic load is the bill for every trip round this curve", color=GREY, size=11)

# ---------------- Panel B: two axes ----------------
d.rect(40, 426, 840, 200, RED, "none", rx=12, width=2)
d.text(460, 454, "The two axes, by speed", color=RED, weight="bold", size=16)

d.rect(70, 474, 380, 134, RED, FILL[RED], rx=10, width=2)
d.text(260, 498, "SAM — seconds", color=RED, weight="bold", size=13)
d.text(260, 522, "hypothalamus → sympathetic nerves", color=NAVY, size=12)
d.text(260, 542, "→ adrenal MEDULLA → epinephrine", color=NAVY, size=12)
d.text(260, 570, "heart, airways, pupils, glucose", color=GREY, size=11)
d.text(260, 592, "this is what a fright feels like", color=RED, weight="bold", size=11)

d.rect(470, 474, 380, 134, BLUE, FILL[BLUE], rx=10, width=2)
d.text(660, 498, "HPA — minutes to hours", color=BLUE, weight="bold", size=13)
d.text(660, 522, "CRH → ACTH → adrenal CORTEX", color=NAVY, size=12)
d.text(660, 542, "→ cortisol, for hours", color=NAVY, size=12)
d.text(660, 570, "glucose up, immunity down, muscle broken down", color=GREY, size=11)
d.text(660, 592, "feedback failure here is what injures", color=BLUE, weight="bold", size=11)

# ---------------- Panel C: appraisal and coping ----------------
d.rect(40, 642, 840, 232, SAGE, "none", rx=12, width=2)
d.text(460, 670, "Appraised twice, then coped with", color=SAGE, weight="bold", size=16)

d.rect(70, 690, 236, 160, SAGE, FILL[SAGE], rx=10, width=2)
d.text(188, 714, "PRIMARY", color=SAGE, weight="bold", size=13)
d.text(188, 734, "does this matter?", color=NAVY, weight="bold", size=12)
for i, t in enumerate(["irrelevant", "benign-positive", "harm · threat · challenge"]):
    d.text(188, 762 + i * 22, t, color=GREY, size=11)
d.text(188, 834, "challenge beats threat", color=SAGE, weight="bold", size=11)

d.rect(326, 690, 236, 160, BLUE, FILL[BLUE], rx=10, width=2)
d.text(444, 714, "SECONDARY", color=BLUE, weight="bold", size=13)
d.text(444, 734, "can I handle it?", color=NAVY, weight="bold", size=12)
for i, t in enumerate(["what are my options", "do I have support", "have I done this before"]):
    d.text(444, 762 + i * 22, t, color=GREY, size=11)
d.text(444, 834, "self-efficacy lives here", color=BLUE, weight="bold", size=11)

d.rect(582, 690, 268, 160, GOLD, FILL[GOLD], rx=10, width=2)
d.text(716, 714, "WHICH COPING HELPS?", color=GOLD, weight="bold", size=13)
d.text(716, 742, "controllable → PROBLEM-focused", color=NAVY, weight="bold", size=12)
d.text(716, 762, "act on the stressor itself", color=GREY, size=11)
d.text(716, 790, "uncontrollable → EMOTION-focused", color=NAVY, weight="bold", size=12)
d.text(716, 810, "reappraise, seek support, accept", color=GREY, size=11)
d.text(716, 836, "mismatch the two and coping backfires", color=GOLD, weight="bold", size=11)

d.save("gas-curve-stress-axes-and-appraisal")
print("ok")
