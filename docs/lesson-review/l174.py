import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 800,
      "Coulomb's law: charges multiply, distance squares, forces add",
      "F = k|q₁||q₂|/r²  —  magnitude from the formula, direction from the signs",
      "Top left: the inverse-square curve, showing that doubling the separation cuts the force to a quarter and "
      "tripling it to a ninth, while halving the separation quadruples it. Top right: the sign rule, with like "
      "charges pushed apart and unlike charges pulled together. Middle: a worked three-charge line showing the two "
      "forces on the middle charge and their vector sum. Bottom: the equilibrium rule — between two like charges "
      "the null point lies between them, and for opposite signs it lies outside, beyond the smaller charge — plus "
      "the dielectric factor kappa that weakens every electrostatic force in water.")

# ---------------- Panel A: inverse square ----------------
d.rect(40, 112, 416, 262, BLUE, "none", rx=12, width=2)
d.text(248, 140, "Force falls off as 1/r²", color=BLUE, weight="bold", size=17)

m = d.axes(112, 172, 286, 134, "separation r (in units of r₀)", "F (fraction of F₀)",
           (0, 3.4), (0, 4.4), ticks_x=[1, 2, 3], ticks_y=[1, 2, 3, 4])
d.curve(m, [(x / 40, min(4.3, 1600.0 / (x * x))) for x in range(20, 137)], BLUE, 2.6)
for xv, yv, lab, col in [(0.5, 4.0, "half r → 4×F", RED), (1, 1, "r₀, F₀", NAVY),
                         (2, 0.25, "2r → F/4", SAGE), (3, 1 / 9, "3r → F/9", GOLD)]:
    px, py = m(xv, yv)
    d.circle(px, py, 5, col, col)
for xv, yv, lab, col, dx, dy in [(1, 1, "r₀, F₀", NAVY, 14, -10),
                                 (2, 0.25, "2r → F/4", SAGE, 10, -12),
                                 (3, 1 / 9, "3r → F/9", GOLD, -4, -14)]:
    px, py = m(xv, yv)
    d.text(px + dx, py + dy, lab, anchor="start", color=col, weight="bold", size=12)
px, py = m(0.5, 4.0)
d.text(px + 12, py + 4, "half r → 4×F", anchor="start", color=RED, weight="bold", size=12)

# ---------------- Panel B: sign rule ----------------
d.rect(472, 112, 408, 262, RED, "none", rx=12, width=2)
d.text(676, 140, "Magnitude from the formula, direction from the signs",
       color=RED, weight="bold", size=15)

d.circle(576, 196, 20, RED, FILL[RED], 2)
d.text(576, 202, "+", color=RED, weight="bold", size=22)
d.circle(776, 196, 20, RED, FILL[RED], 2)
d.text(776, 202, "+", color=RED, weight="bold", size=22)
d.arrow(552, 196, 512, 196, RED, width=2.4)
d.arrow(800, 196, 840, 196, RED, width=2.4)
d.text(676, 234, "like charges: pushed apart", color=RED, weight="bold", size=14)

d.circle(576, 286, 20, BLUE, FILL[BLUE], 2)
d.text(576, 292, "+", color=BLUE, weight="bold", size=22)
d.circle(776, 286, 20, NAVY, FILL[NAVY], 2)
d.text(776, 293, "−", color=NAVY, weight="bold", size=24)
d.arrow(600, 286, 640, 286, BLUE, width=2.4)
d.arrow(752, 286, 712, 286, NAVY, width=2.4)
d.text(676, 324, "unlike charges: pulled together", color=BLUE, weight="bold", size=14)
d.text(676, 352, "the |q| bars mean the formula never gives you a sign",
       color=GREY, size=12)

# ---------------- Panel C: worked line ----------------
d.rect(40, 394, 840, 190, SAGE, "none", rx=12, width=2)
d.text(460, 422, "Three charges on a line: find each force, then add them with signs",
       color=SAGE, weight="bold", size=16)

AX = 480
d.line(140, AX, 790, AX, GREY, 1.6)
for x, lab, sign, col, pos in [(180, "q₁ = +4 µC", "+", RED, "x = 0"),
                               (440, "q₂ = −2 µC", "−", NAVY, "x = 3 m"),
                               (700, "q₃ = +3 µC", "+", RED, "x = 6 m")]:
    d.circle(x, AX, 19, col, FILL[col], 2)
    d.text(x, AX + 7, sign, color=col, weight="bold", size=22)
    d.text(x, AX - 30, lab, color=col, weight="bold", size=13)
    d.text(x, AX + 44, pos, color=GREY, size=12)

d.arrow(420, AX + 68, 330, AX + 68, NAVY, width=2.4)
d.text(375, AX + 58, "8 mN", color=NAVY, weight="bold", size=13)
d.arrow(460, AX + 68, 528, AX + 68, BLUE, width=2.4)
d.text(494, AX + 58, "6 mN", color=BLUE, weight="bold", size=13)
d.text(640, AX + 72, "net on q₂ = 2 mN toward q₁", anchor="start",
       color=SAGE, weight="bold", size=14)

# ---------------- Panel D: equilibrium + medium ----------------
d.rect(40, 604, 416, 160, GOLD, "none", rx=12, width=2)
d.text(248, 632, "Where is the force zero?", color=GOLD, weight="bold", size=16)
d.text(248, 660, "two like charges: the null point sits BETWEEN them,",
       color=NAVY, weight="bold", size=13)
d.text(248, 680, "nearer the smaller charge", color=NAVY, weight="bold", size=13)
d.text(248, 708, "opposite signs: it sits OUTSIDE the pair,", color=NAVY, weight="bold", size=13)
d.text(248, 728, "beyond the smaller charge", color=NAVY, weight="bold", size=13)
d.text(248, 752, "the test charge's own sign never moves it", color=GREY, size=12)

d.rect(472, 604, 408, 160, BLUE, "none", rx=12, width=2)
d.text(676, 632, "The medium matters", color=BLUE, weight="bold", size=16)
d.text(676, 662, "F = k|q₁||q₂| / (κ r²)", color=NAVY, weight="bold", size=18)
d.text(676, 692, "water: κ ≈ 80, so an ion pair in solution feels a force",
       color=GREY, size=13)
d.text(676, 712, "about 80 times weaker than the same pair in vacuum",
       color=GREY, size=13)
d.text(676, 744, "buried salt bridges (κ ≈ 4–10) are far stronger than surface ones",
       color=BLUE, weight="bold", size=13)

d.save("coulomb-inverse-square-and-superposition")
print("ok")
