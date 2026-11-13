import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 820,
      "Surface tension: the surface is the odd place to be",
      "ΔP = 2γ/R makes small spheres tight; h = 2γcosθ/ρgr makes narrow tubes climb",
      "Top left: a molecular picture, with a molecule in the bulk pulled equally in all directions and a molecule at "
      "the surface pulled only inward and sideways. Top right: two alveoli of different size joined by an airway, "
      "with the smaller one at higher pressure emptying into the larger, and a note that surfactant lowers surface "
      "tension more in the smaller one so the pressures match. Bottom left: capillary rise in two glass tubes, higher "
      "in the narrower one, beside mercury depressed below the outside level. Bottom right: the equations and the "
      "surface tension values for water, plasma, surfactant at expiration and mercury.")

# ---------------- Panel A: molecular picture ----------------
d.rect(40, 112, 416, 300, BLUE, "none", rx=12, width=2)
d.text(248, 142, "Why a surface is under tension", color=BLUE, weight="bold", size=17)

LX, LY, LW, LH = 86, 212, 326, 150
d.rect(LX, LY, LW, LH, BLUE, FILL[BLUE], rx=4, width=0)
d.line(LX, LY, LX + LW, LY, BLUE, 3)
for row in range(4):
    for col in range(9):
        cx = LX + 22 + col * 36 + (18 if row % 2 else 0)
        cy = LY + 20 + row * 36
        if cx < LX + LW - 10:
            d.circle(cx, cy, 9, BLUE, "#ffffff", width=1.2)

bx, by = LX + 112, LY + 92
d.circle(bx, by, 11, NAVY, FILL[NAVY], width=2)
for k in range(8):
    a = math.radians(45 * k)
    d.line(bx, by, bx + 24 * math.cos(a), by + 24 * math.sin(a), NAVY, 1.6)
d.rect(bx - 80, by + 32, 160, 22, GREY, "#eef3f7", rx=6, width=0)
d.text(bx, by + 47, "bulk: pulled evenly", color=NAVY, weight="bold", size=13)

sx, sy = LX + 244, LY + 20
d.circle(sx, sy, 11, RED, FILL[RED], width=2)
for a in (135, 180, 225, 270, 45, 315):
    d.line(sx, sy, sx + 24 * math.cos(math.radians(a)), sy - 24 * math.sin(math.radians(a)), RED, 1.6)
d.arrow(sx, sy - 16, sx, sy - 44, RED, width=2.5)
d.text(sx, sy - 52, "net pull inward", color=RED, weight="bold", size=13)

d.text(248, 388, "γ = F/L = J/m²: the energy cost of making new surface",
       color=NAVY, weight="bold", size=15)

# ---------------- Panel B: two alveoli ----------------
d.rect(472, 112, 408, 300, RED, "none", rx=12, width=2)
d.text(676, 142, "Small spheres squeeze harder", color=RED, weight="bold", size=17)

d.circle(568, 226, 30, RED, FILL[RED], width=2.5)
d.circle(790, 238, 54, BLUE, FILL[BLUE], width=2.5)
d.line(598, 226, 640, 226, NAVY, 3)
d.line(736, 238, 700, 238, NAVY, 3)
d.line(640, 226, 668, 282, NAVY, 3)
d.line(700, 238, 668, 282, NAVY, 3)
d.line(668, 282, 668, 320, NAVY, 3)
d.text(568, 180, "high P", color=RED, weight="bold", size=14)
d.text(790, 172, "low P", color=BLUE, weight="bold", size=14)
d.arrow(612, 206, 700, 206, RED, width=3)
d.text(656, 196, "air", color=RED, weight="bold", size=13)

d.text(676, 338, "ΔP = 2γ / R  ⇒  the smaller alveolus empties into the larger",
       color=NAVY, weight="bold", size=14)
d.rect(492, 352, 376, 46, SAGE, FILL[SAGE], rx=9, width=2)
d.text(680, 372, "Surfactant drops γ further as the alveolus shrinks,", color=SAGE, weight="bold", size=13)
d.text(680, 390, "so the two pressures end up matched and both stay open", color=SAGE, weight="bold", size=13)

# ---------------- Panel C: capillary rise ----------------
d.rect(40, 432, 416, 250, SAGE, "none", rx=12, width=2)
d.text(248, 460, "Narrow tubes climb higher", color=SAGE, weight="bold", size=17)

POOL, PBOT = 600, 636
d.rect(70, POOL, 356, PBOT - POOL, BLUE, FILL[BLUE], rx=0, width=0)
d.line(70, POOL, 426, POOL, BLUE, 2)


def tube(cx, w, h, col, concave=True):
    d.line(cx - w, 482, cx - w, PBOT, GREY, 2)
    d.line(cx + w, 482, cx + w, PBOT, GREY, 2)
    top = POOL - h
    d.rect(cx - w + 2, top, 2 * w - 4, PBOT - top, col, FILL[col], rx=0, width=0)
    arc = -10 if concave else 10
    d.path(f"M{cx - w + 2} {top} Q{cx} {top + arc} {cx + w - 2} {top}", col, 2.5)
    return top


t1 = tube(126, 14, 80, BLUE)
t2 = tube(232, 8, 112, BLUE)
t3 = tube(348, 16, -36, GREY, concave=False)
d.text(126, t1 - 14, "wide", color=NAVY, weight="bold", size=13)
d.text(232, t2 - 14, "narrow", color=NAVY, weight="bold", size=13)
d.text(374, 556, "mercury", anchor="start", color=GREY, weight="bold", size=13)
d.text(374, 576, "sits lower", anchor="start", color=GREY, weight="bold", size=13)
d.text(374, 596, "inside", anchor="start", color=GREY, weight="bold", size=13)

d.text(248, 666, "h = 2\u03b3 cos\u03b8 / \u03c1gr  \u2014  halve r, double h", color=NAVY, weight="bold", size=15)

# ---------------- Panel D: the numbers ----------------
d.rect(472, 432, 408, 250, GOLD, "none", rx=12, width=2)
d.text(676, 460, "Numbers worth carrying", color=GOLD, weight="bold", size=17)

vals = [("water, 37°C", "≈ 70 mN/m"), ("blood plasma", "≈ 55–60 mN/m"),
        ("alveolus, inspiration", "≈ 25–30 mN/m"), ("alveolus, expiration", "≈ 1–5 mN/m"),
        ("mercury", "≈ 480 mN/m")]
y = 492
for name, val in vals:
    d.text(500, y, name, anchor="start", color=GREY, size=14)
    d.text(852, y, val, anchor="end", color=NAVY, weight="bold", size=14)
    y += 28
d.line(496, 638, 856, 638, GOLD, 2)
d.text(676, 664, "droplet ΔP = 2γ/R   •   soap bubble ΔP = 4γ/R",
       color=NAVY, weight="bold", size=15)

d.text(460, 722, "θ < 90° wets and climbs (concave);  θ > 90° beads and sinks (convex)",
       color=NAVY, weight="bold", size=16)
d.text(460, 752, "Surfactant always lowers γ — DPPC from type II pneumocytes; its absence is NRDS",
       color=GREY, size=15)
d.text(460, 782, "Law of Laplace for a vessel wall: T = P · r, so a widening aneurysm is self-worsening",
       color=GREY, size=15)

d.save("surface-tension-laplace-and-capillarity")
print("ok")
