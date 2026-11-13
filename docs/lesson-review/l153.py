import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 680,
      "Counting electrons, in a plating bath and in a mitochondrion",
      "Charge becomes moles of electrons; moles of electrons become whatever they are spent on.",
      "Two parallel chains. On the left, electrolysis: current times time gives charge in coulombs, "
      "divided by the Faraday constant gives moles of electrons, divided by the electrons per ion gives "
      "moles of metal, times the molar mass gives grams, worked through for copper plating at 2 amps "
      "for 30 minutes to give 1.18 grams. On the right, the electron transport chain: NADH at minus "
      "0.32 volts hands two electrons to oxygen at plus 0.82 volts, a 1.14 volt drop worth 220 "
      "kilojoules per mole, which pumps ten protons, and at about four protons per ATP once transport "
      "costs are included yields roughly 2.5 ATP.")

# left column
d.text(252, 108, "Electrolysis", color=BLUE, weight="bold", size=21)
d.text(252, 130, "spend charge, get metal", color=GREY, size=13)

steps_l = [("I × t", "2.00 A × 1800 s = 3600 C", "charge"),
           ("÷ F", "3600 / 96,500 = 0.0373 mol", "moles of e⁻"),
           ("÷ n", "0.0373 / 2 = 0.0187 mol", "moles of Cu"),
           ("× M", "0.0187 × 63.5 = 1.18 g", "grams plated")]
y = 158
for op, calc, label in steps_l:
    d.rect(76, y, 352, 62, BLUE, FILL[BLUE], rx=9, width=2)
    d.text(110, y + 26, op, anchor="start", color=BLUE, weight="bold", size=18)
    d.text(414, y + 24, label, anchor="end", color=GREY, size=13)
    d.text(252, y + 48, calc, color=NAVY, size=14)
    if label != "grams plated":
        d.arrow(252, y + 62, 252, y + 76, BLUE)
    y += 82

d.text(252, y + 6, "m = I t M / (n F)", color=BLUE, weight="bold", size=17)

# right column
d.text(650, 108, "Electron transport chain", color=RED, weight="bold", size=21)
d.text(650, 130, "spend electrons, get a gradient", color=GREY, size=13)

steps_r = [("ΔE°′", "+0.82 − (−0.32) = 1.14 V", "NADH → O₂"),
           ("−nFΔE", "−2 × 96,500 × 1.14 ≈ −220 kJ", "free energy"),
           ("pumped", "4 + 4 + 2 = 10 H⁺", "Complexes I, III, IV"),
           ("÷ 4 H⁺", "10 / 4 ≈ 2.5 ATP per NADH", "3 for synthase, 1 for transport")]
y = 158
for op, calc, label in steps_r:
    d.rect(474, y, 352, 62, RED, FILL[RED], rx=9, width=2)
    d.text(508, y + 26, op, anchor="start", color=RED, weight="bold", size=18)
    d.text(812, y + 24, label, anchor="end", color=GREY, size=13)
    d.text(650, y + 48, calc, color=NAVY, size=14)
    if label != "3 for synthase, 1 for transport":
        d.arrow(650, y + 62, 650, y + 76, RED)
    y += 82

d.text(650, y + 6, "ΔG°′ = −nFΔE°′", color=RED, weight="bold", size=17)

pyb = 520
d.rect(60, pyb, 780, 142, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, pyb + 28, "One electrode rule, two kinds of cell", color=NAVY, weight="bold", size=18)
d.text(450, pyb + 54, "Oxidation is at the anode and reduction at the cathode in every cell. Only the sign of the electrode changes.",
       color=NAVY, size=14)
d.text(258, pyb + 86, "galvanic: anode −, cathode +", color=SAGE, weight="bold", size=15)
d.text(646, pyb + 86, "electrolytic: anode +, cathode −", color=GOLD, weight="bold", size=15)
d.text(450, pyb + 118, "The ETC is galvanic, not electrolytic: nothing outside the mitochondrion drives it. The electron drop pays for the pumping.",
       color=GREY, size=13)

d.save("faraday-and-etc")
