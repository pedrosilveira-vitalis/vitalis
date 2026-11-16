import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 846,
      "A capacitor stores charge; what changes depends on what is held fixed",
      "C = κε₀A/d is pure geometry — the battery decides whether Q or V is the constant",
      "Top: the parallel-plate capacitor with its definition C = Q/V, the geometry formula, the uniform field "
      "E = V/d and the three energy expressions. Middle: the two dielectric scenarios side by side — still "
      "connected to the battery, where V and E hold still while C, Q and U all rise by kappa; and disconnected, "
      "where Q holds still while V, E and U all fall by kappa. Lower middle: capacitors combine the opposite way "
      "to resistors, adding directly in parallel and reciprocally in series, with a worked four and twelve "
      "microfarad pair. Bottom: the membrane as a capacitor, where the insulating gap is the two to three "
      "nanometre hydrophobic core, giving about one microfarad per square centimetre, and myelin lowers the "
      "capacitance by thickening that gap.")

# ---------------- Panel A: the capacitor ----------------
d.rect(40, 126, 840, 190, BLUE, "none", rx=12, width=2)
d.text(460, 154, "The parallel-plate capacitor", color=BLUE, weight="bold", size=17)

PX0, PX1, PTOP, PBOT = 110, 390, 188, 282
d.rect(PX0, PTOP, PX1 - PX0, 10, RED, FILL[RED], rx=2, width=2)
d.rect(PX0, PBOT, PX1 - PX0, 10, NAVY, FILL[NAVY], rx=2, width=2)
d.text(PX0 - 12, PTOP + 12, "+Q", anchor="end", color=RED, weight="bold", size=14)
d.text(PX0 - 12, PBOT + 14, "−Q", anchor="end", color=NAVY, weight="bold", size=14)
for x in range(PX0 + 32, PX1, 48):
    d.arrow(x, PTOP + 16, x, PBOT - 4, BLUE, width=1.6)
d.text(PX1 + 16, 226, "area A", anchor="start", color=GREY, weight="bold", size=13)
d.text(PX1 + 16, 250, "gap d", anchor="start", color=GREY, weight="bold", size=13)

d.text(700, 192, "C = Q/V = κε₀A/d", color=NAVY, weight="bold", size=20)
d.text(700, 222, "E = V/d = σ/ε₀ (uniform)", color=NAVY, weight="bold", size=15)
d.text(700, 252, "U = ½QV = ½CV² = Q²/2C", color=NAVY, weight="bold", size=15)
d.text(700, 282, "C is geometry: it does not depend on Q or V",
       color=GREY, size=13)

# ---------------- Panel B: two dielectric cases ----------------
d.text(460, 352, "Insert a dielectric: which column applies?",
       color=NAVY, weight="bold", size=17)

d.rect(50, 368, 400, 182, SAGE, FILL[SAGE], rx=11, width=2)
d.text(250, 394, "STILL ON THE BATTERY", color=SAGE, weight="bold", size=15)
d.text(250, 414, "V is held fixed", color=GREY, size=13)
rows = [("V", "same"), ("E = V/d", "same"), ("C", "× κ"), ("Q = CV", "× κ"), ("U = ½CV²", "× κ")]
y = 440
for a, b in rows:
    d.text(160, y, a, anchor="end", color=NAVY, weight="bold", size=14)
    d.text(196, y, b, anchor="start", color=SAGE, weight="bold", size=14)
    y += 22

d.rect(470, 368, 400, 182, RED, FILL[RED], rx=11, width=2)
d.text(670, 394, "DISCONNECTED", color=RED, weight="bold", size=15)
d.text(670, 414, "Q is held fixed", color=GREY, size=13)
rows = [("Q", "same"), ("C", "× κ"), ("V = Q/C", "÷ κ"), ("E = V/d", "÷ κ"), ("U = Q²/2C", "÷ κ")]
y = 440
for a, b in rows:
    d.text(580, y, a, anchor="end", color=NAVY, weight="bold", size=14)
    d.text(616, y, b, anchor="start", color=RED, weight="bold", size=14)
    y += 22

d.text(460, 572, "κ > 1 always, so C always rises — but the energy rises only if a battery is there to supply it",
       color=GREY, size=14)

# ---------------- Panel C: series/parallel ----------------
d.rect(40, 596, 400, 150, GOLD, "none", rx=12, width=2)
d.text(240, 624, "Backwards from resistors", color=GOLD, weight="bold", size=16)
d.text(240, 654, "parallel: C = C₁ + C₂", color=NAVY, weight="bold", size=15)
d.text(240, 680, "series: 1/C = 1/C₁ + 1/C₂", color=NAVY, weight="bold", size=15)
d.text(240, 712, "4 µF with 12 µF → 16 µF parallel, 3 µF series",
       color=GOLD, weight="bold", size=13)
d.text(240, 734, "series capacitors all carry the same Q", color=GREY, size=12)

# ---------------- Panel D: membrane ----------------
d.rect(466, 596, 414, 150, BLUE, "none", rx=12, width=2)
d.text(673, 624, "The membrane capacitor", color=BLUE, weight="bold", size=16)
d.rect(506, 640, 334, 13, GOLD, FILL[GOLD], rx=3, width=1.5)
d.rect(506, 653, 334, 22, GREY, "#e9e4da", rx=0, width=1.5)
d.rect(506, 675, 334, 13, GOLD, FILL[GOLD], rx=3, width=1.5)
d.text(673, 669, "hydrophobic core ≈ 2–3 nm, κ ≈ 2–3", color=NAVY, weight="bold", size=13)
d.text(673, 708, "C/A ≈ 1 µF/cm²  •  70 mV across it ≈ 10⁷ V/m",
       color=BLUE, weight="bold", size=14)
d.text(673, 732, "myelin thickens the gap, so C falls and signals travel faster",
       color=GREY, size=12)

d.text(460, 790, "Charge is what is conserved when charged capacitors are disconnected and rewired",
       color=NAVY, weight="bold", size=16)
d.text(460, 820, "— voltage is not, so find the total Q first, then divide by the new total C",
       color=GREY, size=14)

d.save("capacitance-dielectrics-and-the-two-cases")
print("ok")
