import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 800,
      "Where the object sits decides what the image is",
      "One equation, 1/f = 1/dₒ + 1/dᵢ, and one sign rule cover every lens and mirror",
      "Top: five object positions for a converging lens or concave mirror — beyond 2f, at 2f, between f and 2f, at f "
      "and inside f — each with the image it produces, from real inverted and diminished through to virtual upright "
      "and magnified. Bottom left: the single rule for diverging lenses and convex mirrors, always virtual, upright "
      "and diminished. Bottom right: the two corrective-lens calculations, a myopic far point giving a negative "
      "dioptre power and a hyperopic near point giving a positive one.")

# ---------------- Panel A: the five positions ----------------
d.rect(40, 112, 840, 290, BLUE, "none", rx=12, width=2)
d.text(460, 142, "Converging lens or concave mirror", color=BLUE, weight="bold", size=17)

cards = [("beyond 2f", "between f and 2f", "real • inverted", "diminished", SAGE),
         ("at 2f", "at 2f", "real • inverted", "same size", SAGE),
         ("between f and 2f", "beyond 2f", "real • inverted", "magnified", GOLD),
         ("at f", "at infinity", "no image", "rays leave parallel", GREY),
         ("inside f", "same side", "virtual • upright", "magnified", RED)]
x = 62
for where, img, kind, size, col in cards:
    d.rect(x, 172, 156, 150, col, FILL[col], rx=10, width=2)
    d.text(x + 78, 198, "object", color=GREY, size=12)
    d.text(x + 78, 220, where, color=col, weight="bold", size=14)
    d.line(x + 24, 236, x + 132, 236, col, 1.5, True)
    d.text(x + 78, 258, img, color=NAVY, weight="bold", size=13)
    d.text(x + 78, 282, kind, color=NAVY, size=13)
    d.text(x + 78, 304, size, color=GREY, size=12)
    x += 168

d.text(460, 352, "m = −dᵢ/dₒ:  negative means inverted, |m| > 1 means magnified",
       color=NAVY, weight="bold", size=15)
d.text(460, 378, "dᵢ > 0 is a real image — light actually goes there and a screen would catch it",
       color=GREY, size=14)

# ---------------- Panel B: the always-rule ----------------
d.rect(40, 422, 416, 232, SAGE, "none", rx=12, width=2)
d.text(248, 450, "Diverging lens, convex mirror", color=SAGE, weight="bold", size=17)

AX = 540
d.line(96, AX, 400, AX, GREY, 1.5, True)
LX = 268
d.path(f"M{LX - 11} {AX - 52} Q{LX} {AX} {LX - 11} {AX + 52} L{LX + 11} {AX + 52} Q{LX} {AX} {LX + 11} {AX - 52} Z",
       SAGE, 2.5, FILL[SAGE])
d.arrow(150, AX, 150, AX - 44, NAVY, width=2.5)
d.text(150, AX - 52, "object", color=NAVY, weight="bold", size=12)
d.arrow(228, AX, 228, AX - 20, RED, width=2.5)
d.text(228, AX - 28, "image", color=RED, weight="bold", size=12)
d.line(150, AX - 44, LX, AX - 30, NAVY, 1.6)
d.line(LX, AX - 30, 392, AX - 6, NAVY, 1.6)
d.line(228, AX - 20, 392, AX - 6, GREY, 1.4, True)

d.text(248, 606, "always virtual • upright • diminished", color=SAGE, weight="bold", size=16)
d.text(248, 630, "whatever the object distance, f < 0 and the image sits inside f",
       color=GREY, size=13)

# ---------------- Panel C: corrections ----------------
d.rect(472, 422, 408, 232, GOLD, "none", rx=12, width=2)
d.text(676, 450, "Two prescriptions, one equation", color=GOLD, weight="bold", size=17)

d.rect(492, 470, 376, 76, BLUE, FILL[BLUE], rx=9, width=2)
d.text(676, 492, "Myopia — distance vision", color=BLUE, weight="bold", size=15)
d.text(676, 514, "object at ∞, image at the far point (virtual)", color=GREY, size=13)
d.text(676, 536, "far point 50 cm  ⇒  P = 1/(−0.50) = −2.0 D", color=NAVY, weight="bold", size=15)

d.rect(492, 556, 376, 84, RED, FILL[RED], rx=9, width=2)
d.text(676, 578, "Hyperopia / presbyopia — reading", color=RED, weight="bold", size=15)
d.text(676, 600, "object at 25 cm, image at the near point (virtual)", color=GREY, size=13)
d.text(676, 622, "near point 100 cm  ⇒  P = 1/0.25 + 1/(−1.00) = +3.0 D",
       color=NAVY, weight="bold", size=15)

d.text(460, 694, "P = 1/f in dioptres with f in metres, and lenses in contact simply add",
       color=NAVY, weight="bold", size=16)
d.text(460, 726, "The eye runs about +60 D, roughly +43 D of it from the cornea alone",
       color=GREY, size=15)
d.text(460, 756, "Accommodation: ciliary muscle contracts, zonules slacken, the lens fattens, P rises",
       color=GREY, size=15)
d.text(460, 786, "Far point fixes distance correction; near point fixes reading correction",
       color=GREY, size=15)

d.save("image-positions-and-prescriptions")
print("ok")
