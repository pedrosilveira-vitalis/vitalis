import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 860,
      "Open a channel and the voltage walks toward that ion's equilibrium",
      "Driving force = V_m − E_ion — that one difference sets the direction and size of every current",
      "Top: a voltage scale from minus ninety-five to plus sixty-seven millivolts showing where each ion's "
      "equilibrium potential sits, with the resting potential near potassium's because the resting membrane is "
      "mostly potassium-permeable, and threshold and the action potential peak marked. Middle: the action "
      "potential traced through its phases — the sodium channels opening on a positive feedback loop, their "
      "inactivation gate closing, the slower potassium channels repolarising and overshooting into "
      "afterhyperpolarisation, with the absolute and relative refractory periods marked underneath. Bottom left: "
      "the membrane as a circuit, a capacitor in parallel with a conductance and battery for each ion. Bottom "
      "right: why myelin is fast — it raises the membrane resistance and lowers its capacitance, so the local "
      "current reaches the next node of Ranvier before it leaks away.")

# ---------------- Panel A: the voltage ladder ----------------
d.rect(40, 136, 840, 180, BLUE, "none", rx=12, width=2)
d.text(460, 164, "Where the voltages sit", color=BLUE, weight="bold", size=16)

X0, X1, AY = 120, 800, 238


def vx(mv):
    return X0 + (mv + 110) / 190 * (X1 - X0)


d.line(X0, AY, X1, AY, GREY, 2.4)
marks = [(-95, "E_K", NAVY, -1), (-89, "", GREY, 0), (-70, "rest", BLUE, 1),
         (-55, "threshold", GOLD, -1), (35, "AP peak", RED, 1), (67, "E_Na", NAVY, -1)]
for mv, lab, col, side in marks:
    if not lab:
        continue
    x = vx(mv)
    d.line(x, AY - 9, x, AY + 9, col, 2.4)
    dy = -20 if side < 0 else 30
    d.text(x, AY + dy, lab, color=col, weight="bold", size=14)
    d.text(x, AY + (dy - 18 if side < 0 else dy + 18), f"{mv:+d} mV", color=GREY, size=11)

d.text(460, 300, "the resting membrane is mostly K⁺-permeable, so V_m sits near E_K",
       color=GREY, size=13)

# ---------------- Panel B: the action potential ----------------
d.rect(40, 332, 840, 300, RED, "none", rx=12, width=2)
d.text(460, 360, "One spike, four jobs", color=RED, weight="bold", size=16)

m = d.axes(130, 378, 540, 148, "time (ms)", "V_m (mV)",
           (0, 6), (-90, 50), ticks_x=[1, 2, 3, 4, 5], ticks_y=[-70, -55, 0, 30])


def ap(t):
    if t < 1.0:
        return -70 + 15 * (t / 1.0) ** 3
    if t < 1.5:
        return -55 + 90 * ((t - 1.0) / 0.5) ** 1.6
    if t < 2.6:
        return 35 - 115 * ((t - 1.5) / 1.1) ** 0.9
    if t < 3.6:
        return -80 + 10 * ((t - 2.6) / 1.0) ** 2 - 0
    return -75 + 5 * (1 - math.exp(-(t - 3.6) * 1.6))


d.curve(m, [(t / 40, ap(t / 40)) for t in range(0, 241)], RED, 2.8)
for mv, lab in [(-70, ""), (-55, "")]:
    px, py = m(0, mv)
    d.line(px, py, m(6, mv)[0], py, GREY, 1, True)

for t, mv, lab, col, dx, dy in [(1.25, 0, "Na⁺ in", NAVY, -56, -6),
                                (1.5, 35, "peak", RED, 16, -10),
                                (2.1, -20, "K⁺ out", SAGE, 24, 0),
                                (3.3, -78, "undershoot", BLUE, 30, -12)]:
    px, py = m(t, mv)
    d.text(px + dx, py + dy, lab, color=col, weight="bold", size=13)

px0, _ = m(1.0, 0)
px1, _ = m(2.6, 0)
px2, _ = m(3.8, 0)
d.line(px0, 592, px1, 592, RED, 4)
d.text((px0 + px1) / 2, 612, "absolute refractory", color=RED, weight="bold", size=12)
d.line(px1, 592, px2, 592, GOLD, 4)
d.text((px1 + px2) / 2, 612, "relative", color=GOLD, weight="bold", size=12)
d.text(700, 420, "Na⁺ channels have TWO gates:", anchor="start", color=NAVY, weight="bold", size=13)
d.text(700, 442, "activation opens fast,", anchor="start", color=GREY, size=13)
d.text(700, 462, "inactivation closes just after —", anchor="start", color=GREY, size=13)
d.text(700, 482, "and only repolarising resets it", anchor="start", color=NAVY, weight="bold", size=13)
d.text(700, 516, "K⁺ channels are simply slow,", anchor="start", color=GREY, size=13)
d.text(700, 536, "which is what causes the undershoot", anchor="start", color=GREY, size=13)

# ---------------- Panel C: equivalent circuit ----------------
d.rect(40, 650, 404, 190, SAGE, "none", rx=12, width=2)
d.text(242, 678, "The membrane as a circuit", color=SAGE, weight="bold", size=15)

d.line(90, 700, 400, 700, GREY, 2)
d.line(90, 800, 400, 800, GREY, 2)
d.line(120, 700, 120, 740, GREY, 2)
d.line(110, 740, 130, 740, NAVY, 3)
d.line(110, 750, 130, 750, NAVY, 3)
d.line(120, 750, 120, 800, GREY, 2)
d.text(120, 820, "C_m", color=NAVY, weight="bold", size=13)
for x, col, lab, e in [(220, SAGE, "g_K", "E_K"), (330, RED, "g_Na", "E_Na")]:
    d.line(x, 700, x, 722, GREY, 2)
    d.rect(x - 11, 722, 22, 30, col, FILL[col], rx=3, width=2)
    d.line(x, 752, x, 766, GREY, 2)
    d.line(x - 11, 766, x + 11, 766, NAVY, 3)
    d.line(x - 6, 774, x + 6, 774, NAVY, 1.8)
    d.line(x, 774, x, 800, GREY, 2)
    d.text(x - 18, 742, lab, anchor="end", color=col, weight="bold", size=13)
    d.text(x + 18, 774, e, anchor="start", color=NAVY, weight="bold", size=13)
d.text(242, 820, "I_ion = g(V_m − E_ion)", color=SAGE, weight="bold", size=14)

# ---------------- Panel D: myelin ----------------
d.rect(466, 650, 414, 190, GOLD, "none", rx=12, width=2)
d.text(673, 678, "Why myelin is fast", color=GOLD, weight="bold", size=15)

d.line(506, 730, 846, 730, NAVY, 5)
for x in (556, 666, 776):
    d.rect(x - 42, 718, 84, 24, GOLD, FILL[GOLD], rx=6, width=2)
for x in (514, 622, 732, 840):
    d.circle(x, 730, 6, RED, RED)
d.text(673, 762, "nodes of Ranvier: all the Na⁺ channels are here",
       color=NAVY, weight="bold", size=13)
d.text(673, 788, "myelin raises R_m and lowers C_m, so the current", color=GREY, size=13)
d.text(673, 808, "reaches the next node before it leaks away", color=GREY, size=13)
d.text(673, 832, "70–120 m/s myelinated vs 0.5–2 m/s bare", color=GOLD, weight="bold", size=13)

d.save("membrane-potential-action-potential-and-myelin")
print("ok")
