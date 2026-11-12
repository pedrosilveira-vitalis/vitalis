import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 640,
      "The Nernst equation is a straight line in log Q",
      "Start at E°cell when Q = 1, slide down by 0.0592/n for every tenfold rise in Q, and hit zero when Q reaches K.",
      "A plot of cell potential against log Q. The line starts high on the left where reactants dominate, "
      "passes through E standard at log Q equal to zero, and crosses zero at log Q equal to log K, beyond "
      "which the potential is negative and the reverse reaction is spontaneous. The slope is minus 0.0592 "
      "over n volts per decade. A panel below lists what each region means and the two special points.")

X0, X1 = 150, 820
Y0, Y1 = 130, 400
QLO, QHI = -8.0, 44.0
E0 = 1.10
N = 2
SLOPE = 0.0592 / N
ELO, EHI = -1.0, 1.6


def px(q):
    return X0 + (X1 - X0) * (q - QLO) / (QHI - QLO)


def py(e):
    return Y1 - (Y1 - Y0) * (e - ELO) / (EHI - ELO)


# axes
d.line(X0, py(0), X1, py(0), GREY, 1.5, dash=True)
d.line(px(0), Y0, px(0), Y1, GREY, 1.5, dash=True)
d.line(X0, Y1, X1, Y1, NAVY, 2)
d.line(X0, Y0, X0, Y1, NAVY, 2)
for q in range(-8, 45, 8):
    d.line(px(q), Y1, px(q), Y1 + 6, NAVY, 1.2)
    d.text(px(q), Y1 + 24, str(q), color=GREY, size=12)
d.text((X0 + X1) / 2, Y1 + 48, "log Q", color=NAVY, weight="bold", size=15)
for e in [-1.0, 0.0, 1.0]:
    d.text(X0 - 12, py(e) + 5, "%.1f" % e, anchor="end", color=GREY, size=12)
d.text(X0 - 12, Y0 - 14, "E (V)", anchor="end", color=NAVY, weight="bold", size=14)

# the line
d.line(px(QLO), py(E0 - SLOPE * QLO), px(QHI), py(E0 - SLOPE * QHI), BLUE, 3)

# marked points
logK = E0 / SLOPE
for q, e, col, lab, sub, up in [(0, E0, SAGE, "Q = 1", "E = E°cell = +1.10 V", False),
                                (logK, 0.0, RED, "Q = K", "E = 0, the battery is flat", False)]:
    d.circle(px(q), py(e), 8, col, col, 0)
    ty = py(e) - 34 if up else py(e) + 46
    d.text(px(q), ty, lab, color=col, weight="bold", size=16)
    d.text(px(q), ty + 20, sub, color=GREY, size=13)

d.text(px(-6.5), py(-0.42), "reactants dominate:", anchor="start", color=BLUE, weight="bold", size=14)
d.text(px(-6.5), py(-0.58), "E sits above E°cell", anchor="start", color=GREY, size=13)



d.text(px(17), py(0.95), "slope = −0.0592 / n", color=BLUE, weight="bold", size=15)
d.text(px(17), py(0.81), "volts per decade of Q", color=GREY, size=13)

pyb = 466
d.rect(60, pyb, 780, 160, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, pyb + 28, "E = E°cell − (0.0592 / n) log Q      at 298 K", color=NAVY, weight="bold", size=18)
rows = [("Q < 1", "products scarce", "E above E°cell", SAGE),
        ("Q = 1", "standard conditions", "E equals E°cell", BLUE),
        ("1 < Q < K", "running down", "E below E°cell, still positive", GOLD),
        ("Q = K", "equilibrium", "E = 0 — no work left", RED)]
y = pyb + 58
for a, b, c, col in rows:
    d.text(196, y, a, anchor="end", color=col, weight="bold", size=15)
    d.text(216, y, b, anchor="start", color=NAVY, size=14)
    d.text(812, y, c, anchor="end", color=col, size=14)
    y += 26
d.text(450, pyb + 148, "Solids, pure liquids and the solvent never appear in Q.", color=GREY, size=13)

d.save("nernst-line")
