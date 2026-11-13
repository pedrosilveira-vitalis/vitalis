import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 810,
      "Radius to the fourth power decides almost everything",
      "Q = πr⁴ΔP/8ηL, so a small squeeze on an arteriole does what no pressure change can",
      "Top left: bars showing how flow falls as the radius shrinks — 100 percent at full radius, 41 percent at 0.8, "
      "32 percent at 0.75 and about 6 percent at half the radius. Top right: the parabolic velocity profile in a "
      "tube, fastest on the axis, zero at the wall, with the mean equal to half the maximum. Bottom left: resistance "
      "equals 8 eta L over pi r to the fourth, with the Ohm's law analogy and the series and parallel rules. Bottom "
      "right: the Reynolds number scale from laminar below 2000 to turbulent above 4000, and a note that murmurs and "
      "bruits are turbulence while the normal heart sounds are valve closure.")

# ---------------- Panel A: the r^4 ladder ----------------
d.rect(40, 112, 416, 318, RED, "none", rx=12, width=2)
d.text(248, 142, "What a little narrowing costs", color=RED, weight="bold", size=17)

bars = [("r", 1.0, "100%", SAGE), ("0.8r", 0.4096, "41%", GOLD),
        ("0.75r", 0.3164, "32%", GOLD), ("0.5r", 0.0625, "6%", RED)]
BASE, MAXW = 190, 236
y = 186
for label, frac, pct, col in bars:
    d.text(BASE - 14, y + 20, label, anchor="end", color=NAVY, weight="bold", size=15)
    d.rect(BASE, y, max(frac * MAXW, 6), 30, col, FILL[col], rx=4, width=1.5)
    d.text(BASE + max(frac * MAXW, 6) + 12, y + 20, pct, anchor="start",
           color=col, weight="bold", size=15)
    y += 46
d.text(248, 388, "flow ∝ r⁴  •  resistance ∝ 1/r⁴", color=NAVY, weight="bold", size=16)
d.text(248, 412, "a 25% narrower coronary carries a third of the blood", color=GREY, size=14)

# ---------------- Panel B: the velocity profile ----------------
d.rect(472, 112, 408, 318, BLUE, "none", rx=12, width=2)
d.text(676, 142, "Laminar flow is parabolic", color=BLUE, weight="bold", size=17)

TX, TY, TW, TH = 540, 190, 280, 150
d.rect(TX, TY, TW, TH, BLUE, FILL[BLUE], rx=0, width=0)
d.line(TX, TY, TX + TW, TY, NAVY, 3)
d.line(TX, TY + TH, TX + TW, TY + TH, NAVY, 3)

mid = TY + TH / 2
for i in range(7):
    fy = TY + 10 + i * (TH - 20) / 6
    rel = 1 - ((fy - mid) / (TH / 2 - 10)) ** 2
    d.arrow(TX + 24, fy, TX + 24 + max(rel * 150, 2), fy, NAVY, width=2)
d.path("M" + " L".join(
    f"{TX + 24 + max((1 - ((TY + 10 + i * (TH - 20) / 6 - mid) / (TH / 2 - 10)) ** 2) * 150, 2):.1f} "
    f"{TY + 10 + i * (TH - 20) / 6:.1f}" for i in range(7)), RED, 2.5)

d.text(TX + 10, TY - 10, "no slip at the wall: v = 0", anchor="start", color=GREY, size=13)
d.text(TX + 196, mid + 5, "v_max on the axis", anchor="start", color=RED, weight="bold", size=13)
d.text(676, 372, "v_mean = v_max / 2", color=NAVY, weight="bold", size=16)
d.text(676, 398, "cells drift to the fast centre, leaving a plasma layer at the wall",
       color=GREY, size=13)
d.text(676, 420, "(the Fåhræus–Lindqvist effect in small vessels)", color=GREY, size=13)

# ---------------- Panel C: resistance ----------------
d.rect(40, 450, 416, 212, SAGE, "none", rx=12, width=2)
d.text(248, 478, "Resistance behaves like a circuit", color=SAGE, weight="bold", size=17)
d.text(248, 512, "R = 8ηL / πr⁴   •   ΔP = Q · R", color=NAVY, weight="bold", size=17)
d.text(248, 544, "ΔP ↔ voltage   •   Q ↔ current   •   R ↔ resistance", color=GREY, size=14)
d.rect(62, 562, 180, 76, SAGE, FILL[SAGE], rx=9, width=2)
d.text(152, 588, "in series", color=SAGE, weight="bold", size=15)
d.text(152, 614, "R = R₁ + R₂ + …", color=NAVY, weight="bold", size=14)
d.rect(254, 562, 180, 76, BLUE, FILL[BLUE], rx=9, width=2)
d.text(344, 588, "in parallel", color=BLUE, weight="bold", size=15)
d.text(344, 614, "1/R = 1/R₁ + 1/R₂ + …", color=NAVY, weight="bold", size=14)

# ---------------- Panel D: Reynolds ----------------
d.rect(472, 450, 408, 212, GOLD, "none", rx=12, width=2)
d.text(676, 478, "Will it stay laminar?", color=GOLD, weight="bold", size=17)
d.text(676, 506, "Re = ρvd / η", color=NAVY, weight="bold", size=17)

segs = [(496, 128, SAGE, "laminar", "Re < 2,000"), (632, 92, GOLD, "mixed", "2,000–4,000"),
        (736, 128, RED, "turbulent", "Re > 4,000")]
for x, w, col, name, rng in segs:
    d.rect(x, 524, w, 38, col, FILL[col], rx=6, width=2)
    d.text(x + w / 2, 548, name, color=col, weight="bold", size=14)
    d.text(x + w / 2, 580, rng, color=GREY, size=13)

d.text(676, 612, "raised by v, d and ρ  •  damped by η", color=NAVY, weight="bold", size=14)
d.text(676, 636, "anaemia: thinner blood and faster flow ⇒ flow murmurs", color=GREY, size=13)

d.text(460, 700, "Murmurs and bruits are turbulence — S1 and S2 are valves closing, not turbulent flow",
       color=RED, weight="bold", size=16)
d.text(460, 732, "Blood is shear-thinning: rouleaux raise its viscosity when flow is slow",
       color=GREY, size=15)
d.text(460, 762, "Arterioles are the resistance vessels; capillaries are slow because they are many",
       color=GREY, size=15)
d.text(460, 792, "Whole blood ≈ 3–4 cP  •  plasma ≈ 1.2–1.5 cP  •  water at 37°C ≈ 0.7 cP",
       color=GREY, size=15)

d.save("poiseuille-r4-and-reynolds")
print("ok")
