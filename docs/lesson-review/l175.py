import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 856,
      "Field is a vector; potential is a scalar",
      "E = kQ/r² falls off faster than V = kQ/r — and E always points downhill in V",
      "Top left: a point charge with its radial field lines and circular equipotentials, noting that the field lines "
      "cross the equipotentials at right angles. Top right: the same charge's field and potential plotted against "
      "distance, showing the inverse-square fall of E against the slower inverse fall of V. Middle: parallel plates "
      "with a uniform field E = V/d running from the positive plate to the negative one, equipotential planes "
      "between them, and the cell membrane as the biological version. Bottom: a sign table giving, for a positive "
      "and a negative charge released from rest, the direction of the force relative to the field, whether the "
      "potential it moves toward is higher or lower, and the fact that both lose potential energy and gain kinetic "
      "energy.")

# ---------------- Panel A: point charge map ----------------
d.rect(40, 118, 404, 288, BLUE, "none", rx=12, width=2)
d.text(242, 146, "Field lines cross equipotentials at 90°", color=BLUE, weight="bold", size=15)

CX, CY = 242, 282
for r in (36, 62, 88):
    d.circle(CX, CY, r, GOLD, "none", 1.6)
for ang in range(0, 360, 30):
    a = math.radians(ang)
    d.arrow(CX + 16 * math.cos(a), CY + 16 * math.sin(a),
            CX + 104 * math.cos(a), CY + 104 * math.sin(a), BLUE, width=1.4)
d.circle(CX, CY, 15, RED, FILL[RED], 2)
d.text(CX, CY + 7, "+", color=RED, weight="bold", size=20)
d.text(242, 388, "equipotentials (gold) • field lines (blue)", color=GREY, size=13)
d.text(242, 170, "V = kQ/r on each circle", color=GOLD, weight="bold", size=13)

# ---------------- Panel B: E vs V falloff ----------------
d.rect(460, 118, 420, 288, SAGE, "none", rx=12, width=2)
d.text(670, 146, "Same charge, two different fall-offs", color=SAGE, weight="bold", size=15)

m = d.axes(530, 178, 300, 150, "distance r", "fraction of the value at r₀",
           (0, 4.2), (0, 1.08), ticks_x=[1, 2, 3, 4], ticks_y=[0.5, 1])
d.curve(m, [(x / 20, 1.0 / (x / 20) ** 2) for x in range(20, 85)], BLUE, 2.6)
d.curve(m, [(x / 20, 1.0 / (x / 20)) for x in range(20, 85)], GOLD, 2.6)
px, py = m(2.1, 1 / 2.1)
d.text(px + 8, py - 6, "V ∝ 1/r", anchor="start", color=GOLD, weight="bold", size=14)
px, py = m(1.75, 1 / 1.75 ** 2)
d.text(px + 10, py + 18, "E ∝ 1/r²", anchor="start", color=BLUE, weight="bold", size=14)
d.text(670, 388, "at double the distance: E is a quarter, V is a half",
       color=NAVY, weight="bold", size=14)

# ---------------- Panel C: parallel plates ----------------
d.rect(40, 426, 840, 216, GOLD, "none", rx=12, width=2)
d.text(460, 454, "Uniform field: E = V/d, pointing from + plate to − plate",
       color=GOLD, weight="bold", size=16)

PX0, PX1, PTOP, PBOT = 120, 520, 486, 606
d.rect(PX0, PTOP, PX1 - PX0, 10, RED, FILL[RED], rx=2, width=2)
d.rect(PX0, PBOT, PX1 - PX0, 10, NAVY, FILL[NAVY], rx=2, width=2)
d.text(PX0 - 10, PTOP + 10, "+", anchor="end", color=RED, weight="bold", size=22)
d.text(PX0 - 10, PBOT + 12, "−", anchor="end", color=NAVY, weight="bold", size=24)
for x in range(PX0 + 40, PX1, 60):
    d.arrow(x, PTOP + 16, x, PBOT - 4, BLUE, width=1.8)
for yy in (526, 566):
    d.line(PX0 + 12, yy, PX1 - 12, yy, GOLD, 1.4, True)
d.text(PX1 - 40, PTOP - 10, "dashed lines = equipotentials", anchor="end", color=GOLD, weight="bold", size=13)
d.text(320, 628, "d is the plate separation; V is the potential difference",
       color=GREY, size=13)

d.rect(600, 478, 268, 136, BLUE, FILL[BLUE], rx=10, width=2)
d.text(734, 502, "The membrane is this capacitor", color=BLUE, weight="bold", size=14)
d.text(734, 528, "ΔV ≈ 70 mV across d ≈ 8 nm", color=NAVY, weight="bold", size=14)
d.text(734, 554, "E ≈ 10⁷ V/m", color=NAVY, weight="bold", size=17)
d.text(734, 582, "a tiny voltage across a tiny gap", color=GREY, size=12)
d.text(734, 602, "makes an enormous field", color=GREY, size=12)

# ---------------- Panel D: sign table ----------------
d.text(460, 684, "Released from rest, which way does it go?", color=NAVY, weight="bold", size=17)

rows = [("positive charge", "force along E", "moves to LOWER V", RED),
        ("negative charge", "force against E", "moves to HIGHER V", NAVY)]
y = 704
for name, f, v, col in rows:
    d.rect(100, y, 720, 44, col, FILL[col], rx=9, width=2)
    d.text(196, y + 28, name, color=col, weight="bold", size=15)
    d.text(420, y + 28, f, color=NAVY, weight="bold", size=15)
    d.text(640, y + 28, v, color=NAVY, weight="bold", size=15)
    y += 52

d.text(460, 816, "Either way the potential energy drops and the kinetic energy rises", color=GREY, size=14)
d.text(460, 840, "U = qV, so the sign of q decides which V is favourable", color=GREY, size=14)


d.save("field-versus-potential-and-uniform-fields")
print("ok")
