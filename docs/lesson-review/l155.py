import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 600,
      "Free-body diagrams: flat surface, incline, elevator",
      "Draw only the forces acting ON the object, then apply ΣF = ma in each direction",
      "Three free-body diagrams side by side. Flat surface: weight down, normal force up, applied force sideways, "
      "giving N = mg and a = F/m. Incline with tilted axes: the normal force is mg cosine theta, the component along "
      "the slope is mg sine theta, and the block slides when tangent theta exceeds the coefficient of static friction. "
      "Elevator: the scale reads the normal force, which is m times g plus a when accelerating upward, mg at rest or "
      "constant velocity, and zero in free fall. A footer shows two genuine third-law pairs and warns that the weight "
      "and normal force on a resting book are not a third-law pair.")

# ================= Panel 1: flat surface =================
d.rect(40, 112, 282, 320, BLUE, "none", rx=12, width=2)
d.text(181, 142, "Flat surface", color=BLUE, weight="bold", size=17)

d.line(72, 320, 290, 320, GREY, 2)
d.rect(146, 264, 72, 56, NAVY, FILL[NAVY], rx=6, width=2)
d.text(182, 298, "m", color=NAVY, weight="bold", size=17)

d.arrow(182, 264, 182, 180, BLUE)
d.text(192, 202, "N", anchor="start", color=BLUE, weight="bold", size=16)
d.arrow(182, 320, 182, 378, RED)
d.text(192, 360, "W = mg", anchor="start", color=RED, weight="bold", size=15)
d.arrow(218, 292, 294, 292, SAGE)
d.text(256, 282, "F", color=SAGE, weight="bold", size=16)

d.text(181, 400, "ΣF_y = 0  ⇒  N = mg", color=NAVY, weight="bold", size=15)
d.text(181, 424, "ΣF_x = F  ⇒  a = F / m", color=NAVY, weight="bold", size=15)

# ================= Panel 2: incline =================
d.rect(338, 112, 282, 320, SAGE, "none", rx=12, width=2)
d.text(479, 142, "Incline: tilt the axes", color=SAGE, weight="bold", size=17)

ax, ay = 362, 372
bx, by = 596, 372
cx, cy = 596, 252
d.path(f"M{ax} {ay} L{bx} {by} L{cx} {cy} Z", GREY, 2, FILL[GREY])

L = math.hypot(cx - ax, cy - ay)
ux, uy = (cx - ax) / L, (cy - ay) / L          # up the slope
nx, ny = -uy, ux                                # rotate +90deg
if ny > 0:                                      # make it point away from the surface
    nx, ny = -nx, -ny
th = math.degrees(math.atan2(ay - cy, cx - ax))

t = 0.60
px, py = ax + ux * L * t, ay + uy * L * t
bcx, bcy = px + nx * 11, py + ny * 11
corners = [(bcx + ux * 28 + nx * 11, bcy + uy * 28 + ny * 11),
           (bcx - ux * 28 + nx * 11, bcy - uy * 28 + ny * 11),
           (bcx - ux * 28 - nx * 11, bcy - uy * 28 - ny * 11),
           (bcx + ux * 28 - nx * 11, bcy + uy * 28 - ny * 11)]
d.path("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in corners) + " Z", NAVY, 2, FILL[NAVY])

d.arrow(bcx, bcy, bcx + nx * 62, bcy + ny * 62, BLUE)
d.text(bcx + nx * 74 - 4, bcy + ny * 74, "N", anchor="end", color=BLUE, weight="bold", size=16)
d.arrow(bcx, bcy, bcx, bcy + 72, RED)
d.text(bcx + 8, bcy + 66, "mg", anchor="start", color=RED, weight="bold", size=15)
d.arrow(bcx, bcy, bcx - ux * 56, bcy - uy * 56, GOLD, dash=True)
d.text(bcx - ux * 86 - 26, bcy - uy * 86 + 18, "mg sin θ", color=GOLD, weight="bold", size=14)

d.text(ax + 42, ay - 8, "θ", anchor="start", color=NAVY, weight="bold", size=17)

d.text(479, 400, "⊥ to slope:  N = mg cos θ", color=NAVY, weight="bold", size=15)
d.text(479, 422, "slides only when tan θ > μₛ", color=GREY, size=14)

# ================= Panel 3: elevator =================
d.rect(636, 112, 244, 320, GOLD, "none", rx=12, width=2)
d.text(758, 142, "Elevator: apparent weight", color=GOLD, weight="bold", size=17)

d.rect(722, 228, 72, 62, NAVY, FILL[NAVY], rx=6, width=2)
d.text(758, 264, "m", color=NAVY, weight="bold", size=17)
d.arrow(758, 228, 758, 172, BLUE)
d.text(768, 196, "N", anchor="start", color=BLUE, weight="bold", size=16)
d.arrow(758, 290, 758, 346, RED)
d.text(768, 328, "W = mg", anchor="start", color=RED, weight="bold", size=15)
d.line(700, 350, 816, 350, GREY, 2)

d.text(758, 378, "accelerating up:  N = m(g + a)", color=NAVY, size=14)
d.text(758, 400, "at rest or constant v:  N = mg", color=NAVY, size=14)
d.text(758, 422, "free fall:  N = 0", color=NAVY, size=14)

# ================= Footer: third-law pairs =================
d.rect(40, 452, 840, 124, RED, "none", rx=12, width=2)
d.text(460, 480, "A third-law pair acts on two different objects and is the same kind of force",
       color=RED, weight="bold", size=17)

d.rect(60, 494, 390, 42, SAGE, FILL[SAGE], rx=9, width=2)
d.text(255, 520, "Earth pulls book down  ↔  book pulls Earth up", color=NAVY, size=15)
d.rect(470, 494, 390, 42, SAGE, FILL[SAGE], rx=9, width=2)
d.text(665, 520, "table pushes book up  ↔  book pushes table down", color=NAVY, size=15)

d.text(460, 560, "W and N on a resting book are NOT a pair: same object, different kinds of force",
       color=RED, size=14)

d.save("fbd-flat-incline-elevator")
print("ok")
