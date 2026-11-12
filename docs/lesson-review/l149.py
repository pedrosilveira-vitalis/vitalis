import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 660,
      "The reduction-potential ladder: electrons fall, never climb",
      "A couple higher on the ladder oxidises anything below it. That one rule predicts every spontaneous pairing.",
      "An ordered ladder of standard reduction potentials from fluorine at plus 2.87 volts at the top "
      "down to lithium at minus 3.04 volts at the bottom, listing permanganate, dichromate, oxygen, "
      "ferric iron, copper, the hydrogen reference at zero, NAD plus, iron, zinc and lithium with a note "
      "on each. An arrow up the side records that electrons flow spontaneously from a lower couple to a "
      "higher one. A panel below gives the cell potential and free energy relations and notes that "
      "scaling a half-reaction does not scale its potential.")

couples = [
    ("F₂ → 2F⁻", "+2.87", "strongest common oxidant", RED),
    ("MnO₄⁻ → Mn²⁺", "+1.51", "acidic permanganate", RED),
    ("Cr₂O₇²⁻ → 2Cr³⁺", "+1.33", "oxidises 1° and 2° alcohols", RED),
    ("O₂ → 2H₂O", "+1.23", "terminal acceptor at Complex IV", GOLD),
    ("Fe³⁺ → Fe²⁺", "+0.77", "cytochromes", GOLD),
    ("Cu²⁺ → Cu", "+0.34", "cathode in a Daniell cell", BLUE),
    ("2H⁺ → H₂", " 0.00", "reference electrode, by definition", BLUE),
    ("NAD⁺ → NADH", "−0.32", "carries electrons to Complex I", SAGE),
    ("Fe²⁺ → Fe", "−0.44", "", SAGE),
    ("Zn²⁺ → Zn", "−0.76", "anode in a Daniell cell", SAGE),
    ("Li⁺ → Li", "−3.04", "strongest common reductant", SAGE),
]

y = 108
RH = 35
for name, e0, note, col in couples:
    d.rect(176, y, 664, RH - 5, col, FILL[col], rx=6, width=1.5)
    d.text(196, y + 21, name, anchor="start", color=col, weight="bold", size=15)
    d.text(430, y + 21, e0 + " V", anchor="end", color=NAVY, weight="bold", size=15)
    if note:
        d.text(452, y + 21, note, anchor="start", color=GREY, size=13)
    y += RH

d.arrow(112, y - 24, 112, 120, NAVY, width=3)
d.lines(76, 250, "electrons flow spontaneously from a lower couple to a higher one",
        chars=14, lh=17, size=13, color=NAVY)

pyb = y + 14
d.rect(60, pyb, 780, 138, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, pyb + 28, "Reading the ladder quantitatively", color=NAVY, weight="bold", size=17)
d.text(230, pyb + 58, "E°cell = E°cathode − E°anode", color=NAVY, weight="bold", size=16)
d.text(560, pyb + 58, "ΔG° = −nFE°cell", color=NAVY, weight="bold", size=16)
d.text(760, pyb + 58, "F = 96,485 C/mol", color=GREY, size=14)
d.text(450, pyb + 86, "E°cell > 0   ↔   ΔG° < 0   ↔   K > 1", color=NAVY, weight="bold", size=16)
d.text(450, pyb + 112, "Potential is intensive: doubling a half-reaction doubles n but leaves E° unchanged.",
       color=GREY, size=13)

d.save("reduction-potential-ladder")
