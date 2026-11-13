import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 830,
      "Torque: only the perpendicular part counts",
      "τ = F · r · sinθ = F · d⊥, and in equilibrium the clockwise and counter-clockwise totals match",
      "Left: a beam on a pivot with a force applied at an angle, showing the distance r along the beam, the "
      "perpendicular lever arm r sine theta, and the component of the force that produces no torque. Right: the three "
      "lever classes drawn with fulcrum, load and effort, with their mechanical advantages and body examples. Bottom: "
      "the biceps calculation showing a 700 newton muscle force holding a 100 newton load, the rule for choosing the "
      "axis of rotation, and the pulley rule that mechanical advantage equals the number of supporting rope segments.")

# ---------------- Panel A: torque geometry ----------------
d.rect(40, 112, 400, 316, BLUE, "none", rx=12, width=2)
d.text(240, 142, "What makes a torque", color=BLUE, weight="bold", size=17)

PX, PY = 92, 320
d.line(PX, PY, 400, PY, NAVY, 4)
d.path(f"M{PX - 14} {PY + 30} L{PX + 14} {PY + 30} L{PX} {PY} Z", GREY, 2, FILL[GREY])
d.text(PX, PY + 50, "pivot", color=GREY, size=13)

AX = 334
ang = math.radians(52)
FX, FY = AX + 86 * math.cos(ang), PY - 86 * math.sin(ang)
d.arrow(AX, PY, FX, FY, RED, width=3)
d.text(FX + 12, FY - 4, "F", anchor="start", color=RED, weight="bold", size=17)

# components of F
d.arrow(AX, PY, AX, PY - 86 * math.sin(ang), SAGE, width=2.5, dash=True)
d.text(AX - 12, PY - 28, "F sinθ", anchor="end", color=SAGE, weight="bold", size=14)
d.arrow(AX, PY, AX + 86 * math.cos(ang), PY, GREY, width=2.5, dash=True)
d.text(AX + 44, PY + 40, "F cosθ: no torque", color=GREY, size=13)

d.line(PX, PY - 64, AX, PY - 64, NAVY, 1.5, True)
d.text((PX + AX) / 2, PY - 72, "r", color=NAVY, weight="bold", size=16)
d.text(AX + 30, PY - 14, "θ", anchor="start", color=NAVY, weight="bold", size=16)

d.text(240, 382, "τ = F r sinθ = F · d⊥", color=NAVY, weight="bold", size=17)
d.text(240, 408, "θ = 90° gives the most torque; θ = 0° gives none",
       color=GREY, size=14)

# ---------------- Panel B: lever classes ----------------
d.rect(456, 112, 424, 316, SAGE, "none", rx=12, width=2)
d.text(668, 142, "The three lever classes", color=SAGE, weight="bold", size=17)


def lever(y, order, cls, ma, example, col):
    x0, x1 = 486, 700
    d.line(x0, y, x1, y, NAVY, 3)
    pos = {}
    for i, token in enumerate(order):
        pos[token] = x0 + 26 + i * 82
    fx = pos["F"]
    d.path(f"M{fx - 12} {y + 24} L{fx + 12} {y + 24} L{fx} {y} Z", GREY, 2, FILL[GREY])
    d.arrow(pos["L"], y - 36, pos["L"], y - 6, RED, width=2.5)
    d.text(pos["L"], y - 44, "load", color=RED, weight="bold", size=12)
    d.arrow(pos["E"], y - 36, pos["E"], y - 6, BLUE, width=2.5)
    d.text(pos["E"], y - 44, "effort", color=BLUE, weight="bold", size=12)
    d.text(716, y - 8, cls, anchor="start", color=col, weight="bold", size=14)
    d.text(716, y + 12, ma, anchor="start", color=NAVY, weight="bold", size=14)
    d.text(716, y + 32, example, anchor="start", color=GREY, size=12)


lever(210, "LFE", "1st class", "MA \u2277 1", "seesaw, skull on spine", NAVY)
lever(300, "FLE", "2nd class", "MA > 1", "wheelbarrow, tiptoe", SAGE)
lever(390, "FEL", "3rd class", "MA < 1", "tweezers, biceps", RED)

# ---------------- Bottom ----------------
d.rect(40, 452, 400, 176, RED, FILL[RED], rx=10, width=2)
d.text(240, 480, "Why muscles pull so hard", color=RED, weight="bold", size=17)
d.text(240, 512, "biceps inserts 5 cm from the elbow;", color=NAVY, size=15)
d.text(240, 536, "the load sits 35 cm away", color=NAVY, size=15)
d.text(240, 566, "F × 0.05 = 100 × 0.35  ⇒  F = 700 N", color=RED, weight="bold", size=16)
d.text(240, 598, "MA = 0.05/0.35 ≈ 0.14: force traded for speed", color=GREY, size=14)

d.rect(456, 452, 424, 176, GOLD, FILL[GOLD], rx=10, width=2)
d.text(668, 480, "Two habits that save the most time", color=GOLD, weight="bold", size=17)
d.text(668, 512, "1. Put the axis where the unknowns are:", color=NAVY, weight="bold", size=15)
d.text(668, 536, "a force through the axis has r = 0, so it drops out", color=GREY, size=14)
d.text(668, 566, "2. Pulley MA = supporting rope segments", color=NAVY, weight="bold", size=15)
d.text(668, 590, "one movable pulley ⇒ MA = 2; a fixed pulley only", color=GREY, size=14)
d.text(668, 612, "turns the force around", color=GREY, size=14)

d.text(460, 672, "Equilibrium needs both: ΣF = 0 and Στ = 0, about any axis you like",
       color=NAVY, weight="bold", size=16)
d.text(460, 704, "Ideal machines conserve work: a bigger MA always costs a longer pull",
       color=GREY, size=15)
d.text(460, 734, "An object tips when its centre of mass leaves the base of support",
       color=GREY, size=15)
d.text(460, 764, "On an incline: N = mg cosθ and F = mg sinθ, with MA = L/h = 1/sinθ",
       color=GREY, size=15)
d.text(460, 798, "Pick counter-clockwise as positive once, and never switch mid-problem",
       color=GREY, size=15)

d.save("torque-levers-and-equilibrium")
print("ok")
