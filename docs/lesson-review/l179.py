import sys, math
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 800,
      "A real battery keeps part of its voltage for itself",
      "V_terminal = ε − Ir when discharging, ε + Ir when charging",
      "Top left: a battery drawn as an ideal EMF in series with its internal resistance, feeding an external "
      "resistor; the terminal voltage is measured across the terminals and is less than the EMF whenever current "
      "flows. Top right: terminal voltage plotted against current, a straight line starting at the EMF when no "
      "current is drawn and falling with slope minus r until it reaches zero at the short-circuit current "
      "epsilon over r. Middle: the worked twelve volt example with half an ohm internal and five and a half ohms "
      "external, giving two amps, eleven volts at the terminals, twenty-two watts delivered and two watts wasted "
      "inside. Bottom: the two-loop recipe — name a current in every branch, write the junction rule, walk each "
      "loop with consistent signs, and read a negative answer as a direction guessed backwards.")

# ---------------- Panel A: the real battery ----------------
d.rect(40, 118, 420, 258, BLUE, "none", rx=12, width=2)
d.text(250, 146, "Inside the case: an ideal source plus r", color=BLUE, weight="bold", size=15)

d.rect(90, 180, 200, 118, GREY, "none", rx=6, width=2, )
d.text(190, 198, "the battery", color=GREY, weight="bold", size=12)
d.line(120, 250, 148, 250, NAVY, 4)
d.line(126, 262, 142, 262, NAVY, 1.8)
d.text(134, 232, "ε", color=NAVY, weight="bold", size=17)
d.rect(196, 240, 54, 16, RED, FILL[RED], rx=3, width=2)
d.text(223, 230, "r", color=RED, weight="bold", size=14)

d.line(290, 248, 380, 248, GREY, 2)
d.line(380, 248, 380, 320, GREY, 2)
d.line(290, 320, 380, 320, GREY, 2)
d.line(90, 320, 290, 320, GREY, 2)
d.line(290, 248, 290, 320, GREY, 2)
d.rect(368, 262, 20, 44, BLUE, FILL[BLUE], rx=3, width=2)
d.text(404, 288, "R", anchor="start", color=BLUE, weight="bold", size=15)
d.circle(290, 248, 5, NAVY, NAVY)
d.circle(290, 320, 5, NAVY, NAVY)
d.text(300, 290, "V_T", anchor="start", color=NAVY, weight="bold", size=14)

d.text(250, 346, "the Ir drop happens inside, so you never see it on a meter",
       color=GREY, size=12)
d.text(250, 368, "no current ⇒ V_T = ε", color=NAVY, weight="bold", size=14)

# ---------------- Panel B: V_T vs I ----------------
d.rect(476, 118, 404, 258, SAGE, "none", rx=12, width=2)
d.text(678, 146, "Draw more current, get less voltage", color=SAGE, weight="bold", size=15)

m = d.axes(548, 168, 268, 118, "current drawn I", "terminal voltage",
           (0, 1.15), (0, 1.15), ticks_x=None, ticks_y=None)
d.curve(m, [(x / 100, 1 - x / 100) for x in range(0, 101)], SAGE, 2.8)
px, py = m(0, 1)
d.circle(px, py, 5, NAVY, NAVY)
d.text(px + 10, py - 8, "ε at I = 0", anchor="start", color=NAVY, weight="bold", size=13)
px, py = m(1, 0)
d.circle(px, py, 5, RED, RED)
d.text(px - 12, py - 7, "short circuit: I = ε/r", anchor="end", color=RED, weight="bold", size=13)
px, py = m(0.5, 0.5)
d.text(px + 12, py + 2, "slope = −r", anchor="start", color=SAGE, weight="bold", size=13)
d.text(678, 362, "a tired battery is one whose r has grown", color=GREY, size=13)

# ---------------- Panel C: worked numbers ----------------
d.rect(40, 396, 840, 150, GOLD, "none", rx=12, width=2)
d.text(460, 424, "ε = 12 V, r = 0.5 Ω, R = 5.5 Ω", color=GOLD, weight="bold", size=16)

cells = [("I = ε/(R+r)", "12/6.0 = 2.0 A", NAVY),
         ("V_T = ε − Ir", "12 − 1.0 = 11.0 V", NAVY),
         ("to the resistor", "I²R = 22 W", SAGE),
         ("wasted inside", "I²r = 2 W", RED)]
x = 80
for top, bot, col in cells:
    d.rect(x, 444, 190, 68, col, FILL[col], rx=10, width=2)
    d.text(x + 95, 468, top, color=GREY, size=13)
    d.text(x + 95, 494, bot, color=col, weight="bold", size=15)
    x += 200
d.text(460, 532, "and εI = 24 W accounts for both — always check the power balance",
       color=GREY, size=13)

# ---------------- Panel D: two-loop recipe ----------------
d.rect(40, 566, 840, 204, NAVY, "none", rx=12, width=2)
d.text(460, 594, "When it will not reduce to series and parallel", color=NAVY, weight="bold", size=16)

steps = [("1", "name a current, with a guessed direction, in every branch"),
         ("2", "junction rule: what flows in flows out (conservation of charge)"),
         ("3", "loop rule: walk each loop one way and set ΣΔV = 0 (conservation of energy)"),
         ("4", "−IR going with your current, +IR against it; +ε from − to +, −ε from + to −"),
         ("5", "solve; a negative current just means that branch runs the other way")]
y = 624
for n, t in steps:
    d.circle(92, y - 5, 12, BLUE, FILL[BLUE], 2)
    d.text(92, y, n, color=BLUE, weight="bold", size=14)
    d.text(116, y, t, anchor="start", color=NAVY, size=14)
    y += 28

d.save("emf-internal-resistance-and-loop-analysis")
print("ok")
