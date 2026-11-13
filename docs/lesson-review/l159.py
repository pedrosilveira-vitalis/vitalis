import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 820,
      "Mechanical energy: what stays constant, and what leaks",
      "Only conservative forces keep KE + U fixed; friction moves part of it out of the ledger",
      "Left: stacked energy bars at three points of a track. Without friction the kinetic plus potential total is the "
      "same at every point; with friction the mechanical total shrinks and the missing part appears as heat. Right: a "
      "potential energy curve with a total energy line, showing turning points where the curve meets the line, a "
      "stable minimum, an unstable maximum, and the kinetic energy as the gap between the line and the curve. "
      "Bottom: springs in parallel add while springs in series add reciprocally, with the combination rules matching "
      "capacitors rather than resistors.")

# ---------------- Panel A: energy bars ----------------
d.rect(40, 112, 430, 388, BLUE, "none", rx=12, width=2)
d.text(255, 142, "The same energy, re-labelled", color=BLUE, weight="bold", size=17)

BARW, XS = 74, [86, 206, 326]
LBL = ["top", "middle", "bottom"]


def bars(baseline, data, show_heat):
    for x, (ke, u, heat) in zip(XS, data):
        y = baseline
        if ke:
            d.rect(x, y - ke, BARW, ke, BLUE, FILL[BLUE], rx=4, width=1.5)
            d.text(x + BARW / 2, y - ke / 2 + 5, "KE", color=BLUE, weight="bold", size=13)
            y -= ke
        if u:
            d.rect(x, y - u, BARW, u, GOLD, FILL[GOLD], rx=4, width=1.5)
            d.text(x + BARW / 2, y - u / 2 + 5, "U", color=GOLD, weight="bold", size=13)
            y -= u
        if heat >= 12 and show_heat:
            d.rect(x, y - heat, BARW, heat, GREY, FILL[GREY], rx=4, width=1.5)
            d.text(x + BARW / 2, y - heat / 2 + 4, "heat", color=GREY, size=11)
    d.line(70, baseline, 420, baseline, NAVY, 2)
    for x, lab in zip(XS, LBL):
        d.text(x + BARW / 2, baseline + 20, lab, color=GREY, size=13)


d.text(255, 168, "no friction:  KE + U is the same at every point",
       color=SAGE, weight="bold", size=15)
bars(300, [(0, 110, 0), (55, 55, 0), (110, 0, 0)], False)
d.line(70, 190, 420, 190, SAGE, 2, True)
d.text(424, 186, "E", anchor="start", color=SAGE, weight="bold", size=14)

d.text(255, 350, "with friction:  KE + U falls, the rest is heat",
       color=RED, weight="bold", size=15)
bars(470, [(0, 110, 0), (46, 50, 14), (82, 0, 28)], True)
d.line(70, 360, 420, 360, SAGE, 2, True)
d.text(424, 356, "E", anchor="start", color=SAGE, weight="bold", size=14)

# ---------------- Panel B: potential energy curve ----------------
d.rect(486, 112, 394, 388, GOLD, "none", rx=12, width=2)
d.text(683, 142, "Reading a U(x) curve", color=GOLD, weight="bold", size=17)

f = d.axes(546, 180, 294, 190, "position x", "U(x)", xr=(0, 10), yr=(0, 10),
           ticks_x=[], ticks_y=[])


def U(x):
    return 5.2 - 3.1 * math.cos(x * 0.72) + 0.16 * x


pts = [(x / 10, U(x / 10)) for x in range(0, 101)]
d.curve(f, pts, GOLD, 3)
ET = 7.4
d.line(f(0, ET)[0], f(0, ET)[1], f(10, ET)[0], f(10, ET)[1], SAGE, 2, True)
d.text(f(10, ET)[0] + 6, f(10, ET)[1] + 5, "E", anchor="start", color=SAGE, weight="bold", size=15)

xmax = 4.35
xmin = 8.7
d.circle(f(xmin, U(xmin))[0], f(xmin, U(xmin))[1], 5, SAGE, SAGE)
d.text(f(xmin, U(xmin))[0], f(xmin, U(xmin))[1] + 24, "stable", color=SAGE, weight="bold", size=13)
d.circle(f(xmax, U(xmax))[0], f(xmax, U(xmax))[1], 5, RED, RED)
d.text(f(xmax, U(xmax))[0] - 4, f(xmax, U(xmax))[1] - 14, "unstable", anchor="end",
       color=RED, weight="bold", size=13)

xk = 7.4
d.arrow(f(xk, U(xk))[0], f(xk, U(xk))[1], f(xk, ET)[0], f(xk, ET)[1], BLUE, width=2.5)
d.text(f(xk, (U(xk) + ET) / 2)[0] + 8, f(xk, (U(xk) + ET) / 2)[1] + 5, "KE",
       anchor="start", color=BLUE, weight="bold", size=14)

d.text(683, 444, "KE = E − U(x);  U = E is a turning point", color=NAVY, weight="bold", size=15)
d.text(683, 468, "slope zero ⇒ F = 0:  a dip is stable, a crest is not", color=GREY, size=14)
d.text(683, 492, "the object can never reach x where U > E", color=GREY, size=14)

# ---------------- Bottom: springs and the master equations ----------------
d.rect(40, 520, 430, 136, SAGE, FILL[SAGE], rx=10, width=2)
d.text(255, 548, "Combining springs", color=SAGE, weight="bold", size=17)
d.text(255, 578, "parallel (side by side):  k_eff = k₁ + k₂", color=NAVY, weight="bold", size=15)
d.text(255, 602, "series (end to end):  1/k_eff = 1/k₁ + 1/k₂", color=NAVY, weight="bold", size=15)
d.text(255, 632, "same pattern as capacitors — the reverse of resistors", color=GREY, size=14)

d.rect(486, 520, 394, 136, NAVY, FILL[NAVY], rx=10, width=2)
d.text(683, 548, "The two equations", color=NAVY, weight="bold", size=17)
d.text(683, 578, "conservative only:  KEᵢ + Uᵢ = KEᶠ + Uᶠ", color=NAVY, weight="bold", size=15)
d.text(683, 602, "otherwise:  W_nc = ΔKE + ΔU = ΔE_mech", color=NAVY, weight="bold", size=15)
d.text(683, 632, "friction makes W_nc negative: −μₖNd", color=GREY, size=14)

d.text(460, 700, "U_g = mgh (near Earth)   •   U_g = −GMm/r (far)   •   U_e = ½kx²",
       color=NAVY, weight="bold", size=16)
d.text(460, 730, "The h = 0 line is yours to choose — only ΔU is physical",
       color=GREY, size=15)
d.text(460, 760, "A conservative force does zero net work around any closed loop",
       color=GREY, size=15)
d.text(460, 790, "Potential energy exists only for conservative forces",
       color=GREY, size=15)

d.save("mechanical-energy-ledger-and-curve")
print("ok")
