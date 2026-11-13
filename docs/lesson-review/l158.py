import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 780,
      "Work: the sign comes from the angle, the total comes from every force",
      "W = Fd cos θ for each force, then W_net = ΔKE",
      "Top left: three cases showing a force at less than 90 degrees to the displacement doing positive work, at "
      "90 degrees doing zero work, and at more than 90 degrees doing negative work. Top right: a worked tally for a "
      "2 kg object pushed 5 m, with 43.3 joules from the applied force, minus 15 joules from friction and zero from "
      "the normal force and gravity, summing to 28.3 joules of net work and the same change in kinetic energy. "
      "Bottom: four forces that do no work, and the split between conservative and non-conservative forces.")

# ---------------- Panel A: sign of the work ----------------
d.rect(40, 112, 412, 344, BLUE, "none", rx=12, width=2)
d.text(246, 142, "The angle sets the sign", color=BLUE, weight="bold", size=17)

cases = [("θ < 90°", "cos θ > 0", "W > 0: speeds it up", SAGE, -40),
         ("θ = 90°", "cos θ = 0", "W = 0: no energy moved", GREY, -90),
         ("θ > 90°", "cos θ < 0", "W < 0: slows it down", RED, -140)]
y = 172
for label, cosline, note, col, deg in cases:
    d.rect(58, y, 376, 72, col, FILL[col], rx=9, width=2)
    bx, by = 136, y + 46
    d.arrow(bx - 44, by, bx + 44, by, NAVY, width=2.5)
    d.text(bx - 22, by + 19, "d", color=NAVY, weight="bold", size=14)
    ang = math.radians(deg)
    d.arrow(bx, by, bx + 52 * math.cos(ang), by + 52 * math.sin(ang), col, width=3)
    d.text(bx + 66 * math.cos(ang), by + 66 * math.sin(ang) + 4, "F", color=col, weight="bold", size=15)
    d.text(240, y + 24, label, anchor="start", color=col, weight="bold", size=16)
    d.text(240, y + 44, cosline, anchor="start", color=GREY, size=14)
    d.text(240, y + 64, note, anchor="start", color=NAVY, size=14)
    y += 82

d.text(246, 436, "W = F d cos θ   — a scalar, in joules", color=NAVY, weight="bold", size=16)

# ---------------- Panel B: the tally ----------------
d.rect(468, 112, 412, 344, GOLD, "none", rx=12, width=2)
d.text(674, 142, "Add every force's work, then use ΔKE", color=GOLD, weight="bold", size=17)
d.text(674, 166, "2 kg object, pushed 5 m: F = 10 N at 30°, fₖ = 3 N", color=GREY, size=14)

tally = [("applied, 10 N at 30°", "(10)(5)cos30° = +43.3 J", NAVY),
         ("kinetic friction, 3 N", "(3)(5)cos180° = −15.0 J", RED),
         ("normal force", "θ = 90° ⇒ 0 J", GREY),
         ("gravity", "θ = 90° ⇒ 0 J", GREY)]
y = 188
for label, val, col in tally:
    d.text(492, y + 22, label, anchor="start", color=col, size=15)
    d.text(858, y + 22, val, anchor="end", color=col, weight="bold", size=15)
    y += 36
d.line(492, 340, 858, 340, GOLD, 2)
d.text(492, 366, "W_net", anchor="start", color=NAVY, weight="bold", size=16)
d.text(858, 366, "+28.3 J", anchor="end", color=NAVY, weight="bold", size=16)
d.rect(492, 384, 366, 44, SAGE, FILL[SAGE], rx=9, width=2)
d.text(675, 412, "W_net = ΔKE = ½mvᶠ² − ½mvᵢ²", color=NAVY, weight="bold", size=16)

# ---------------- Panel C: zero-work forces ----------------
d.text(60, 486, "Four forces that move no energy at all", anchor="start",
       color=GREY, weight="bold", size=17)

zero = [("normal force", "⊥ to the slide, on a flat floor,\nan incline or a curved track"),
        ("centripetal force", "⊥ to v at every instant,\nso speed never changes"),
        ("holding a weight still", "force but no displacement,\nso W = 0 however tiring"),
        ("magnetic force on a charge", "qv × B is ⊥ to v,\nso it only turns the path")]
x = 40
for head, body in zero:
    d.rect(x, 508, 200, 116, GREY, FILL[GREY], rx=10, width=2)
    d.text(x + 100, 536, head, color=NAVY, weight="bold", size=15)
    for i, ln in enumerate(body.split("\n")):
        d.text(x + 100, 566 + i * 22, ln, color=GREY, size=13)
    x += 213

d.rect(40, 646, 412, 104, SAGE, FILL[SAGE], rx=10, width=2)
d.text(246, 674, "Conservative: path does not matter", color=SAGE, weight="bold", size=16)
d.text(246, 700, "gravity, springs, electrostatic", color=NAVY, size=15)
d.text(246, 728, "W = −ΔPE, so define U = mgh or ½kx²", color=GREY, size=14)

d.rect(468, 646, 412, 104, RED, FILL[RED], rx=10, width=2)
d.text(674, 674, "Non-conservative: path matters", color=RED, weight="bold", size=16)
d.text(674, 700, "friction, drag, applied pushes", color=NAVY, size=15)
d.text(674, 728, "W_nc = ΔKE + ΔPE", color=GREY, size=14)

d.save("work-sign-tally-and-zero-work")
print("ok")
