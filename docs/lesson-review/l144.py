import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 600,
      "Acyl reactivity is set by two things, and they point the same way",
      "A good leaving group and a heteroatom that donates little into the carbonyl both make the acyl carbon easier to attack.",
      "A ladder of carboxylic acid derivatives from acyl chloride at the top to amide at the bottom. "
      "For each row the table gives the leaving group with the pKa of its conjugate acid, how strongly "
      "that group donates electron density into the carbonyl, and the infrared carbonyl stretch. An "
      "arrow down the side marks that interconversion runs downhill only: any derivative can be "
      "converted into one below it, but going back up needs an activating reagent.")

rows = [
    ("Acyl chloride", "RCOCl", "Cl⁻   pKₐ ≈ −7", "minimal (3p/2p mismatch)", "~1800", RED),
    ("Anhydride", "(RCO)₂O", "RCOO⁻   pKₐ ≈ 4.8", "moderate", "~1820 and ~1760", RED),
    ("Thioester", "RCOSR'", "RS⁻   pKₐ ≈ 10", "weak (3p/2p mismatch)", "—", GOLD),
    ("Ester", "RCOOR'", "RO⁻   pKₐ ≈ 16", "significant", "~1735", BLUE),
    ("Amide", "RCONR₂", "R₂N⁻   pKₐ ≈ 38", "strongest", "~1650–1690", SAGE),
]

d.text(310, 108, "leaving group (conj. acid pKₐ)", color=NAVY, weight="bold", size=14)
d.text(575, 108, "donation into C=O", color=NAVY, weight="bold", size=14)
d.text(778, 108, "IR C=O stretch", color=NAVY, weight="bold", size=14)

y = 124
RH = 68
for name, formula, lg, don, ir, col in rows:
    d.rect(96, y, 748, RH - 10, col, FILL[col], rx=8, width=2)
    d.text(112, y + 26, name, anchor="start", color=col, weight="bold", size=16)
    d.text(112, y + 45, formula, anchor="start", color=GREY, size=13)
    d.text(310, y + 36, lg, color=NAVY, size=14)
    d.text(575, y + 36, don, color=NAVY, size=14)
    d.text(778, y + 36, ir, color=NAVY, size=14)
    y += RH

d.arrow(72, 130, 72, y - 18, NAVY, width=3)
d.text(56, 150, "more", color=NAVY, size=12)
d.text(56, 166, "reactive", color=NAVY, size=12)

py = y + 6
d.rect(60, py, 780, 86, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 28, "Interconversion runs downhill only", color=NAVY, weight="bold", size=18)
d.text(450, py + 52, "acyl chloride → anhydride → ester → amide happens on contact with the right nucleophile.",
       color=NAVY, size=15)
d.text(450, py + 74, "Climbing back up needs an activating reagent such as SOCl₂ or PCl₅ — or, in a cell, ATP.",
       color=GREY, size=13)

d.save("acyl-reactivity-ladder")
