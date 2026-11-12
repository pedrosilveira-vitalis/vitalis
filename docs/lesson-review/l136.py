import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 696,
      "Seniority decides the suffix; everything else drops to a prefix",
      "The highest-ranked group present becomes the ending and takes the lowest locant. Every other group is cited as a prefix.",
      "A ranked ladder of eleven functional groups from carboxylic acid down to alkane, each with the "
      "suffix it takes when it is the senior group and the prefix it takes when outranked. Below, the "
      "name methyl (2S)-2-amino-3-(4-hydroxyphenyl)propanoate is split into its parts and each part is "
      "labelled.")

rows = [
    ("1", "Carboxylic acid", "-oic acid", "carboxy-", RED),
    ("2", "Ester",           "-oate",     "alkoxycarbonyl-", RED),
    ("3", "Acid halide",     "-oyl halide", "halocarbonyl-", RED),
    ("4", "Amide",           "-amide",    "carbamoyl-", RED),
    ("5", "Aldehyde",        "-al",       "oxo- / formyl-", BLUE),
    ("6", "Ketone",          "-one",      "oxo-", BLUE),
    ("7", "Alcohol",         "-ol",       "hydroxy-", BLUE),
    ("8", "Amine",           "-amine",    "amino-", SAGE),
    ("9", "Alkene",          "-ene",      "(none)", GREY),
    ("10", "Alkyne",         "-yne",      "(none)", GREY),
    ("11", "Alkane",         "-ane",      "alkyl-", GREY),
]

y = 112
RH = 36
d.text(104, 104, "rank", color=NAVY, weight="bold", size=14)
d.text(230, 104, "group", color=NAVY, weight="bold", size=14)
d.text(452, 104, "suffix when senior", color=NAVY, weight="bold", size=14)
d.text(706, 104, "prefix when outranked", color=NAVY, weight="bold", size=14)

for rank, name, suf, pre, col in rows:
    d.rect(76, y, 760, RH - 6, col, FILL[col], rx=6, width=1.5)
    d.text(104, y + 21, rank, color=col, weight="bold", size=15)
    d.text(230, y + 21, name, color=NAVY, size=15)
    d.text(452, y + 21, suf, color=col, weight="bold", size=15)
    d.text(706, y + 21, pre, color=GREY, size=14)
    y += RH

d.arrow(60, 116, 60, y - 12, NAVY, width=2)
d.text(44, (116 + y) / 2, "senior", color=NAVY, size=13, anchor="middle")

# name anatomy
ay = y + 22
d.rect(60, ay, 780, 134, NAVY, FILL[NAVY], rx=12, width=2)
d.text(450, ay + 26, "methyl (2S)-2-amino-3-(4-hydroxyphenyl)propanoate",
       color=NAVY, weight="bold", size=21)

parts = [
    (166, "methyl", "alcohol half\nof the ester"),
    (300, "(2S)", "configuration\nat C2"),
    (420, "2-amino", "NH₂ at C2,\ndemoted to prefix"),
    (585, "3-(4-hydroxyphenyl)", "para-OH phenyl\nring at C3"),
    (770, "propanoate", "3 C acid half,\nester is senior"),
]
for px, _, note in parts:
    d.line(px, ay + 38, px, ay + 54, GREY, 1.5, dash=True)
    d.lines(px, ay + 72, note.replace("\n", " "), chars=18, lh=17, size=13, color=GREY)

d.text(450, ay + 124, "Reading it back: the methyl ester of L-tyrosine.",
       color=NAVY, weight="bold", size=15)

d.save("iupac-seniority-ladder")
