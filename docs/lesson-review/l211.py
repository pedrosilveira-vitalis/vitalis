import sys
sys.path.insert(0, "/home/claude/dkit")
from dkit import *

d = D(920, 884,
      "The face is universal; the permission to use it is not",
      "Same emotion, different rules about showing it",
      "Top: the Ekman and Friesen experiment that separates the two claims, and it is worth holding in mind "
      "as a single picture. Watching a distressing film alone, Japanese and American viewers made the same "
      "faces. Watching it with an authority figure in the room, the American viewers went on showing "
      "distress while the Japanese viewers covered it with smiles. The emotion did not differ; the display "
      "rule did. Middle: the four things a display rule can do to an expression, and the fact that these "
      "rules vary within a culture too — by gender, by role, by who is watching. Bottom: the universalist "
      "and constructionist positions, which the exam expects you to be able to argue either way, and the "
      "kinds of evidence each one leans on."
      )

# ---------------- Panel A: the 1972 study ----------------
d.rect(40, 170, 840, 236, BLUE, "none", rx=12, width=2)
d.text(460, 198, "Alone, the same face. Watched, a different one.",
       color=BLUE, weight="bold", size=16)

d.rect(80, 222, 360, 150, SAGE, FILL[SAGE], rx=10, width=2)
d.text(260, 248, "WATCHING ALONE", color=SAGE, weight="bold", size=14)
d.text(260, 278, "Japanese viewers", color=NAVY, weight="bold", size=12)
d.text(260, 300, "American viewers", color=NAVY, weight="bold", size=12)
d.line(170, 312, 350, 312, SAGE, 1.4, dash="3,3")
d.text(260, 334, "the same disgust and distress", color=SAGE, weight="bold", size=13)
d.text(260, 356, "no difference worth measuring", color=GREY, size=11)

d.rect(480, 222, 360, 150, RED, FILL[RED], rx=10, width=2)
d.text(660, 248, "WITH AN AUTHORITY FIGURE", color=RED, weight="bold", size=14)
d.text(660, 278, "Japanese viewers → masked with smiles", color=NAVY, weight="bold", size=12)
d.text(660, 300, "American viewers → distress shown", color=NAVY, weight="bold", size=12)
d.line(570, 312, 750, 312, RED, 1.4, dash="3,3")
d.text(660, 334, "the display rule did the work", color=RED, weight="bold", size=13)
d.text(660, 356, "the felt emotion was never the variable", color=GREY, size=11)

# ---------------- Panel B: what display rules do ----------------
d.rect(40, 422, 840, 196, GOLD, "none", rx=12, width=2)
d.text(460, 450, "Four things a display rule can do", color=GOLD, weight="bold", size=16)

rules = [
    ("INTENSIFY", "show more than you feel", "delight at a dull gift", SAGE),
    ("DEINTENSIFY", "show less than you feel", "modesty after winning", BLUE),
    ("NEUTRALISE", "show nothing at all", "the poker face", GREY),
    ("MASK", "show a different emotion", "smiling over anger", RED),
]
x = 66
for name, what, ex, col in rules:
    d.rect(x, 472, 190, 104, col, FILL[col], rx=10, width=2)
    d.text(x + 95, 500, name, color=col, weight="bold", size=13)
    d.text(x + 95, 526, what, color=NAVY, size=12)
    d.text(x + 95, 554, ex, color=GREY, size=11)
    x += 198

d.text(460, 600, "these vary within a culture as well as between: by gender, by role, by who is in the room",
       color=NAVY, weight="bold", size=12)

# ---------------- Panel C: the two positions ----------------
d.rect(40, 634, 840, 216, SAGE, "none", rx=12, width=2)
d.text(460, 662, "Two positions the exam wants you to argue either way",
       color=SAGE, weight="bold", size=16)

d.rect(70, 682, 380, 150, BLUE, FILL[BLUE], rx=10, width=2)
d.text(260, 708, "UNIVERSALIST · Ekman", color=BLUE, weight="bold", size=13)
for i, t in enumerate(["six basic emotions, recognised everywhere",
                       "the Fore of Papua New Guinea matched them",
                       "congenitally blind people make the faces",
                       "FACS measures the muscles objectively"]):
    d.text(260, 732 + i * 22, t, color=NAVY, size=11)

d.rect(470, 682, 380, 150, GOLD, FILL[GOLD], rx=10, width=2)
d.text(660, 708, "CONSTRUCTIONIST · Barrett", color=GOLD, weight="bold", size=13)
for i, t in enumerate(["no brain region maps onto one emotion",
                       "languages cut the space up differently",
                       "concepts and context build the feeling",
                       "amae, saudade, fago have no translation"]):
    d.text(660, 732 + i * 22, t, color=NAVY, size=11)

d.save("display-rules-and-the-universality-debate")
print("ok")
