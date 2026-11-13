import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 800,
      "Narrow means fast, and fast means low pressure",
      "Continuity sets the speed (A₁v₁ = A₂v₂); Bernoulli then spends the pressure to pay for it",
      "Top: a pipe that narrows and widens again, with pressure-tap columns that are tall in the wide sections and "
      "short at the constriction, and the worked numbers 0.04 square metres at 2 metres per second and 200 kPa "
      "widening to 0.01 square metres at 8 metres per second and 170 kPa. Bottom left: the three Bernoulli terms as "
      "stacked bars, showing pressure energy converting into kinetic energy at the constriction while the total stays "
      "fixed. Bottom right: the same arithmetic in the circulation, where the capillary bed's total cross-section is "
      "about a thousand times the aorta's and the velocity is a thousand times lower, at the same 5 litres per minute.")

# ---------------- Panel A: the pipe ----------------
d.rect(40, 112, 840, 300, BLUE, "none", rx=12, width=2)
d.text(460, 142, "One flow rate, two speeds, two pressures", color=BLUE, weight="bold", size=17)

TOP = "M140 286 L360 286 L410 311 L560 311 L610 286 L830 286"
BOT = "M140 366 L360 366 L410 341 L560 341 L610 366 L830 366"
d.path(TOP + " L830 366 L610 366 L560 341 L410 341 L360 366 L140 366 Z", BLUE, 2.5, FILL[BLUE])

for x in (230, 700):
    d.rect(x - 11, 196, 22, 90, NAVY, FILL[NAVY], rx=3, width=1.5)
d.rect(474, 236, 22, 75, NAVY, FILL[NAVY], rx=3, width=1.5)
d.text(230, 186, "high P", color=NAVY, weight="bold", size=13)
d.text(485, 226, "low P", color=RED, weight="bold", size=13)
d.text(700, 186, "high P again", color=NAVY, weight="bold", size=13)

d.arrow(170, 326, 240, 326, NAVY, width=2.5)
d.arrow(440, 326, 540, 326, RED, width=3)
d.arrow(640, 326, 710, 326, NAVY, width=2.5)

d.text(250, 392, "A₁ = 0.04 m²  •  v₁ = 2 m/s  •  P₁ = 200 kPa",
       color=NAVY, weight="bold", size=15)
d.text(700, 392, "A₂ = 0.01 m²  •  v₂ = 8 m/s  •  P₂ = 170 kPa",
       color=RED, weight="bold", size=15)
d.text(485, 366, "4× narrower ⇒ 4× faster", color=RED, weight="bold", size=13)

# ---------------- Panel B: the energy bars ----------------
d.rect(40, 432, 416, 222, GOLD, "none", rx=12, width=2)
d.text(248, 460, "The same total, split differently", color=GOLD, weight="bold", size=17)

BASE, H = 600, 110
for cx, p, k, lab in [(150, 0.94, 0.06, "wide"), (348, 0.80, 0.20, "narrow")]:
    y = BASE
    d.rect(cx - 52, y - p * H, 104, p * H, NAVY, FILL[NAVY], rx=4, width=1.5)
    d.text(cx, y - p * H / 2 + 5, "P", color=NAVY, weight="bold", size=15)
    y -= p * H
    d.rect(cx - 52, y - k * H, 104, k * H, RED, FILL[RED], rx=4, width=1.5)
    d.text(cx, y - k * H / 2 + 5, "½ρv²", color=RED, weight="bold", size=13)
    d.text(cx, BASE + 20, lab, color=GREY, size=14)
d.line(80, BASE, 420, BASE, NAVY, 2)
d.line(80, BASE - H, 420, BASE - H, SAGE, 2, True)
d.text(424, BASE - H + 5, "total", anchor="end", color=SAGE, weight="bold", size=13)
d.text(248, 640, "P + ½ρv² + ρgh is what stays constant", color=NAVY, weight="bold", size=15)

# ---------------- Panel C: the circulation ----------------
d.rect(472, 432, 408, 222, SAGE, "none", rx=12, width=2)
d.text(676, 460, "The same sum in the circulation", color=SAGE, weight="bold", size=17)

rows = [("", "aorta", "capillaries"),
        ("total area", "2.5 cm²", "2,500 cm²"),
        ("velocity", "33 cm/s", "0.03 cm/s"),
        ("Q = Av", "≈83 cm³/s", "≈75 cm³/s")]
y = 492
for label, a, b in rows:
    bold = (label == "")
    d.text(500, y, label, anchor="start", color=GREY, size=14)
    d.text(700, y, a, color=NAVY, weight="bold" if bold else None, size=15)
    d.text(840, y, b, anchor="end", color=NAVY if not bold else RED,
           weight="bold" if bold else None, size=15)
    y += 32
d.line(496, 604, 856, 604, SAGE, 2)
d.text(676, 630, "both ≈ 5 L/min — the resting cardiac output",
       color=SAGE, weight="bold", size=15)

d.text(460, 692, "Torricelli: a hole a height h below the surface empties at v = √(2gh), whatever its size",
       color=NAVY, weight="bold", size=16)
d.text(460, 722, "Bernoulli needs ideal flow; where viscosity rules, use Poiseuille's Q = πr⁴ΔP/8ηL",
       color=GREY, size=15)
d.text(460, 752, "In a stenosis: low pressure inside it (Bernoulli), raised pressure upstream (resistance)",
       color=GREY, size=15)
d.text(460, 782, "Re = ρvd/η: below ~2,000 laminar, above ~4,000 turbulent",
       color=GREY, size=15)

d.save("continuity-bernoulli-and-the-circulation")
print("ok")
