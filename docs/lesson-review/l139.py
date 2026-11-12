import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 644,
      "Substrate class × reagent decides the mechanism",
      "Read the substrate down the side and the reagent across the top. Substitution and elimination always compete.",
      "A four-by-four grid. Rows are methyl, primary, secondary and tertiary substrates; columns are a "
      "weak nucleophile that is also a weak base, a strong nucleophile that is a weak base, a small "
      "strong base, and a bulky strong base. Each cell names the mechanism that dominates, from no "
      "reaction for methyl and primary substrates with a weak nucleophile, through SN2 for unhindered "
      "substrates with strong nucleophiles, to SN1/E1 and E2 for tertiary substrates.")

cols = [
    (255, "weak Nu,\nweak base", "H₂O, ROH"),
    (410, "strong Nu,\nweak base", "I⁻, CN⁻, RS⁻, N₃⁻"),
    (565, "strong base,\nsmall", "RO⁻, HO⁻"),
    (720, "strong base,\nbulky", "t-BuO⁻, LDA"),
]
for cx, head, ex in cols:
    a, b = head.split("\n")
    d.text(cx, 100, a, color=NAVY, weight="bold", size=15)
    d.text(cx, 118, b, color=NAVY, weight="bold", size=15)
    d.text(cx, 138, ex, color=GREY, size=12)

CELL = {
    "SN2": BLUE, "SN1 / E1": RED, "E2": SAGE, "no reaction": GREY,
    "SN2 (some E2)": BLUE, "E2 (some SN2)": SAGE,
}

rows = [
    ("Methyl", "CH₃–LG", ["no reaction", "SN2", "SN2", "SN2"]),
    ("Primary", "RCH₂–LG", ["no reaction", "SN2", "SN2 (some E2)", "E2"]),
    ("Secondary", "R₂CH–LG", ["SN1 / E1", "SN2", "E2 (some SN2)", "E2"]),
    ("Tertiary", "R₃C–LG", ["SN1 / E1", "SN1 / E1", "E2", "E2"]),
]

y = 156
RH, CW = 76, 146
for name, formula, cells in rows:
    d.text(150, y + 36, name, anchor="end", color=NAVY, weight="bold", size=17)
    d.text(150, y + 56, formula, anchor="end", color=GREY, size=13)
    for (cx, _, _), label in zip(cols, cells):
        col = CELL[label]
        d.rect(cx - CW / 2, y + 8, CW, RH - 16, col, FILL[col], rx=8, width=2)
        if "(" in label:
            main, par = label.split(" (")
            d.text(cx, y + 36, main, color=col, weight="bold", size=17)
            d.text(cx, y + 54, "(" + par, color=GREY, size=12)
        else:
            d.text(cx, y + 45, label, color=col, weight="bold", size=17)
    y += RH

py = y + 14
d.rect(60, py, 780, 72, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 26, "Two levers move every cell", color=NAVY, weight="bold", size=17)
d.text(450, py + 48, "Heat pushes any box toward elimination.  Polar protic solvent pushes toward SN1/E1, polar aprotic toward SN2.",
       color=GREY, size=13)

d.legend(60, py + 92, [(BLUE, "Blue: substitution, concerted", False),
                       (RED, "Red: carbocation route (SN1/E1), rearrangement possible", False),
                       (SAGE, "Sage: elimination (E2)", False)])

d.save("sn1-sn2-e1-e2-grid")
