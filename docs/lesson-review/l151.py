import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 620,
      "E°cell, ΔG° and K are one fact in three languages",
      "Know any one of them and the other two follow. The only thing to get right is the sign.",
      "A triangle linking standard cell potential, standard free energy change and the equilibrium "
      "constant. The edge from potential to free energy carries delta G equals minus nFE; the edge from "
      "free energy to K carries delta G equals minus RT ln K; the edge from potential back to K carries "
      "E equals 0.0592 over n times log K at 298 kelvin. A table below shows the three quantities "
      "moving together: positive potential with negative free energy and K above one is spontaneous, "
      "the reverse is not, and all three at their neutral values means equilibrium. A note records that "
      "potential is intensive while free energy is extensive.")

CX, CY, R = 450, 250, 128
pts = {}
for ang, key, label, sub, col in [(90, "E", "E°cell", "volts", BLUE),
                                  (210, "G", "ΔG°", "joules per mole", RED),
                                  (330, "K", "K", "unitless", SAGE)]:
    x = CX + R * math.cos(math.radians(ang))
    y = CY - R * math.sin(math.radians(ang))
    pts[key] = (x, y)
    d.circle(x, y, 54, col, FILL[col], 2.5)
    d.text(x, y - 2, label, color=col, weight="bold", size=22)
    d.text(x, y + 20, sub, color=GREY, size=12)

edges = [("E", "G", "ΔG° = −nFE°cell", -118, -4),
         ("G", "K", "ΔG° = −RT ln K", 0, 36),
         ("E", "K", "E°cell = (0.0592/n) log K", 122, -4)]
for a, b, label, dx, dy in edges:
    (x1, y1), (x2, y2) = pts[a], pts[b]
    ux, uy = x2 - x1, y2 - y1
    L = math.hypot(ux, uy)
    ux, uy = ux / L, uy / L
    d.line(x1 + 54 * ux, y1 + 54 * uy, x2 - 54 * ux, y2 - 54 * uy, NAVY, 2)
    mx, my = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy
    d.text(mx, my, label, color=NAVY, weight="bold", size=15)

d.text(450, 396, "F = 96,485 C/mol   ·   at 298 K", color=GREY, size=13)

py = 420
d.rect(60, py, 780, 180, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 28, "The three always move together", color=NAVY, weight="bold", size=17)

cols = [(206, "E°cell"), (396, "ΔG°"), (568, "K"), (752, "meaning")]
for x, h in cols:
    d.text(x, py + 56, h, color=NAVY, weight="bold", size=15)
rows = [("> 0", "< 0", "> 1", "spontaneous as written", SAGE),
        ("= 0", "= 0", "= 1", "at equilibrium", GREY),
        ("< 0", "> 0", "< 1", "reverse is spontaneous", RED)]
y = py + 84
for e, g, k, m, col in rows:
    d.text(206, y, e, color=col, weight="bold", size=16)
    d.text(396, y, g, color=col, weight="bold", size=16)
    d.text(568, y, k, color=col, weight="bold", size=16)
    d.text(752, y, m, color=col, size=14)
    y += 26
d.text(450, py + 166, "E°cell is intensive — scaling a half-reaction leaves it alone. ΔG° is extensive and scales with n.",
       color=GREY, size=13)

d.save("emf-gibbs-k-triangle")
