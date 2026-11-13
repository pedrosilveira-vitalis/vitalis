import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 850,
      "Kinematics: signs, projectile components, and graph areas",
      "g is a positive magnitude; the sign comes from the axis you choose",
      "Four panels. Top left: g equals 9.8 metres per second squared as a positive magnitude, with a equal to minus g "
      "when up is positive and plus g when down is positive, and a note that acceleration is still minus g at the peak. "
      "Top right: a projectile parabola showing that the horizontal velocity arrows stay the same length while "
      "the vertical arrow shrinks to zero at the peak and grows downward after it. Middle: the symmetric-flight "
      "formulas for time of flight, range and maximum height. Bottom: a velocity-versus-time graph in three phases "
      "whose slopes give accelerations of 5, 0 and minus 10 metres per second squared and whose areas give "
      "displacements of 40, 80 and 20 metres, totalling 140 metres.")

# ---------------- Panel A: sign conventions ----------------
d.rect(40, 112, 258, 306, GREY, FILL[GREY], rx=12, width=2)
d.text(169, 142, "Signs come from your axis", color=GREY, weight="bold", size=17)

d.rect(58, 160, 222, 48, NAVY, FILL[NAVY], rx=9, width=2)
d.text(169, 190, "g = 9.8 ≈ 10 m/s²", color=NAVY, weight="bold", size=17)
d.text(169, 228, "always a positive magnitude", color=GREY, size=14)

d.text(169, 262, "up positive:", color=BLUE, weight="bold", size=15)
d.text(169, 286, "a = −g = −10 m/s²", color=NAVY, size=17)
d.text(169, 316, "down positive:", color=BLUE, weight="bold", size=15)
d.text(169, 340, "a = +g = +10 m/s²", color=NAVY, size=17)

d.rect(58, 356, 222, 48, RED, FILL[RED], rx=9, width=2)
d.text(169, 386, "At the peak v = 0, a = −10", color=RED, weight="bold", size=15)

# ---------------- Panel B: projectile ----------------
d.rect(318, 112, 562, 306, BLUE, "none", rx=12, width=2)
d.text(599, 142, "Horizontal and vertical motion are independent",
       color=BLUE, weight="bold", size=17)

X0, XP, X1 = 380, 580, 780
YG, YP = 330, 190


def para(x):
    u = (x - XP) / (XP - X0)
    return YG - (YG - YP) * (1 - u * u)


d.line(348, YG, 852, YG, GREY, 2)
pts = [(x, para(x)) for x in range(X0, X1 + 1, 10)]
d.path("M" + " L".join(f"{x} {y:.1f}" for x, y in pts), NAVY, 3)

for cx, cy in [(X0, YG), (XP, YP), (X1, YG)]:
    d.arrow(cx, cy - 2, cx + 56, cy - 2, BLUE, width=2.5)
d.text(X0 + 28, YG - 14, "vₓ", color=BLUE, weight="bold", size=15)
d.text(XP + 28, YP - 14, "vₓ", color=BLUE, weight="bold", size=15)
d.text(X1 + 28, YG - 14, "vₓ", color=BLUE, weight="bold", size=15)

d.arrow(X0, YG, X0, YG - 66, SAGE, width=2.5)
d.text(X0 - 14, YG - 36, "vᵧ", anchor="end", color=SAGE, weight="bold", size=15)
d.circle(XP, YP, 6, SAGE, SAGE)
d.text(XP, YP - 24, "vᵧ = 0", color=SAGE, weight="bold", size=15)
d.arrow(X1, YG - 66, X1, YG, SAGE, width=2.5)
d.text(X1 - 14, YG - 36, "vᵧ", anchor="end", color=SAGE, weight="bold", size=15)

d.text(X0, YG + 22, "launch", color=GREY, size=14)
d.text(XP, YG + 22, "peak", color=GREY, size=14)
d.text(X1, YG + 22, "landing", color=GREY, size=14)

d.legend(348, 378, [(BLUE, "vₓ = v₀cosθ  — never changes, aₓ = 0", False),
                    (SAGE, "vᵧ = v₀sinθ − gt  — changes at −g", False)])

# ---------------- Formula band ----------------
d.rect(40, 436, 840, 76, SAGE, FILL[SAGE], rx=12, width=2)
d.text(460, 464, "Equal launch and landing height only", color=SAGE, weight="bold", size=16)
d.text(174, 492, "T = 2v₀sinθ / g", color=NAVY, size=16)
d.text(460, 492, "R = v₀² sin2θ / g", color=NAVY, size=16)
d.text(746, 492, "H = (v₀sinθ)² / 2g", color=NAVY, size=16)

# ---------------- Panel C: v-t graph ----------------
d.text(60, 548, "Slope of a v–t graph = acceleration;  area under it = displacement",
       anchor="start", color=GOLD, weight="bold", size=17)

f = d.axes(108, 578, 400, 196, "time t (s)", "velocity v (m/s)",
           xr=(0, 10), yr=(0, 24), ticks_x=[0, 2, 4, 6, 8, 10], ticks_y=[0, 10, 20])

shade = [(0, 0), (4, 20), (8, 20), (10, 0)]
d.path("M" + " L".join(f"{f(a, b)[0]:.1f} {f(a, b)[1]:.1f}" for a, b in shade) + " Z",
       GOLD, 0, FILL[GOLD])
d.curve(f, [(0, 0), (4, 20), (8, 20), (10, 0)], GOLD, 3)
for t in (4, 8):
    d.line(f(t, 0)[0], f(t, 0)[1], f(t, 20)[0], f(t, 20)[1], GREY, 1, True)

d.text(f(2, 7)[0], f(2, 7)[1], "40 m", color=NAVY, weight="bold", size=15)
d.text(f(6, 9)[0], f(6, 9)[1], "80 m", color=NAVY, weight="bold", size=15)
d.text(f(9, 4.5)[0], f(9, 4.5)[1], "20 m", color=NAVY, weight="bold", size=15)

d.rect(556, 578, 324, 196, GOLD, "none", rx=12, width=2)
rows = [("0 – 4 s", "a = (20−0)/4 = +5 m/s²", "½·4·20 = 40 m"),
        ("4 – 8 s", "a = 0 m/s²", "4·20 = 80 m"),
        ("8 – 10 s", "a = (0−20)/2 = −10 m/s²", "½·2·20 = 20 m")]
y = 604
for phase, acc, area in rows:
    d.text(574, y, phase, anchor="start", color=GOLD, weight="bold", size=15)
    d.text(862, y, area, anchor="end", color=NAVY, weight="bold", size=15)
    d.text(574, y + 22, acc, anchor="start", color=GREY, size=14)
    y += 48
d.line(574, 738, 862, 738, GOLD, 2)
d.text(574, 762, "total displacement", anchor="start", color=NAVY, size=15)
d.text(862, 762, "140 m", anchor="end", color=NAVY, weight="bold", size=16)

d.save("kinematics-signs-components-areas")
print("ok")
