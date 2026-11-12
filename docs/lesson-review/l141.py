import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 600,
      "Every alkene addition is one regiochemistry plus one stereochemistry",
      "Place a reaction on both axes and the product follows. Blank cells are combinations no common reagent gives.",
      "A three by three grid. Columns are Markovnikov, anti-Markovnikov, and no regiochemistry because "
      "both carbons receive the same group. Rows are syn addition, anti addition, and no stereochemical "
      "control. Oxymercuration-demercuration, HX addition and acid-catalysed hydration sit in the "
      "Markovnikov column with no stereochemical control; halohydrin formation is Markovnikov and anti; "
      "hydroboration-oxidation is the only anti-Markovnikov entry and is syn; halogenation with X2 is "
      "anti and catalytic hydrogenation is syn, both with no regiochemistry.")

COLS = [(290, "Markovnikov", "group adds to the\nmore substituted C"),
        (520, "anti-Markovnikov", "group adds to the\nless substituted C"),
        (750, "no regiochemistry", "both carbons get\nthe same group")]
ROWS = [(168, "syn", "both groups, same face"),
        (284, "anti", "groups, opposite faces"),
        (400, "no control", "planar cation, either face")]

for cx, head, sub in COLS:
    d.text(cx, 104, head, color=NAVY, weight="bold", size=16)
    a, b = sub.split("\n")
    d.text(cx, 122, a, color=GREY, size=12)
    d.text(cx, 136, b, color=GREY, size=12)

for cy, head, sub in ROWS:
    d.text(168, cy + 34, head, anchor="end", color=NAVY, weight="bold", size=16)
    d.text(168, cy + 52, sub, anchor="end", color=GREY, size=12)

CW, CH = 212, 96

ENTRIES = {
    (1, 0): (BLUE, "hydroboration–oxidation", "1. BH₃·THF  2. H₂O₂, NaOH\nno carbocation, no rearrangement"),
    (2, 0): (SAGE, "catalytic hydrogenation", "H₂, Pt / Pd / Ni\nboth H from the catalyst face"),
    (0, 1): (RED, "halohydrin formation", "X₂ in H₂O\nOH to the more substituted C"),
    (2, 1): (RED, "halogenation", "X₂ in CCl₄\nbromonium opened from behind"),
    (0, 2): (GOLD, "HX · H₂O/H⁺ · oxymercuration", "planar cation (or bridged Hg)\nracemic; rearranges except with Hg"),
}

for (ci, ri), (col, title, body) in ENTRIES.items():
    cx = COLS[ci][0]
    cy = ROWS[ri][0]
    d.rect(cx - CW / 2, cy, CW, CH, col, FILL[col], rx=10, width=2)
    d.lines(cx, cy + 26, title, chars=24, lh=19, size=16, color=col, weight="bold")
    for k, line in enumerate(body.split("\n")):
        d.text(cx, cy + 60 + k * 17, line, color=GREY, size=12)

d.text(520, 284 + 48, "—", color=GREY, size=22)
d.text(520, 400 + 48, "—", color=GREY, size=22)
d.text(290, 168 + 48, "—", color=GREY, size=22)

py = 512
d.rect(60, py, 780, 72, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, py + 28, "The one-line test", color=NAVY, weight="bold", size=17)
d.text(450, py + 50, "Does a free carbocation form?  Yes → Markovnikov, racemic, rearrangements possible.  No → read the bridged or concerted geometry.",
       color=GREY, size=13)

d.save("alkene-addition-map")
