import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(900, 716,
      "Two structures in front of you: what is their relationship?",
      "Work down the questions in order. The first “no” you hit names the relationship.",
      "A decision tree for classifying two structures. Same connectivity or not separates constitutional "
      "isomers from stereoisomers; mirror image or not separates enantiomers from diastereomers; and a "
      "side branch covers the single molecule that contains stereocentres but has an internal mirror "
      "plane, the meso compound. A lower strip lists which cases rotate plane-polarised light.")

NODE_W, NODE_H = 236, 58


def node(cx, cy, head, color=BLUE, w=NODE_W, h=NODE_H):
    d.rect(cx - w / 2, cy - h / 2, w, h, color, FILL[color], rx=10, width=2)
    d.text(cx, cy + 6, head, color=color, weight="bold", size=16)


def leaf(cx, cy, head, sub, color):
    d.rect(cx - 102, cy - 34, 204, 68, color, FILL[color], rx=10, width=2)
    d.text(cx, cy - 6, head, color=color, weight="bold", size=16)
    d.lines(cx, cy + 16, sub, chars=30, lh=15, size=12, color=GREY)


# level 1
node(450, 106, "Same molecular formula?", NAVY)
d.arrow(450, 136, 450, 166, NAVY)
d.text(466, 156, "yes", anchor="start", color=GREY, size=13)
d.arrow(568, 106, 682, 106, GREY)
leaf(786, 106, "Not isomers", "different compounds", GREY)

# level 2
node(450, 196, "Same connectivity?", NAVY)
d.arrow(332, 196, 218, 196, GREY)
d.text(273, 188, "no", color=GREY, size=13)
leaf(114, 196, "Constitutional", "same formula, different skeleton", GREY)
d.arrow(450, 226, 450, 256, NAVY)
d.text(466, 246, "yes — stereoisomers", anchor="start", color=GREY, size=13)

# level 3
node(450, 286, "Mirror images?", NAVY)

d.arrow(332, 286, 218, 286, SAGE)
d.text(268, 278, "no", color=GREY, size=13)
leaf(114, 300, "Diastereomers", "differ at some centres; separable", SAGE)

d.arrow(568, 286, 682, 286, BLUE)
d.text(620, 278, "yes", color=GREY, size=13)
leaf(786, 300, "Enantiomers", "every centre inverted", BLUE)

# meso side branch
d.rect(180, 388, 540, 96, RED, FILL[RED], rx=12, width=2)
d.text(450, 412, "One structure, stereocentres, internal mirror plane", color=RED, weight="bold", size=16)
d.text(450, 436, "→ meso: achiral, optically inactive, a single compound", color=RED, size=15)
d.text(450, 462, "Needs matching halves: 2,3-dibromobutane has a meso form, 2-bromo-3-chlorobutane does not.",
       color=GREY, size=12)

# optical activity strip
sy = 506
d.text(450, sy, "Does it rotate plane-polarised light?", color=NAVY, weight="bold", size=18)
cells = [
    ("Single enantiomer", "yes", BLUE),
    ("Unequal R / S mix", "yes", BLUE),
    ("Racemic 50:50", "no — cancels between molecules", GREY),
    ("Meso compound", "no — cancels within one molecule", RED),
    ("Achiral molecule", "no", GREY),
]
cy = sy + 26
for name, ans, col in cells:
    d.rect(150, cy, 600, 30, col, FILL[col], rx=6, width=1.5)
    d.text(166, cy + 20, name, anchor="start", color=NAVY, size=15)
    d.text(734, cy + 20, ans, anchor="end", color=col, weight="bold", size=14)
    cy += 34

d.save("stereo-relationship-tree")
