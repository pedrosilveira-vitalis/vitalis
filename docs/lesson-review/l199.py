import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 902,
      "Four stages, and the one thing each one cannot yet do",
      "Vignette questions give you an age and a behaviour — read the behaviour",
      "Top: Piaget's four stages laid on an age line, each with the achievement that defines it and the "
      "limitation that gives it away in a vignette. Middle: the engine — a schema that absorbs new input is "
      "assimilating; when the input will not fit, the resulting disequilibrium forces the schema itself to "
      "change, and that accommodation is what moves development forward. Bottom: the same child described by "
      "Piaget and by Vygotsky. For Piaget the child is a lone scientist and readiness has to come before "
      "teaching; for Vygotsky the child is an apprentice, teaching leads development, and the useful zone is "
      "the gap between what the child manages alone and what the child manages with help."
      )

# ---------------- Panel A: the four stages ----------------
d.rect(40, 150, 840, 282, BLUE, "none", rx=12, width=2)
d.text(460, 178, "The four stages, by what the child cannot yet do",
       color=BLUE, weight="bold", size=16)

stages = [
    ("SENSORIMOTOR", "birth – 2 yr", "object permanence;\ndeferred imitation",
     "no symbols early on;\nA-not-B error at 8–12 mo", SAGE),
    ("PREOPERATIONAL", "2 – 7 yr", "symbols, language,\npretend play",
     "egocentrism, centration,\nno conservation", GOLD),
    ("CONCRETE OPERATIONAL", "7 – 11 yr", "conservation, seriation,\nclassification",
     "cannot reason from a\npremise it knows is false", BLUE),
    ("FORMAL OPERATIONAL", "11 yr +", "hypothetical-deductive\nreasoning",
     "not universal; many adults\nnever use it in every domain", RED),
]
x = 62
for name, age, got, lack, col in stages:
    d.rect(x, 200, 198, 196, col, FILL[col], rx=10, width=2)
    d.text(x + 99, 226, name, color=col, weight="bold", size=12)
    d.text(x + 99, 246, age, color=NAVY, weight="bold", size=12)
    g1, g2 = got.split("\n")
    d.text(x + 99, 276, g1, color=NAVY, size=11)
    d.text(x + 99, 292, g2, color=NAVY, size=11)
    d.line(x + 24, 310, x + 174, 310, col, 1, dash="3,3")
    d.text(x + 99, 332, "cannot yet:", color=col, weight="bold", size=11)
    l1, l2 = lack.split("\n")
    d.text(x + 99, 352, l1, color=GREY, size=11)
    d.text(x + 99, 368, l2, color=GREY, size=11)
    x += 204

d.text(460, 418, "the order never changes and no stage is skipped — the ages are approximate, the sequence is not",
       color=GREY, size=12)

# ---------------- Panel B: the engine ----------------
d.rect(40, 448, 840, 196, GOLD, "none", rx=12, width=2)
d.text(460, 476, "What actually moves a child forward", color=GOLD, weight="bold", size=16)

d.rect(70, 496, 212, 118, SAGE, FILL[SAGE], rx=10, width=2)
d.text(176, 522, "ASSIMILATION", color=SAGE, weight="bold", size=13)
d.text(176, 546, "new input fits the", color=NAVY, size=12)
d.text(176, 564, "schema you have", color=NAVY, size=12)
d.text(176, 594, "every four-legged", color=GREY, size=11)
d.text(176, 608, "animal is \"doggie\"", color=GREY, size=11)

d.rect(354, 496, 212, 118, RED, FILL[RED], rx=10, width=2)
d.text(460, 522, "DISEQUILIBRIUM", color=RED, weight="bold", size=13)
d.text(460, 546, "the input will not fit", color=NAVY, size=12)
d.text(460, 564, "— that is the cat", color=NAVY, size=12)
d.text(460, 594, "cognitive conflict is", color=GREY, size=11)
d.text(460, 608, "the motivator", color=GREY, size=11)

d.rect(638, 496, 212, 118, BLUE, FILL[BLUE], rx=10, width=2)
d.text(744, 522, "ACCOMMODATION", color=BLUE, weight="bold", size=13)
d.text(744, 546, "the schema itself", color=NAVY, size=12)
d.text(744, 564, "splits or changes", color=NAVY, size=12)
d.text(744, 594, "equilibrium returns,", color=GREY, size=11)
d.text(744, 608, "at a higher level", color=GREY, size=11)

d.arrow(290, 555, 346, 555, GREY, width=2)
d.arrow(574, 555, 630, 555, GREY, width=2)

# ---------------- Panel C: Piaget vs Vygotsky ----------------
d.rect(40, 660, 840, 212, SAGE, "none", rx=12, width=2)
d.text(460, 688, "The same child, two theories", color=SAGE, weight="bold", size=16)

d.text(258, 716, "PIAGET", color=BLUE, weight="bold", size=14)
d.text(690, 716, "VYGOTSKY", color=RED, weight="bold", size=14)
d.line(474, 706, 474, 856, GREY, 1, dash="4,4")

pairs = [
    ("development drives learning", "learning drives development"),
    ("readiness must come first", "teach inside the ZPD"),
    ("the child as lone scientist", "the child as apprentice"),
    ("private speech = egocentrism", "private speech = a tool for self-control"),
    ("thought comes first, language follows", "language transforms thought"),
]
y = 742
for left, right in pairs:
    d.text(452, y, left, anchor="end", color=NAVY, size=12)
    d.text(496, y, right, anchor="start", color=NAVY, size=12)
    y += 24

d.save("piaget-stages-and-the-vygotsky-contrast")
print("ok")
