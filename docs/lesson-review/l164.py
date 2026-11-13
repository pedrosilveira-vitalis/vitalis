import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 840,
      "Pressure counts depth; buoyancy counts displaced fluid",
      "P = P₀ + ρgh depends on depth and density alone — never on the shape of the container",
      "Top left: a tank showing pressure rising linearly with depth, about one extra atmosphere every ten metres of "
      "water, with a note that container shape does not matter. Top right: two floating blocks showing that the "
      "submerged fraction equals the ratio of the object's density to the fluid's, 60 percent for wood and 92 percent "
      "for ice. Bottom left: a hydraulic lift, where a small force on a small piston supports a large force on a "
      "large piston while the work stays equal. Bottom right: the standing blood column, higher pressure at the feet "
      "and lower at the brain than at the heart.")

# ---------------- Panel A: pressure with depth ----------------
d.rect(40, 112, 416, 330, BLUE, "none", rx=12, width=2)
d.text(248, 142, "Pressure builds with depth", color=BLUE, weight="bold", size=17)

TX, TY, TW, TH = 96, 180, 180, 182
d.rect(TX, TY, TW, TH, BLUE, FILL[BLUE], rx=4, width=2)
d.line(TX, TY, TX + TW, TY, BLUE, 3)

for frac, depth, press in [(0.0, "0 m", "1 atm"), (0.5, "10 m", "2 atm"), (1.0, "20 m", "3 atm")]:
    y = TY + frac * TH
    d.line(TX - 10, y, TX + TW + 10, y, NAVY, 1.5, True)
    d.text(TX - 16, y + 5, depth, anchor="end", color=GREY, size=13)
    d.text(TX + TW + 16, y + 5, press, anchor="start", color=NAVY, weight="bold", size=14)

d.text(248, 398, "P = P₀ + ρgh   •   ≈1 atm per 10 m of water",
       color=NAVY, weight="bold", size=16)
d.text(248, 424, "same depth ⇒ same pressure, whatever the shape", color=GREY, size=13)

# ---------------- Panel B: floating fraction ----------------
d.rect(472, 112, 408, 330, SAGE, "none", rx=12, width=2)
d.text(676, 142, "How much sits below the line", color=SAGE, weight="bold", size=17)


def floater(cx, rho, frac, label):
    top, w, h = 218, 120, 96
    d.rect(cx - 86, top + (1 - frac) * h, 172, 150 - (1 - frac) * h, BLUE, FILL[BLUE], rx=3, width=0)
    d.line(cx - 86, top + (1 - frac) * h, cx + 86, top + (1 - frac) * h, BLUE, 2.5)
    d.rect(cx - w / 2, top, w, h, NAVY, FILL[NAVY], rx=4, width=2)
    d.line(cx - w / 2, top + (1 - frac) * h, cx + w / 2, top + (1 - frac) * h, NAVY, 2, True)
    d.text(cx, top - 14, label, color=NAVY, weight="bold", size=15)
    d.text(cx, top + (1 - frac) * h + 26, f"{int(frac * 100)}%", color=NAVY, weight="bold", size=18)
    d.text(cx, top + 150, f"ρ = {rho}", color=GREY, size=13)


floater(576, "600", 0.60, "wood")
floater(778, "917", 0.92, "ice")

d.text(676, 398, "fraction submerged = ρ_object / ρ_fluid", color=SAGE, weight="bold", size=16)
d.text(676, 424, "F_b = ρ_fluid · V_displaced · g — the fluid's density, never the object's",
       color=GREY, size=13)

# ---------------- Panel C: hydraulic lift ----------------
d.rect(40, 462, 416, 234, GOLD, "none", rx=12, width=2)
d.text(248, 490, "Pascal: pressure goes everywhere", color=GOLD, weight="bold", size=17)

d.path("M110 560 L110 630 L390 630 L390 548 L330 548 L330 600 L170 600 L170 560 Z",
       GOLD, 2, FILL[GOLD])
d.rect(108, 552, 64, 12, NAVY, FILL[NAVY], rx=2, width=1.5)
d.rect(328, 540, 64, 12, NAVY, FILL[NAVY], rx=2, width=1.5)
d.arrow(140, 520, 140, 548, RED, width=3)
d.text(140, 512, "F₁ = 200 N", color=RED, weight="bold", size=14)
d.arrow(360, 518, 360, 538, SAGE, width=3)
d.text(360, 512, "10,000 N", color=SAGE, weight="bold", size=14)
d.text(140, 652, "A₁ = 0.01 m²", color=GREY, size=13)
d.text(360, 652, "A₂ = 0.5 m²", color=GREY, size=13)

d.text(248, 676, "F₂ = F₁ · A₂/A₁, and F₁d₁ = F₂d₂: force gained, distance paid",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel D: the standing column ----------------
d.rect(472, 462, 408, 234, RED, "none", rx=12, width=2)
d.text(676, 490, "The body is a fluid column too", color=RED, weight="bold", size=17)

d.line(676, 512, 676, 660, GREY, 2)
marks = [(524, "brain", "≈ 30 mmHg lower", BLUE),
         (578, "heart", "reference level", NAVY),
         (648, "feet", "≈ 100 mmHg higher", RED)]
for y, name, note, col in marks:
    d.circle(676, y, 7, col, col)
    d.text(664, y + 5, name, anchor="end", color=col, weight="bold", size=14)
    d.text(692, y + 5, note, anchor="start", color=GREY, size=13)

d.text(676, 682, "ΔP = ρgh with ρ_blood ≈ 1060 kg/m³", color=NAVY, weight="bold", size=14)

d.text(460, 742, "Gauge pressure is ρgh alone; absolute pressure adds the atmosphere on top",
       color=NAVY, weight="bold", size=16)
d.text(460, 774, "A floating object at rest always has F_b = W exactly — that is what sets how deep it sits",
       color=GREY, size=15)
d.text(460, 804, "Blood pressure readings are gauge pressures, referenced to the right atrium",
       color=GREY, size=15)

d.save("fluid-statics-depth-and-buoyancy")
print("ok")
