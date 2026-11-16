import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 830,
      "Two slits add; one slit cancels; a film does both",
      "Path difference decides everything — count wavelengths, and count phase flips",
      "Top left: the double-slit pattern, with bright fringes where the path difference is a whole number of "
      "wavelengths and the spacing lambda L over d. Top right: single-slit diffraction, where a sine theta equals m "
      "lambda gives the dark fringes and a narrower slit spreads the central maximum wider. Bottom left: thin-film "
      "interference, with the rule that a reflection off a higher-index medium flips the phase, and the two cases "
      "that follow. Bottom right: polarization, with Malus's law, Brewster's angle, and the vertical transmission "
      "axis of sunglasses blocking horizontally polarized glare.")

# ---------------- Panel A: double slit ----------------
d.rect(40, 112, 416, 300, BLUE, "none", rx=12, width=2)
d.text(248, 142, "Two slits: maxima at d sinθ = mλ", color=BLUE, weight="bold", size=17)

SX = 110
d.line(SX, 180, SX, 330, NAVY, 4)
for yy in (232, 278):
    d.line(SX, yy - 9, SX, yy + 9, "#faf6ee", 5)
d.text(SX - 14, 205, "d", anchor="end", color=NAVY, weight="bold", size=14)
d.line(SX - 6, 232, SX - 6, 278, NAVY, 1.5)

SCX = 400
d.line(SCX, 174, SCX, 340, GREY, 3)
for m, yy in [(2, 186), (1, 218), (0, 255), (1, 292), (2, 324)]:
    w = 15 - m * 4
    d.rect(SCX - 3, yy - w / 2, 10, w, GOLD, GOLD, rx=1, width=0)
    d.text(SCX + 22, yy + 4, f"m={m}", anchor="start", color=GREY, size=11)
for yy in (232, 278):
    for ty in (186, 218, 255, 292, 324):
        d.line(SX, yy, SCX, ty, BLUE, 0.6)

d.text(248, 362, "Δy = λL/d: longer λ or bigger L spreads the fringes",
       color=NAVY, weight="bold", size=14)
d.text(248, 386, "dark where the path difference is (m + ½)λ", color=GREY, size=13)

# ---------------- Panel B: single slit ----------------
d.rect(472, 112, 408, 300, GOLD, "none", rx=12, width=2)
d.text(676, 142, "One slit: minima at a sinθ = mλ", color=GOLD, weight="bold", size=17)


def sinc_pattern(cx, cy, half, scale, col, lab):
    pts = []
    for i in range(-80, 81):
        u = i / 80 * half
        x = cx + u
        arg = (i / 80) * scale
        val = 1.0 if abs(arg) < 1e-6 else (math.sin(math.pi * arg) / (math.pi * arg)) ** 2
        pts.append((x, cy - 64 * val))
    d.path("M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts), col, 2.5)
    d.line(cx - half, cy, cx + half, cy, GREY, 1.2)
    d.text(cx, cy + 20, lab, color=col, weight="bold", size=13)


sinc_pattern(590, 282, 86, 3.2, NAVY, "wide slit")
sinc_pattern(782, 282, 86, 1.6, RED, "half as wide")

d.text(676, 330, "halve the slit and the central maximum doubles in width",
       color=NAVY, weight="bold", size=14)
d.rect(492, 344, 376, 54, GOLD, FILL[GOLD], rx=9, width=2)
d.text(676, 366, "Resolution: θ_min = 1.22 λ/D", color=NAVY, weight="bold", size=15)
d.text(676, 388, "a bigger aperture resolves finer detail", color=GREY, size=13)

# ---------------- Panel C: thin film ----------------
d.rect(40, 432, 416, 246, SAGE, "none", rx=12, width=2)
d.text(248, 460, "Thin films: count the phase flips", color=SAGE, weight="bold", size=17)

FY, FH = 506, 44
d.rect(96, FY, 264, FH, SAGE, FILL[SAGE], rx=0, width=2)
d.text(228, FY - 10, "n_film", color=SAGE, weight="bold", size=13)
d.text(70, FY + 26, "t", anchor="end", color=NAVY, weight="bold", size=14)
d.arrow(150, FY - 40, 178, FY - 2, NAVY, width=2)
d.arrow(178, FY - 2, 206, FY - 40, RED, width=2)
d.text(214, FY - 34, "flip", anchor="start", color=RED, weight="bold", size=12)
d.arrow(178, FY + 2, 236, FY + FH - 2, GREY, width=1.6)
d.arrow(236, FY + FH - 2, 294, FY + 2, GREY, width=1.6)
d.text(300, FY + 12, "no flip", anchor="start", color=GREY, weight="bold", size=12)

d.rect(62, 574, 180, 56, RED, FILL[RED], rx=9, width=2)
d.text(152, 596, "one flip", color=RED, weight="bold", size=14)
d.text(152, 618, "bright: 2nt = (m+½)λ", color=NAVY, weight="bold", size=13)
d.rect(254, 574, 180, 56, BLUE, FILL[BLUE], rx=9, width=2)
d.text(344, 596, "zero or two flips", color=BLUE, weight="bold", size=14)
d.text(344, 618, "bright: 2nt = mλ", color=NAVY, weight="bold", size=13)

d.text(248, 656, "the n belongs in the path: inside the film λ shrinks to λ/n",
       color=GREY, size=13)

# ---------------- Panel D: polarization ----------------
d.rect(472, 432, 408, 246, RED, "none", rx=12, width=2)
d.text(676, 460, "Polarization", color=RED, weight="bold", size=17)

d.text(676, 490, "I = I₀ cos²θ   •   unpolarized first ⇒ I₀/2",
       color=NAVY, weight="bold", size=15)
d.text(676, 516, "tan θ_B = n₂/n₁: reflection at Brewster's angle comes back",
       color=GREY, size=13)
d.text(676, 536, "polarized parallel to the surface — horizontal off water",
       color=GREY, size=13)

d.rect(500, 556, 360, 62, BLUE, FILL[BLUE], rx=9, width=2)
d.text(680, 578, "So sunglasses transmit the vertical component:", color=BLUE, weight="bold", size=13)
d.text(680, 600, "a vertical axis is what blocks horizontal glare", color=NAVY, weight="bold", size=14)

d.text(676, 646, "Chiral molecules rotate the plane — the basis of polarimetry",
       color=GREY, size=13)

d.text(460, 716, "E = hf = hc/λ: shorter wavelength, more energy per photon",
       color=NAVY, weight="bold", size=16)
d.text(460, 748, "UV-B (280–315 nm) makes thymine dimers; UV-A ages skin through reactive oxygen",
       color=GREY, size=15)
d.text(460, 778, "Single slit a sinθ = mλ gives DARK fringes; double slit d sinθ = mλ gives BRIGHT ones",
       color=RED, weight="bold", size=15)
d.text(460, 808, "Everything travels at c in vacuum; in glass the index, and so the speed, depends on λ",
       color=GREY, size=15)

d.save("interference-diffraction-and-polarization")
print("ok")
