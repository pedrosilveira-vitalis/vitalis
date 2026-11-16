import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 840,
      "Bend toward the normal going in, away coming out",
      "n₁sinθ₁ = n₂sinθ₂, and past the critical angle nothing gets out at all",
      "Top left: a ray crossing from air into water, bending toward the normal, with Snell's law and the critical "
      "angle condition for the reverse direction. Top right: a converging lens with a parallel ray through the far "
      "focus and a ray straight through the centre, meeting at a real inverted image, with the thin lens equation. "
      "Bottom left: the sign conventions for lenses and mirrors. Bottom right: myopia, where light focuses in front "
      "of the retina and needs a diverging lens, against hyperopia, where it focuses behind and needs a converging "
      "lens.")

# ---------------- Panel A: refraction ----------------
d.rect(40, 112, 416, 318, BLUE, "none", rx=12, width=2)
d.text(248, 142, "Refraction at an interface", color=BLUE, weight="bold", size=17)

IY, IX = 252, 236
d.line(76, IY, 420, IY, NAVY, 3)
d.rect(76, IY, 344, 62, BLUE, FILL[BLUE], rx=0, width=0)
d.line(IX, IY - 66, IX, IY + 70, GREY, 1.5, True)
d.text(IX + 8, IY - 60, "normal", anchor="start", color=GREY, size=12)

d.arrow(IX - 84, IY - 62, IX - 6, IY - 4, NAVY, width=2.5)
d.arrow(IX + 4, IY + 4, IX + 40, IY + 62, NAVY, width=2.5)
d.text(IX - 44, IY - 20, "θ₁", color=NAVY, weight="bold", size=15)
d.text(IX + 14, IY + 40, "θ₂", color=NAVY, weight="bold", size=15)
d.text(96, IY - 16, "n₁ = 1.00  (air)", anchor="start", color=GREY, weight="bold", size=13)
d.text(96, IY + 24, "n₂ = 1.33  (water)", anchor="start", color=NAVY, weight="bold", size=13)
d.text(400, IY - 16, "slower below ⇒", anchor="end", color=GREY, size=12)
d.text(400, IY + 24, "bent toward the normal", anchor="end", color=NAVY, weight="bold", size=12)

d.rect(62, 334, 372, 82, RED, FILL[RED], rx=9, width=2)
d.text(248, 358, "Going the other way, there is a limit", color=RED, weight="bold", size=15)
d.text(248, 382, "sin θ_c = n₂/n₁   (only when n₁ > n₂)", color=NAVY, weight="bold", size=15)
d.text(248, 404, "glass–air 42°  •  water–air 49°  •  diamond–air 24°", color=GREY, size=13)

# ---------------- Panel B: the lens ----------------
d.rect(472, 112, 408, 318, SAGE, "none", rx=12, width=2)
d.text(676, 142, "Two rays locate the image", color=SAGE, weight="bold", size=17)

AX = 258
d.line(508, AX, 862, AX, GREY, 1.5, True)
LX = 700
d.path(f"M{LX} {AX - 58} Q{LX + 16} {AX} {LX} {AX + 58} Q{LX - 16} {AX} {LX} {AX - 58} Z",
       SAGE, 2.5, FILL[SAGE])
for fx, lab in ((650, "F"), (750, "F")):
    d.circle(fx, AX, 3.5, NAVY, NAVY)
    d.text(fx, AX + 20, lab, color=NAVY, weight="bold", size=13)

OX, OH = 580, 40
d.arrow(OX, AX, OX, AX - OH, NAVY, width=2.5)
d.text(OX - 10, AX - OH - 8, "object", anchor="end", color=NAVY, weight="bold", size=13)

d.line(OX, AX - OH, LX, AX - OH, RED, 2)
d.line(LX, AX - OH, 786, AX + 29, RED, 2)
d.line(OX, AX - OH, 786, AX + 29, BLUE, 2)
d.arrow(786, AX, 786, AX + 29, NAVY, width=2.5)
d.text(800, AX + 26, "real, inverted", anchor="start", color=NAVY, weight="bold", size=12)

d.text(676, 372, "1/dₒ + 1/dᵢ = 1/f   •   m = −dᵢ/dₒ", color=NAVY, weight="bold", size=16)
d.text(676, 398, "object inside f ⇒ virtual, upright, enlarged: a magnifier",
       color=GREY, size=14)
d.text(676, 420, "P = 1/f in dioptres, and lenses in contact add their P",
       color=GREY, size=14)

# ---------------- Panel C: sign conventions ----------------
d.rect(40, 450, 416, 214, GOLD, "none", rx=12, width=2)
d.text(248, 478, "Signs, once and consistently", color=GOLD, weight="bold", size=17)

rows = [("f > 0", "converging lens, concave mirror"),
        ("f < 0", "diverging lens, convex mirror"),
        ("dᵢ > 0", "real image — far side of a lens, front of a mirror"),
        ("dᵢ < 0", "virtual image — same side as the object"),
        ("m < 0", "inverted;  |m| > 1 enlarged")]
y = 506
for sym, meaning in rows:
    d.text(74, y, sym, anchor="start", color=GOLD, weight="bold", size=15)
    d.text(154, y, meaning, anchor="start", color=NAVY, size=13)
    y += 30

d.text(248, 650, "Angles are always measured from the normal, never the surface",
       color=RED, weight="bold", size=13)

# ---------------- Panel D: the eye ----------------
d.rect(472, 450, 408, 214, RED, "none", rx=12, width=2)
d.text(676, 478, "Where the focus lands", color=RED, weight="bold", size=17)


def eye(cx, cy, focus_dx, label, fix, col):
    d.circle(cx, cy, 36, GREY, "#ffffff", width=2)
    d.path(f"M{cx + 26} {cy - 24} A36 36 0 0 1 {cx + 26} {cy + 24}", RED, 3)
    d.line(cx - 76, cy - 16, cx - 36, cy - 10, NAVY, 2)
    d.line(cx - 76, cy + 16, cx - 36, cy + 10, NAVY, 2)
    fx = cx + focus_dx
    d.line(cx - 36, cy - 10, fx, cy, NAVY, 2)
    d.line(cx - 36, cy + 10, fx, cy, NAVY, 2)
    d.circle(fx, cy, 4, col, col)
    d.text(cx, cy + 58, label, color=col, weight="bold", size=14)
    d.text(cx, cy + 78, fix, color=NAVY, size=13)


eye(580, 536, 8, "myopia: eye too long", "needs a diverging lens", BLUE)
eye(782, 536, 48, "hyperopia: eye too short", "needs a converging lens", GOLD)
d.text(676, 648, "cornea ≈ 40–44 D of the eye's ≈ 60 D; the lens accommodates",
       color=GREY, size=13)

d.text(460, 702, "Frequency never changes at a boundary; λ and v do, with λ = λ₀/n",
       color=NAVY, weight="bold", size=16)
d.text(460, 734, "Violet bends more than red: higher n at shorter wavelength — that is dispersion",
       color=GREY, size=15)
d.text(460, 764, "Total internal reflection runs the endoscope and makes the diamond sparkle",
       color=GREY, size=15)
d.text(460, 794, "A flat mirror: virtual, upright, same size, as far behind as the object is in front",
       color=GREY, size=15)

d.save("snell-lenses-and-the-eye")
print("ok")
