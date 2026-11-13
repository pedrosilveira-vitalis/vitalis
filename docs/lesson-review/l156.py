import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 780,
      "Inclines and friction: resolve, then decide",
      "N is whatever the perpendicular balance requires — it equals mg only on a flat surface",
      "Left: an incline showing weight resolved into mg sine theta down the slope and mg cosine theta into the "
      "surface, with the normal force equal to mg cosine theta and friction acting up the slope. Right: a decision "
      "ladder comparing tangent theta with the coefficient of static friction, giving a stationary block with static "
      "friction equal to mg sine theta when tangent theta is at most mu_s, and a sliding block with acceleration "
      "g times sine theta minus mu_k cosine theta otherwise. Bottom: four cases showing the normal force on a flat "
      "surface, when pushed at an angle, when pulled at an angle, and on an incline.")

# ---------------- Panel A: the resolution ----------------
d.rect(40, 112, 452, 356, SAGE, "none", rx=12, width=2)
d.text(266, 142, "Resolve gravity along the tilted axes", color=SAGE, weight="bold", size=17)

ax, ay = 86, 420
bx, by = 452, 420
cx, cy = 452, 212
d.path(f"M{ax} {ay} L{bx} {by} L{cx} {cy} Z", GREY, 2, FILL[GREY])

Ln = math.hypot(cx - ax, cy - ay)
ux, uy = (cx - ax) / Ln, (cy - ay) / Ln
nx, ny = -uy, ux
if ny > 0:
    nx, ny = -nx, -ny

t = 0.50
px, py = ax + ux * Ln * t, ay + uy * Ln * t
bcx, bcy = px + nx * 14, py + ny * 14
corners = [(bcx + ux * 34 + nx * 14, bcy + uy * 34 + ny * 14),
           (bcx - ux * 34 + nx * 14, bcy - uy * 34 + ny * 14),
           (bcx - ux * 34 - nx * 14, bcy - uy * 34 - ny * 14),
           (bcx + ux * 34 - nx * 14, bcy + uy * 34 - ny * 14)]
d.path("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in corners) + " Z", NAVY, 2, FILL[NAVY])

# weight and its two components
d.arrow(bcx, bcy, bcx, bcy + 108, RED, width=3)
d.text(bcx + 10, bcy + 104, "mg", anchor="start", color=RED, weight="bold", size=16)
d.arrow(bcx, bcy, bcx - ux * 76, bcy - uy * 76, GOLD, width=3)
d.text(bcx - ux * 84 - 30, bcy - uy * 84 + 22, "mg sin θ", color=GOLD, weight="bold", size=15)
d.arrow(bcx, bcy, bcx - nx * 72, bcy - ny * 72, BLUE, width=3, dash=True)
d.text(bcx - nx * 78 + 56, bcy - ny * 78 + 14, "mg cos θ", color=BLUE, weight="bold", size=15)
# normal force and friction
d.arrow(bcx, bcy, bcx + nx * 72, bcy + ny * 72, BLUE, width=3)
d.text(bcx + nx * 84 - 6, bcy + ny * 84, "N", anchor="end", color=BLUE, weight="bold", size=17)
d.arrow(bcx, bcy, bcx + ux * 76, bcy + uy * 76, SAGE, width=3)
d.text(bcx + ux * 86 + 2, bcy + uy * 86 - 10, "f", anchor="start", color=SAGE, weight="bold", size=17)

d.text(ax + 40, ay - 12, "θ", anchor="start", color=NAVY, weight="bold", size=18)
d.text(266, 446, "⊥ balance: N = mg cos θ   •   along the slope: mg sin θ drives it down",
       color=NAVY, weight="bold", size=15)

# ---------------- Panel B: the decision ----------------
d.rect(508, 112, 372, 356, GOLD, "none", rx=12, width=2)
d.text(694, 142, "Then decide: does it slide?", color=GOLD, weight="bold", size=17)

d.rect(530, 158, 328, 58, NAVY, FILL[NAVY], rx=9, width=2)
d.text(694, 182, "mg sin θ   vs   μₛ mg cos θ", color=NAVY, weight="bold", size=16)
d.text(694, 204, "mg cancels  ⇒  compare tan θ with μₛ", color=GREY, size=14)
d.arrow(620, 216, 600, 248, NAVY)
d.arrow(768, 216, 788, 248, NAVY)

d.rect(524, 252, 170, 112, SAGE, FILL[SAGE], rx=9, width=2)
d.text(609, 278, "tan θ ≤ μₛ", color=SAGE, weight="bold", size=16)
d.text(609, 302, "stays put", color=NAVY, size=15)
d.text(609, 328, "fₛ = mg sin θ", color=NAVY, weight="bold", size=15)
d.text(609, 350, "(not μₛN)", color=GREY, size=13)

d.rect(700, 252, 170, 112, RED, FILL[RED], rx=9, width=2)
d.text(785, 278, "tan θ > μₛ", color=RED, weight="bold", size=16)
d.text(785, 302, "slides", color=NAVY, size=15)
d.text(785, 328, "a = g(sin θ", color=NAVY, weight="bold", size=15)
d.text(785, 348, "− μₖ cos θ)", color=NAVY, weight="bold", size=15)

d.text(694, 392, "θᴄ = arctan(μₛ)  is the angle of repose", color=GOLD, weight="bold", size=15)
d.text(694, 420, "a carries no m: same slope, same acceleration,", color=GREY, size=14)
d.text(694, 440, "whatever the mass", color=GREY, size=14)

# ---------------- Panel C: N is not always mg ----------------
d.text(60, 506, "The normal force is never assumed — it comes from the perpendicular balance",
       anchor="start", color=BLUE, weight="bold", size=17)

cases = [("flat surface", "N = mg", "nothing else vertical", SAGE),
         ("push at angle θ", "N = mg + F sin θ", "friction goes up", GOLD),
         ("pull at angle θ", "N = mg − F sin θ", "friction goes down", BLUE),
         ("incline θ", "N = mg cos θ", "friction goes down", RED)]
x = 40
for head, eq, note, col in cases:
    d.rect(x, 528, 200, 116, col, FILL[col], rx=10, width=2)
    d.text(x + 100, 558, head, color=col, weight="bold", size=16)
    d.text(x + 100, 592, eq, color=NAVY, weight="bold", size=16)
    d.text(x + 100, 620, note, color=GREY, size=14)
    x += 213

d.text(460, 684, "fₛ adjusts up to μₛN; fₖ = μₖN is fixed and opposes the velocity",
       color=NAVY, weight="bold", size=16)
d.text(460, 712, "Neither depends on contact area, and fₖ does not depend on speed",
       color=GREY, size=15)
d.text(460, 744, "μₖ ≤ μₛ for a given pair of surfaces", color=GREY, size=15)

d.save("incline-resolve-then-decide")
print("ok")
