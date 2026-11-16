import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 824,
      "The magnetic force turns a charge but never speeds it up",
      "F = qvB sinθ, always perpendicular to v — so it does no work, only curves the path",
      "Top left: the right-hand rule, with fingers along v, curling toward B, and the thumb giving the force on a "
      "positive charge, reversed for a negative one, plus the reminder that the force vanishes when v is parallel "
      "to B and is largest when they are perpendicular. Top right: a charge entering a field perpendicular to it "
      "and going in a circle of radius r = mv/qB, with the period T = 2 pi m over qB that does not depend on the "
      "speed. Middle: a table contrasting the electric force, which acts on any charge, points along E and does "
      "work, with the magnetic force, which acts only on moving charges, points perpendicular to both v and B, and "
      "does none. Bottom: two parallel wires attracting when their currents run the same way and repelling when "
      "they oppose, with the field of a long wire, and the mass spectrometer, where the heavier isotope sweeps "
      "the wider arc.")

# ---------------- Panel A: right-hand rule ----------------
d.rect(40, 126, 420, 262, BLUE, "none", rx=12, width=2)
d.text(250, 154, "Direction: fingers v, curl to B, thumb F", color=BLUE, weight="bold", size=15)

OX, OY = 190, 268
d.arrow(OX, OY, OX + 118, OY, NAVY, width=2.6)
d.text(OX + 128, OY + 5, "v", anchor="start", color=NAVY, weight="bold", size=17)
d.arrow(OX, OY, OX, OY - 92, SAGE, width=2.6)
d.text(OX + 8, OY - 100, "B", anchor="start", color=SAGE, weight="bold", size=17)
d.arrow(OX, OY, OX - 66, OY + 62, RED, width=2.6)
d.text(OX - 80, OY + 40, "F on +q", anchor="end", color=RED, weight="bold", size=15)
d.circle(OX, OY, 6, NAVY, NAVY)

d.text(250, 352, "for a negative charge, point the thumb the other way",
       color=RED, weight="bold", size=13)
d.text(250, 376, "v ∥ B ⇒ F = 0   •   v ⊥ B ⇒ F = qvB (largest)",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel B: circular motion ----------------
d.rect(476, 126, 404, 262, GOLD, "none", rx=12, width=2)
d.text(678, 154, "Perpendicular entry ⇒ a circle", color=GOLD, weight="bold", size=15)

CX, CY, R = 640, 262, 62
d.circle(CX, CY, R, GOLD, "none", 2.4)
d.circle(CX, CY, 4, GREY, GREY)
d.line(CX, CY, CX + R, CY, GREY, 1.6, True)
d.text(CX + R / 2, CY - 8, "r", color=GREY, weight="bold", size=14)
d.circle(CX, CY - R, 9, RED, FILL[RED], 2)
d.arrow(CX + 6, CY - R - 14, CX + 54, CY - R - 14, NAVY, width=2)
d.text(CX + 30, CY - R - 22, "v", color=NAVY, weight="bold", size=14)
d.arrow(CX, CY - R + 12, CX, CY - 14, RED, width=2)
d.text(CX + 10, CY - R + 34, "F", anchor="start", color=RED, weight="bold", size=14)
for xx in range(560, 741, 30):
    for yy in range(200, 331, 32):
        d.text(xx, yy, "×", color=SAGE, size=11)
d.text(768, 206, "B into", anchor="start", color=SAGE, weight="bold", size=12)
d.text(768, 224, "the page", anchor="start", color=SAGE, weight="bold", size=12)

d.text(678, 348, "r = mv/qB  •  T = 2πm/qB", color=NAVY, weight="bold", size=17)
d.text(678, 374, "the period does not depend on speed or radius", color=GREY, size=13)

# ---------------- Panel C: comparison table ----------------
d.rect(40, 408, 840, 196, NAVY, "none", rx=12, width=2)
d.text(460, 436, "Electric force against magnetic force", color=NAVY, weight="bold", size=16)

rows = [("acts on", "any charge, moving or not", "only a moving charge"),
        ("direction", "along E", "⊥ to both v and B"),
        ("does work?", "yes — changes speed", "never — speed is constant"),
        ("turns it?", "yes", "yes")]
d.text(250, 464, "F = qE", color=BLUE, weight="bold", size=15)
d.text(690, 464, "F = qvB sinθ", color=RED, weight="bold", size=15)
y = 492
for lab, e, m_ in rows:
    d.text(148, y, lab, anchor="end", color=GREY, size=13)
    d.text(250, y, e, color=BLUE, weight="bold", size=13)
    d.text(690, y, m_, color=RED, weight="bold", size=13)
    y += 26
d.text(460, 592, "so a magnetic field alone can never change a particle's kinetic energy",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel D: wires ----------------
d.rect(40, 624, 404, 176, SAGE, "none", rx=12, width=2)
d.text(242, 652, "Two parallel wires", color=SAGE, weight="bold", size=15)

for x0, lab, col, up in [(120, "same way", SAGE, True), (310, "opposite", RED, False)]:
    d.line(x0 - 26, 672, x0 - 26, 744, GREY, 3)
    d.line(x0 + 26, 672, x0 + 26, 744, GREY, 3)
    d.arrow(x0 - 26, 700, x0 - 26, 678, NAVY, width=2)
    d.arrow(x0 + 26, 700, x0 + 26, 678 if up else 722, NAVY, width=2)
    if up:
        d.arrow(x0 - 16, 756, x0 - 2, 756, col, width=2)
        d.arrow(x0 + 16, 756, x0 + 2, 756, col, width=2)
    else:
        d.arrow(x0 - 2, 756, x0 - 18, 756, col, width=2)
        d.arrow(x0 + 2, 756, x0 + 18, 756, col, width=2)
    d.text(x0, 782, lab + (": attract" if up else ": repel"), color=col, weight="bold", size=13)

# ---------------- Panel E: mass spec ----------------
d.rect(466, 624, 414, 176, RED, "none", rx=12, width=2)
d.text(673, 652, "Mass spectrometer", color=RED, weight="bold", size=15)
d.line(520, 764, 860, 764, GREY, 2)
d.circle(520, 764, 5, NAVY, NAVY)
for rr, col, lab in [(44, BLUE, "lighter"), (70, RED, "heavier")]:
    d.path(f"M520 764 A {rr} {rr} 0 0 1 {520 + 2 * rr} 764", col, 2.4)
    d.text(520 + rr, 764 - rr + 18, lab, color=col, weight="bold", size=12)
d.text(673, 786, "r = mv/qB, so the heavier ion lands further along",
       color=GREY, size=13)
d.text(673, 680, "velocity selector first: qE = qvB ⇒ v = E/B",
       color=NAVY, weight="bold", size=13)

d.save("magnetic-force-right-hand-rule-and-circular-motion")
print("ok")
