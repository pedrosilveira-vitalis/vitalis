import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 812,
      "In a conductor at rest, the charge runs to the surface",
      "E = 0 inside • excess charge on the outer surface • the whole body at one potential",
      "Top left: a solid conductor with all its excess charge on the outer surface, zero field inside and the field "
      "lines leaving at right angles, with charge piling up at a sharp point. Top right: a neutral shell around a "
      "charge plus Q, showing minus Q induced on the inner surface and plus Q on the outer one; grounding the shell "
      "drains the outer charge and kills the field outside. Middle: conductor against insulator — free carriers "
      "that migrate versus bound charges that only polarise in place, with the charge staying where it was rubbed. "
      "Bottom: field against radius for a conducting sphere and a uniformly charged insulating sphere, identical "
      "outside and completely different inside, plus the membrane as a capacitor whose thin, low-dielectric "
      "hydrophobic core carries about a microfarad per square centimetre.")

# ---------------- Panel A: solid conductor ----------------
d.rect(40, 118, 404, 272, BLUE, "none", rx=12, width=2)
d.text(242, 146, "Solid conductor in equilibrium", color=BLUE, weight="bold", size=16)

d.path("M160 300 Q140 212 236 196 Q330 182 356 236 Q376 288 300 322 Q220 352 160 300 Z",
       BLUE, 2.5, FILL[BLUE])
for ang in range(0, 360, 45):
    a = math.radians(ang)
    cx, cy = 258, 258
    d.text(cx + 62 * math.cos(a), cy + 46 * math.sin(a) + 5, "+", color=RED, weight="bold", size=17)
d.text(258, 254, "E = 0", color=NAVY, weight="bold", size=20)
d.text(258, 278, "V constant", color=NAVY, weight="bold", size=14)
d.arrow(352, 232, 404, 216, BLUE, width=1.8)
d.text(380, 196, "⊥ to the surface", anchor="middle", color=BLUE, weight="bold", size=12)
d.text(242, 358, "charge crowds where the surface curves sharply",
       color=GREY, size=13)

# ---------------- Panel B: shell ----------------
d.rect(460, 118, 420, 272, RED, "none", rx=12, width=2)
d.text(670, 146, "A charge inside a shell", color=RED, weight="bold", size=16)

SX, SY = 620, 258
d.circle(SX, SY, 76, GREY, "#e9e4da", 2)
d.circle(SX, SY, 52, GREY, "#faf6ee", 2)
d.circle(SX, SY, 11, RED, FILL[RED], 2)
d.text(SX, SY + 6, "+Q", color=RED, weight="bold", size=13)
for ang in (120, 180, 240):
    a = math.radians(ang)
    d.text(SX + 60 * math.cos(a), SY + 60 * math.sin(a) + 5, "−", color=NAVY, weight="bold", size=19)
for ang in (300, 0, 60):
    a = math.radians(ang)
    d.text(SX + 86 * math.cos(a), SY + 86 * math.sin(a) + 5, "+", color=RED, weight="bold", size=17)
d.text(SX, SY + 96, "inner −Q  •  outer +Q", color=NAVY, weight="bold", size=14)

d.rect(720, 196, 148, 128, SAGE, FILL[SAGE], rx=10, width=2)
d.text(794, 220, "ground it", color=SAGE, weight="bold", size=15)
d.line(738, 232, 850, 232, SAGE, 1.4, True)
d.text(794, 254, "inner −Q stays", color=NAVY, weight="bold", size=12)
d.text(794, 276, "outer charge drains", color=NAVY, weight="bold", size=12)
d.text(794, 302, "no field outside", color=NAVY, weight="bold", size=13)
d.text(670, 380, "outside, you cannot tell where in the cavity the charge sits",
       color=GREY, size=12)

# ---------------- Panel C: conductor vs insulator ----------------
d.rect(40, 410, 840, 150, GOLD, "none", rx=12, width=2)
d.text(460, 438, "Free carriers move; bound charges only lean",
       color=GOLD, weight="bold", size=16)

d.rect(80, 456, 370, 86, BLUE, FILL[BLUE], rx=10, width=2)
d.text(265, 480, "CONDUCTOR", color=BLUE, weight="bold", size=14)
d.text(265, 504, "carriers migrate — charge spreads over the", color=NAVY, size=13)
d.text(265, 524, "surface and the inside goes field-free", color=NAVY, size=13)

d.rect(470, 456, 370, 86, RED, FILL[RED], rx=10, width=2)
d.text(655, 480, "INSULATOR (dielectric)", color=RED, weight="bold", size=14)
d.text(655, 504, "charges stay in their molecules and only", color=NAVY, size=13)
d.text(655, 524, "polarise — rubbed charge stays put", color=NAVY, size=13)

# ---------------- Panel D: sphere fields ----------------
d.rect(40, 578, 460, 218, SAGE, "none", rx=12, width=2)
d.text(270, 606, "Same outside, opposite inside", color=SAGE, weight="bold", size=16)

m = d.axes(110, 630, 300, 112, "distance from centre (R = 1)", "E",
           (0, 3.2), (0, 1.25), ticks_x=[1, 2, 3], ticks_y=None)
d.curve(m, [(x / 25, 1.0 / (x / 25) ** 2) for x in range(25, 81)], NAVY, 2.6)
d.curve(m, [(x / 25, 0.0) for x in range(1, 26)], BLUE, 3)
d.curve(m, [(x / 25, x / 25) for x in range(1, 26)], RED, 2.6)
px, py = m(1.06, 1.16)
d.text(px, py, "insulating sphere", anchor="start", color=RED, weight="bold", size=12)
px, py = m(0.3, 0.0)
d.text(px + 6, py - 8, "conducting sphere: E = 0", anchor="start", color=BLUE, weight="bold", size=12)
px, py = m(1.7, 1 / 1.7 ** 2)
d.text(px + 8, py - 8, "kQ/r² for both", anchor="start", color=NAVY, weight="bold", size=12)

# ---------------- Panel E: membrane ----------------
d.rect(516, 578, 364, 218, BLUE, "none", rx=12, width=2)
d.text(698, 606, "The membrane capacitor", color=BLUE, weight="bold", size=16)
d.rect(556, 630, 284, 16, GOLD, FILL[GOLD], rx=3, width=1.5)
d.rect(556, 646, 284, 26, GREY, "#e9e4da", rx=0, width=1.5)
d.rect(556, 672, 284, 16, GOLD, FILL[GOLD], rx=3, width=1.5)
d.text(698, 664, "hydrophobic core: κ ≈ 2–3", color=NAVY, weight="bold", size=13)
d.text(698, 710, "the conducting fluids are the plates;", color=GREY, size=13)
d.text(698, 730, "the thin low-κ core is the dielectric", color=GREY, size=13)
d.text(698, 762, "C/A ≈ 1 µF/cm²  •  E ≈ 10⁷ V/m", color=BLUE, weight="bold", size=15)
d.text(698, 786, "water's κ ≈ 80 screens charge within about 1 nm", color=GREY, size=12)

d.save("conductors-insulators-and-charge-distribution")
print("ok")
