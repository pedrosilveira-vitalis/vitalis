import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 640,
      "The galvanic cell, and which way everything moves",
      "Electrons go one way through the wire; ions go the other way through the salt bridge. Both loops have to close.",
      "A zinc-copper galvanic cell. On the left the zinc anode sits in zinc sulfate solution and is "
      "labelled negative, the site of oxidation, and losing mass. On the right the copper cathode sits "
      "in copper sulfate solution and is labelled positive, the site of reduction, and gaining mass. A "
      "wire across the top carries electrons from left to right through a voltmeter reading 1.10 volts, "
      "and a salt bridge below carries anions left into the anode compartment and cations right into "
      "the cathode compartment. A panel below gives the cell notation and the conventions.")

# beakers
for x0, col, sol in ((110, BLUE, "Zn²⁺ solution"), (530, RED, "Cu²⁺ solution")):
    d.path("M %d 220 L %d 400 Q %d 420 %d 420 L %d 420 Q %d 420 %d 400 L %d 220"
           % (x0, x0, x0, x0 + 20, x0 + 240, x0 + 260, x0 + 260, x0 + 260), NAVY, 2.5)
    d.rect(x0 + 6, 300, 248, 112, col, FILL[col], rx=0, width=0)
    d.text(x0 + 130, 396, sol, color=col, size=13)

# electrodes
d.rect(206, 180, 26, 170, BLUE, FILL[BLUE], rx=3, width=2.5)
d.text(219, 168, "Zn", color=BLUE, weight="bold", size=17)
d.rect(668, 180, 26, 170, RED, FILL[RED], rx=3, width=2.5)
d.text(681, 168, "Cu", color=RED, weight="bold", size=17)

# wire + voltmeter
d.line(219, 180, 219, 118, NAVY, 2.5)
d.line(681, 180, 681, 118, NAVY, 2.5)
d.line(219, 118, 406, 118, NAVY, 2.5)
d.line(494, 118, 681, 118, NAVY, 2.5)
d.circle(450, 118, 44, NAVY, "#ffffff", 2.5)
d.text(450, 112, "V", color=NAVY, weight="bold", size=19)
d.text(450, 132, "1.10 V", color=NAVY, size=12)
d.arrow(300, 100, 380, 100, SAGE, width=2.5)
d.text(340, 88, "e⁻", color=SAGE, weight="bold", size=15)
d.arrow(600, 100, 520, 100, SAGE, width=2.5)
d.text(560, 88, "e⁻", color=SAGE, weight="bold", size=15)

# salt bridge
d.path("M 330 300 L 330 250 Q 330 232 350 232 L 550 232 Q 570 232 570 250 L 570 300", GOLD, 3)
d.text(450, 220, "salt bridge  (KNO₃)", color=GOLD, weight="bold", size=14)
d.arrow(430, 258, 360, 258, GOLD, width=2)
d.text(395, 250, "NO₃⁻", color=GOLD, weight="bold", size=13)
d.arrow(470, 280, 540, 280, GOLD, width=2)
d.text(505, 272, "K⁺", color=GOLD, weight="bold", size=13)

# electrode captions
d.lines(219, 442, "ANODE  ·  negative  ·  oxidation  ·  loses mass   Zn → Zn²⁺ + 2e⁻",
        chars=30, lh=18, size=14, color=BLUE)
d.lines(681, 442, "CATHODE  ·  positive  ·  reduction  ·  gains mass   Cu²⁺ + 2e⁻ → Cu",
        chars=30, lh=18, size=14, color=RED)

py = 496
d.rect(60, py, 780, 128, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 28, "Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s)", color=NAVY, weight="bold", size=19)
d.text(450, py + 52, "anode on the left, cathode on the right; one bar is a phase boundary, two is the salt bridge",
       color=GREY, size=13)
d.text(228, py + 84, "E°cell = E°cathode − E°anode", color=NAVY, weight="bold", size=16)
d.text(560, py + 84, "= 0.34 − (−0.76) = +1.10 V", color=NAVY, weight="bold", size=16)
d.text(450, py + 110, "Both potentials come straight off the reduction table — the subtraction already flips the anode.",
       color=GREY, size=13)

d.save("galvanic-cell-anatomy")
