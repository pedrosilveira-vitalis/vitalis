import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 770,
      "Power, efficiency, and where the missing energy went",
      "Efficiency divides: the input is always larger than the useful output",
      "Left: an energy-flow bar for a muscle at 25 percent efficiency, with 2000 joules of chemical energy entering "
      "and splitting into 500 joules of useful work and 1500 joules of heat. Right: the four power formulas, with the "
      "note that at constant velocity the applied force equals the opposing force. Bottom: the efficiency equation "
      "with the warning to divide rather than multiply, the multiplication rule for stages in series, and the power "
      "dissipated by friction together with the terminal-velocity case.")

# ---------------- Panel A: energy flow ----------------
d.rect(40, 112, 430, 322, SAGE, "none", rx=12, width=2)
d.text(255, 142, "Where the input goes:  η = 25% muscle", color=SAGE, weight="bold", size=17)

d.rect(66, 214, 132, 120, NAVY, FILL[NAVY], rx=6, width=2)
d.text(132, 268, "2000 J", color=NAVY, weight="bold", size=17)
d.text(132, 292, "chemical in", color=GREY, size=13)
d.text(132, 200, "100%", color=NAVY, weight="bold", size=14)

d.arrow(198, 240, 240, 240, SAGE, width=3)
d.arrow(198, 300, 240, 300, RED, width=3)

d.rect(244, 214, 186, 30, SAGE, FILL[SAGE], rx=6, width=2)
d.text(337, 235, "500 J useful work  —  25%", color=SAGE, weight="bold", size=15)

d.rect(244, 256, 186, 78, RED, FILL[RED], rx=6, width=2)
d.text(337, 288, "1500 J heat  —  75%", color=RED, weight="bold", size=16)
d.text(337, 312, "raises body temperature", color=GREY, size=12)

d.text(255, 368, "W_in = W_useful / η = 500 / 0.25 = 2000 J", color=NAVY, weight="bold", size=16)
d.text(255, 394, "heat = W_in − W_useful = 1500 J", color=GREY, size=15)
d.text(255, 418, "muscle ≈ 25%  •  heart ≈ 15–25%  •  whole body ≈ 20–25%", color=GREY, size=14)

# ---------------- Panel B: power formulas ----------------
d.rect(486, 112, 394, 322, BLUE, "none", rx=12, width=2)
d.text(683, 142, "Four ways to write power", color=BLUE, weight="bold", size=17)

rows = [("P = W / t", "work done per second — use for average power"),
        ("P = F v", "constant force along the motion — instantaneous"),
        ("P = ΔP · Q", "a pump: pressure rise × volume flow rate"),
        ("P = fₖ v", "the rate friction turns motion into heat")]
y = 170
for eq, note in rows:
    d.rect(506, y, 356, 52, BLUE, FILL[BLUE], rx=9, width=2)
    d.text(524, y + 22, eq, anchor="start", color=NAVY, weight="bold", size=17)
    d.text(524, y + 42, note, anchor="start", color=GREY, size=13)
    y += 58

d.text(683, 420, "At constant v the net force is zero, so F_applied = F_opposing",
       color=BLUE, weight="bold", size=14)

# ---------------- Bottom: three rules ----------------
box = [(40, "Divide, never multiply", RED,
        ["η = W_out / W_in = P_out / P_in", "so W_in = W_out / η", "η < 1 always ⇒ input > output"]),
       (320, "Stages multiply", GOLD,
        ["η_total = η₁ × η₂ × …", "0.80 × 0.80 = 0.64", "losses compound fast"]),
       (600, "Nothing is destroyed", SAGE,
        ["W_nc = ΔKE + ΔPE", "friction → heat in the surfaces", "drag → heat in the fluid"])]
for x, head, col, lines in box:
    d.rect(x, 462, 280, 150, col, FILL[col], rx=10, width=2)
    d.text(x + 140, 492, head, color=col, weight="bold", size=16)
    for i, ln in enumerate(lines):
        d.text(x + 140, 524 + i * 30, ln, color=NAVY if i == 0 else GREY,
               weight="bold" if i == 0 else None, size=15 if i == 0 else 14)

d.text(460, 660, "At terminal velocity mg = F_drag, so gravity's power mgv goes entirely to heating the air",
       color=NAVY, weight="bold", size=16)
d.text(460, 692, "Energy is joules, power is joules per second — if a \"power\" answer comes out in J, a ÷t is missing",
       color=GREY, size=15)
d.text(460, 724, "1 hp ≈ 746 W   •   1 kWh = 3.6 × 10⁶ J (an energy, not a power)",
       color=GREY, size=15)

d.save("power-efficiency-and-dissipation")
print("ok")
