import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 1046,
      "Five targets a bacterium has that you do not",
      "Selective toxicity is the whole story — and resistance answers each target in kind",
      "Top: the bacterial cell with the five druggable targets marked, each one a structure or pathway with "
      "no close human counterpart. That absence is what makes an antibiotic safe to take, and it is also why "
      "the targets are so few. Middle: the drug classes at each target, with the one fact per class that "
      "questions turn on. Bottom: resistance read as a reply to each mechanism — destroy the drug, change "
      "the lock, pump it out, or shut the door. Pairing a resistance mechanism with the mechanism it defeats "
      "is how these are usually tested."
      )

# ---------------- Panel A: the cell and its targets ----------------
d.rect(40, 180, 840, 262, NAVY, "none", rx=12, width=2)
d.text(460, 208, "Where a drug can attack", color=NAVY, weight="bold", size=15)

# schematic cell
d.rect(300, 236, 320, 180, NAVY, "none", rx=46, width=2.4)
d.rect(312, 248, 296, 156, GREY, FILL[GREY], rx=38, width=1.4)

d.text(460, 262, "PEPTIDOGLYCAN WALL", color=SAGE, weight="bold", size=9)
d.text(460, 284, "CELL MEMBRANE", color=GOLD, weight="bold", size=9)
d.circle(400, 330, 16, BLUE, FILL[BLUE], width=1.8)
d.text(400, 334, "70S", color=BLUE, weight="bold", size=9)
d.circle(460, 330, 16, BLUE, FILL[BLUE], width=1.8)
d.text(460, 334, "70S", color=BLUE, weight="bold", size=9)
d.text(430, 356, "RIBOSOMES", color=BLUE, weight="bold", size=8.5)
d.text(545, 326, "DNA", color=RED, weight="bold", size=9)
d.text(545, 342, "gyrase", color=RED, size=8)
d.text(460, 386, "FOLATE SYNTHESIS", color=NAVY, weight="bold", size=9)
d.text(460, 400, "made here, not eaten", color=GREY, size=8)

labels = [(150, 262, "no human equivalent", SAGE),
          (150, 300, "different lipid make-up", GOLD),
          (150, 338, "yours are 80S", BLUE),
          (770, 300, "human topoisomerases differ", RED),
          (770, 386, "you get folate from food", NAVY)]
for x, y, t, col in labels:
    d.text(x, y, t, color=col, size=8.5)

d.text(460, 430, "every one of these is a structure or pathway you do not have — that absence IS the drug's safety margin",
       color=NAVY, weight="bold", size=9.5)

# ---------------- Panel B: classes at each target ----------------
d.rect(40, 458, 840, 268, GOLD, "none", rx=12, width=2)
d.text(460, 486, "The classes, and the one fact each is tested on", color=GOLD, weight="bold", size=14)

classes = [("WALL", SAGE, "beta-lactams · vancomycin", "beta-lactams block the transpeptidase (PBP);\nvancomycin caps D-Ala–D-Ala and cannot cross\na gram-negative outer membrane"),
           ("30S", BLUE, "aminoglycosides · tetracyclines", "aminoglycosides need oxygen to get in, so they\nfail against anaerobes; tetracyclines are chelated\nby calcium and are bacteriostatic"),
           ("50S", BLUE, "macrolides · clindamycin · linezolid", "macrolides cover the atypicals — Mycoplasma,\nChlamydia, Legionella — which is why they are\nthe answer for community-acquired pneumonia"),
           ("DNA / RNA", RED, "fluoroquinolones · rifampin · metronidazole", "rifampin resistance appears fast enough that it is\nnever used alone; metronidazole must be reduced\nby an anaerobe to become toxic"),
           ("FOLATE", NAVY, "sulfonamides · trimethoprim", "two consecutive steps of one pathway, which is\nwhy the combination is synergistic")]
y = 506
for name, col, drugs, note in classes:
    d.rect(60, y, 800, 40, col, FILL[col], rx=6, width=1.3)
    d.text(122, y + 25, name, color=col, weight="bold", size=9.5)
    d.text(300, y + 25, drugs, color=NAVY, weight="bold", size=8.5)
    lines = note.split("\n")
    for j, ln in enumerate(lines):
        d.text(660, y + 15 + j * 11, ln, color=GREY, size=7.5)
    y += 44

# ---------------- Panel C: resistance as a reply ----------------
d.rect(40, 742, 840, 282, RED, "none", rx=12, width=2)
d.text(460, 770, "Resistance, read as a reply", color=RED, weight="bold", size=14)

res = [("DESTROY THE DRUG", "beta-lactamases hydrolyse the ring;\ncarbapenemases take even carbapenems", "answered by clavulanate,\nsulbactam, tazobactam", RED),
       ("CHANGE THE LOCK", "MRSA's mecA makes PBP2a, which\nbeta-lactams barely bind", "VRE swaps D-Ala–D-Ala for\nD-Ala–D-Lac: 1,000× weaker", GOLD),
       ("PUMP IT OUT", "RND efflux pumps export several\nclasses at once", "one pump, multidrug\nresistance", BLUE),
       ("SHUT THE DOOR", "porins are downregulated so the drug\nnever gets in", "with a beta-lactamase,\nthis gives carbapenem resistance", SAGE)]
y = 790
for name, how, note, col in res:
    d.rect(60, y, 800, 46, col, FILL[col], rx=6, width=1.3)
    d.text(150, y + 28, name, color=col, weight="bold", size=9.5)
    for j, ln in enumerate(how.split("\n")):
        d.text(430, y + 18 + j * 13, ln, color=NAVY, size=8)
    for j, ln in enumerate(note.split("\n")):
        d.text(730, y + 18 + j * 13, ln, color=GREY, size=8)
    y += 50

d.text(460, 1008, "and all four spread sideways — conjugation, transformation, transduction — so resistance need not be reinvented",
       color=NAVY, weight="bold", size=9)

d.save("five-antibiotic-targets-and-four-replies")
print("ok")
