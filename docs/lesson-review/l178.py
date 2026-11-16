import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 836,
      "Series shares the current; parallel shares the voltage",
      "Everything else — which resistor drops more volts, which one gets hot — follows from that",
      "Top left: a series loop in which one current passes through both resistors, so the resistances add and the "
      "larger resistor takes the larger share of the voltage and dissipates the more power. Top right: a parallel "
      "pair across the same battery, where the voltage is common, the currents add, the equivalent resistance is "
      "smaller than either branch, and the smaller resistor now dissipates the more power. Middle: the worked "
      "twelve volt circuit with six ohms in series with four and twelve ohms in parallel, reduced step by step to "
      "an equivalent of nine ohms, a total current of one and a third amps, four volts across the parallel pair, "
      "and sixteen watts in total. Bottom: the two Kirchhoff rules as conservation of charge at a junction and "
      "conservation of energy around a loop.")

# ---------------- Panel A: series ----------------
d.rect(40, 126, 404, 268, BLUE, "none", rx=12, width=2)
d.text(242, 154, "Series: one current, shared voltage", color=BLUE, weight="bold", size=15)

d.rect(90, 190, 300, 130, GREY, "none", rx=0, width=2)
d.rect(150, 182, 56, 17, BLUE, FILL[BLUE], rx=3, width=2)
d.rect(274, 182, 56, 17, BLUE, FILL[BLUE], rx=3, width=2)
d.text(178, 174, "R₁", color=BLUE, weight="bold", size=13)
d.text(302, 174, "R₂", color=BLUE, weight="bold", size=13)
d.line(76, 236, 104, 236, NAVY, 3)
d.line(82, 246, 98, 246, NAVY, 1.6)
d.text(66, 240, "ε", anchor="end", color=NAVY, weight="bold", size=16)
d.arrow(200, 338, 280, 338, BLUE, width=2)
d.text(242, 362, "the same I everywhere", color=BLUE, weight="bold", size=13)

d.text(242, 276, "R = R₁ + R₂", color=NAVY, weight="bold", size=17)
d.text(242, 302, "Vᵢ = IRᵢ • P = I²R", color=NAVY, weight="bold", size=14)
d.text(242, 384, "the BIGGER resistor gets more volts and more watts",
       color=GREY, size=13)

# ---------------- Panel B: parallel ----------------
d.rect(460, 126, 420, 268, RED, "none", rx=12, width=2)
d.text(670, 154, "Parallel: one voltage, shared current", color=RED, weight="bold", size=15)

d.rect(530, 184, 280, 102, GREY, "none", rx=0, width=2)
d.line(670, 184, 670, 286, GREY, 2)
d.rect(642, 212, 56, 17, RED, FILL[RED], rx=3, width=2)
d.rect(782, 212, 56, 17, RED, FILL[RED], rx=3, width=2)
d.text(670, 204, "R₁", color=RED, weight="bold", size=13)
d.text(810, 204, "R₂", color=RED, weight="bold", size=13)
d.line(516, 230, 544, 230, NAVY, 3)
d.line(522, 240, 538, 240, NAVY, 1.6)
d.text(506, 234, "ε", anchor="end", color=NAVY, weight="bold", size=16)

d.text(670, 314, "1/R = 1/R₁ + 1/R₂", color=NAVY, weight="bold", size=17)
d.text(670, 340, "Iᵢ = V/Rᵢ • P = V²/R", color=NAVY, weight="bold", size=14)
d.text(670, 364, "R is always SMALLER than either branch", color=RED, weight="bold", size=14)
d.text(670, 384, "now the SMALLER resistor gets more current and more watts",
       color=GREY, size=13)

# ---------------- Panel C: worked reduction ----------------
d.rect(40, 412, 840, 228, SAGE, "none", rx=12, width=2)
d.text(460, 440, "Reduce, solve, then work backwards", color=SAGE, weight="bold", size=16)

steps = [("12 V across", "6 Ω  +  (4 Ω ∥ 12 Ω)"),
         ("4 ∥ 12", "= 48/16 = 3 Ω"),
         ("total", "6 + 3 = 9 Ω"),
         ("I from the battery", "12/9 = 1.33 A")]
y = 474
for a, b in steps:
    d.text(300, y, a, anchor="end", color=GREY, size=14)
    d.text(320, y, b, anchor="start", color=NAVY, weight="bold", size=15)
    y += 28

d.rect(560, 460, 296, 160, SAGE, FILL[SAGE], rx=10, width=2)
d.text(708, 484, "back-substitute", color=SAGE, weight="bold", size=14)
d.text(708, 508, "V across the pair = 1.33 × 3 = 4 V", color=NAVY, weight="bold", size=13)
d.text(708, 532, "I₄ = 4/4 = 1 A   •   I₁₂ = 4/12 = 0.33 A", color=NAVY, weight="bold", size=13)
d.text(708, 558, "they add back to 1.33 A", color=GREY, size=13)
d.text(708, 588, "P total = εI = 12 × 1.33 = 16 W", color=SAGE, weight="bold", size=14)
d.text(708, 610, "always check the currents at the junction", color=GREY, size=12)

# ---------------- Panel D: Kirchhoff ----------------
d.rect(40, 658, 404, 158, GOLD, "none", rx=12, width=2)
d.text(242, 686, "Junction rule = charge is conserved", color=GOLD, weight="bold", size=15)
JX, JY = 242, 744
d.circle(JX, JY, 7, NAVY, NAVY)
d.arrow(150, 720, JX - 10, JY - 4, BLUE, width=2)
d.arrow(150, 772, JX - 10, JY + 6, BLUE, width=2)
d.arrow(JX + 10, JY - 4, 338, 720, RED, width=2)
d.arrow(JX + 10, JY + 6, 338, 772, RED, width=2)
d.text(140, 714, "3 A", anchor="end", color=BLUE, weight="bold", size=14)
d.text(140, 782, "5 A", anchor="end", color=BLUE, weight="bold", size=14)
d.text(348, 714, "I₃", anchor="start", color=RED, weight="bold", size=14)
d.text(348, 782, "2 A", anchor="start", color=RED, weight="bold", size=14)
d.text(242, 806, "in = out, so I₃ = 8 − 2 = 6 A", color=NAVY, weight="bold", size=14)

d.rect(466, 658, 414, 158, BLUE, "none", rx=12, width=2)
d.text(673, 686, "Loop rule = energy is conserved", color=BLUE, weight="bold", size=15)
d.text(673, 716, "ΣΔV = 0 around any closed loop", color=NAVY, weight="bold", size=16)
d.text(673, 744, "rises across the battery must equal", color=GREY, size=13)
d.text(673, 764, "the IR drops around the rest of the loop", color=GREY, size=13)
d.text(673, 794, "a negative answer just means your assumed", color=GREY, size=12)
d.text(673, 812, "current direction was backwards", color=GREY, size=12)

d.save("series-parallel-and-kirchhoff")
print("ok")
